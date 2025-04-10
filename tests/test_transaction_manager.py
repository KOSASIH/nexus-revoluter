# test_transaction_manager.py

import unittest
from transaction import TransactionManager

class TestTransactionManager(unittest.TestCase):
    def setUp(self):
        self.transaction_manager = TransactionManager()

    def test_get_pending_transactions(self):
        """Test retrieving pending transactions."""
        self.transaction_manager.add_transaction("tx1")
        self.transaction_manager.add_transaction("tx2")
        pending_transactions = self.transaction_manager.get_pending_transactions()
        self.assertEqual(len(pending_transactions), 2)
        print("Pending transactions test passed.")

    def test_confirm_transaction(self):
        """Test confirming a transaction."""
        self.transaction_manager.add_transaction("tx1")
        self.transaction_manager.confirm_transaction("tx1")
        self.assertIn("tx1", self.transaction_manager.confirmed_transactions)
        print("Transaction confirmation test passed.")

if __name__ == "__main__":
    unittest.main()
