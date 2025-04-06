import os
import json
import hashlib
import base64
from typing import Dict, Any, List
from cryptography.fernet import Fernet
from mnemonic import Mnemonic
from bip32 import BIP32
from bip44 import BIP44
from src.config import Config  # Import the STABLECOIN_VALUE from the config

class Wallet:
    def __init__(self, password: str):
        self.password = password
        self.addresses: Dict[str, float] = {}  # Address to balance mapping
        self.transactions: List[Dict[str, Any]] = []  # List of transactions
        self.mnemonic = Mnemonic("english")
        self.bip32 = None
        self.load_or_create_wallet()

    def load_or_create_wallet(self):
        """Load existing wallet or create a new one."""
        if os.path.exists("wallet.json"):
            self.load_wallet("wallet.json")
        else:
            self.create_wallet()

    def create_wallet(self):
        """Create a new HD wallet."""
        seed = self.mnemonic.to_seed(self.mnemonic.generate())
        self.bip32 = BIP32.from_seed(seed)
        for i in range(5):  # Generate 5 addresses for demonstration
            address = self.generate_address(i)
            self.addresses[address] = 0.0  # Initialize balance to 0

    def generate_address(self, index: int) -> str:
        """Generate a new wallet address from the HD wallet."""
        child_key = self.bip32.get_child(index)
        public_key = child_key.public_key.hex()
        address = self.hash_address(public_key)
        return address

    def hash_address(self, public_key: str) -> str:
        """Create a wallet address from a public key."""
        return hashlib.sha256(public_key.encode()).hexdigest()

    def get_balance(self, address: str) -> float:
        """Get the balance of a specific address."""
        return self.addresses.get(address, 0.0)

    def add_balance(self, address: str, amount: float) -> None:
        """Add balance to a specific address."""
        if address not in self.addresses:
            raise Exception("Address does not exist.")
        if amount <= 0:
            raise Exception("Amount must be positive.")
        self.addresses[address] += amount

    def get_balance_in_usd(self, address: str) -> float:
        """Get the balance of a specific address in USD."""
        balance = self.get_balance(address)
        return balance * Config.STABLECOIN_VALUE  # Convert balance to USD

    def create_transaction(self, from_address: str, to_address: str, amount: float) -> bool:
        """Create a transaction from one address to another."""
        if from_address not in self.addresses:
            raise Exception("From address does not exist.")
        if to_address not in self.addresses:
            raise Exception("To address does not exist.")
        if self.addresses[from_address] < amount:
            raise Exception("Insufficient balance.")

        # Create the transaction
        transaction = {
            "from": from_address,
            "to": to_address,
            "amount": amount,
            "hash": self.hash_transaction(from_address, to_address, amount),
            "timestamp": self.get_current_timestamp()
        }
        self.transactions.append(transaction)

        # Update balances
        self.addresses[from_address] -= amount
        self.addresses[to_address] += amount
        return True

    def hash_transaction(self, from_address: str, to_address: str, amount: float) -> str:
        """Create a hash for the transaction."""
        transaction_string = f"{from_address}->{to_address}:{amount}"
        return hashlib.sha256(transaction_string.encode()).hexdigest()

    def get_current_timestamp(self) -> str:
        """Get the current timestamp."""
        from datetime import datetime
        return datetime.utcnow().isoformat()

    def get_transactions(self) -> List[Dict[str, Any]]:
        """Get the list of transactions."""
        return self.transactions

    def save_wallet(self, filename: str):
        """Save the wallet to a file with encryption."""
        wallet_data = {
            "addresses": self.addresses,
            "transactions": self.transactions
        }
        encrypted_data = self.encrypt_data(json.dumps(wallet_data))
        with open(filename, 'wb') as f:
            f.write(encrypted_data)

    def load_wallet(self, filename: str):
        """Load the wallet from a file with decryption."""
        if not os.path.exists(filename):
            raise Exception("Wallet file does not exist.")
        with open(filename, 'rb') as f:
            encrypted_data = f.read()
            data = self.decrypt_data(encrypted_data)
            wallet_data = json.loads(data)
            self.addresses = wallet_data.get("addresses", {})
            self.transactions = wallet_data.get("transactions", [])

    def encrypt_data(self, data: str) -> bytes:
        """Encrypt data using a symmetric key derived from the password."""
        key = base64.urlsafe_b64encode(hashlib.sha256(self.password.encode()).digest())
        fernet = Fernet(key)
        return fernet.encrypt(data.encode())

    def decrypt_data(self, encrypted_data: bytes) -> str:
        """Decrypt data using a symmetric key derived from the password."""
        key = base64.urlsafe_b64encode(hashlib.sha256(self.password.encode()).digest())
        fernet = Fernet(key)
        return fernet.decrypt(encrypted_data).decode()

    def multi_signature_transaction(self, from_addresses: List[str], to_address: str, amount: float, required_signatures: int) -> bool:
        """Create a multi-signature transaction."""
        if len(from_addresses) < required_signatures:
            raise Exception("Not enough addresses to create a multi-signature transaction.")
        
        # Check balances
        total_balance = sum(self.get_balance(addr) for addr in from_addresses)
        if total_balance < amount:
            raise Exception("Insufficient balance across provided addresses.")

        # Create the transaction
        transaction = {
            "from": from_addresses,
            "to": to_address,
            "amount": amount,
            "hash": self.hash_transaction_multi(from_addresses, to_address, amount),
            "timestamp": self.get_current_timestamp(),
            "required_signatures": required_signatures,
            "signatures": []
        }
        self.transactions.append(transaction)

        # Update balances
        for addr in from_addresses:
            self.addresses[addr] -= amount / len(from_addresses)  # Split amount equally for simplicity
        self.addresses[to_address] += amount
        return True

    def hash_transaction_multi(self, from_addresses: List[str], to_address: str, amount: float) -> str:
        """Create a hash for the multi-signature transaction."""
        transaction_string = f"{'|'.join(from_addresses)}->{to_address}:{amount}"
        return hashlib.sha256(transaction_string.encode()).hexdigest()

# Example usage
if __name__ == "__main__":
    password = input("Enter a password for your wallet: ")
    wallet = Wallet(password)

    # Generate addresses
    for i in range(5):
        address = wallet.generate_address(i)
        print(f"Address {i}: {address}, Balance: {wallet.get_balance(address)}")

    # Create a transaction
    address1 = list(wallet.addresses.keys())[0]
    address2 = list(wallet.addresses.keys())[1]
    wallet.add_balance(address1, 100.0)  # Manually set balance for testing
    wallet.create_transaction(address1, address2, 50.0)

    print(f"Transaction successful: {wallet.get_transactions()}")
    print(f"Address 1 Balance: {wallet.get_balance(address1)}")
    print(f"Address 2 Balance: {wallet.get_balance(address2)}")

    # Multi-signature transaction
    address3 = wallet.generate_address(2)
    wallet.add_balance(address3, 100.0)  # Manually set balance for testing
    wallet.multi_signature_transaction([address1, address3 ], address2, 50.0, required_signatures=2)

    print(f"Multi-signature Transaction successful: {wallet.get_transactions()}")
    print(f"Address 1 Balance: {wallet.get_balance(address1)}")
    print(f"Address 2 Balance: {wallet.get_balance(address2)}")
    print(f"Address 3 Balance: {wallet.get_balance(address3)}")

    # Save and load wallet
    wallet.save_wallet("my_wallet.json")
    new_wallet = Wallet(password)
    new_wallet.load_wallet("my_wallet.json")
    print(f"Loaded Address 1 Balance: {new_wallet.get_balance(address1)}")
    print(f"Pi Coin Symbol: Pi")  # Displaying the Pi Coin symbol
