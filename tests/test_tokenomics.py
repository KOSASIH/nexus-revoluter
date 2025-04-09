import unittest
from decimal import Decimal
from tokenomics import Tokenomics  # Assuming the Tokenomics class is in a file named tokenomics.py

class TestTokenomics(unittest.TestCase):
    def setUp(self):
        """Set up a Tokenomics instance for testing."""
        self.tokenomics = Tokenomics(initial_supply=100000000000, max_supply=100000000000, stable_value=314159.00, reward_per_block=50)

    def test_initial_conditions(self):
        """Test initial conditions of the Tokenomics instance."""
        self.assertEqual(self.tokenomics.total_supply, Decimal('100000000000'))
        self.assertEqual(self.tokenomics.max_supply, Decimal('100000000000'))
        self.assertEqual(self.tokenomics.stable_value, Decimal('314159.00'))
        self.assertEqual(self.tokenomics.reward_per_block, Decimal('50'))
        self.assertEqual(self.tokenomics.staking_rewards, Decimal('0'))
        self.assertEqual(self.tokenomics.liquidity_rewards, Decimal('0'))
        self.assertEqual(self.tokenomics.price_stability_fund, Decimal('0'))

    def test_distribute_block_rewards(self):
        """Test the distribution of block rewards."""
        self.tokenomics.distribute_block_rewards(blocks_mined=10)
        self.assertEqual(self.tokenomics.total_supply, Decimal('100000000500'))  # 10 * 50 = 500

        # Test max supply limit
        self.tokenomics.total_supply = Decimal('100000000000')  # Reset to max supply
        self.tokenomics.distribute_block_rewards(blocks_mined=1)
        self.assertEqual(self.tokenomics.total_supply, Decimal('100000000000'))  # Should not exceed max supply

    def test_stake_tokens(self):
        """Test staking functionality."""
        self.tokenomics.stake_tokens(amount=100)
        self.assertEqual(self.tokenomics.total_supply, Decimal('100000000100'))  # 100 * 0.1 = 10, total supply should increase by 10
        self.assertEqual(self.tokenomics.staking_rewards, Decimal('10'))

        # Test invalid staking amount
        with self.assertRaises(ValueError):
            self.tokenomics.stake_tokens(amount=0)

    def test_provide_liquidity(self):
        """Test providing liquidity functionality."""
        self.tokenomics.provide_liquidity(amount=200)
        self.assertEqual(self.tokenomics.total_supply, Decimal('100000000200'))  # 200 * 0.05 = 10, total supply should increase by 10
        self.assertEqual(self.tokenomics.liquidity_rewards, Decimal('10'))

        # Test invalid liquidity amount
        with self.assertRaises(ValueError):
            self.tokenomics.provide_liquidity(amount=0)

    def test_stabilize_price(self):
        """Test price stabilization functionality."""
        # Test when market price is below stable value
        self.tokenomics.price_stability_fund = Decimal('1000000')  # Set some funds
        self.tokenomics.stabilize_price(market_price=300000.00)
        self.assertGreater(self.tokenomics.price_stability_fund, Decimal('999999'))  # Should decrease by some amount

        # Test when market price is above stable value
        initial_fund = self.tokenomics.price_stability_fund
        self.tokenomics.stabilize_price(market_price=400000.00)
        self.assertGreater(self.tokenomics.price_stability_fund, initial_fund)  # Should increase by the amount sold

    def test_get_tokenomics_summary(self):
        """Test the summary of tokenomics."""
        summary = self.tokenomics.get_tokenomics_summary()
        self.assertEqual(summary['Total Supply'], '100000000000')
        self.assertEqual(summary['Max Supply'], '100000000000')
        self.assertEqual(summary['Stable Value (USD)'], '314159.00')
        self.assertEqual(summary['Staking Rewards Distributed'], '0')
        self.assertEqual(summary['Liquidity Rewards Distributed'], '0')
        self.assertEqual(summary['Price Stability Fund'], '0')
        self.assertEqual(summary['Reward per Block'], '50')

if __name__ == '__main__':
    unittest.main()
