import unittest
from unittest.mock import patch, MagicMock
from interoperability import CrossChainInteroperability

class TestCrossChainInteroperability(unittest.TestCase):
    def setUp(self):
        """Set up a new CrossChainInteroperability instance for testing."""
        self.interoperability = CrossChainInteroperability()
        self.from_chain = "Ethereum"
        self.to_chain = "BinanceSmartChain"
        self.amount = 1.5
        self.recipient_address = "recipient_bsc_address"
        self.sender_address = "sender_btc_address"
        self.transaction_id = "tx123456789"

    @patch('interoperability.requests.post')
    def test_send_asset_success(self, mock_post):
        """Test sending an asset successfully."""
        mock_post.return_value = MagicMock(status_code=200, json=lambda: {"status": "success", "transaction_id": self.transaction_id})
        
        response = self.interoperability.send_asset(self.from_chain, self.to_chain, self.amount, self.recipient_address)
        self.assertEqual(response["status"], "success")
        self.assertEqual(response["transaction_id"], self.transaction_id)

    @patch('interoperability.requests.post')
    def test_send_asset_failure(self, mock_post):
        """Test sending an asset failure due to API error."""
        mock_post.return_value = MagicMock(status_code=400, json=lambda: {"status": "error", "error": "Insufficient funds"})
        
        with self.assertRaises(Exception) as context:
            self.interoperability.send_asset(self.from_chain, self.to_chain, self.amount, self.recipient_address)
        self.assertTrue("Asset transfer failed." in str(context.exception))

    @patch('interoperability.requests.post')
    def test_receive_asset_success(self, mock_post):
        """Test receiving an asset successfully."""
        mock_post.return_value = MagicMock(status_code=200, json=lambda: {"status": "success", "transaction_id": self.transaction_id})
        
        response = self.interoperability.receive_asset(self.from_chain, self.amount, self.sender_address)
        self.assertEqual(response["status"], "success")
        self.assertEqual(response["transaction_id"], self.transaction_id)

    @patch('interoperability.requests.post')
    def test_receive_asset_failure(self, mock_post):
        """Test receiving an asset failure due to API error."""
        mock_post.return_value = MagicMock(status_code=400, json=lambda: {"status": "error", "error": "Invalid sender address"})
        
        with self.assertRaises(Exception) as context:
            self.interoperability.receive_asset(self.from_chain, self.amount, self.sender_address)
        self.assertTrue("Asset reception failed." in str(context.exception))

    @patch('interoperability.requests.post')
    def test_get_chain_balance(self, mock_post):
        """Test getting the balance of an address."""
        mock_post.return_value = MagicMock(status_code=200, json=lambda: {"balance": 100.0})
        
        balance = self.interoperability.get_chain_balance(self.from_chain, self.recipient_address)
        self.assertEqual(balance, 100.0)

    @patch('interoperability.requests.post')
    def test_get_chain_balance_failure(self, mock_post):
        """Test getting the balance failure due to API error."""
        mock_post.return_value = MagicMock(status_code=400, json=lambda: {"status": "error", "error": "Address not found"})
        
        with self.assertRaises(ValueError) as context:
            self.interoperability.get_chain_balance(self.from_chain, "invalid_address")
        self.assertTrue("Unsupported blockchain." in str(context.exception))

    @patch('interoperability.time.sleep', return_value=None)  # Mock sleep to speed up tests
    @patch('interoperability.CrossChainInteroperability.mock_check_transaction_status', return_value=True)
    def test_confirm_transaction_success(self, mock_check_status, mock_sleep):
        """Test confirming a transaction successfully."""
        confirmed = self.interoperability.confirm_transaction(self.from_chain, self.transaction_id)
        self.assertTrue(confirmed)

    @patch('interoperability.time.sleep', return_value=None)  # Mock sleep to speed up tests
    @patch('interoperability.CrossChainInteroperability.mock_check_transaction_status', return_value=False)
    def test_confirm_transaction_timeout(self, mock_check_status, mock_sleep):
        """Test confirming a transaction with timeout."""
        confirmed = self.interoperability.confirm_transaction(self.from_chain, self.transaction_id, timeout=1)
        self.assertFalse(confirmed)

if __name__ == "__main__":
    unittest.main()
