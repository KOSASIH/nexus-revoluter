import hashlib
import json
from typing import Any, Dict, List

class Transaction:
    def __init__(self, sender: str, recipient: str, amount: float):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.transaction_id = self.create_transaction_id()

    def create_transaction_id(self) -> str:
        """Create a unique transaction ID based on the transaction details."""
        transaction_string = json.dumps({
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount
        }, sort_keys=True).encode()
        return hashlib.sha256(transaction_string).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        """Convert the transaction to a dictionary for easy serialization."""
        return {
            "transaction_id": self.transaction_id,
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount
        }

    def sign_transaction(self, private_key: str) -> str:
        """Sign the transaction with the sender's private key."""
        # In a real implementation, you would use a cryptographic library to sign the transaction
        # Here we just return a placeholder for the signature
        return hashlib.sha256((self.transaction_id + private_key).encode()).hexdigest()

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
    transaction_pool.add_transaction(transaction)

    # Sign the transaction (placeholder for actual signing)
    private_key = "Alice's private key"
    signature = transaction.sign_transaction(private_key)
    print(f"Transaction signed with signature: {signature}")

    # Print the transaction pool
    print("Transaction Pool:", transaction_pool.get_transactions())
