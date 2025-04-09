import unittest
from decimal import Decimal
from user_engagement import UserEngagement  # Assuming the UserEngagement class is in a file named user_engagement.py

class TestUser Engagement(unittest.TestCase):
    def setUp(self):
        """Set up a UserEngagement instance for testing."""
        self.engagement = UserEngagement()

    def test_add_reward(self):
        """Test adding rewards to the system."""
        self.engagement.add_reward("Reward1", "Description for Reward1")
        self.assertIn("Reward1", self.engagement.rewards)
        self.assertEqual(self.engagement.rewards["Reward1"], "Description for Reward1")

    def test_update_leaderboard(self):
        """Test updating the leaderboard with user scores."""
        self.engagement.update_leaderboard("User 1", Decimal('100'))
        self.assertIn("User 1", self.engagement.leaderboard)
        self.assertEqual(self.engagement.leaderboard["User 1"], Decimal('100'))

        # Update the score
        self.engagement.update_leaderboard("User 1", Decimal('200'))
        self.assertEqual(self.engagement.leaderboard["User 1"], Decimal('200'))

    def test_send_notification(self):
        """Test sending notifications to users."""
        self.engagement.send_notification("Notification1")
        self.assertIn("Notification1", self.engagement.notifications)

        self.engagement.send_notification("Notification2")
        self.assertIn("Notification2", self.engagement.notifications)

    def test_create_user_profile(self):
        """Test creating user profiles."""
        self.engagement.create_user_profile("User 1", {"name": "John Doe", "email": "john@example.com"})
        self.assertIn("User 1", self.engagement.user_profiles)
        self.assertEqual(self.engagement.user_profiles["User 1"], {"name": "John Doe", "email": "john@example.com"})

    def test_update_user_profile(self):
        """Test updating user profiles."""
        self.engagement.create_user_profile("User 1", {"name": "John Doe", "email": "john@example.com"})
        self.engagement.update_user_profile("User 1", {"name": "John Doe", "email": "john2@example.com"})
        self.assertEqual(self.engagement.user_profiles["User 1"], {"name": "John Doe", "email": "john2@example.com"})

        # Test updating a non-existent user profile
        with self.assertRaises(ValueError):
            self.engagement.update_user_profile("User 2", {"name": "Jane Doe", "email": "jane@example.com"})

    def test_share_achievement(self):
        """Test sharing user achievements."""
        self.engagement.create_user_profile("User 1", {"name": "John Doe", "email": "john@example.com"})
        with self.assertLogs(level='INFO') as log:
            self.engagement.share_achievement("User 1", "Achievement1")
            self.assertIn("User   'User 1' shared achievement 'Achievement1' on social media.", log.output)

        # Test sharing achievement for a non-existent user
        with self.assertRaises(ValueError):
            self.engagement.share_achievement("User 2", "Achievement2")

    def test_get_leaderboard(self):
        """Test getting the leaderboard."""
        self.engagement.update_leaderboard("User 1", Decimal('100'))
        self.engagement.update_leaderboard("User 2", Decimal('200'))
        leaderboard = self.engagement.get_leaderboard()
        self.assertEqual(leaderboard["User 1"], Decimal('100'))
        self.assertEqual(leaderboard["User 2"], Decimal('200'))

    def test_get_notifications(self):
        """Test getting notifications."""
        self.engagement.send_notification("Notification1")
        self.engagement.send_notification("Notification2")
        notifications = self.engagement.get_notifications()
        self.assertIn("Notification1", notifications)
        self.assertIn("Notification2", notifications)

    def test_get_user_profile(self):
        """Test getting user profiles."""
        self.engagement.create_user_profile("User 1", {"name": "John Doe", "email": "john@example.com"})
        profile = self.engagement.get_user_profile("User 1")
        self.assertEqual(profile, {"name": "John Doe", "email": "john@example.com"})

        # Test getting a non-existent user profile
        with self.assertRaises(ValueError):
            self.engagement.get_user_profile("User 2")

if __name__ == '__main__':
    unittest.main()
