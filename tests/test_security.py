import unittest
from security import Security
from cryptography.exceptions import InvalidSignature

class TestSecurity(unittest.TestCase):
    def setUp(self):
        """Set up the Security instance for testing."""
        self.security = Security()
        self.test_data = "Sensitive information"
        self.test_password = "my_secure_password"
        self.test_mfa_token = self.security.generate_mfa_token()
        self.private_key, self.public_key = self.security.create_rsa_keypair()

    def test_encrypt_decrypt(self):
        """Test encryption and decryption of data."""
        encrypted_data = self.security.encrypt_data(self.test_data)
        decrypted_data = self.security.decrypt_data(encrypted_data)
        self.assertEqual(decrypted_data, self.test_data, "Decrypted data does not match original data.")

    def test_hash_password(self):
        """Test password hashing."""
        hashed_password = self.security.hash_password(self.test_password)
        self.assertNotEqual(hashed_password, self.test_password, "Hashed password should not match the original.")
        self.assertEqual(hashed_password, self.security.hash_password(self.test_password), "Hashing should be consistent.")

    def test_generate_mfa_token(self):
        """Test MFA token generation."""
        self.assertEqual(len(self.test_mfa_token), 32, "MFA token should be 32 characters long.")

    def test_rsa_keypair_generation(self):
        """Test RSA key pair generation."""
        self.assertIsNotNone(self.private_key, "Private key should not be None.")
        self.assertIsNotNone(self.public_key, "Public key should not be None.")

    def test_sign_verify_data(self):
        """Test signing and verifying data."""
        signature = self.security.sign_data(self.test_data, self.private_key)
        is_valid = self.security.verify_signature(self.test_data, signature, self.public_key)
        self.assertTrue(is_valid, "Signature should be valid.")

        # Test with altered data
        altered_data = "Altered data"
        with self.assertRaises(InvalidSignature):
            self.security.verify_signature(altered_data, signature, self.public_key)

    def test_decrypt_invalid_data(self):
        """Test decryption of invalid data."""
        with self.assertRaises(Exception):
            self.security.decrypt_data(b"invalid_encrypted_data")

if __name__ == "__main__":
    unittest.main()
