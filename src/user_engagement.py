from decimal import Decimal
from collections import defaultdict

class UserEngagement:
    """Class to manage user engagement features."""
    def __init__(self):
        self.rewards = {}  # Mapping of rewards to their descriptions
        self.leaderboard = defaultdict(Decimal)  # Mapping of users to their scores
        self.notifications = []  # List of notifications
        self.user_profiles = {}  # Mapping of users to their profiles

    def add_reward(self, reward, description):
        """Add a new reward to the system."""
        self.rewards[reward] = description
        print(f"Reward '{reward}' added with description: {description}")

    def update_leaderboard(self, user, score):
        """Update the leaderboard with a user's score."""
        self.leaderboard[user] = score
        print(f"User  '{user}' updated with score: {score}")

    def send_notification(self, notification):
        """Send a notification to users."""
        self.notifications.append(notification)
        print(f"Notification '{notification}' sent to users.")

    def create_user_profile(self, user, profile):
        """Create a new user profile."""
        self.user_profiles[user] = profile
        print(f"User  '{user}' created with profile: {profile}")

    def update_user_profile(self, user, profile):
        """Update a user's profile."""
        if user in self.user_profiles:
            self.user_profiles[user] = profile
            print(f"User  '{user}' updated with profile: {profile}")
        else:
            raise ValueError("User  does not exist.")

    def share_achievement(self, user, achievement):
        """Share a user's achievement on social media."""
        if user in self.user_profiles:
            print(f"User  '{user}' shared achievement '{achievement}' on social media.")
        else:
            raise ValueError("User  does not exist.")

    def get_leaderboard(self):
        """Get the leaderboard."""
        return dict(self.leaderboard)

    def get_notifications(self):
        """Get the notifications."""
        return self.notifications

    def get_user_profile(self, user):
        """Get a user's profile."""
        if user in self.user_profiles:
            return self.user_profiles[user]
        else:
            raise ValueError("User  does not exist.")

# Example usage
if __name__ == "__main__":
    # Create a user engagement instance
    engagement = UserEngagement()

    # Add rewards
    engagement.add_reward("Reward1", "Description for Reward1")
    engagement.add_reward("Reward2", "Description for Reward2")

    # Update leaderboard
    engagement.update_leaderboard("User 1", Decimal('100'))
    engagement.update_leaderboard("User 2", Decimal('200'))

    # Send notifications
    engagement.send_notification("Notification1")
    engagement.send_notification("Notification2")

    # Create user profiles
    engagement.create_user_profile("User 1", {"name": "John Doe", "email": "john@example.com"})
    engagement.create_user_profile("User 2", {"name": "Jane Doe", "email": "jane@example.com"})

    # Update user profiles
    engagement.update_user_profile("User 1", {"name": "John Doe", "email": "john2@example.com"})

    # Share achievements
    engagement.share_achievement("User 1", "Achievement1")
    engagement.share_achievement("User 2", "Achievement2")

    # Get leaderboard
    leaderboard = engagement.get_leaderboard()
    print("Leaderboard:")
    for user, score in leaderboard.items():
        print(f"{user}: {score}")

    # Get notifications
    notifications = engagement.get_notifications()
    print("Notifications:")
    for notification in notifications:
        print(notification)

    # Get user profiles
    user_profile = engagement.get_user_profile("User 1")
    print("User  Profile:")
    for key, value in user_profile.items():
        print(f"{key}: {value}")
