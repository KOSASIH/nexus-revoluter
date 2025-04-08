import unittest
import os
import json
from src.pi_wallet import PiWallet  # Adjust the import based on your project structure
from src.config import Config

class TestPiWallet(unittest.TestCase):
    def setUp(self):
        """Set up a new wallet for testing."""
        self.password = "StrongPassword123!"
        self.wallet = PiWallet(self.password)
        self.test_address1 = self.wallet.generate_address(0)
        self.test_address2 = self.wallet.generate_address(1)
        self.wallet.add_balance(self.test_address1, 100.0)  # Set initial balance for testing

    def tearDown(self):
        """Clean up after tests."""
        if os.path.exists("wallet.json"):
            os.remove("wallet.json")
        if os.path.exists("my_pi_wallet_backup.json"):
            os.remove("my_pi_wallet_backup.json")

    def test_wallet_creation(self):
        """Test wallet creation and address generation."""
        self.assertIsNotNone(self.wallet.bip32)
        self.assertIn(self.test_address1, self.wallet.addresses)
        self.assertEqual(self.wallet.get_balance(self.test_address1), 100.0)

    def test_add_balance(self):
        """Test adding balance to an address."""
        self.wallet.add_balance(self.test_address1, 50.0)
        self.assertEqual(self.wallet.get_balance(self.test_address1), 150.0)

    def test_insufficient_balance(self):
        """Test transaction creation with insufficient balance."""
        with self.assertRaises(Exception) as context:
            self.wallet.create_transaction(self.test_address1, self.test_address2, 200.0, fee=1.0)
        self.assertTrue("Insufficient balance." in str(context.exception))

    def test_create_transaction(self):
        """Test creating a transaction."""
        self.wallet.create_transaction(self.test_address1, self.test_address2, 50.0, fee=1.0)
        self.assertEqual(self.wallet.get_balance(self.test_address1), 49.0)  # 100 - 50 - 1
        self.assertEqual(self.wallet.get_balance(self.test_address2), 50.0)  # 0 + 50
        self.assertEqual(len(self.wallet.get_transactions()), 1)

    def test_multi_signature_transaction(self):
        """Test creating a multi-signature transaction."""
        self.wallet.add_balance(self.test_address2, 100.0)  # Add balance to the second address
        address3 = self.wallet.generate_address(2)
        self.wallet.add_balance(address3, 100.0)  # Add balance to the third address

        self.wallet.multi_signature_transaction([self.test_address1, address3], self.test_address2, 50.0, required_signatures=2)
        self.assertEqual(self.wallet.get_balance(self.test_address2), 150.0)  # 100 + 50
        self.assertEqual(self.wallet.get_balance(self.test_address1), 49.0)  # 100 - 50 - 1
        self.assertEqual(self.wallet.get_balance(address3), 99.0)  # 100 - 1

    def test_save_and_load_wallet(self):
        """Test saving and loading the wallet."""
        self.wallet.save_wallet("my_pi_wallet.json")
        new_wallet = PiWallet(self.password)
        new_wallet.load_wallet("my_pi_wallet.json")
        self.assertEqual(new_wallet.get_balance(self.test_address1), 100.0)

    def test_backup_and_restore_wallet(self):
        """Test wallet backup and restore functionality."""
        self.wallet.backup_wallet("my_pi_wallet_backup.json")
        new_wallet = PiWallet(self.password)
        new_wallet.restore_wallet("my_pi_wallet_backup.json")
        self.assertEqual(new_wallet.get_balance(self.test_address1), 100.0)

    def test_fetch_real_time_price(self):
        """Test fetching real-time price."""
        price = self.wallet.fetch_real_time_price("usd-coin")  # Example for USD Coin
        self.assertIsInstance(price, float)

    def test_password_strength_validation(self):
        """Test password strength validation."""
        self.assertTrue(self.wallet.validate_password_strength())

    def test_enable_two_factor_authentication(self):
        """Test enabling two-factor authentication."""
        self.wallet.enable_two_factor_authentication()
        self.assertTrue(self.wallet.two_factor_enabled)

    def test_verify_2fa(self):
        """Test 2FA verification."""
        self.wallet.enable_two_factor_authentication()
        # Simulate user input for 2FA
        with unittest.mock.patch('builtins.input', return_value='123456'):
            self.assertTrue(self.wallet.verify_2fa())

if __name__ == "__main__":
    unittest.main()
