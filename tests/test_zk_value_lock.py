import unittest
from unittest.mock import patch, MagicMock
from zk_value_lock import ZKValueLock
from transaction import Transaction

class TestZKValueLock(unittest.TestCase):

    @patch('zk_value_lock.ZKProof')
    @patch('zk_value_lock.Transaction')
    def setUp(self, mock_transaction, mock_zkproof):
        # Mock the zero-knowledge proof methods
        self.mock_proof = "mock_proof"
        mock_zkproof.create_proof.return_value = self.mock_proof
        mock_zkproof.verify_proof.return_value = True

        # Mock the Transaction class
        self.mock_transaction_instance = MagicMock()
        mock_transaction.return_value = self.mock_transaction_instance

        # Initialize the ZKValueLock class
        self.zk_value_lock = ZKValueLock()

    def test_create_transaction_success(self):
        transaction = self.zk_value_lock.create_transaction("user1", "user2", 314159.00)
        self.assertIsNotNone(transaction)
        self.assertEqual(transaction.sender, "user1")
        self.assertEqual(transaction.recipient, "user2")
        self.assertEqual(transaction.amount, 314159.00)
        self.assertEqual(transaction.proof, self.mock_proof)

    def test_create_transaction_invalid_amount(self):
        with self.assertRaises(ValueError) as context:
            self.zk_value_lock.create_transaction("user1", "user2", 100000.00)
        self.assertTrue("Transaction amount must equal the target value." in str(context.exception))

    def test_validate_transaction_success(self):
        transaction = Transaction("user1", "user2", 314159.00, self.mock_proof)
        is_valid = self.zk_value_lock.validate_transaction(transaction)
        self.assertTrue(is_valid)

    def test_validate_transaction_failure(self):
        # Mock the verify_proof method to return False
        with patch('zk_value_lock.ZKProof.verify_proof', return_value=False):
            transaction = Transaction("user1", "user2", 314159.00, self.mock_proof)
            is_valid = self.zk_value_lock.validate_transaction(transaction)
            self.assertFalse(is_valid)

    @patch('zk_value_lock.logging.info')
    def test_audit_transaction(self, mock_logging_info):
        transaction = Transaction("user1", "user2", 314159.00, self.mock_proof)
        self.zk_value_lock.audit_transaction(transaction)
        mock_logging_info.assert_called_with(f"Auditing transaction: {{'sender': 'user1', 'recipient': 'user2', 'amount': 314159.0, 'proof': '{self.mock_proof}'}}")

if __name__ == '__main__':
    unittest.main()
