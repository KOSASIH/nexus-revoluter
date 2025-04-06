# tests/test_integration.py

import unittest
from unittest.mock import patch
from src.blockchain import Blockchain
from src.transaction import Transaction

class TestIntegration(unittest.TestCase):

    def setUp(self):
        """Initialize blockchain and transaction before each test."""
        self.blockchain = Blockchain()
        self.transaction = Transaction()

    def test_create_and_add_transaction(self):
        """Test creating and adding a transaction to the blockchain."""
        tx = self.transaction.create_transaction("address1", "address2", 10)
        self.blockchain.add_transaction(tx)
        
        # Validate that the transaction is in the current transactions pool
        self.assertIn(tx, self.blockchain.current_transactions)

    def test_mine_block_with_transaction(self):
        """Test mining a block with an existing transaction."""
        tx = self.transaction.create_transaction("address1", "address2", 10)
        self.blockchain.add_transaction(tx)
        
        previous_hash = self.blockchain.hash(self.blockchain.last_block)
        block = self.blockchain.mine_block(previous_hash)
        
        # Validate that the new block contains the transaction
        self.assertIn(tx, block['transactions'])
        self.assertEqual(block['previous_hash'], previous_hash)

    def test_invalid_transaction(self):
        """Test handling of an invalid transaction."""
        with self.assertRaises(ValueError):
            self.transaction.create_transaction("", "address2", 10)  # Invalid sender address

    def test_double_spending(self):
        """Test double spending scenario."""
        tx1 = self.transaction.create_transaction("address1", "address2", 10)
        tx2 = self.transaction.create_transaction("address1", "address2", 10)  # Same sender and amount
        
        self.blockchain.add_transaction(tx1)
        self.blockchain.add_transaction(tx2)  # Attempt to add a second transaction with the same inputs
        
        # Mine the block
        previous_hash = self.blockchain.hash(self.blockchain.last_block)
        self.blockchain.mine_block(previous_hash)
        
        # Check that only one transaction is processed
        self.assertEqual(len(self.blockchain.last_block['transactions']), 1)

    @patch('src.transaction.Transaction.create_transaction')
    def test_transaction_creation_with_mock(self, mock_create_transaction):
        """Test transaction creation using mocking."""
        mock_create_transaction.return_value = {"sender": "address1", "recipient": "address2", "amount": 10}
        
        tx = self.transaction.create_transaction("address1", "address2", 10)
        self.assertEqual(tx, {"sender": "address1", "recipient": "address2", "amount": 10})
        mock_create_transaction.assert_called_once_with("address1", "address2", 10)

    def test_blockchain_integrity(self):
        """Test the integrity of the blockchain."""
        tx1 = self.transaction.create_transaction("address1", "address2", 10)
        self.blockchain.add_transaction(tx1)
        previous_hash = self.blockchain.hash(self.blockchain.last_block)
        self.blockchain.mine_block(previous_hash)

        # Tamper with the blockchain
        self.blockchain.chain[0]['transactions'] = []  # Remove transactions from the first block
        
        # Validate that the blockchain is invalid
        self.assertFalse(self.blockchain.is_chain_valid(self.blockchain.chain))

    def test_large_number_of_transactions(self):
        """Test handling a large number of transactions."""
        for i in range(1000):
            tx = self.transaction.create_transaction(f"address{i}", f"address{i+1}", i)
            self.blockchain.add_transaction(tx)
        
        previous_hash = self.blockchain.hash(self.blockchain.last_block)
        block = self.blockchain.mine_block(previous_hash)
        
        # Validate that the block contains all transactions
        self.assertEqual(len(block['transactions']), 1000)

if __name__ == '__main__':
    unittest.main()
