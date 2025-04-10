# test_user_interaction.py

import unittest
from user_experience import UserExperience

class TestUser Experience(unittest.TestCase):
    def setUp(self):
        self.user_experience = UserExperience()

    def test_voice_command(self):
        """Test voice command recognition."""
        command = "Show transactions"
        response = self.user_experience.process_voice_command(command)
        self.assertEqual(response, "Displaying transactions.")
        print("Voice command test passed.")

    def test_gesture_control(self):
        """Test gesture control functionality."""
        gesture = "Swipe Up"
        response = self.user_experience.process_gesture(gesture)
        self.assertEqual(response, "Zooming in.")
        print("Gesture control test passed.")

if __name__ == "__main__":
    unittest.main()
