import logging
from typing import Dict, Any, List

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class RewardDistribution:
    def __init__(self):
        self.participants: Dict[str, Dict[str, Any]] = {}  # User address -> { "stake": amount, "rewards": amount, "reward_history": [] }
        self.total_rewards_distributed = 0.0

    def register_participant(self, user: str, stake: float) -> None:
        """Register a participant with their stake."""
        if user in self.participants:
            logging.warning(f"User  {user} is already registered.")
            return
        self.participants[user] = {"stake": stake, "rewards": 0.0, "reward_history": []}
        logging.info(f"Registered user {user} with stake {stake}.")

    def register_participants(self, participants: List[Dict[str, float]]) -> None:
        """Batch register multiple participants."""
        for participant in participants:
            user, stake = list(participant.items())[0]
            self.register_participant(user, stake)

    def calculate_rewards(self, total_rewards: float, strategy: str = "proportional") -> None:
        """Calculate rewards for all participants based on their stake and chosen strategy."""
        total_stake = sum(participant["stake"] for participant in self.participants.values())
        if total_stake == 0:
            logging.warning("No stakes found. Cannot distribute rewards.")
            return

        for user, data in self.participants.items():
            user_stake = data["stake"]
            if strategy == "proportional":
                user_reward = (user_stake / total_stake) * total_rewards
            elif strategy == "fixed":
                user_reward = total_rewards / len(self.participants)  # Equal distribution
            else:
                logging.error(f"Unknown reward strategy: {strategy}")
                continue

            data["rewards"] += user_reward
            data["reward_history"].append(user_reward)  # Track reward history
            logging.info(f"Calculated rewards for user {user}: {user_reward}.")

    def distribute_rewards(self) -> None:
        """Distribute the accumulated rewards to participants."""
        for user, data in self.participants.items():
            if data["rewards"] > 0:
                # Here you would implement the logic to transfer rewards to the user's wallet
                logging.info(f"Distributing {data['rewards']} rewards to user {user}.")
                self.total_rewards_distributed += data["rewards"]
                # Reset rewards after distribution
                data["rewards"] = 0.0
            else:
                logging.info(f"No rewards to distribute for user {user}.")

    def apply_penalty(self, user: str, penalty_amount: float) -> None:
        """Apply a penalty to a participant for early withdrawal."""
        if user in self.participants:
            self.participants[user]["stake"] -= penalty_amount
            logging.info(f"Applied penalty of {penalty_amount} to user {user}. New stake: {self.participants[user]['stake']}.")
        else:
            logging.warning(f"User  {user} not found for penalty application.")

    def get_participant_info(self, user: str) -> Dict[str, Any]:
        """Get information about a specific participant."""
        return self.participants.get(user, {"stake": 0, "rewards": 0, "reward_history": []})

    def get_all_participants(self) -> Dict[str, Dict[str, Any]]:
        """Get information about all participants."""
        return self.participants

# Example usage of the RewardDistribution class
if __name__ == "__main__":
    rewards = RewardDistribution()

    # Register participants
    rewards.register_participant("user1", 100.0)
    rewards.register_participant("user2", 200.0)

    # Calculate rewards based on total rewards pool
    rewards.calculate_rewards(total_rewards=300.0, strategy="proportional")

    # Distribute rewards
    rewards.distribute_rewards()

    # Apply penalty
    rewards.apply_penalty("user1", 10.0)

    # Get participant info
    print(rewards.get_participant_info("user1"))
    print(rewards.get_all_participants())
