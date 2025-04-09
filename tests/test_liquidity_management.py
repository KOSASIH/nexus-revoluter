import unittest
from decimal import Decimal
from liquidity_management import LiquidityPool  # Assuming the LiquidityPool class is in a file named liquidity_management.py

class TestLiquidityPool(unittest.TestCase):
    def setUp(self):
        """Set up a LiquidityPool instance for testing."""
        self.pool = LiquidityPool("TokenA", "TokenB")

    def test_add_liquidity(self):
        """Test adding liquidity to the pool."""
        self.pool.add_liquidity(Decimal('1000'), Decimal('2000'), "Provider1")
        self.assertEqual(self.pool.balance_a, Decimal('1000'))
        self.assertEqual(self.pool.balance_b, Decimal('2000'))
        self.assertEqual(self.pool.total_liquidity, Decimal('3000'))
        self.assertEqual(self.pool.liquidity_providers["Provider1"], Decimal('3000'))

        # Test adding liquidity with a different ratio
        with self.assertRaises(ValueError):
            self.pool.add_liquidity(Decimal('500'), Decimal('1000'), "Provider2")  # Should maintain the ratio

    def test_remove_liquidity(self):
        """Test removing liquidity from the pool."""
        self.pool.add_liquidity(Decimal('1000'), Decimal('2000'), "Provider1")
        self.pool.remove_liquidity(Decimal('3000'), "Provider1")  # Remove all liquidity
        self.assertEqual(self.pool.balance_a, Decimal('0'))
        self.assertEqual(self.pool.balance_b, Decimal('0'))
        self.assertEqual(self.pool.total_liquidity, Decimal('0'))
        self.assertEqual(self.pool.liquidity_providers["Provider1"], Decimal('0'))

        # Test removing more liquidity than available
        with self.assertRaises(ValueError):
            self.pool.remove_liquidity(Decimal('1000'), "Provider1")  # No liquidity left

    def test_trade(self):
        """Test trading in the pool."""
        self.pool.add_liquidity(Decimal('1000'), Decimal('2000'), "Provider1")
        amount_out = self.pool.trade(Decimal('100'), "TokenA", "Trader1")
        self.assertEqual(amount_out, Decimal('199.4'))  # Check expected output amount
        self.assertEqual(self.pool.balance_a, Decimal('1100'))  # Updated balance after trade
        self.assertEqual(self.pool.balance_b, Decimal('1800.6'))  # Updated balance after trade

        # Test trading with invalid token
        with self.assertRaises(ValueError):
            self.pool.trade(Decimal('100'), "InvalidToken", "Trader2")

    def test_collect_fee(self):
        """Test fee collection during trades."""
        self.pool.add_liquidity(Decimal('1000'), Decimal('2000'), "Provider1")
        self.pool.trade(Decimal('100'), "TokenA", "Trader1")
        self.assertGreater(self.pool.fees_collected, Decimal('0'))  # Check that fees were collected

    def test_distribute_rewards(self):
        """Test rewards distribution to liquidity providers."""
        self.pool.add_liquidity(Decimal('1000'), Decimal('2000'), "Provider1")
        self.pool.trade(Decimal('100'), "TokenA", "Trader1")
        self.pool.distribute_rewards()  # Distribute rewards after trade
        self.assertGreater(self.pool.liquidity_providers["Provider1"], Decimal('3000'))  # Check that rewards were added

    def test_get_pool_info(self):
        """Test getting pool information."""
        self.pool.add_liquidity(Decimal('1000'), Decimal('2000'), "Provider1")
        pool_info = self.pool.get_pool_info()
        self.assertEqual(pool_info["Token A"], "TokenA")
        self.assertEqual(pool_info["Token B"], "TokenB")
        self.assertEqual(pool_info["Balance A"], '1000')
        self.assertEqual(pool_info["Balance B"], '2000')
        self.assertEqual(pool_info["Total Liquidity"], '3000')
        self.assertEqual(pool_info["Fees Collected"], '0')
        self.assertEqual(pool_info["Liquidity Providers"]["Provider1"], Decimal('3000'))

if __name__ == '__main__':
    unittest.main()
