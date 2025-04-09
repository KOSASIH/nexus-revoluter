from decimal import Decimal
from collections import defaultdict

class LiquidityPool:
    """Class to manage a liquidity pool."""
    def __init__(self, token_a, token_b):
        self.token_a = token_a  # Token A in the pool
        self.token_b = token_b  # Token B in the pool
        self.balance_a = Decimal(0)  # Balance of Token A
        self.balance_b = Decimal(0)  # Balance of Token B
        self.total_liquidity = Decimal(0)  # Total liquidity in the pool
        self.fees_collected = Decimal(0)  # Fees collected from trades
        self.liquidity_providers = defaultdict(Decimal)  # Mapping of liquidity providers to their shares

    def add_liquidity(self, amount_a, amount_b, provider):
        """Add liquidity to the pool."""
        if amount_a <= 0 or amount_b <= 0:
            raise ValueError("Amounts must be greater than zero.")
        
        # Calculate the total liquidity before adding new liquidity
        if self.total_liquidity == 0:
            self.balance_a += amount_a
            self.balance_b += amount_b
            self.total_liquidity += amount_a + amount_b
            self.liquidity_providers[provider] += amount_a + amount_b
        else:
            # Ensure the ratio of tokens remains constant
            ratio_a = self.balance_a / self.balance_b
            ratio_b = amount_a / amount_b
            if ratio_a != ratio_b:
                raise ValueError("Token amounts must maintain the pool's ratio.")
            
            self.balance_a += amount_a
            self.balance_b += amount_b
            self.total_liquidity += amount_a + amount_b
            self.liquidity_providers[provider] += amount_a + amount_b
        
        print(f"Provider '{provider}' added {amount_a} {self.token_a} and {amount_b} {self.token_b} to the pool.")

    def remove_liquidity(self, amount, provider):
        """Remove liquidity from the pool."""
        if provider not in self.liquidity_providers:
            raise ValueError("Provider does not have liquidity in the pool.")
        
        share = self.liquidity_providers[provider]
        if amount > share:
            raise ValueError("Insufficient liquidity to remove.")
        
        # Calculate the amount of tokens to return based on the share
        amount_a = (self.balance_a * amount) / self.total_liquidity
        amount_b = (self.balance_b * amount) / self.total_liquidity
        
        self.balance_a -= amount_a
        self.balance_b -= amount_b
        self.total_liquidity -= amount
        self.liquidity_providers[provider] -= amount
        
        print(f"Provider '{provider}' removed {amount_a} {self.token_a} and {amount_b} {self.token_b} from the pool.")

    def trade(self, amount_in, token_in, trader):
        """Execute a trade in the pool."""
        if token_in == self.token_a:
            amount_out = self.calculate_amount_out(amount_in, self.balance_a, self.balance_b)
            self.balance_a += amount_in
            self.balance_b -= amount_out
            fee = self.collect_fee(amount_out)
            print(f"Trader '{trader}' traded {amount_in} {self.token_a} for {amount_out} {self.token_b} (fee: {fee}).")
            return amount_out
        elif token_in == self.token_b:
            amount_out = self.calculate_amount_out(amount_in, self.balance_b, self.balance_a)
            self.balance_b += amount_in
            self.balance_a -= amount_out
            fee = self.collect_fee(amount_out)
            print(f"Trader '{trader}' traded {amount_in} {self.token_b} for {amount_out} {self.token_a} (fee: {fee}).")
            return amount_out
        else:
            raise ValueError("Invalid token for trading.")

    def calculate_amount_out(self, amount_in, reserve_in, reserve_out):
        """Calculate the amount of output tokens for a given input amount."""
        amount_in_with_fee = amount_in * Decimal(0.997)  # Assuming a 0.3% fee
        numerator = amount_in_with_fee * reserve_out
        denominator = reserve_in + amount_in_with_fee
        return numerator / denominator

    def collect_fee(self, amount_out):
        """Collect fees from trades."""
        fee = amount_out * Decimal(0.003)  # 0.3% fee
        self.fees_collected += fee
        return fee

    def distribute_rewards(self):
        """Distribute rewards to liquidity providers based on their share."""
        for provider, share in self.liquidity_providers.items():
            reward = (self.fees_collected * (share / self.total_liquidity)) if self.total_liquidity > 0 else Decimal(0)
            print(f"Provider '{provider}' receives a reward of {reward} from fees.")
            self.liquidity_providers[provider] += reward  # Update provider's balance with rewards
        self.fees_collected = Decimal(0)  # Reset fees after distribution

    def get_pool_info(self):
        """Get information about the liquidity pool."""
        return {
            "Token A": self.token_a,
            "Token B": self.token_b,
            "Balance A": str(self.balance_a),
            "Balance B": str(self.balance_b),
            "Total Liquidity": str(self.total_liquidity),
            "Fees Collected": str(self.fees_collected),
            "Liquidity Providers": dict(self.liquidity_providers)
        }

# Example usage
if __name__ == "__main__":
    # Create a liquidity pool for Token A and Token B
    pool = LiquidityPool("TokenA", "TokenB")

    # Add liquidity to the pool
    pool.add_liquidity(Decimal('1000'), Decimal('2000'), "Provider1")
    pool.add_liquidity(Decimal('500'), Decimal('1000'), "Provider2")

    # Execute trades
    pool.trade(Decimal('100'), "TokenA", "Trader1")
    pool.trade(Decimal('200'), "TokenB", "Trader2")

    # Distribute rewards to liquidity providers
    pool.distribute_rewards()

    # Get pool information
    pool_info = pool.get_pool_info()
    for key, value in pool_info.items():
        print(f"{key}: {value}")
