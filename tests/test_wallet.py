import unittest
import os
from src.wallet import Wallet  # Adjust the import based on your project structure
from src.config import Config  # Ensure this is correctly imported

class TestWallet(unittest.TestCase):
    def setUp(self):
        """Set up a new wallet for testing."""
        self.password = "StrongPassword123!"
        self.wallet = Wallet(self.password)

    def tearDown(self):
        """Clean up after tests."""
        if os.path.exists("my_wallet.json"):
            os.remove("my_wallet.json")

    def test_create_wallet(self):
        """Test wallet creation and address generation."""
        self.assertIsNotNone(self.wallet.bip32)
        self.assertEqual(len(self.wallet.addresses), 5)  # 5 addresses should be generated

    def test_get_balance(self):
        """Test getting balance for a new address."""
        address = list(self.wallet.addresses.keys())[0]
        self.assertEqual(self.wallet.get_balance(address), 0.0)

    def test_add_balance(self):
        """Test adding balance to an address."""
        address = list(self.wallet.addresses.keys())[0]
        self.wallet.add_balance(address, 100.0)
        self.assertEqual(self.wallet.get_balance(address), 100.0)

    def test_create_transaction(self):
        """Test creating a transaction."""
        address1 = list(self.wallet.addresses.keys())[0]
        address2 = list(self.wallet.addresses.keys())[1]
        self.wallet.add_balance(address1, 100.0)
        success = self.wallet.create_transaction(address1, address2, 50.0, fee=1.0)
        self.assertTrue(success)
        self.assertEqual(self.wallet.get_balance(address1), 49.0)  # 100 - 50 - 1
        self.assertEqual(self.wallet.get_balance(address2), 50.0)

    def test_insufficient_balance_transaction(self):
        """Test transaction with insufficient balance."""
        address1 = list(self.wallet.addresses.keys())[0]
        address2 = list(self.wallet.addresses.keys())[1]
        with self.assertRaises(Exception) as context:
            self.wallet.create_transaction(address1, address2, 100.0, fee=1.0)
        self.assertTrue("Insufficient balance." in str(context.exception))

    def test_multi_signature_transaction(self):
        """Test creating a multi-signature transaction."""
        address1 = list(self.wallet.addresses.keys())[0]
        address2 = list(self.wallet.addresses.keys())[1]
        address3 = list(self.wallet.addresses.keys())[2]
        self.wallet.add_balance(address1, 100.0)
        self.wallet.add_balance(address3, 100.0)

        success = self.wallet.multi_signature_transaction([address1, address3], address2, 50.0, required_signatures=2)
        self.assertTrue(success)
        self.assertEqual(self.wallet.get_balance(address1), 50.0)  # 100 - 50
        self.assertEqual(self.wallet.get_balance(address3), 50.0)  # 100 - 50
        self.assertEqual(self.wallet.get_balance(address2), 50.0)   # 0 + 50

    def test_multi_signature_insufficient_balance(self):
        """Test multi-signature transaction with insufficient balance."""
        address1 = list(self.wallet.addresses.keys())[0]
        address2 = list(self.wallet.addresses.keys())[1]
        address3 = list(self.wallet.addresses.keys())[2]
        self.wallet.add_balance(address1, 30.0)
        self.wallet.add_balance(address3, 30.0)

        with self.assertRaises(Exception) as context:
            self.wallet.multi_signature_transaction([address1, address3], address2, 100.0, required_signatures=2)
        self.assertTrue("Insufficient balance across provided addresses." in str(context.exception))

    def test_save_and_load_wallet(self):
        """Test saving and loading the wallet."""
        self.wallet.add_balance(list(self.wallet.addresses.keys())[0], 100.0)
        self.wallet.save_wallet("my_wallet.json")

        new_wallet = Wallet(self.password)
        new_wallet.load_wallet("my_wallet.json")
        self.assertEqual(new_wallet.get_balance(list(new_wallet.addresses.keys())[0]), 100.0)

    def test_password_strength_validation(self):
        """Test password strength validation."""
        weak_password = "weak"
        wallet_weak = Wallet(weak_password)
        with self.assertRaises(Exception) as context:
            wallet_weak.validate_password_strength()
        self.assertTrue("Password must be at least 8 characters long." in str(context.exception))

        strong_password = "StrongPassword123!"
        wallet_strong = Wallet(strong_password)
        self.assertTrue(wallet_strong.validate_password_strength())

if __name__ == "__main__":
    unittest.main()
