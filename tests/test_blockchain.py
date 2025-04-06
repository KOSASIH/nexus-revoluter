import unittest
import time
from blockchain import Blockchain, Block  # Assuming your blockchain implementation is in a file named blockchain.py

class TestBlockchain(unittest.TestCase):
    def setUp(self):
        """Set up a new Blockchain instance for testing."""
        self.blockchain = Blockchain()

    def test_initialization(self):
        """Test the initialization of the Blockchain."""
        self.assertEqual(len(self.blockchain), 1)  # Should have the genesis block
        self.assertEqual(self.blockchain.get_latest_block().data, "Genesis Block")

    def test_add_block(self):
        """Test adding a new block to the blockchain."""
        self.blockchain.add_transaction({"sender": "Alice", "recipient": "Bob", "amount": 10.0})
        new_block = self.blockchain.add_block(self.blockchain.current_transactions)
        self.assertEqual(len(self.blockchain), 2)  # One more block should be added
        self.assertEqual(new_block.data, self.blockchain.current_transactions)

    def test_add_transaction(self):
        """Test adding a transaction to the current transactions pool."""
        transaction = {"sender": "Alice", "recipient": "Bob", "amount": 10.0}
        self.blockchain.add_transaction(transaction)
        self.assertIn(transaction, self.blockchain.current_transactions)

    def test_add_transaction_invalid_amount(self):
        """Test adding a transaction with an invalid amount."""
        with self.assertRaises(ValueError) as context:
            self.blockchain.add_transaction({"sender": "Alice", "recipient": "Bob", "amount": -10.0})
        self.assertEqual(str(context.exception), "Transaction amount must be positive.")

    def test_validate_chain(self):
        """Test validating the blockchain."""
        self.blockchain.add_transaction({"sender": "Alice", "recipient": "Bob", "amount": 10.0})
        self.blockchain.add_block(self.blockchain.current_transactions)
        self.assertTrue(self.blockchain.validate_chain())

    def test_validate_chain_invalid_hash(self):
        """Test validating the blockchain with an invalid hash."""
        self.blockchain.add_transaction({"sender": "Alice", "recipient": "Bob", "amount": 10.0})
        self.blockchain.add_block(self.blockchain.current_transactions)
        # Tamper with the last block's hash
        self.blockchain.chain[-1].hash = "invalid_hash"
        self.assertFalse(self.blockchain.validate_chain())

    def test_get_block(self):
        """Test getting a block by its index."""
        self.blockchain.add_transaction({"sender": "Alice", "recipient": "Bob", "amount": 10.0})
        self.blockchain.add_block(self.blockchain.current_transactions)
        block = self.blockchain.get_block(1)
        self.assertIsNotNone(block)
        self.assertEqual(block.index, 1)

    def test_get_block_invalid_index(self):
        """Test getting a block with an invalid index."""
        block = self.blockchain.get_block(10)  # Out of range
        self.assertIsNone(block)

    def test_print_chain(self):
        """Test printing the blockchain."""
        # This is a simple test to ensure no exceptions are raised
        self.blockchain.print_chain()

if __name__ == '__main__':
    unittest.main()
