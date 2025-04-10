import unittest
from unittest.mock import patch, MagicMock
from global_liquidity_adjuster import GlobalLiquidityAdjuster

class TestGlobalLiquidityAdjuster(unittest.TestCase):

    @patch('global_liquidity_adjuster.LiquidityManager')
    @patch('global_liquidity_adjuster.DeFiManager')
    @patch('global_liquidity_adjuster.StakingManager')
    @patch('global_liquidity_adjuster.RewardsManager')
    def setUp(self, mock_rewards_manager, mock_staking_manager, mock_defi_manager, mock_liquidity_manager):
        # Mock the managers
        self.mock_liquidity_manager = mock_liquidity_manager.return_value
        self.mock_defi_manager = mock_defi_manager.return_value
        self.mock_staking_manager = mock_staking_manager.return_value
        self.mock_rewards_manager = mock_rewards_manager.return_value

        # Initialize the GlobalLiquidityAdjuster class
        self.liquidity_adjuster = GlobalLiquidityAdjuster()

    def test_monitor_liquidity(self):
        # Mock the liquidity data
        self.mock_liquidity_manager.get_liquidity_data.return_value = [
            {'name': 'Pool A', 'liquidity': 1000, 'trading_volume': 5000},
            {'name': 'Pool B', 'liquidity': 2000, 'trading_volume': 10000}
        ]

        with patch('time.sleep', return_value=None):  # Mock sleep to avoid delays
            self.liquidity_adjuster.monitor_liquidity()

        # Check that liquidity data was fetched
        self.mock_liquidity_manager.get_liquidity_data.assert_called_once()

    def test_adjust_liquidity_provide(self):
        # Mock a pool with low liquidity
        pool = {'name': 'Pool A', 'liquidity': 1000, 'trading_volume': 5000}
        self.liquidity_adjuster.calculate_required_liquidity = MagicMock(return_value=6000)

        # Call adjust_liquidity
        self.liquidity_adjuster.adjust_liquidity(pool)

        # Check that liquidity was provided
        self.mock_defi_manager.provide_liquidity.assert_called_once_with('Pool A', 5000)

    def test_adjust_liquidity_no_provide(self):
        # Mock a pool with sufficient liquidity
        pool = {'name': 'Pool B', 'liquidity': 6000, 'trading_volume': 10000}
        self.liquidity_adjuster.calculate_required_liquidity = MagicMock(return_value=5000)

        # Call adjust_liquidity
        self.liquidity_adjuster.adjust_liquidity(pool)

        # Check that liquidity was not provided
        self.mock_defi_manager.provide_liquidity.assert_not_called()

    def test_calculate_required_liquidity(self):
        pool = {'name': 'Pool A', 'trading_volume': 5000}
        required_liquidity = self.liquidity_adjuster.calculate_required_liquidity(pool)
        expected_liquidity = 5000 * (self.liquidity_adjuster.target_value / 100)  # Example calculation
        self.assertEqual(required_liquidity, expected_liquidity)

if __name__ == '__main__':
    unittest.main()
