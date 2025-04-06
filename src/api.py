from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import List, Dict, Optional
from wallet import Wallet
import os
import jwt
import datetime
import logging
from passlib.context import CryptContext
from fastapi_limiter import FastAPILimiter, Limiter

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app initialization
app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limiting
limiter = Limiter(key="global", default_limit="100/minute")
app.add_middleware(FastAPILimiter)

# JWT configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")  # Use a secure key in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Initialize the wallet
PASSWORD = os.getenv("WALLET_PASSWORD", "your_secure_password")  # Use environment variables in production
wallet = Wallet(PASSWORD)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 password bearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Pydantic models
class User(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    password: str

class UserInDB(User):
    hashed_password: str

class TransactionRequest(BaseModel):
    from_address: str
    to_address: str
    amount: float

class AddressResponse(BaseModel):
    address: str
    balance: float

class TransactionResponse(BaseModel):
    success: bool
    message: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Dummy user database
fake_users_db: Dict[str, UserInDB] = {}

# Utility functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def create_access_token(data: dict, expires_delta: Optional[datetime.timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# User registration endpoint
@app.post("/register", response_model=User )
async def register(user: User):
    if user.username in fake_users_db:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    fake_users_db[user.username] = UserInDB(**user.dict(), hashed_password=hashed_password)
    logger.info(f"User  registered: {user.username}")
    return user

# Authentication endpoint
@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user(fake_users_db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

# Dependency to get the current user
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username)
    if user is None:
        raise credentials_exception
    return user

@app.get("/addresses", response_model=List[AddressResponse])
async def get_addresses(current_user: User = Depends(get_current_user)):
    """Get all wallet addresses and their balances."""
    logger.info(f"User  {current_user.username} requested addresses.")
    return [{"address": address, "balance": wallet.get_balance(address)} for address in wallet.addresses]

@app.post("/addresses", response_model=AddressResponse)
async def create_address(current_user: User = Depends(get_current_user)):
    """Create a new wallet address."""
    address = wallet.generate_address(len(wallet.addresses))
    wallet.addresses[address] = 0.0  # Initialize balance to 0
    logger.info(f"User  {current_user.username} created address: {address}.")
    return {"address": address, "balance": 0.0}

@app.get("/balance/{address}", response_model=float)
async def get_balance(address: str, current_user: User = Depends(get_current_user)):
    """Get the balance of a specific address."""
    balance = wallet.get_balance(address)
    if balance is None:
        raise HTTPException(status_code=404, detail="Address not found")
    logger.info(f"User  {current_user.username} requested balance for address: {address}.")
    return balance

@app.post("/transactions", response_model=TransactionResponse)
async def create_transaction(transaction: TransactionRequest, current_user: User = Depends(get_current_user)):
    """Create a new transaction."""
    try:
        success = wallet.create_transaction(transaction.from_address, transaction.to_address, transaction.amount)
        logger.info(f"User  {current_user.username} created transaction: {transaction}.")
        return {"success": success, "message": "Transaction successful"}
    except Exception as e:
        logger.error(f"Transaction failed: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/transactions", response_model=List[Dict[str, str]])
async def get_transactions(current_user: User = Depends(get_current_user)):
    """Get the list of transactions."""
    logger.info(f"User  {current_user.username} requested transactions.")
    return wallet.get_transactions()

@app.post("/save")
async def save_wallet(current_user: User = Depends(get_current_user), background_tasks: BackgroundTasks):
    """Save the wallet to a file."""
    background_tasks.add_task(wallet.save_wallet, "my_wallet.json")
    logger.info(f"User  {current_user.username} initiated wallet save.")
    return {"message": "Wallet save initiated."}

@app.post("/load")
async def load_wallet(current_user: User = Depends(get_current_user)):
    """Load the wallet from a file."""
    try:
        wallet.load_wallet("my_wallet.json")
        logger.info(f"User  {current_user.username} loaded the wallet.")
        return {"message": "Wallet loaded successfully"}
    except Exception as e:
        logger.error(f"Failed to load wallet: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/addresses/{address}", response_model=TransactionResponse)
async def delete_address(address: str, current_user: User = Depends(get_current_user)):
    """Delete a wallet address."""
    if address not in wallet.addresses:
        raise HTTPException(status_code=404, detail="Address not found")
    del wallet.addresses[address]
    logger.info(f"User  {current_user.username} deleted address: {address}.")
    return {"success": True, "message": "Address deleted successfully"}

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    if not os.path.exists("my_wallet.json"):
        wallet.create_wallet()  # Create a new wallet if it doesn't exist
    uvicorn.run(app, host="0.0.0.0", port=8000)
