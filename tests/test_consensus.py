import unittest
from blockchain import Block, Blockchain  # Assuming your classes are in a file named blockchain.py
import time

class TestBlock(unittest.TestCase):
    def test_block_initialization(self):
        """Test the initialization of a Block."""
        block = Block(1, "0", time.time(), "Test Block Data", "abc123")
        self.assertEqual(block.index, 1)
        self.assertEqual(block.previous_hash, "0")
        self.assertEqual(block.data, "Test Block Data")
        self.assertEqual(block.hash, "abc123")
        self.assertIsInstance(block.timestamp, float)
        self.assertIsInstance(block.nonce, int)

    def test_block_to_dict(self):
        """Test the conversion of a Block to a dictionary."""
        block = Block(1, "0", time.time(), "Test Block Data", "abc123")
        expected_dict = {
            "index": 1,
            "previous_hash": "0",
            "timestamp": block.timestamp,
            "data": "Test Block Data",
            "hash": "abc123",
            "nonce": 0
        }
        self.assertEqual(block.to_dict(), expected_dict)

class TestBlockchain(unittest.TestCase):
    def setUp(self):
        """Set up a new Blockchain instance for testing."""
        self.blockchain = Blockchain()

    def test_genesis_block(self):
        """Test that the genesis block is created correctly."""
        genesis_block = self.blockchain.get_chain()[0]
        self.assertEqual(genesis_block.index, 0)
        self.assertEqual(genesis_block.previous_hash, "0")
        self.assertEqual(genesis_block.data, "Genesis Block")
        self.assertEqual(len(self.blockchain.chain), 1)

    def test_add_block(self):
        """Test adding a new block to the blockchain."""
        new_block = self.blockchain.add_block("First block data")
        self.assertEqual(new_block.index, 1)
        self.assertEqual(new_block.data, "First block data")
        self.assertEqual(len(self.blockchain.chain), 2)

    def test_proof_of_work(self):
        """Test the proof of work mechanism."""
        previous_block = self.blockchain.chain[-1]
        index = previous_block.index + 1
        timestamp = time.time()
        data = "Test data"
        nonce, hash_value = self.blockchain.proof_of_work(index, previous_block.hash, timestamp, data)
        self.assertIsInstance(nonce, int)
        self.assertTrue(hash_value.startswith('0' * self.blockchain.difficulty))

    def test_adjust_difficulty(self):
        """Test the difficulty adjustment mechanism."""
        self.blockchain.add_block("First block data")
        self.blockchain.add_block("Second block data")
        self.blockchain.add_block("Third block data")
        self.assertEqual(self.blockchain.difficulty, 4)  # Initial difficulty

        # Simulate fast mining
        self.blockchain.chain[-1].timestamp -= 1  # Pretend the last block was mined quickly
        self.blockchain.adjust_difficulty()
        self.assertGreater(self.blockchain.difficulty, 4)  # Difficulty should increase

        # Simulate slow mining
        self.blockchain.chain[-1].timestamp += 20  # Pretend the last block took a long time
        self.blockchain.adjust_difficulty()
        self.assertLess(self.blockchain.difficulty, 5)  # Difficulty should decrease

    def test_validate_chain(self):
        """Test that the blockchain validates correctly."""
        self.blockchain.add_block("First block data")
        self.blockchain.add_block("Second block data")
        self.assertTrue(self.blockchain.validate_chain())

    def test_invalid_chain(self):
        """Test that an invalid chain is detected."""
        self.blockchain.add_block("First block data")
        self.blockchain.add_block("Second block data")
        
        # Tamper with the blockchain
        self.blockchain.chain[1].data = "Tampered data"
        self.assertFalse(self.blockchain.validate_chain())

if __name__ == '__main__':
    unittest.main()
