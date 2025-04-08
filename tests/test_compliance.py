import unittest
import os
import json
import sqlite3
from compliance import Compliance  # Assuming compliance.py is in the same directory

class TestCompliance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up a temporary database for testing."""
        cls.db_name = 'test_compliance.db'
        cls.compliance = Compliance(db_name=cls.db_name)

    @classmethod
    def tearDownClass(cls):
        """Clean up the temporary database after tests."""
        if os.path.exists(cls.db_name):
            os.remove(cls.db_name)

    def test_register_user(self):
        """Test user registration."""
        self.compliance.register_user('user1', 'Alice Smith', 'alice@example.com', '123-456-7890', 'doc1.pdf')
        with self.compliance.conn:
            cursor = self.compliance.conn.execute('SELECT * FROM users WHERE user_id = ?', ('user1',))
            user = cursor.fetchone()
            self.assertIsNotNone(user)
            self.assertEqual(user[1], 'Alice Smith')

    def test_verify_kyc(self):
        """Test KYC verification."""
        self.compliance.register_user('user2', 'Bob Johnson', 'bob@example.com', '098-765-4321', 'doc2.pdf')
        self.compliance.verify_kyc('user2')
        with self.compliance.conn:
            cursor = self.compliance.conn.execute('SELECT kyc_verified FROM users WHERE user_id = ?', ('user2',))
            kyc_verified = cursor.fetchone()[0]
            self.assertEqual(kyc_verified, 1)

    def test_log_transaction(self):
        """Test logging transactions."""
        self.compliance.register_user('user1', 'Alice Smith', 'alice@example.com', '123-456-7890', 'doc1.pdf')
        self.compliance.log_transaction('user1', 5000)
        with self.compliance.conn:
            cursor = self.compliance.conn.execute('SELECT * FROM transactions WHERE user_id = ?', ('user1',))
            transactions = cursor.fetchall()
            self.assertEqual(len(transactions), 1)
            self.assertEqual(transactions[0][2], 5000)

    def test_monitor_transactions(self):
        """Test monitoring for suspicious transactions."""
        self.compliance.register_user('user1', 'Alice Smith', 'alice@example.com', '123-456-7890', 'doc1.pdf')
        self.compliance.log_transaction('user1', 5000)
        self.compliance.log_transaction('user1', 15000)  # This should trigger suspicious activity
        suspicious = self.compliance.monitor_transactions()
        self.assertIn('user1', suspicious)

    def test_generate_regulatory_report(self):
        """Test generating a regulatory report."""
        self.compliance.register_user('user1', 'Alice Smith', 'alice@example.com', '123-456-7890', 'doc1.pdf')
        self.compliance.verify_kyc('user1')
        self.compliance.log_transaction('user1', 5000)
        report = self.compliance.generate_regulatory_report()
        self.assertIn('users', report)
        self.assertIn('suspicious_transactions', report)

    def test_save_report_to_file(self):
        """Test saving the regulatory report to a file."""
        self.compliance.register_user('user1', 'Alice Smith', 'alice@example.com', '123-456-7890', 'doc1.pdf')
        report_file = 'test_report.json'
        self.compliance.save_report_to_file(report_file)
        self.assertTrue(os.path.exists(report_file))
        with open(report_file, 'r') as f:
            report = json.load(f)
            self.assertIn('report_generated_at', report)
        os.remove(report_file)  # Clean up

    def test_export_report_to_csv(self):
        """Test exporting the regulatory report to a CSV file."""
        self.compliance.register_user('user1', 'Alice Smith', 'alice@example.com', '123-456-7890', 'doc1.pdf')
        csv_file = 'test_report.csv'
        self.compliance.export_report_to_csv(csv_file)
        self.assertTrue(os.path.exists(csv_file))
        os.remove(csv_file)  # Clean up

if __name__ == '__main__':
    unittest.main()
