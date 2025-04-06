import unittest
from blockchain import Block, Blockchain

class TestBlock(unittest.TestCase):
    def test_block_initialization(self):
        """Test the initialization of a Block."""
        block = Block(1, "0", 1633072800.0, "Test Block Data", "abc123")
        self.assertEqual(block.index, 1)
        self.assertEqual(block.previous_hash, "0")
        self.assertEqual(block.timestamp, 1633072800.0)
        self.assertEqual(block.data, "Test Block Data")
        self.assertEqual(block.hash, "abc123")

    def test_block_to_dict(self):
        """Test the conversion of a Block to a dictionary."""
        block = Block(1, "0", 1633072800.0, "Test Block Data", "abc123")
        expected_dict = {
            "index": 1,
            "previous_hash": "0",
            "timestamp": 1633072800.0,
            "data": "Test Block Data",
            "hash": "abc123"
        }
        self.assertEqual(block.to_dict(), expected_dict)

class TestBlockchain(unittest.TestCase):
    def setUp(self):
        """Set up a new Blockchain instance for testing."""
        self.blockchain = Blockchain()

    def test_genesis_block(self):
        """Test that the genesis block is created correctly."""
        genesis_block = self.blockchain.get_block(0)
        self.assertIsNotNone(genesis_block)
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

    def test_get_chain(self):
        """Test getting the blockchain as a list of dictionaries."""
        self.blockchain.add_block("First block data")
        chain_data = self.blockchain.get_chain()
        self.assertEqual(len(chain_data), 2)  # Genesis + 1 new block
        self.assertEqual(chain_data[1]["data"], "First block data")

    def test_get_block(self):
        """Test getting a specific block by index."""
        self.blockchain.add_block("First block data")
        block = self.blockchain.get_block(1)
        self.assertIsNotNone(block)
        self.assertEqual(block.data, "First block data")
        self.assertIsNone(self.blockchain.get_block(2))  # Out of range

if __name__ == '__main__':
    unittest.main()
