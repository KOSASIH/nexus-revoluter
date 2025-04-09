import os
import pytest
from fastapi.testclient import TestClient
from api import app  # Assuming your FastAPI implementation is in a file named api.py
from wallet import Wallet

# Initialize the test client
client = TestClient(app)

# Mock wallet for testing
PASSWORD = "test_password"
wallet = Wallet(PASSWORD)

# Create a test user
test_user = {
    "username": "testuser",
    "email": "testuser@example.com",
    "full_name": "Test User",
    "password": "testpassword"
}

@pytest.fixture(scope="module", autouse=True)
def setup_wallet():
    """Setup the wallet before running tests."""
    if not os.path.exists("my_wallet.json"):
        wallet.create_wallet()  # Create a new wallet if it doesn't exist
    yield
    # Cleanup after tests
    if os.path.exists("my_wallet.json"):
        os.remove("my_wallet.json")

@pytest.fixture
def register_user():
    """Register a test user."""
    response = client.post("/register", json=test_user)
    assert response.status_code == 200
    return response.json()

@pytest.fixture
def login_user(register_user):
    """Login the test user and return the access token."""
    response = client.post("/token", data={"username": test_user["username"], "password": test_user["password"]})
    assert response.status_code == 200
    return response.json()["access_token"]

def test_register_user():
    """Test user registration."""
    response = client.post("/register", json=test_user)
    assert response.status_code == 200
    assert response.json()["username"] == test_user["username"]

def test_register_user_duplicate():
    """Test duplicate user registration."""
    response = client.post("/register", json=test_user)
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already registered"

def test_login_user():
    """Test user login."""
    response = client.post("/token", data={"username": test_user["username"], "password": test_user["password"]})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_user_invalid_password():
    """Test login with invalid password."""
    response = client.post("/token", data={"username": test_user["username"], "password": "wrongpassword"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect username or password"

def test_create_address(login_user):
    """Test creating a new wallet address."""
    headers = {"Authorization": f"Bearer {login_user}"}
    response = client.post("/addresses", headers=headers)
    assert response.status_code == 200
    assert "address" in response.json()

def test_get_addresses(login_user):
    """Test getting all wallet addresses."""
    headers = {"Authorization": f"Bearer {login_user}"}
    response = client.get("/addresses", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_balance(login_user):
    """Test getting the balance of a specific address."""
    headers = {"Authorization": f"Bearer {login_user}"}
    address_response = client.post("/addresses", headers=headers)
    address = address_response.json()["address"]
    response = client.get(f"/balance/{address}", headers=headers)
    assert response.status_code == 200
    assert response.json() == 0.0  # Initial balance should be 0.0

def test_create_transaction(login_user):
    """Test creating a new transaction."""
    headers = {"Authorization": f"Bearer {login_user}"}
    address_response_1 = client.post("/addresses", headers=headers)
    address_response_2 = client.post("/addresses", headers=headers)
    from_address = address_response_1.json()["address"]
    to_address = address_response_2.json()["address"]
    
    # Fund the from_address for testing
    wallet.addresses[from_address] = 100.0  # Set balance for testing

    transaction_data = {
        "from_address": from_address,
        "to_address": to_address,
        "amount": 50.0
    }
    response = client.post("/transactions", json=transaction_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["success"] is True

def test_create_transaction_insufficient_funds(login_user):
    """Test creating a transaction with insufficient funds."""
    headers = {"Authorization": f"Bearer {login_user}"}
    address_response_1 = client.post("/addresses", headers=headers)
    address_response_2 = client.post("/addresses", headers=headers)
    from_address = address_response_1.json()["address"]
    to_address = address_response_2.json()["address"]
    
    # Set balance to 10.0 for testing
    wallet.addresses[from_address] = 10.0

    transaction_data = {
        "from_address": from_address,
        "to_address": to_address,
        "amount": 50.0  # Attempt to send more than available
    }
    response = client.post("/transactions", json=transaction_data, headers=headers)
    assert response.status_code == 400
    assert "detail" in response.json()  # Check for error message

def test_delete_address(login_user):
    """Test deleting a wallet address."""
    headers = {"Authorization": f"Bearer {login_user}"}
    address_response = client.post("/addresses", headers=headers)
    address = address_response.json()["address"]
    response = client.delete(f"/addresses/{address}", headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Address deleted successfully"

def test_delete_address_not_found(login_user):
    """Test deleting a non-existent wallet address."""
    headers = {"Authorization": f"Bearer {login_user}"}
    response = client.delete("/addresses/nonexistent_address", headers=headers)
    assert response.status_code == 404
    assert response.json()["detail"] == "Address not found"

def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

if __name__ == "__main__":
    pytest.main()
