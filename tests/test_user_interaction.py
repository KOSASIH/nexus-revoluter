import unittest
from user_experience import UserExperience

class TestUser Experience(unittest.TestCase):
    def setUp(self):
        """Set up the UserExperience instance for testing."""
        self.user_experience = UserExperience()

    def test_voice_command(self):
        """Test voice command recognition."""
        command = "Show transactions"
        expected_response = "Displaying transactions."
        response = self.user_experience.process_voice_command(command)
        self.assertEqual(response, expected_response, f"Expected '{expected_response}', but got '{response}'.")
        print("Voice command test passed.")

    def test_gesture_control(self):
        """Test gesture control functionality."""
        gesture = "Swipe Up"
        expected_response = "Zooming in."
        response = self.user_experience.process_gesture(gesture)
        self.assertEqual(response, expected_response, f"Expected '{expected_response}', but got '{response}'.")
        print("Gesture control test passed.")

    def test_invalid_voice_command(self):
        """Test handling of an invalid voice command."""
        command = "Invalid command"
        expected_response = "Command not recognized."
        response = self.user_experience.process_voice_command(command)
        self.assertEqual(response, expected_response, f"Expected '{expected_response}', but got '{response}'.")
        print("Invalid voice command test passed.")

    def test_invalid_gesture(self):
        """Test handling of an invalid gesture."""
        gesture = "Unknown Gesture"
        expected_response = "Gesture not recognized."
        response = self.user_experience.process_gesture(gesture)
        self.assertEqual(response, expected_response, f"Expected '{expected_response}', but got '{response}'.")
        print("Invalid gesture test passed.")

if __name__ == "__main__":
    unittest.main()
