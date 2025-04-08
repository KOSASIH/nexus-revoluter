import unittest
import json
from blockchain import Blockchain  # Assuming your blockchain code is in blockchain.py
from flask import Flask

class TestBlockchain(unittest.TestCase):

    def setUp(self):
        """Create a new blockchain instance for testing."""
        self.blockchain = Blockchain()
        self.app = Flask(__name__)
        self.app.testing = True
        self.client = self.app.test_client()

    def test_genesis_block(self):
        """Test that the genesis block is created correctly."""
        self.assertEqual(len(self.blockchain.chain), 1)
        self.assertEqual(self.blockchain.chain[0].index, 0)
        self.assertEqual(self.blockchain.chain[0].data, "Genesis Block")

    def test_add_transaction(self):
        """Test adding a transaction."""
        self.blockchain.wallets["Alice"] = 1000.00
        self.blockchain.wallets["Bob"] = 500.00
        transaction = {
            "sender": "Alice",
            "recipient": "Bob",
            "amount": 100.00,
            "currency": "Pi"
        }
        self.blockchain.add_transaction(transaction)
        self.assertEqual(len(self.blockchain.current_transactions), 1)
        self.assertEqual(self.blockchain.wallets["Alice"], 899.00)  # 1000 - 100 - 1% fee
        self.assertEqual(self.blockchain.wallets["Bob"], 600.00)    # 500 + 100

    def test_mine_block(self):
        """Test mining a block."""
        self.blockchain.wallets["Alice"] = 1000.00
        self.blockchain.add_transaction({
            "sender": "Alice",
            "recipient": "Bob",
            "amount": 100.00,
            "currency": "Pi"
        })
        mined_block = self.blockchain.mine_block()
        self.assertEqual(len(self.blockchain.chain), 2)
        self.assertEqual(mined_block.index, 1)
        self.assertEqual(mined_block.data[0]['sender'], "Alice")
        self.assertEqual(mined_block.data[0]['recipient'], "Bob")

    def test_validate_chain(self):
        """Test that the blockchain validation works."""
        self.blockchain.wallets["Alice"] = 1000.00
        self.blockchain.add_transaction({
            "sender": "Alice",
            "recipient": "Bob",
            "amount": 100.00,
            "currency": "Pi"
        })
        self.blockchain.mine_block()
        self.assertTrue(self.blockchain.validate_chain())

    def test_api_new_transaction(self):
        """Test the /transactions/new API endpoint."""
        self.blockchain.wallets["Alice"] = 1000.00
        response = self.client.post('/transactions/new', json={
            "sender": "Alice",
            "recipient": "Bob",
            "amount": 100.00
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn(b'Transaction will be added to the next block', response.data)

    def test_api_mine(self):
        """Test the /mine API endpoint."""
        self.blockchain.wallets["Alice"] = 1000.00
        self.blockchain.add_transaction({
            "sender": "Alice",
            "recipient": "Bob",
            "amount": 100.00,
            "currency": "Pi"
        })
        response = self.client.get('/mine')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'New block mined', response.data)

    def test_api_chain(self):
        """Test the /chain API endpoint."""
        response = self.client.get('/chain')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'chain', response.data)

if __name__ == '__main__':
    unittest.main()
