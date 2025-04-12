import unittest
from unittest.mock import patch, MagicMock
import requests
from npas.api.pi_network_client import PiNetworkClient

class TestPiNetworkClient(unittest.TestCase):
    def setUp(self):
        # Sample configuration for the PiNetworkClient
        self.config = {
            "main_site": "https://minepi.com",
            "wallet": "https://wallet.pinet.com",
            "ecosystem": "https://ecosystem.pinet.com",
            "api_key": "test_api_key"
        }
        self.client = PiNetworkClient(self.config)

    @patch('npas.api.pi_network_client.requests.post')
    def test_apply_change_success(self, mock_post):
        """Test successful application of a change."""
        # Mock the response of the POST request
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        change = {"id": "1", "content": "code update"}
        self.client.apply_change(change)

        # Check that the POST request was made with the correct parameters
        self.assertEqual(mock_post.call_count, 3)  # One for each endpoint
        for endpoint in self.config.values():
            mock_post.assert_any_call(
                f"{endpoint}/api/sync",
                json=change,
                headers={"Authorization": "Bearer test_api_key"},
                timeout=10
            )

    @patch('npas.api.pi_network_client.requests.post')
    def test_apply_change_timeout(self, mock_post):
        """Test handling of a timeout error during change application."""
        mock_post.side_effect = requests.Timeout

        change = {"id": "1", "content": "code update"}
        with self.assertRaises(requests.Timeout):
            self.client.apply_change(change)

    @patch('npas.api.pi_network_client.requests.post')
    def test_apply_change_connection_error(self, mock_post):
        """Test handling of a connection error during change application."""
        mock_post.side_effect = requests.ConnectionError

        change = {"id": "1", "content": "code update"}
        with self.assertRaises(requests.ConnectionError):
            self.client.apply_change(change)

    @patch('npas.api.pi_network_client.requests.post')
    def test_apply_change_http_error(self, mock_post):
        """Test handling of an HTTP error during change application."""
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_post.return_value = mock_response

        change = {"id": "1", "content": "code update"}
        with self.assertRaises(requests.HTTPError):
            self.client.apply_change(change)

    @patch('npas.api.pi_network_client.requests.get')
    def test_get_status_success(self, mock_get):
        """Test successful fetching of status."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "active"}
        mock_get.return_value = mock_response

        status = self.client.get_status()
        self.assertEqual(status, {"status": "active"})
        mock_get.assert_called_once_with(
            f"{self.config['main_site']}/api/status",
            headers={"Authorization": "Bearer test_api_key"},
            timeout=10
        )

    @patch('npas.api.pi_network_client.requests.get')
    def test_get_status_request_exception(self, mock_get):
        """Test handling of a request exception during status fetching."""
        mock_get.side_effect = requests.RequestException

        status = self.client.get_status()
        self.assertIsNone(status)

if __name__ == "__main__":
    unittest.main()
