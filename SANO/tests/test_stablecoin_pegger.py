import unittest
from unittest.mock import patch, MagicMock
import logging
import json
import os
from stablecoin_pegger import StablecoinPegger  # Assuming the class is in stablecoin_pegger.py

class TestStablecoinPegger(unittest.TestCase):
    def setUp(self):
        """Set up the StablecoinPegger instance for testing."""
        self.pegger = StablecoinPegger(target_price=314159.00, tolerance=0.05, w3_provider="https://rpc.pi-network.io")

    @patch('ccxt.binance.fetch_ticker')
    @patch('ccxt.kraken.fetch_ticker')
    def test_fetch_market_price(self, mock_kraken, mock_binance):
        """Test fetching market price from exchanges."""
        mock_binance.return_value = {"last": 315000.00}
        mock_kraken.return_value = {"last": 313000.00}

        price = self.pegger.fetch_market_price()
        self.assertAlmostEqual(price, 314000.00, places=2)

    @patch('ccxt.binance.fetch_ticker')
    @patch('ccxt.kraken.fetch_ticker')
    def test_fetch_market_price_failure(self, mock_kraken, mock_binance):
        """Test fetching market price failure handling."""
        mock_binance.side_effect = Exception("Binance error")
        mock_kraken.return_value = {"last": 313000.00}

        with self.assertLogs(self.pegger.logger, level='ERROR') as log:
            price = self.pegger.fetch_market_price()
            self.assertIsNone(price)
            self.assertIn("Failed to fetch price from <ccxt.binance object", log.output[0])

    @patch('stablecoin_pegger.StablecoinPegger._execute_supply_action')
    def test_adjust_supply_burn(self, mock_execute):
        """Test adjusting supply when price is below target."""
        self.pegger.adjust_supply(300000.00)  # Below target price
        mock_execute.assert_called_once_with("burn", 0.05 * 1000000)  # 5% of 1M

    @patch('stablecoin_pegger.StablecoinPegger._execute_supply_action')
    def test_adjust_supply_mint(self, mock_execute):
        """Test adjusting supply when price is above target."""
        self.pegger.adjust_supply(320000.00)  # Above target price
        mock_execute.assert_called_once_with("mint", 0.05 * 1000000)  # 5% of 1M

    @patch('web3.Web3')
    @patch('os.getenv')
    def test_execute_supply_action_burn(self, mock_getenv, mock_web3):
        """Test executing burn action."""
        mock_getenv.return_value = "test_private_key"
        mock_web3.eth.contract.return_value.functions.burn.return_value.buildTransaction.return_value = {}
        mock_web3.eth.getTransactionCount.return_value = 1
        mock_web3.eth.account.sign_transaction.return_value.rawTransaction = b'test_raw_transaction'
        mock_web3.eth.send_raw_transaction.return_value = b'test_tx_hash'

        self.pegger._execute_supply_action("burn", 1000000)
        self.assertTrue(mock_web3.eth.send_raw_transaction.called)

    @patch('web3.Web3')
    @patch('os.getenv')
    def test_execute_supply_action_mint(self, mock_getenv, mock_web3):
        """Test executing mint action."""
        mock_getenv.return_value = "test_private_key"
        mock_web3.eth.contract.return_value.functions.mint.return_value.buildTransaction.return_value = {}
        mock_web3.eth.getTransactionCount.return_value = 1
        mock_web3.eth.account.sign_transaction.return_value.rawTransaction = b'test_raw_transaction'
        mock_web3.eth.send_raw_transaction.return_value = b'test_tx_hash'

        self.pegger._execute_supply_action("mint", 1000000)
        self.assertTrue(mock_web3.eth.send_raw_transaction.called)

    @patch('web3.Web3')
    def test_confirm_transaction_success(self, mock_web3):
        """Test confirming a successful transaction."""
        mock_web3.eth.waitForTransactionReceipt.return_value = MagicMock(status=1)
        tx_hash = b'test_tx_hash'
        
        with self.assertLogs(self.pegger.logger, level='INFO') as log:
            self.pegger.confirm_transaction(tx_hash)
            self.assertIn("Transaction confirmed: test_tx_hash", log.output[0])

    @patch('web3.Web3')
    def test_confirm_transaction_failure(self, mock_web3):
        """Test confirming a failed transaction."""
        mock_web3.eth.waitForTransactionReceipt.return_value = MagicMock(status=0)
        tx_hash = b'test_tx_hash'
        
        with self.assertLogs(self.pegger.logger, level='ERROR') as log:
            self.pegger.confirm_transaction(tx_hash)
            self.assertIn("Transaction failed: test_tx_hash", log.output[0])

    @patch('time.sleep', return_value=None)  # Mock sleep to avoid delays
    @patch('stablecoin_pegger.StablecoinPegger.fetch_market_price')
    @patch('stablecoin_pegger.StablecoinPegger.adjust_supply')
    def test_monitor_market(self, mock_adjust_supply, mock_fetch_price):
        """Test the market monitoring functionality."""
        mock_fetch_price.return_value = 314000.00
        self.pegger.monitor_market(interval=1)  # Set a short interval for testing

        mock_fetch_price.assert_called()
        mock_adjust_supply.assert_called_with(314000.00)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    unittest.main()
