# quantum_resistant_crypto.py

import logging
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import os

class QuantumResistantCrypto:
    def __init__(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.private_key = None
        self.public_key = None

    def generate_keys(self):
        """Generate quantum-resistant keys (RSA as a placeholder)."""
        logging.info("Generating RSA key pair.")
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        self.public_key = self.private_key.public_key()
        logging.info("RSA key pair generated successfully.")

    def encrypt(self, plaintext):
        """Encrypt the plaintext using the public key."""
        if self.public_key is None:
            raise Exception("Public key is not set. Please generate or load keys first.")
        
        logging.info("Encrypting data.")
        ciphertext = self.public_key.encrypt(
            plaintext.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        logging.info("Data encrypted successfully.")
        return ciphertext

    def decrypt(self, ciphertext):
        """Decrypt the ciphertext using the private key."""
        if self.private_key is None:
            raise Exception("Private key is not set. Please generate or load keys first.")
        
        logging.info("Decrypting data.")
        plaintext = self.private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        logging.info("Data decrypted successfully.")
        return plaintext.decode()

    def serialize_private_key(self):
        """Serialize the private key to PEM format."""
        if self.private_key is None:
            raise Exception("Private key is not set.")
        
        logging.info("Serializing private key.")
        return self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL
        )

    def serialize_public_key(self):
        """Serialize the public key to PEM format."""
        if self.public_key is None:
            raise Exception("Public key is not set.")
        
        logging.info("Serializing public key.")
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

    def load_private_key(self, pem_data):
        """Load a private key from PEM format."""
        logging.info("Loading private key from PEM data.")
        self.private_key = serialization.load_pem_private_key(
            pem_data,
            password=None
        )
        logging.info("Private key loaded successfully.")

    def load_public_key(self, pem_data):
        """Load a public key from PEM format."""
        logging.info("Loading public key from PEM data.")
        self.public_key = serialization.load_pem_public_key(pem_data)
        logging.info("Public key loaded successfully.")

    def save_keys_to_file(self, private_key_path, public_key_path):
        """Save the private and public keys to files."""
        logging.info(f"Saving keys to {private_key_path} and {public_key_path}.")
        with open(private_key_path, 'wb') as f:
            f.write(self.serialize_private_key())
        with open(public_key_path, 'wb') as f:
            f.write(self.serialize_public_key())
        logging.info("Keys saved successfully.")

    def load_keys_from_file(self, private_key_path, public_key_path):
        """Load the private and public keys from files."""
        logging.info(f"Loading keys from {private_key_path} and {public_key_path}.")
        with open(private_key_path, 'rb') as f:
            self.load_private_key(f.read())
        with open(public_key_path, 'rb') as f:
            self.load_public_key(f.read())
        logging.info("Keys loaded successfully.")

# Example usage
if __name__ == "__main__":
    crypto = QuantumResistantCrypto()
    
    # Generate keys
    crypto.generate_keys()
    
    # Encrypt a message
    message = "This is a secret message."
    ciphertext = crypto.encrypt(message)
    print(f"Ciphertext: { ciphertext}")

    # Decrypt the message
    decrypted_message = crypto.decrypt(ciphertext)
    print(f"Decrypted Message: {decrypted_message}")

    # Save keys to files
    crypto.save_keys_to_file("private_key.pem", "public_key.pem")

    # Load keys from files
    crypto.load_keys_from_file("private_key.pem", "public_key.pem")

    # Verify decryption with loaded keys
    decrypted_message_loaded = crypto.decrypt(ciphertext)
    print(f"Decrypted Message with Loaded Key: {decrypted_message_loaded}")
