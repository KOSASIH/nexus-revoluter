import unittest
from unittest.mock import patch, MagicMock
import json
import os
from green_mining import GreenMining

class TestGreenMining(unittest.TestCase):

    def setUp(self):
        """Set up a GreenMining instance for testing."""
        self.miner = GreenMining(miner_id="Miner_001", energy_source="solar", carbon_credit_rate=0.1)

    def tearDown(self):
        """Clean up after each test."""
        if os.path.exists("mining_activity_log.json"):
            os.remove("mining_activity_log.json")

    def test_initialization(self):
        """Test that the miner initializes correctly."""
        self.assertEqual(self.miner.miner_id, "Miner_001")
        self.assertEqual(self.miner.energy_source, "solar")
        self.assertEqual(self.miner.carbon_credit_rate, 0.1)
        self.assertEqual(self.miner.energy_consumed, 0)
        self.assertEqual(self.miner.carbon_credits_earned, 0)

    def test_calculate_energy_consumed(self):
        """Test energy consumption calculation."""
        energy_used = self.miner.calculate_energy_consumed(5)  # Simulate 5 seconds of mining
        self.assertAlmostEqual(energy_used, 2.5)  # 0.5 kWh/s * 5s

    def test_calculate_carbon_credits(self):
        """Test carbon credits calculation."""
        energy_used = 2.5  # 2.5 kWh
        credits = self.miner.calculate_carbon_credits(energy_used)
        self.assertEqual(credits, 0.25)  # 2.5 kWh * 0.1 credits/kWh

    @patch('builtins.open', new_callable=MagicMock)
    def test_log_mining_activity(self, mock_open):
        """Test logging of mining activity."""
        self.miner.log_mining_activity(5, 2.5, 0.25)
        mock_open.assert_called_once_with("mining_activity_log.json", "a")
        handle = mock_open()
        handle.write.assert_called_once()
        log_entry = json.loads(handle.write.call_args[0][0])
        self.assertEqual(log_entry['miner_id'], "Miner_001")
        self.assertEqual(log_entry['energy_used'], 2.5)
        self.assertEqual(log_entry['carbon_credits_earned'], 0.25)

    @patch('requests.post')
    def test_trade_carbon_credits_success(self, mock_post):
        """Test successful trading of carbon credits."""
        mock_post.return_value.status_code = 200
        self.miner.trade_carbon_credits(1)  # Trade 1 credit
        mock_post.assert_called_once()

    @patch('requests.post')
    def test_trade_carbon_credits_failure(self, mock_post):
        """Test failure in trading carbon credits."""
        mock_post.return_value.status_code = 400
        with patch('builtins.print') as mocked_print:
            self.miner.trade_carbon_credits(1)  # Trade 1 credit
            mocked_print.assert_called_with("Failed to trade carbon credits: <MagicMock name='post().text' id='...'>")

    def test_update_dashboard(self):
        """Test that the dashboard updates correctly."""
        self.miner.update_dashboard(5, 2.5, 0.25)
        self.assertEqual(len(self.miner.dashboard), 1)
        dashboard_entry = self.miner.dashboard[0]
        self.assertEqual(dashboard_entry['miner_id'], "Miner_001")
        self.assertEqual(dashboard_entry['energy_used'], 2.5)
        self.assertEqual(dashboard_entry['carbon_credits_earned'], 0.25)

if __name__ == '__main__':
    unittest.main()
