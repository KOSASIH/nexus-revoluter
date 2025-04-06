import unittest
import logging
import os
from monitoring import Monitoring
from unittest.mock import patch, MagicMock

class TestMonitoring(unittest.TestCase):
    def setUp(self):
        """Set up the Monitoring instance for testing."""
        self.log_file = "test_monitor.log"
        self.monitoring = Monitoring(log_file=self.log_file)

    def tearDown(self):
        """Clean up after tests."""
        if os.path.exists(self.log_file):
            os.remove(self.log_file)

    @patch('psutil.cpu_percent')
    @patch('psutil.virtual_memory')
    @patch('psutil.disk_usage')
    def test_log_system_metrics(self, mock_disk_usage, mock_virtual_memory, mock_cpu_percent):
        """Test logging of system metrics."""
        # Mock the return values
        mock_cpu_percent.return_value = 50.0
        mock_virtual_memory.return_value = MagicMock(percent=70, total=8000, available=2400)
        mock_disk_usage.return_value = MagicMock(percent=60, total=10000, used=6000, free=4000)

        metrics = self.monitoring.log_system_metrics()

        self.assertEqual(metrics['cpu_usage'], 50.0)
        self.assertEqual(metrics['memory_usage'], 70)
        self.assertEqual(metrics['memory_total'], 8000)
        self.assertEqual(metrics['memory_available'], 2400)
        self.assertEqual(metrics['disk_usage'], 60)
        self.assertEqual(metrics['disk_total'], 10000)
        self.assertEqual(metrics['disk_used'], 6000)
        self.assertEqual(metrics['disk_free'], 4000)

        # Check if the log file contains the metrics
        with open(self.log_file, 'r') as f:
            log_contents = f.read()
            self.assertIn("System Metrics", log_contents)

    def test_log_transaction(self):
        """Test logging of a transaction."""
        transaction_id = "tx123"
        status = "success"
        details = {"amount": 100, "currency": "Pi"}

        self.monitoring.log_transaction(transaction_id, status, details)

        # Check if the log file contains the transaction log
        with open(self.log_file, 'r') as f:
            log_contents = f.read()
            self.assertIn(transaction_id, log_contents)
            self.assertIn(status, log_contents)
            self.assertIn(str(details), log_contents)

    def test_log_error(self):
        """Test logging of an error message."""
        error_message = "This is a test error."

        self.monitoring.log_error(error_message)

        # Check if the log file contains the error log
        with open(self.log_file, 'r') as f:
            log_contents = f.read()
            self.assertIn("Error: This is a test error.", log_contents)

    def test_log_event(self):
        """Test logging of a general event."""
        event_message = "This is a test event."

        self.monitoring.log_event(event_message)

        # Check if the log file contains the event log
        with open(self.log_file, 'r') as f:
            log_contents = f.read()
            self.assertIn("Event: This is a test event.", log_contents)

if __name__ == "__main__":
    unittest.main()
