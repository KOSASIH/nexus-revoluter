import hashlib
import json
import random
from datetime import datetime

class MultiSignatureWallet:
    def __init__(self, owners, required_signatures):
        """
        Initialize a multi-signature wallet.
        
        :param owners: List of public keys of wallet owners.
        :param required_signatures: Number of signatures required to authorize a transaction.
        """
        self.owners = owners
        self.required_signatures = required_signatures
        self.transactions = []

    def create_transaction(self, amount, to_address):
        """Create a new transaction."""
        transaction = {
            "amount": amount,
            "to": to_address,
            "timestamp": datetime.now().isoformat(),
            "status": "pending",
            "signatures": []
        }
        self.transactions.append(transaction)
        return transaction

    def sign_transaction(self, transaction, owner_private_key):
        """Sign a transaction with a private key."""
        if owner_private_key not in self.owners:
            raise ValueError("Invalid owner private key.")
        
        transaction_hash = self.hash_transaction(transaction)
        signature = self.sign(transaction_hash, owner_private_key)
        
        if signature not in transaction["signatures"]:
            transaction["signatures"].append(signature)
        
        if len(transaction["signatures"]) >= self.required_signatures:
            transaction["status"] = "completed"
            self.execute_transaction(transaction)

    def execute_transaction(self, transaction):
        """Execute the transaction (placeholder for actual execution logic)."""
        print(f"Transaction executed: {transaction}")

    @staticmethod
    def hash_transaction(transaction):
        """Hash the transaction for signing."""
        transaction_string = json.dumps(transaction, sort_keys=True)
        return hashlib.sha256(transaction_string.encode()).hexdigest()

    @staticmethod
    def sign(transaction_hash, private_key):
        """Simulate signing a transaction with a private key."""
        return f"{transaction_hash}_{private_key}"

class DecentralizedInsurance:
    def __init__(self):
        """Initialize the decentralized insurance pool."""
        self.policies = []

    def create_policy(self, miner_id, coverage_amount, premium):
        """Create a new insurance policy."""
        policy = {
            "miner_id": miner_id,
            "coverage_amount": coverage_amount,
            "premium": premium,
            "status": "active",
            "claims": []
        }
        self.policies.append(policy)
        return policy

    def file_claim(self, miner_id, claim_amount):
        """File a claim against an insurance policy."""
        for policy in self.policies:
            if policy["miner_id"] == miner_id and policy["status"] == "active":
                if claim_amount <= policy["coverage_amount"]:
                    claim = {
                        "amount": claim_amount,
                        "timestamp": datetime.now().isoformat(),
                        "status": "approved"
                    }
                    policy["claims"].append(claim)
                    print(f"Claim approved for {miner_id}: {claim}")
                    return claim
                else:
                    print(f"Claim amount exceeds coverage for {miner_id}.")
                    return None
        print(f"No active policy found for {miner_id}.")
        return None

# Example usage
if __name__ == "__main__":
    # Multi-Signature Wallet Example
    owners = ["owner1_pubkey", "owner2_pubkey", "owner3_pubkey"]
    wallet = MultiSignatureWallet(owners, required_signatures=2)

    transaction = wallet.create_transaction(amount=100, to_address="recipient_address")
    wallet.sign_transaction(transaction, "owner1_private_key")
    wallet.sign_transaction(transaction, "owner2_private_key")  # This should complete the transaction

    # Decentralized Insurance Example
    insurance = DecentralizedInsurance()
    policy = insurance.create_policy(miner_id="Miner_001", coverage_amount=500, premium=50)
    claim = insurance.file_claim(miner_id="Miner_001", claim_amount=300)  # Should approve the claim
    claim = insurance.file_claim(miner_id="Miner_001", claim_amount=600)  # Should fail due to exceeding coverage
