import unittest
from unittest.mock import patch, MagicMock
import asyncio
from universal_price_oracle import UniversalPriceOracle

class TestUniversalPriceOracle(unittest.TestCase):

    @patch('universal_price_oracle.requests.get')
    @patch('universal_price_oracle.validate_data')
    @patch('universal_price_oracle.apply_penalty')
    def setUp(self, mock_apply_penalty, mock_validate_data, mock_requests_get):
        # Mock the validate_data function to always return True
        mock_validate_data.return_value = True

        # Mock the requests.get method to simulate API responses
        self.mock_response_binance = MagicMock()
        self.mock_response_binance.json.return_value = {'price': '314200'}
        self.mock_response_binance.raise_for_status = MagicMock()

        self.mock_response_coinbase = MagicMock()
        self.mock_response_coinbase.json.return_value = {'data': {'amount': '314100'}}
        self.mock_response_coinbase.raise_for_status = MagicMock()

        # Set the side effects for the mocked requests.get
        mock_requests_get.side_effect = [self.mock_response_binance, self.mock_response_coinbase]

        # Initialize the UniversalPriceOracle
        self.oracle = UniversalPriceOracle()

    @patch('universal_price_oracle.aiohttp.ClientSession')
    async def test_fetch_price_data(self, mock_client_session):
        # Mock the ClientSession and its context manager
        mock_session = MagicMock()
        mock_client_session.return_value.__aenter__.return_value = mock_session

        # Mock the response for the Binance API
        mock_session.get.side_effect = [
            MagicMock(status=200, json=lambda: {'price': '314200'}),
            MagicMock(status=200, json=lambda: {'data': {'amount': '314100'}})
        ]

        await self.oracle.fetch_price_data()

        # Check that prices were fetched correctly
        self.assertIn('https://api.binance.com/api/v3/ticker/price?symbol=PICUSDT', self.oracle.price_data)
        self.assertIn('https://api.coinbase.com/v2/prices/PI-USD/spot', self.oracle.price_data)
        self.assertEqual(len(self.oracle.price_data['https://api.binance.com/api/v3/ticker/price?symbol=PICUSDT']), 1)
        self.assertEqual(len(self.oracle.price_data['https://api.coinbase.com/v2/prices/PI-USD/spot']), 1)

    def test_validate_prices(self):
        # Simulate price data
        self.oracle.price_data['https://api.binance.com/api/v3/ticker/price?symbol=PICUSDT'] = [314200]
        self.oracle.price_data['https://api.coinbase.com/v2/prices/PI-USD/spot'] = [314100]

        # Run validation
        self.oracle.validate_prices()

        # Check that apply_penalty was not called since prices are valid
        self.assertFalse(self.oracle.apply_penalty.called)

        # Now simulate a deviation
        self.oracle.price_data['https://api.binance.com/api/v3/ticker/price?symbol=PICUSDT'] = [315000]
        self.oracle.validate_prices()

        # Check that apply_penalty was called due to deviation
        self.assertTrue(self.oracle.apply_penalty.called)

    def test_aggregate_prices(self):
        # Simulate price data
        self.oracle.price_data['https://api.binance.com/api/v3/ticker/price?symbol=PICUSDT'] = [314200, 314300]
        self.oracle.price_data['https://api.coinbase.com/v2/prices/PI-USD/spot'] = [314100]

        # Run aggregation
        aggregated_price = self.oracle.aggregate_prices()

        # Check the aggregated price
        self.assertAlmostEqual(aggregated_price, (314200 + 314300 + 314100) / 4)

    @patch('universal_price_oracle.sleep', return_value=None)  # Mock sleep to avoid delays
    def test_run(self, mock_sleep):
        with patch.object(self.oracle, 'fetch_price_data', return_value=None), \
             patch.object(self.oracle, 'validate_prices', return_value=None), \
             patch.object(self.oracle, 'aggregate_prices', return_value=314200) as mock_aggregate_prices:

            # Run the oracle for a single iteration
            self.oracle.run()
            mock_aggregate_prices.assert_called_once()

if __name__ == '__main__':
    unittest.main()
