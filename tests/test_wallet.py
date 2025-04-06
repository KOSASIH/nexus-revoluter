import unittest
from unittest.mock import patch, MagicMock
import json
import os
from wallet import Wallet  # Assuming your wallet implementation is in a file named wallet.py

class TestWallet(unittest.TestCase):
    def setUp(self):
        """Set up a new Wallet instance for testing."""
        self.password = "test_password"
        self.wallet = Wallet(self.password)

    def test_initialization(self):
        """Test the initialization of the Wallet."""
        self.assertIsInstance(self.wallet.addresses, dict)
        self.assertIsInstance(self.wallet.transactions, list)
        self.assertGreater(len(self.wallet.addresses), 0)  # Should have generated addresses

    def test_generate_address(self):
        """Test generating a new address."""
        address = self.wallet.generate_address(0)
        self.assertIsInstance(address, str)
        self.assertEqual(len(address), 64)  # SHA-256 hash length

    def test_get_balance(self):
        """Test getting the balance of an address."""
        address = list(self.wallet.addresses.keys())[0]
        self.assertEqual(self.wallet.get_balance(address), 0.0)

    def test_create_transaction(self):
        """Test creating a transaction."""
        address1 = list(self.wallet.addresses.keys())[0]
        address2 = list(self.wallet.addresses.keys())[1]
        self.wallet.addresses[address1] = 100.0  # Set balance for testing
        success = self.wallet.create_transaction(address1, address2, 50.0)
        self.assertTrue(success)
        self.assertEqual(self.wallet.get_balance(address1), 50.0)
        self.assertEqual(self.wallet.get_balance(address2), 50.0)
        self.assertEqual(len(self.wallet.transactions), 1)

    def test_create_transaction_insufficient_balance(self):
        """Test creating a transaction with insufficient balance."""
        address1 = list(self.wallet.addresses.keys())[0]
        address2 = list(self.wallet.addresses.keys())[1]
        self.wallet.addresses[address1] = 30.0  # Set balance for testing
        with self.assertRaises(Exception) as context:
            self.wallet.create_transaction(address1, address2, 50.0)
        self.assertEqual(str(context.exception), "Insufficient balance.")

    def test_multi_signature_transaction(self):
        """Test creating a multi-signature transaction."""
        address1 = list(self.wallet.addresses.keys())[0]
        address2 = list(self.wallet.addresses.keys())[1]
        address3 = list(self.wallet.addresses.keys())[2]
        self.wallet.addresses[address1] = 100.0  # Set balance for testing
        self.wallet.addresses[address3] = 100.0  # Set balance for testing
        success = self.wallet.multi_signature_transaction([address1, address3], address2, 50.0, required_signatures=2)
        self.assertTrue(success)
        self.assertEqual(self.wallet.get_balance(address1), 50.0)
        self.assertEqual(self.wallet.get_balance(address3), 50.0)
        self.assertEqual(self.wallet.get_balance(address2), 50.0)
        self.assertEqual(len(self.wallet.transactions), 1)

    def test_save_wallet(self):
        """Test saving the wallet to a file."""
        self.wallet.save_wallet("test_wallet.json")
        self.assertTrue(os.path.exists("test_wallet.json"))

    def test_load_wallet(self):
        """Test loading the wallet from a file."""
        self.wallet.save_wallet("test_wallet.json")
        new_wallet = Wallet(self.password)
        new_wallet.load_wallet("test_wallet.json")
        self.assertEqual(new_wallet.get_balance(list(new_wallet.addresses.keys())[0]), 0.0)

    @patch("builtins.open", new_callable=MagicMock)
    def test_load_wallet_file_not_exist(self, mock_open):
        """Test loading a wallet that does not exist."""
        mock_open.side_effect = FileNotFoundError
        with self.assertRaises(Exception) as context:
            self.wallet.load_wallet("non_existent_wallet.json")
        self.assertEqual(str(context.exception), "Wallet file does not exist.")

    def tearDown(self):
        """Clean up after tests."""
        if os.path.exists("test_wallet.json"):
            os.remove("test_wallet.json")

if __name__ == '__main__':
    unittest.main()
