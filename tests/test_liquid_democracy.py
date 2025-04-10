import unittest
from liquid_democracy import LiquidDemocracy

class TestLiquidDemocracy(unittest.TestCase):
    def setUp(self):
        """Set up a new LiquidDemocracy instance for testing."""
        self.democracy = LiquidDemocracy()

    def test_delegate_vote(self):
        """Test delegating a vote to another user."""
        self.democracy.delegate_vote("Alice", "Bob")
        self.assertEqual(self.democracy.get_delegate("Alice"), "Bob")

    def test_delegate_vote_self(self):
        """Test that a user cannot delegate their vote to themselves."""
        with self.assertRaises(ValueError):
            self.democracy.delegate_vote("Alice", "Alice")

    def test_revoke_delegation(self):
        """Test revoking a user's delegation."""
        self.democracy.delegate_vote("Alice", "Bob")
        self.democracy.revoke_delegation("Alice")
        self.assertEqual(self.democracy.get_delegate("Alice"), "Alice")

    def test_create_proposal(self):
        """Test creating a new proposal."""
        self.democracy.create_proposal("Increase funding for education")
        self.assertIn("Increase funding for education", self.democracy.proposals)

    def test_vote_on_proposal(self):
        """Test voting on a proposal."""
        self.democracy.create_proposal("Increase funding for education")
        self.democracy.delegate_vote("Alice", "Bob")
        self.democracy.vote("Alice", "Increase funding for education", "Yes")
        self.assertIn("Bob", self.democracy.votes["Increase funding for education"])
        self.assertEqual(self.democracy.votes["Increase funding for education"]["Bob"], "Yes")

    def test_vote_with_delegation(self):
        """Test that a user's vote is counted through their delegate."""
        self.democracy.create_proposal("Increase funding for education")
        self.democracy.delegate_vote("Alice", "Bob")
        self.democracy.vote("Charlie", "Increase funding for education", "Yes")  # Charlie votes directly
        self.democracy.vote("Alice", "Increase funding for education", "No")  # Alice's vote goes to Bob
        self.assertEqual(self.democracy.votes["Increase funding for education"]["Bob"], "No")
        self.assertEqual(self.democracy.votes["Increase funding for education"]["Charlie"], "Yes")

    def test_tally_votes(self):
        """Test tallying votes for a proposal."""
        self.democracy.create_proposal("Increase funding for education")
        self.democracy.vote("Alice", "Increase funding for education", "Yes")
        self.democracy.vote("Bob", "Increase funding for education", "No")
        self.democracy.vote("Charlie", "Increase funding for education", "Yes")
        tally = self.democracy.tally_votes("Increase funding for education")
        self.assertEqual(tally, {"Yes": 2, "No": 1})

    def test_get_user_votes(self):
        """Test getting the votes cast by a user."""
        self.democracy.create_proposal("Increase funding for education")
        self.democracy.create_proposal("Implement universal basic income")
        self.democracy.vote("Alice", "Increase funding for education", "Yes")
        self.democracy.vote("Bob", "Implement universal basic income", "No")
        user_votes = self.democracy.get_user_votes("Alice")
        self.assertEqual(user_votes, {"Increase funding for education": "Yes"})

if __name__ == '__main__':
    unittest.main()
