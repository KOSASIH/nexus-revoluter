import unittest
from unittest.mock import patch, MagicMock
from interoperability import CrossChainInteroperability

class TestCrossChainInteroperability(unittest.TestCase):

    @patch('interoperability.requests.post')
    def setUp(self, mock_requests_post):
        # Mock the response for sending assets
        self.mock_send_response = MagicMock()
        self.mock_send_response.json.return_value = {
            "status": "success",
            "transaction_id": "tx12345"
        }
        self.mock_send_response.status_code = 200
        mock_requests_post.return_value = self.mock_send_response

        # Initialize the CrossChainInteroperability class
        self.interoperability = CrossChainInteroperability()

    def test_send_asset_success(self):
        response = self.interoperability.send_asset("Ethereum", "BinanceSmartChain", 1.5, "recipient_bsc_address")
        self.assertEqual(response["status"], "success")
        self.assertEqual(response["transaction_id"], "tx12345")

    @patch('interoperability.logging.error')
    def test_send_asset_failure(self, mock_logging_error):
        # Mock a failed response
        self.mock_send_response.json.return_value = {
            "status": "error",
            "error": "Insufficient funds"
        }
        self.mock_send_response.status_code = 400

        with self.assertRaises(Exception) as context:
            self.interoperability.send_asset("Ethereum", "BinanceSmartChain", 1.5, "recipient_bsc_address")
        
        self.assertTrue("Asset transfer failed." in str(context.exception))
        mock_logging_error.assert_called_with("Failed to send asset: Insufficient funds")

    def test_receive_asset_success(self):
        # Mock the receive request
        self.interoperability.mock_receive_request = MagicMock(return_value={"status": "success", "transaction_id": "rx12345"})
        response = self.interoperability.receive_asset("Bitcoin", 0.5, "sender_btc_address")
        self.assertEqual(response["status"], "success")
        self.assertEqual(response["transaction_id"], "rx12345")

    @patch('interoperability.logging.error')
    def test_receive_asset_failure(self, mock_logging_error):
        # Mock a failed receive request
        self.interoperability.mock_receive_request = MagicMock(return_value={"status": "error", "error": "Transfer failed"})
        
        with self.assertRaises(Exception) as context:
            self.interoperability.receive_asset("Bitcoin", 0.5, "sender_btc_address")
        
        self.assertTrue("Asset reception failed." in str(context.exception))
        mock_logging_error.assert_called_with("Failed to receive asset: Transfer failed")

    def test_get_chain_balance(self):
        # Mock the balance retrieval
        self.interoperability.mock_get_balance = MagicMock(return_value=100.0)
        balance = self.interoperability.get_chain_balance("Ethereum", "user_eth_address")
        self.assertEqual(balance, 100.0)

    @patch('interoperability.logging.error')
    def test_get_chain_balance_unsupported_chain(self, mock_logging_error):
        with self.assertRaises(ValueError) as context:
            self.interoperability.get_chain_balance("UnsupportedChain", "user_address")
        
        self.assertTrue("Unsupported blockchain." in str(context.exception))
        mock_logging_error.assert_called_with("Unsupported blockchain.")

    def test_validate_data_success(self):
        is_valid = self.interoperability.validate_data(314200, 314159)
        self.assertTrue(is_valid)

    def test_validate_data_failure(self):
        is_valid = self.interoperability.validate_data(300000, 314159)
        self.assertFalse(is_valid)

    def test_validate_data_invalid_type(self):
        is_valid = self.interoperability.validate_data("invalid_price", 314159)
        self.assertFalse(is_valid)

    def test_confirm_transaction_success(self):
        # Mock the transaction status check
        self.interoperability.mock_check_transaction_status = MagicMock(return_value=True)
        confirmed = self.interoperability.confirm_transaction("Ethereum", "tx12345")
        self.assertTrue(confirmed)

    @patch('interoperability.logging.warning')
    def test_confirm_transaction_timeout(self, mock_logging_warning):
        # Mock the transaction status check to always return False
        self.interoperability.mock_check_transaction_status = MagicMock(return_value=False)
        confirmed = self.interoperability.confirm_transaction("Ethereum", "tx12345", timeout=1)
        self.assertFalse(confirmed)
        mock_logging_warning.assert_called_with("Transaction tx12345 not confirmed within timeout.")

if __name__ == '__main__':
    unittest.main()
