import logging
from typing import Dict, Any, List
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Staking:
    def __init__(self):
        self.stakers: Dict[str, Dict[str, Any]] = {}  # User address -> { "staked_amount": amount, "rewards": amount, "staking_history": [], "staking_time": datetime }
        self.total_staked = 0.0
        self.reward_rate = 0.1  # Example: 10% reward rate per staking period
        self.staking_period = timedelta(days=30)  # Example: 30 days staking period
        self.penalty_rate = 0.05  # Example: 5% penalty for early unstaking

    def stake(self, user: str, amount: float) -> None:
        """Stake a certain amount of tokens."""
        if user not in self.stakers:
            self.stakers[user] = {"staked_amount": 0.0, "rewards": 0.0, "staking_history": [], "staking_time": None}
        
        self.stakers[user]["staked_amount"] += amount
        self.total_staked += amount
        self.stakers[user]["staking_history"].append(amount)
        self.stakers[user]["staking_time"] = datetime.now()  # Update staking time
        logging.info(f"User  {user} staked {amount}. Total staked: {self.stakers[user]['staked_amount']}.")

    def unstake(self, user: str, amount: float) -> None:
        """Unstake a certain amount of tokens with penalty for early unstaking."""
        if user not in self.stakers or self.stakers[user]["staked_amount"] < amount:
            logging.warning(f"User  {user} does not have enough staked amount to unstake {amount}.")
            return
        
        # Check if unstaking is within the staking period
        if datetime.now() < self.stakers[user]["staking_time"] + self.staking_period:
            penalty = amount * self.penalty_rate
            amount -= penalty
            logging.info(f"User  {user} incurred a penalty of {penalty}. Unstaking {amount} after penalty.")
        
        self.stakers[user]["staked_amount"] -= amount
        self.total_staked -= amount
        logging.info(f"User  {user} unstaked {amount}. Total staked: {self.stakers[user]['staked_amount']}.")

    def calculate_rewards(self) -> None:
        """Calculate rewards for all stakers based on their staked amount."""
        for user, data in self.stakers.items():
            user_rewards = data["staked_amount"] * self.reward_rate
            data["rewards"] += user_rewards
            logging.info(f"Calculated rewards for user {user}: {user_rewards}. Total rewards: {data['rewards']}.")

    def distribute_rewards(self) -> None:
        """Distribute the accumulated rewards to stakers."""
        for user, data in self.stakers.items():
            if data["rewards"] > 0:
                # Here you would implement the logic to transfer rewards to the user's wallet
                logging.info(f"Distributing {data['rewards']} rewards to user {user}.")
                # Reset rewards after distribution
                data["rewards"] = 0.0
            else:
                logging.info(f"No rewards to distribute for user {user}.")

    def get_staker_info(self, user: str) -> Dict[str, Any]:
        """Get information about a specific staker."""
        return self.stakers.get(user, {"staked_amount": 0, "rewards": 0, "staking_history": [], "staking_time": None})

    def get_all_stakers(self) -> Dict[str, Dict[str, Any]]:
        """Get information about all stakers."""
        return self.stakers

# Example usage of the Staking class
if __name__ == "__main__":
    staking = Staking()

    # Users stake tokens
    staking.stake("user1", 100.0)
    staking.stake("user2", 200.0)

    # Calculate rewards
    staking.calculate_rewards()

    # Distribute rewards
    staking.distribute_rewards()

    # Unstake with penalty
    staking.unstake("user1", 50.0)

    # Get staker info
    print(staking.get_staker_info("user1"))
    print(staking.get_all_stakers())
