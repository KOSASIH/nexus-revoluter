import time
from decimal import Decimal

class Tokenomics:
    def __init__(self, initial_supply, max_supply, stable_value, reward_per_block):
        self.total_supply = Decimal(initial_supply)  # Total supply of Pi Coin
        self.max_supply = Decimal(max_supply)        # Maximum supply of Pi Coin
        self.stable_value = Decimal(stable_value)    # Stable value of Pi Coin in USD
        self.reward_per_block = Decimal(reward_per_block)  # Reward per block mined
        self.block_time = 60  # Average block time in seconds
        self.last_reward_time = time.time()  # Timestamp of the last reward distribution
        self.staking_rewards = Decimal(0)  # Total staking rewards distributed
        self.liquidity_rewards = Decimal(0)  # Total liquidity rewards distributed
        self.price_stability_fund = Decimal(0)  # Fund to stabilize the price of Pi Coin

    def calculate_inflation(self):
        """Calculate the new supply based on inflation rate."""
        # Inflation is not applicable for a stablecoin; we can implement a mechanism to adjust supply based on demand.
        pass

    def distribute_block_rewards(self, blocks_mined):
        """Distribute rewards for mined blocks."""
        rewards = self.reward_per_block * blocks_mined
        if self.total_supply + rewards <= self.max_supply:
            self.total_supply += rewards
            print(f"Distributed {rewards} Pi Coins as block rewards.")
        else:
            print("Max supply reached, cannot distribute block rewards.")

    def stake_tokens(self, amount):
        """Stake tokens and calculate rewards."""
        if amount <= 0:
            raise ValueError("Amount to stake must be greater than zero.")
        staking_reward = amount * Decimal(0.1)  # 10% staking reward
        self.staking_rewards += staking_reward
        self.total_supply += staking_reward
        print(f"Staked {amount} Pi Coins, earned {staking_reward} as rewards.")

    def provide_liquidity(self, amount):
        """Provide liquidity and earn rewards."""
        if amount <= 0:
            raise ValueError("Amount to provide must be greater than zero.")
        liquidity_reward = amount * Decimal(0.05)  # 5% liquidity reward
        self.liquidity_rewards += liquidity_reward
        self.total_supply += liquidity_reward
        print(f"Provided {amount} Pi Coins as liquidity, earned {liquidity_reward} as rewards.")

    def stabilize_price(self, market_price):
        """Adjust the price stability fund based on market price fluctuations."""
        if market_price < self.stable_value:
            # Use the price stability fund to buy back Pi Coins to support the price
            amount_to_buy = (self.stable_value - market_price) * self.total_supply / self.stable_value
            if self.price_stability_fund >= amount_to_buy:
                self.price_stability_fund -= amount_to_buy
                print(f"Used {amount_to_buy} from the stability fund to stabilize the price.")
            else:
                print("Insufficient funds in the price stability fund.")
        elif market_price > self.stable_value:
            # Increase the price stability fund by selling Pi Coins
            amount_to_sell = (market_price - self.stable_value) * self.total_supply / self.stable_value
            self.price_stability_fund += amount_to_sell
            print(f"Added {amount_to_sell} to the stability fund by selling Pi Coins.")

    def get_tokenomics_summary(self):
        """Get a summary of the tokenomics."""
        return {
            "Total Supply": str(self.total_supply),
            "Max Supply": str(self.max_supply),
            "Stable Value (USD)": str(self.stable_value),
            "Staking Rewards Distributed": str(self.staking_rewards),
            "Liquidity Rewards Distributed": str(self.liquidity_rewards),
            "Price Stability Fund": str(self.price_stability_fund),
            "Reward per Block": str(self.reward_per_block),
        }

# Example usage
if __name__ == "__main__":
    tokenomics = Tokenomics(initial_supply=100000000000, max_supply=100000000000, stable_value=314159.00, reward_per_block=50)

    # Simulate block mining
    tokenomics.distribute_block_rewards(blocks_mined=10)

    # Simulate staking
    tokenomics.stake_tokens(amount=100)

    # Simulate providing liquidity
    tokenomics.provide_liquidity(amount=200)

    # Simulate price stabilization
    tokenomics.stabilize_price(market_price=300000.00)

 # Print tokenomics summary
    summary = tokenomics.get_tokenomics_summary()
    for key, value in summary.items():
        print(f"{key}: {value}")
