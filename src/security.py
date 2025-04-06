import os
import base64
import hashlib
import secrets
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from typing import Tuple, Any

class Security:
    def __init__(self):
        self.key = self.generate_key()
        self.fernet = Fernet(self.key)

    @staticmethod
    def generate_key() -> bytes:
        """Generate a secure key for encryption."""
        return Fernet.generate_key()

    def encrypt_data(self, data: str) -> bytes:
        """Encrypt data using Fernet symmetric encryption."""
        return self.fernet.encrypt(data.encode())

    def decrypt_data(self, encrypted_data: bytes) -> str:
        """Decrypt data using Fernet symmetric encryption."""
        return self.fernet.decrypt(encrypted_data).decode()

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def generate_mfa_token() -> str:
        """Generate a random MFA token."""
        return secrets.token_hex(16)

    @staticmethod
    def create_rsa_keypair() -> Tuple[bytes, bytes]:
        """Generate an RSA key pair."""
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        public_key = private_key.public_key()

        # Serialize the private key
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL
        )

        # Serialize the public key
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        return private_pem, public_pem

    @staticmethod
    def sign_data(data: str, private_key: bytes) -> bytes:
        """Sign data using RSA private key."""
        private_key_obj = serialization.load_pem_private_key(
            private_key,
            password=None,
            backend=default_backend()
        )
        signature = private_key_obj.sign(
            data.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return signature

    @staticmethod
    def verify_signature(data: str, signature: bytes, public_key: bytes) -> bool:
        """Verify the signature using RSA public key."""
        public_key_obj = serialization.load_pem_public_key(
            public_key,
            backend=default_backend()
        )
        try:
            public_key_obj.verify(
                signature,
                data.encode(),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except Exception:
            return False

# Example usage
if __name__ == "__main__":
    security = Security()

    # Encrypt and decrypt data
    original_data = "Sensitive information"
    encrypted_data = security.encrypt_data(original_data)
    decrypted_data = security.decrypt_data(encrypted_data)
    print(f"Original: {original_data}, Encrypted: {encrypted_data}, Decrypted: {decrypted_data}")

    # Hash a password
    password = "my_secure_password"
    hashed_password = security.hash_password(password)
    print(f"Hashed Password: {hashed_password}")

    # Generate MFA token
    mfa_token = security.generate_mfa_token()
    print(f"MFA Token: {mfa_token}")

    # Create RSA key pair
    private_key, public_key = security.create_rsa_keypair()
    print(f"Private Key: {private_key.decode()}")
    print(f"Public Key: {public_key.decode()}")

    # Sign and verify data
    data_to_sign = "Data to be signed"
    signature = security.sign_data(data_to_sign, private_key)
    is_valid = security.verify_signature(data_to_sign, signature, public_key)
    print(f"Signature valid: {is_valid}")
