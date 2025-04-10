import unittest
from cryptography.hazmat.primitives.asymmetric import rsa
from quantum_resistant_crypto import QuantumResistantCrypto

class TestQuantumResistantCrypto(unittest.TestCase):
    def setUp(self):
        """Set up a new QuantumResistantCrypto instance for testing."""
        self.crypto = QuantumResistantCrypto()
        self.private_key, self.public_key = self.crypto.generate_keys()

    def test_key_generation(self):
        """Test the generation of RSA keys."""
        self.assertIsInstance(self.private_key, rsa.RSAPrivateKey)
        self.assertIsInstance(self.public_key, rsa.RSAPublicKey)

    def test_encrypt_decrypt(self):
        """Test encryption and decryption."""
        message = "This is a secret message."
        ciphertext = self.crypto.encrypt(message, self.public_key)
        decrypted_message = self.crypto.decrypt(ciphertext, self.private_key)
        self.assertEqual(decrypted_message, message)

    def test_serialize_private_key(self):
        """Test serialization of the private key."""
        private_key_pem = self.crypto.serialize_private_key(self.private_key)
        self.assertIsInstance(private_key_pem, bytes)

    def test_serialize_public_key(self):
        """Test serialization of the public key."""
        public_key_pem = self.crypto.serialize_public_key(self.public_key)
        self.assertIsInstance(public_key_pem, bytes)

    def test_load_private_key(self):
        """Test loading a private key from PEM format."""
        private_key_pem = self.crypto.serialize_private_key(self.private_key)
        loaded_private_key = self.crypto.load_private_key(private_key_pem)
        self.assertIsInstance(loaded_private_key, rsa.RSAPrivateKey)

    def test_load_public_key(self):
        """Test loading a public key from PEM format."""
        public_key_pem = self.crypto.serialize_public_key(self.public_key)
        loaded_public_key = self.crypto.load_public_key(public_key_pem)
        self.assertIsInstance(loaded_public_key, rsa.RSAPublicKey)

    def test_decrypt_with_loaded_key(self):
        """Test decryption with a loaded private key."""
        private_key_pem = self.crypto.serialize_private_key(self.private_key)
        loaded_private_key = self.crypto.load_private_key(private_key_pem)
        
        message = "This is a secret message."
        ciphertext = self.crypto.encrypt(message, self.public_key)
        decrypted_message_loaded = self.crypto.decrypt(ciphertext, loaded_private_key)
        self.assertEqual(decrypted_message_loaded, message)

if __name__ == '__main__':
    unittest.main()
