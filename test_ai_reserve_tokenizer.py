import unittest
from unittest.mock import patch, MagicMock
from ai_reserve_tokenizer import AiReserveTokenizer

class TestAiReserveTokenizer(unittest.TestCase):

    @patch('ai_reserve_tokenizer.AIAnalyzer')
    @patch('ai_reserve_tokenizer.RealWorldAssetTokenizer')
    @patch('ai_reserve_tokenizer.OnChainAnalytics')
    @patch('ai_reserve_tokenizer.DeFiManager')
    def setUp(self, mock_defi_manager, mock_analytics, mock_asset_tokenizer, mock_ai_analyzer):
        # Mock the managers
        self.mock_ai_analyzer = mock_ai_analyzer.return_value
        self.mock_asset_tokenizer = mock_asset_tokenizer.return_value
        self.mock_analytics = mock_analytics.return_value
        self.mock_defi_manager = mock_defi_manager.return_value

        # Initialize the AiReserveTokenizer class
        self.reserve_tokenizer = AiReserveTokenizer()

    def test_manage_reserves(self):
        # Mock asset performance analysis
        self.mock_ai_analyzer.analyze_asset_performance.return_value = [
            {'id': 'asset1', 'performance': 0.05},
            {'id': 'asset2', 'performance': -0.02}
        ]

        # Call manage_reserves
        self.reserve_tokenizer.manage_reserves()

        # Check that asset performance was analyzed
        self.mock_ai_analyzer.analyze_asset_performance.assert_called_once()

        # Check that reserves were adjusted for underperforming assets
        self.mock_defi_manager.rebalance_asset.assert_called_once_with('asset2', self.reserve_tokenizer.target_value)

    def test_adjust_reserves(self):
        # Mock asset performance
        asset_performance = [
            {'id': 'asset1', 'performance': 0.1},
            {'id': 'asset2', 'performance': -0.1}
        ]

        # Call adjust_reserves
        self.reserve_tokenizer.adjust_reserves(asset_performance)

        # Check that rebalance was called for the underperforming asset
        self.mock_defi_manager.rebalance_asset.assert_called_once_with('asset2', self.reserve_tokenizer.target_value)

    def test_tokenize_real_world_assets(self):
        # Call tokenize_real_world_assets
        self.reserve_tokenizer.tokenize_real_world_assets()

        # Check that the asset tokenizer was called
        self.mock_asset_tokenizer.tokenize_assets.assert_called_once()

if __name__ == '__main__':
    unittest.main()
