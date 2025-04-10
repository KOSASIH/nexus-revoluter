import unittest
import os
import json
import sqlite3
from sustainability_tracking import SustainabilityTracker  # Adjust the import based on your file structure

class TestSustainabilityTracker(unittest.TestCase):
    def setUp(self):
        """Set up a temporary database for testing."""
        self.db_name = 'test_sustainability.db'
        self.tracker = SustainabilityTracker(db_name=self.db_name)
    
    def tearDown(self):
        """Clean up the temporary database after tests."""
        if os.path.exists(self.db_name):
            os.remove(self.db_name)

    def test_create_database(self):
        """Test if the database is created successfully."""
        self.assertTrue(os.path.exists(self.db_name))
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="transactions";')
            self.assertIsNotNone(cursor.fetchone())

    def test_validate_data(self):
        """Test data validation for energy and emissions."""
        self.assertTrue(self.tracker.validate_data(10, 5))
        self.assertFalse(self.tracker.validate_data(-1, 5))
        self.assertFalse(self.tracker.validate_data(10, -1))

    def test_log_transaction(self):
        """Test logging a transaction."""
        self.tracker.log_transaction("tx001", 10, 2.5)
        report = self.tracker.generate_report()
        self.assertEqual(report['total_energy_consumption'], 10)
        self.assertEqual(report['total_carbon_emissions'], 2.5)
        self.assertEqual(len(report['transactions']), 1)

    def test_duplicate_transaction_id(self):
        """Test logging a transaction with a duplicate ID."""
        self.tracker.log_transaction("tx002", 10, 2.5)
        self.tracker.log_transaction("tx002", 5, 1.0)  # Duplicate ID
        report = self.tracker.generate_report()
        self.assertEqual(len(report['transactions']), 1)  # Should still be 1

    def test_generate_report(self):
        """Test report generation."""
        self.tracker.log_transaction("tx003", 20, 5.0)
        report = self.tracker.generate_report()
        self.assertIn("total_energy_consumption", report)
        self.assertIn("total_carbon_emissions", report)
        self.assertIn("transactions", report)

    def test_save_report_to_file(self):
        """Test saving the report to a file."""
        self.tracker.log_transaction("tx004", 15, 3.0)
        self.tracker.save_report_to_file('test_report.json')
        self.assertTrue(os.path.exists('test_report.json'))
        with open('test_report.json', 'r') as f:
            data = json.load(f)
            self.assertIn("total_energy_consumption", data)
            self.assertIn("total_carbon_emissions", data)
            self.assertIn("transactions", data)
        os.remove('test_report.json')  # Clean up

    async def test_fetch_external_data(self):
        """Test fetching external data (mocking required)."""
        # This test requires mocking the aiohttp request.
        # You can use a library like aioresponses or unittest.mock to mock the response.
        pass  # Implement this test with a mocking library

if __name__ == '__main__':
    unittest.main()
