import os
import pytest
from fastapi.testclient import TestClient
from api import app  # Assuming your FastAPI app is in a file named api.py
from wallet import Wallet

# Set up a test client
client = TestClient(app)

# Test data
TEST_USERNAME = "testuser"
TEST_PASSWORD = "testpassword"
TEST_EMAIL = "testuser@example.com"
TEST_FULL_NAME = "Test User"

# Create a wallet for testing
PASSWORD = "test_wallet_password"
wallet = Wallet(PASSWORD)

@pytest.fixture(scope="module", autouse=True)
def setup_module():
    """Setup for the entire module."""
    if not os.path.exists("my_wallet.json"):
        wallet.create_wallet()  # Create a new wallet if it doesn't exist

def test_register():
    """Test user registration."""
    response = client.post("/register", json={
        "username": TEST_USERNAME,
        "email": TEST_EMAIL,
        "full_name": TEST_FULL_NAME,
        "password": TEST_PASSWORD
    })
    assert response.status_code == 200
    assert response.json()["username"] == TEST_USERNAME

def test_login():
    """Test user login."""
    response = client.post("/token", data={
        "username": TEST_USERNAME,
        "password": TEST_PASSWORD
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_create_address():
    """Test creating a new wallet address."""
    response = client.post("/addresses", headers={
        "Authorization": f"Bearer {get_access_token()}"
    })
    assert response.status_code == 200
    assert "address" in response.json()

def test_get_addresses():
    """Test getting all wallet addresses."""
    response = client.get("/addresses", headers={
        "Authorization": f"Bearer {get_access_token()}"
    })
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_transaction():
    """Test creating a transaction."""
    # First, create two addresses
    address1_response = client.post("/addresses", headers={
        "Authorization": f"Bearer {get_access_token()}"
    })
    address2_response = client.post("/addresses", headers={
        "Authorization": f"Bearer {get_access_token()}"
    })
    
    address1 = address1_response.json()["address"]
    address2 = address2_response.json()["address"]

    # Fund the first address
    wallet.addresses[address1] = 100.0

    # Create a transaction
    response = client.post("/transactions", json={
        "from_address": address1,
        "to_address": address2,
        "amount": 50.0
    }, headers={
        "Authorization": f"Bearer {get_access_token()}"
    })
    assert response.status_code == 200
    assert response.json()["success"] is True

def test_get_balance():
    """Test getting the balance of an address."""
    response = client.get("/balance/{address}", headers={
        "Authorization": f"Bearer {get_access_token()}"
    })
    assert response.status_code == 200
    assert isinstance(response.json(), float)

def test_delete_address():
    """Test deleting a wallet address."""
    response = client.delete("/addresses/{address}", headers={
        "Authorization": f"Bearer {get_access_token()}"
    })
    assert response.status_code == 200
    assert response.json()["success"] is True

def get_access_token():
    """Helper function to get access token for authenticated requests."""
    response = client.post("/token", data={
        "username": TEST_USERNAME,
        "password": TEST_PASSWORD
    })
    return response.json()["access_token"]

if __name__ == "__main__":
    pytest.main()
