import unittest
from transaction import Transaction, TransactionPool
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

class TestTransaction(unittest.TestCase):

    def setUp(self):
        # Sample private and public keys for testing
        self.private_key = """-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQ...
-----END PRIVATE KEY-----"""
        
        self.public_key = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQ...
-----END PUBLIC KEY-----"""
        
        self.sender = "Alice"
        self.recipient = "Bob"
        self.amount = 10.0
        self.transaction = Transaction(sender=self.sender, recipient=self.recipient, amount=self.amount)

    def test_transaction_initialization(self):
        self.assertEqual(self.transaction.sender, self.sender)
        self.assertEqual(self.transaction.recipient, self.recipient)
        self.assertEqual(self.transaction.amount, self.amount)
        self.assertGreater(self.transaction.value_in_usd, 0)

    def test_transaction_id_creation(self):
        transaction_id = self.transaction.create_transaction_id()
        self.assertEqual(transaction_id, self.transaction.transaction_id)

    def test_sign_transaction(self):
        self.transaction.sign_transaction(self.private_key)
        self.assertIsNotNone(self.transaction.signature)

    def test_verify_signature(self):
        self.transaction.sign_transaction(self.private_key)
        self.assertTrue(self.transaction.verify_signature())

    def test_invalid_signature(self):
        self.transaction.sign_transaction(self.private_key)
        # Modify the signature to test invalid verification
        self.transaction.signature = "invalid_signature"
        self.assertFalse(self.transaction.verify_signature())

    def test_transaction_pool(self):
        pool = TransactionPool()
        pool.add_transaction(self.transaction)
        self.assertEqual(len(pool), 1)
        self.assertEqual(pool.get_transactions()[0]['sender'], self.sender)

    def test_invalid_transaction_pool(self):
        pool = TransactionPool()
        with self.assertRaises(ValueError):
            pool.add_transaction(Transaction(sender=self.sender, recipient=self.recipient, amount=-5.0))

if __name__ == '__main__':
    unittest.main()
