import unittest
from transaction import Transaction, TransactionPool

class TestTransaction(unittest.TestCase):
    def test_transaction_initialization(self):
        """Test the initialization of a Transaction."""
        transaction = Transaction(sender="Alice", recipient="Bob", amount=10.0)
        self.assertEqual(transaction.sender, "Alice")
        self.assertEqual(transaction.recipient, "Bob")
        self.assertEqual(transaction.amount, 10.0)
        self.assertIsNotNone(transaction.transaction_id)

    def test_create_transaction_id(self):
        """Test the creation of a unique transaction ID."""
        transaction = Transaction(sender="Alice", recipient="Bob", amount=10.0)
        transaction_id = transaction.create_transaction_id()
        self.assertEqual(transaction.transaction_id, transaction_id)

    def test_transaction_to_dict(self):
        """Test the conversion of a Transaction to a dictionary."""
        transaction = Transaction(sender="Alice", recipient="Bob", amount=10.0)
        expected_dict = {
            "transaction_id": transaction.transaction_id,
            "sender": "Alice",
            "recipient": "Bob",
            "amount": 10.0
        }
        self.assertEqual(transaction.to_dict(), expected_dict)

    def test_sign_transaction(self):
        """Test signing a transaction."""
        transaction = Transaction(sender="Alice", recipient="Bob", amount=10.0)
        private_key = "Alice's private key"
        signature = transaction.sign_transaction(private_key)
        self.assertIsNotNone(signature)

class TestTransactionPool(unittest.TestCase):
    def setUp(self):
        """Set up a new TransactionPool instance for testing."""
        self.transaction_pool = TransactionPool()

    def test_add_transaction(self):
        """Test adding a valid transaction to the pool."""
        transaction = Transaction(sender="Alice", recipient="Bob", amount=10.0)
        self.transaction_pool.add_transaction(transaction)
        self.assertEqual(len(self.transaction_pool.transactions), 1)

    def test_add_invalid_transaction(self):
        """Test adding an invalid transaction to the pool."""
        # In this case, we assume all transactions are valid, but you can implement checks
        transaction = Transaction(sender="Alice", recipient="Bob", amount=10.0)
        self.transaction_pool.add_transaction(transaction)
        self.assertEqual(len(self.transaction_pool.transactions), 1)

    def test_get_transactions(self):
        """Test getting the list of transactions in the pool."""
        transaction1 = Transaction(sender="Alice", recipient="Bob", amount=10.0)
        transaction2 = Transaction(sender="Charlie", recipient="Dave", amount=20.0)
        self.transaction_pool.add_transaction(transaction1)
        self.transaction_pool.add_transaction(transaction2)
        transactions = self.transaction_pool.get_transactions()
        self.assertEqual(len(transactions), 2)

    def test_clear_transactions(self):
        """Test clearing the transaction pool."""
        transaction = Transaction(sender="Alice", recipient="Bob", amount=10.0)
        self.transaction_pool.add_transaction(transaction)
        self.transaction_pool.clear_transactions()
        self.assertEqual(len(self.transaction_pool.transactions), 0)

    def test_transaction_pool_length(self):
        """Test the length of the transaction pool."""
        self.assertEqual(len(self.transaction_pool), 0)
        transaction = Transaction(sender="Alice", recipient="Bob", amount=10.0)
        self.transaction_pool.add_transaction(transaction)
        self.assertEqual(len(self.transaction_pool), 1)

if __name__ == '__main__':
    unittest.main()
