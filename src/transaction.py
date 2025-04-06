import hashlib
import json
from typing import Any, Dict, List
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from src.config import Config  # Import the Config class to access STABLECOIN_VALUE

class Transaction:
    def __init__(self, sender: str, recipient: str, amount: float):
        if amount <= 0:
            raise ValueError("Transaction amount must be positive.")
        
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.value_in_usd = self.calculate_value_in_usd()  # Calculate USD value
        self.transaction_id = self.create_transaction_id()
        self.signature = None  # Placeholder for the transaction signature

    def calculate_value_in_usd(self) -> float:
        """Calculate the value of the transaction in USD based on the stablecoin value."""
        return self.amount * Config.STABLECOIN_VALUE  # Pi Coin as stablecoin

    def create_transaction_id(self) -> str:
        """Create a unique transaction ID based on the transaction details."""
        transaction_string = json.dumps({
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "value_in_usd": self.value_in_usd  # Include USD value in the transaction ID
        }, sort_keys=True).encode()
        return hashlib.sha256(transaction_string).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        """Convert the transaction to a dictionary for easy serialization."""
        return {
            "transaction_id": self.transaction_id,
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "value_in_usd": self.value_in_usd,  # Include USD value in the dictionary
            "signature": self.signature  # Include signature in the dictionary
        }

    def sign_transaction(self, private_key: str) -> None:
        """Sign the transaction with the sender's private key."""
        private_key_obj = serialization.load_pem_private_key(
            private_key.encode(),
            password=None,
            backend=default_backend()
        )
        self.signature = private_key_obj.sign(
            self.transaction_id.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        ).hex()  # Store the signature as a hex string

    def verify_signature(self) -> bool:
        """Verify the transaction signature using the sender's public key."""
        public_key = self.get_public_key(self.sender)  # Placeholder for public key retrieval
        public_key_obj = serialization.load_pem_public_key(
            public_key.encode(),
            backend=default_backend()
        )
        try:
            public_key_obj.verify(
                bytes.fromhex(self.signature),
                self.transaction_id.encode(),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except Exception:
            return False

    def get_public_key(self, sender: str) -> str:
        """Retrieve the public key for the sender (placeholder implementation)."""
        # In a real implementation, you would retrieve the public key from a secure storage
        # Here we return a placeholder public key for demonstration purposes
        return "-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----"

class TransactionPool:
    def __init__(self):
        self.transactions: List[Transaction] = []

    def add_transaction(self, transaction: Transaction) -> None:
        """Add a transaction to the pool."""
        if self.validate_transaction(transaction):
            self.transactions.append(transaction)
        else:
            raise ValueError("Invalid transaction.")

    def validate_transaction(self, transaction: Transaction) -> bool:
        """Validate a transaction (e.g., check if the sender has enough balance)."""
        # Placeholder for validation logic (e.g., checking balances)
        # In a real implementation, you would check the sender's balance against the amount
        # For now, we assume all transactions are valid
        return True

    def get_transactions(self) -> List[Dict[str, Any]]:
        """Get the list of transactions in the pool as dictionaries."""
        return [transaction.to_dict() for transaction in self.transactions]

    def clear_transactions(self) -> None:
        """Clear the transaction pool."""
        self.transactions = []

    def __len__(self) -> int:
        """Return the number of transactions in the pool."""
        return len(self.transactions)

# Example usage
if __name__ == "__main__":
    # Create a transaction pool
    transaction_pool = TransactionPool()

    # Create a new transaction
    transaction = Transaction(sender="Alice", recipient="Bob", amount=10.0)
    
    # Sign the transaction (using a placeholder private key)
    private_key = """-----BEGIN PRIVATE KEY-----
...
-----END PRIVATE KEY-----"""
    
    transaction.sign_transaction(private_key)

    # Verify the transaction signature
    if transaction.verify_signature():
        transaction_pool.add_transaction(transaction)
        print("Transaction added to the pool.")
    else:
        print("Transaction signature verification failed.")

    # Print the transaction pool
    print("Transaction Pool:", transaction_pool.get_transactions())
