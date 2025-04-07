import unittest
import json
import os
from defi import Token, LendingPool, LiquidityPool, DeFiPlatform

class TestDeFiPlatform(unittest.TestCase):
    def setUp(self):
        """Set up a new DeFi platform instance for testing."""
        self.defi_platform = DeFiPlatform()
        self.token_name = "MyToken"
        self.token_symbol = "MTK"
        self.total_supply = 1000000

        # Create a token for testing
        self.token = self.defi_platform.create_token(self.token_name, self.token_symbol, self.total_supply)

    def test_create_token(self):
        """Test token creation."""
        self.assertEqual(self.token.name, self.token_name)
        self.assertEqual(self.token.symbol, self.token_symbol)
        self.assertEqual(self.token.total_supply, self.total_supply)
        self.assertIn("admin", self.token.balances)
        self.assertEqual(self.token.balances["admin"], self.total_supply)

    def test_lending_pool_creation(self):
        """Test lending pool creation."""
        lending_pool = self.defi_platform.create_lending_pool(self.token_symbol)
        self.assertIsNotNone(lending_pool)
        self.assertEqual(lending_pool.token.symbol, self.token_symbol)

    def test_lend_tokens(self):
        """Test lending tokens to the pool."""
        lending_pool = self.defi_platform.create_lending_pool(self.token_symbol)
        lending_pool.lend("admin", 1000)
        self.assertIn("admin", lending_pool.lenders)
        self.assertEqual(lending_pool.lenders["admin"], 1000)

    def test_borrow_tokens_with_collateral(self):
        """Test borrowing tokens with collateral."""
        lending_pool = self.defi_platform.create_lending_pool(self.token_symbol)
        lending_pool.lend("admin", 1000)
        repayment_amount = lending_pool.borrow("user1", 500, 750)  # 150% collateral
        self.assertIsNotNone(repayment_amount)
        self.assertIn("user1", lending_pool.borrowers)
        self.assertEqual(lending_pool.borrowers["user1"], 500)

    def test_borrow_insufficient_collateral(self):
        """Test borrowing with insufficient collateral."""
        lending_pool = self.defi_platform.create_lending_pool(self.token_symbol)
        lending_pool.lend("admin", 1000)
        repayment_amount = lending_pool.borrow("user1", 500, 300)  # Not enough collateral
        self.assertIsNone(repayment_amount)
        self.assertNotIn("user1", lending_pool.borrowers)

    def test_provide_liquidity(self):
        """Test providing liquidity to the pool."""
        liquidity_pool = self.defi_platform.create_liquidity_pool(self.token_symbol)
        liquidity_pool.provide_liquidity("user2", 200)
        self.assertIn("user2", liquidity_pool.liquidity_providers)
        self.assertEqual(liquidity_pool.liquidity_providers["user2"], 200)

    def test_withdraw_liquidity(self):
        """Test withdrawing liquidity from the pool."""
        liquidity_pool = self.defi_platform.create_liquidity_pool(self.token_symbol)
        liquidity_pool.provide_liquidity("user2", 200)
        success = liquidity_pool.withdraw_liquidity("user2", 100)
        self.assertTrue(success)
        self.assertEqual(liquidity_pool.liquidity_providers["user2"], 100)

    def test_withdraw_insufficient_liquidity(self):
        """Test withdrawing more liquidity than provided."""
        liquidity_pool = self.defi_platform.create_liquidity_pool(self.token_symbol)
        liquidity_pool.provide_liquidity("user2", 200)
        success = liquidity_pool.withdraw_liquidity("user2", 300)  # Not enough liquidity
        self.assertFalse(success)
        self.assertEqual(liquidity_pool.liquidity_providers["user2"], 200)

    def test_save_and_load_state(self):
        """Test saving and loading the state of the DeFi platform."""
        self.defi_platform.save_state("defi_state.json")
        self.defi_platform.load_state("defi_state.json")

        # Verify that the loaded state matches the original state
        self.assertIn(self.token_symbol, self.defi_platform.tokens)
        loaded_token = self.defi_platform.tokens[self.token_symbol]
        self.assertEqual(loaded_token.name, self.token_name)
        self.assertEqual(loaded_token.total_supply, self.total_supply)
        self.assertIn("admin", loaded_token.balances)
        self.assertEqual(loaded_token.balances["admin"], self.total_supply)

    def tearDown(self):
        """Clean up after tests."""
        if os.path.exists("defi_state.json"):
            os.remove("defi_state.json")

if __name__ == "__main__":
    unittest.main()
