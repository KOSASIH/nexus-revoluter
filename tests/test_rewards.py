import unittest
import logging
from rewards import RewardDistribution  # Assuming rewards.py is in the same directory

# Configure logging for testing
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TestRewardDistribution(unittest.TestCase):

    def setUp(self):
        """Set up a new RewardDistribution instance for testing."""
        self.rewards = RewardDistribution()

    def test_register_participant(self):
        """Test registering a new participant."""
        self.rewards.register_participant("user1", 100.0)
        self.assertIn("user1", self.rewards.participants)
        self.assertEqual(self.rewards.participants["user1"]["stake"], 100.0)
        self.assertEqual(self.rewards.participants["user1"]["rewards"], 0.0)

    def test_register_duplicate_participant(self):
        """Test registering a duplicate participant."""
        self.rewards.register_participant("user1", 100.0)
        self.rewards.register_participant("user1", 150.0)  # Should not change the stake
        self.assertEqual(self.rewards.participants["user1"]["stake"], 100.0)

    def test_register_multiple_participants(self):
        """Test batch registration of participants."""
        participants = [{"user2": 200.0}, {"user3": 300.0}]
        self.rewards.register_participants(participants)
        self.assertIn("user2", self.rewards.participants)
        self.assertIn("user3", self.rewards.participants)
        self.assertEqual(self.rewards.participants["user2"]["stake"], 200.0)
        self.assertEqual(self.rewards.participants["user3"]["stake"], 300.0)

    def test_calculate_rewards_proportional(self):
        """Test reward calculation using proportional strategy."""
        self.rewards.register_participant("user1", 100.0)
        self.rewards.register_participant("user2", 200.0)
        self.rewards.calculate_rewards(total_rewards=300.0, strategy="proportional")

        self.assertEqual(self.rewards.participants["user1"]["rewards"], 100.0)  # 100/300 * 300
        self.assertEqual(self.rewards.participants["user2"]["rewards"], 200.0)  # 200/300 * 300

    def test_calculate_rewards_fixed(self):
        """Test reward calculation using fixed strategy."""
        self.rewards.register_participant("user1", 100.0)
        self.rewards.register_participant("user2", 200.0)
        self.rewards.calculate_rewards(total_rewards=300.0, strategy="fixed")

        self.assertEqual(self.rewards.participants["user1"]["rewards"], 150.0)  # 300 / 2
        self.assertEqual(self.rewards.participants["user2"]["rewards"], 150.0)  # 300 / 2

    def test_calculate_rewards_no_stakes(self):
        """Test reward calculation with no stakes."""
        self.rewards.calculate_rewards(total_rewards=300.0)
        self.assertEqual(len(self.rewards.participants), 0)  # No participants registered

    def test_distribute_rewards(self):
        """Test distribution of rewards."""
        self.rewards.register_participant("user1", 100.0)
        self.rewards.calculate_rewards(total_rewards=300.0, strategy="proportional")
        self.rewards.distribute_rewards()

        self.assertEqual(self.rewards.total_rewards_distributed, 300.0)
        self.assertEqual(self.rewards.participants["user1"]["rewards"], 0.0)  # Rewards should be reset after distribution

    def test_apply_penalty(self):
        """Test applying a penalty to a participant."""
        self.rewards.register_participant("user1", 100.0)
        self.rewards.apply_penalty("user1", 10.0)

        self.assertEqual(self.rewards.participants["user1"]["stake"], 90.0)  # Stake should be reduced by penalty

    def test_apply_penalty_nonexistent_user(self):
        """Test applying a penalty to a nonexistent user."""
        with self.assertLogs(level='WARNING') as log:
            self.rewards.apply_penalty("user2", 10.0)
            self.assertIn("User   user2 not found for penalty application.", log.output[0])

    def test_get_participant_info(self):
        """Test retrieving participant information."""
        self.rewards.register_participant("user1", 100.0)
        info = self.rewards.get_participant_info("user1")
        self.assertEqual(info["stake"], 100.0)
        self.assertEqual(info["rewards"], 0.0)

    def test_get_all_participants(self):
        """Test retrieving all participants."""
        self.rewards.register_participant("user1", 100.0)
        self.rewards.register_participant("user2", 200.0)
        all_participants = self.rewards.get_all_participants()
        self.assertEqual(len(all_participants), 2)

if __name__ == "__main__":
    unittest.main()
