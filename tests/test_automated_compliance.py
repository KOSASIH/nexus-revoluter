import unittest
from automated_compliance import AutomatedCompliance
from unittest.mock import patch, MagicMock
import json

class TestAutomatedCompliance(unittest.TestCase):

    def setUp(self):
        self.compliance_tool = AutomatedCompliance()

    def test_register_user(self):
        """Test user registration."""
        user_id = self.compliance_tool.register_user("john_doe", "john@example.com", "securepassword123")
        self.assertIsNotNone(user_id)
        self.assertIn("john_doe", self.compliance_tool.users)

    def test_register_user_duplicate(self):
        """Test duplicate user registration."""
        self.compliance_tool.register_user("john_doe", "john@example.com", "securepassword123")
        with self.assertRaises(AssertionError):
            self.compliance_tool.register_user("john_doe", "john@example.com", "securepassword123")

    def test_authenticate_user(self):
        """Test user authentication."""
        self.compliance_tool.register_user("john_doe", "john@example.com", "securepassword123")
        authenticated = self.compliance_tool.authenticate_user("john_doe", "securepassword123")
        self.assertTrue(authenticated)

    def test_authenticate_user_invalid_password(self):
        """Test user authentication with invalid password."""
        self.compliance_tool.register_user("john_doe", "john@example.com", "securepassword123")
        authenticated = self.compliance_tool.authenticate_user("john_doe", "wrongpassword")
        self.assertFalse(authenticated)

    def test_collect_data(self):
        """Test data collection."""
        data = self.compliance_tool.collect_data("Database")
        self.assertIsNotNone(data)
        self.assertIn("timestamp", data)
        self.assertIn("source", data)
        self.assertIn("data", data)

    @patch('automated_compliance.requests.get')
    def test_collect_data_external_source(self, mock_get):
        """Test data collection from an external source."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"example_key": "example_value"}
        mock_get.return_value = mock_response
        data = self.compliance_tool.collect_data("External API")
        self.assertIsNotNone(data)
        self.assertIn("example_key", data["data"])

    def test_monitor_compliance(self):
        """Test compliance monitoring."""
        monitored = self.compliance_tool.monitor_compliance()
        self.assertTrue(monitored)

    def test_generate_report(self):
        """Test report generation."""
        report = self.compliance_tool.generate_report("GDPR")
        self.assertIsNotNone(report)
        self.assertIn("report_id", report)
        self.assertIn("type", report)
        self.assertIn("data", report)
        self.assertIn("generated_at", report)

    def test_generate_report_invalid_type(self):
        """Test report generation with invalid type."""
        with self.assertRaises(AssertionError):
            self.compliance_tool.generate_report("Invalid Type")

    def test_send_alert(self):
        """Test alert sending."""
        sent = self.compliance_tool.send_alert("Compliance breach detected!", "alert_recipient@example.com")
        self.assertTrue(sent)

    @patch('automated_compliance.smtplib.SMTP')
    def test_send_alert_smtp(self, mock_smtp):
        """Test alert sending via SMTP."""
        mock_smtp.return_value.sendmail.return_value = {}
        sent = self.compliance_tool.send_alert("Compliance breach detected!", "alert_recipient@example.com")
        self.assertTrue(sent)

    def test_encrypt_data(self):
        """Test data encryption."""
        encrypted_data = self.compliance_tool.encrypt_data("Sensitive Data")
        self.assertIsNotNone(encrypted_data)

    def test_decrypt_data(self):
        """Test data decryption."""
        encrypted_data = self.compliance_tool.encrypt_data("Sensitive Data")
        decrypted_data = self.compliance_tool.decrypt_data(encrypted_data)
        self.assertEqual(decrypted_data, "Sensitive Data")

    def test_get_compliance_metrics(self):
        """Test compliance metrics retrieval."""
        metrics = self.compliance_tool.get_compliance_metrics()
        self.assertIsNotNone(metrics)
        self.assertIn("total_data_collected", metrics)
        self.assertIn("total_reports_generated", metrics)

if __name__ == "__main__":
    unittest.main()
