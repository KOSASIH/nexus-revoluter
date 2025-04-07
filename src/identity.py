import json
import hashlib
import logging
import base64
import requests
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature
from ipfshttpclient import connect

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DecentralizedIdentity:
    def __init__(self):
        self.identities = {}  # Store identities
        self.credentials = {}  # Store issued credentials
        self.revocation_list = {}  # Store revoked credentials
        self.ipfs_client = connect()  # Connect to IPFS

    def create_identity(self, user_id: str, multi_sig_keys: list = None) -> dict:
        """Create a new decentralized identity."""
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        public_key = private_key.public_key()

        identity = {
            "user_id": user_id,
            "public_key": self.serialize_public_key(public_key),
            "multi_sig_keys": multi_sig_keys or [],
            "credentials": []
        }

        self.identities[user_id] = {
            "private_key": private_key,
            "identity": identity
        }

        logging.info(f"Identity created for user: {user_id}")
        return identity

    def serialize_public_key(self, public_key) -> str:
        """Serialize the public key to a PEM format."""
        return public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode()

    def issue_credential(self, user_id: str, credential_data: dict) -> dict:
        """Issue a credential to a user."""
        if user_id not in self.identities:
            raise Exception("Identity does not exist.")

        private_key = self.identities[user_id]["private_key"]
        credential_id = self.generate_credential_id(credential_data)

        # Sign the credential data
        signature = private_key.sign(
            json.dumps(credential_data).encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        credential = {
            "credential_id": credential_id,
            "data": credential_data,
            "signature": signature.hex(),
            "revoked": False
        }

        # Store credential in IPFS
        ipfs_hash = self.store_in_ipfs(credential)
        credential["ipfs_hash"] = ipfs_hash

        self.identities[user_id]["identity"]["credentials"].append(credential)
        self.credentials[credential_id] = credential

        logging.info(f"Credential issued to {user_id}: {credential_id}")
        return credential

    def store_in_ipfs(self, data: dict) -> str:
        """Store data in IPFS and return the hash."""
        response = self.ipfs_client.add_json(data)
        return response['Hash']

    def generate_credential_id(self, credential_data: dict) -> str:
        """Generate a unique credential ID based on the credential data."""
        return hashlib.sha256(json.dumps(credential_data).encode()).hexdigest()

    def verify_credential(self, credential_id: str) -> bool:
        """Verify the issued credential."""
        if credential_id in self.revocation_list:
            logging.warning(f"Credential {credential_id} has been revoked.")
            return False

        if credential_id not in self.credentials:
            raise Exception("Credential does not exist.")

        credential = self.credentials[credential_id]
        public_key = self.get_public_key(credential)

        try:
            public_key.verify(
                bytes.fromhex(credential["signature"]),
                json.dumps(credential["data"]).encode(),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            logging.info(f"Credential { credential_id} verified successfully.")
            return True
        except InvalidSignature:
            logging.error(f"Credential {credential_id} verification failed.")
            return False

    def get_public_key(self, credential: dict):
        """Retrieve the public key from the credential."""
        for identity in self.identities.values():
            if credential in identity["identity"]["credentials"]:
                return serialization.load_pem_public_key(identity["identity"]["public_key"])
        raise Exception("Public key not found.")

    def revoke_credential(self, user_id: str, credential_id: str) -> bool:
        """Revoke an issued credential."""
        if user_id not in self.identities:
            raise Exception("Identity does not exist.")

        identity = self.identities[user_id]
        credentials = identity["identity"]["credentials"]

        for credential in credentials:
            if credential["credential_id"] == credential_id:
                credential["revoked"] = True
                self.revocation_list[credential_id] = credential
                logging.info(f"Credential {credential_id} revoked for user: {user_id}")
                return True

        logging.warning(f"Credential {credential_id} not found for user: {user_id}")
        return False

    def present_credential(self, user_id: str, credential_id: str) -> dict:
        """Present a credential selectively."""
        if user_id not in self.identities:
            raise Exception("Identity does not exist.")

        identity = self.identities[user_id]
        for credential in identity["identity"]["credentials"]:
            if credential["credential_id"] == credential_id and not credential["revoked"]:
                logging.info(f"Presenting credential {credential_id} for user: {user_id}")
                return {
                    "credential_id": credential["credential_id"],
                    "data": credential["data"]
                }

        raise Exception("Credential not found or has been revoked.")

# Example usage of the DecentralizedIdentity class
if __name__ == "__main__":
    did_system = DecentralizedIdentity()

    # Create a new identity
    user_id = "user123"
    identity = did_system.create_identity(user_id)

    # Issue a credential
    credential_data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "role": "admin"
    }
    credential = did_system.issue_credential(user_id, credential_data)

    # Verify the issued credential
    is_verified = did_system.verify_credential(credential["credential_id"])
    print(f"Credential verified: {is_verified}")

    # Present the credential
    presented_credential = did_system.present_credential(user_id, credential["credential_id"])
    print(f"Presented Credential: {presented_credential}")

    # Revoke the credential
    did_system.revoke_credential(user_id, credential["credential_id"])

    # Attempt to verify the revoked credential
    is_verified_after_revocation = did_system.verify_credential(credential["credential_id"])
    print(f"Credential verified after revocation: {is_verified_after_revocation}")
