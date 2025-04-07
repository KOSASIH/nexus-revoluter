import unittest
import json
from governance import Governance, Proposal  # Assuming governance.py is in the same directory

class TestGovernance(unittest.TestCase):

    def setUp(self):
        """Set up a new Governance instance for testing."""
        self.governance = Governance()

    def test_create_proposal(self):
        """Test creating a new proposal."""
        proposal_id = self.governance.create_proposal("Test Proposal", "Description", "admin", 3600, "Technical")
        self.assertEqual(proposal_id, 1)
        self.assertIn(proposal_id, self.governance.proposals)
        proposal = self.governance.get_proposal(proposal_id)
        self.assertEqual(proposal['title'], "Test Proposal")
        self.assertEqual(proposal['description'], "Description")
        self.assertEqual(proposal['creator'], "admin")
        self.assertEqual(proposal['status'], "Pending")

    def test_vote_on_proposal(self):
        """Test voting on a proposal."""
        proposal_id = self.governance.create_proposal("Vote Test", "Description", "admin", 3600, "Technical")
        self.governance.vote_on_proposal(proposal_id, "user1", True, weight=2)
        self.governance.vote_on_proposal(proposal_id, "user2", False, weight=1)

        proposal = self.governance.get_proposal(proposal_id)
        self.assertEqual(proposal['yes_votes'], 2)
        self.assertEqual(proposal['no_votes'], 1)
        self.assertEqual(proposal['total_votes'], 3)

    def test_finalize_proposal(self):
        """Test finalizing a proposal."""
        proposal_id = self.governance.create_proposal("Finalize Test", "Description", "admin", 3600, "Technical")
        self.governance.vote_on_proposal(proposal_id, "user1", True, weight=2)
        self.governance.vote_on_proposal(proposal_id, "user2", False, weight=1)

        # Finalize the proposal
        self.governance.finalize_proposal(proposal_id)
        proposal = self.governance.get_proposal(proposal_id)
        self.assertEqual(proposal['status'], "Completed")

    def test_finalize_proposal_with_insufficient_votes(self):
        """Test finalizing a proposal with insufficient votes."""
        proposal_id = self.governance.create_proposal("Insufficient Votes", "Description", "admin", 3600, "Technical")
        self.governance.vote_on_proposal(proposal_id, "user1", True, weight=1)  # Only 1 vote

        # Finalize the proposal
        self.governance.finalize_proposal(proposal_id)
        proposal = self.governance.get_proposal(proposal_id)
        self.assertEqual(proposal['status'], "Rejected")

    def test_proposal_expiration(self):
        """Test proposal expiration."""
        proposal_id = self.governance.create_proposal("Expiration Test", "Description", "admin", 1, "Technical")  # 1 second duration
        self.governance.vote_on_proposal(proposal_id, "user1", True, weight=1)

        # Wait for the proposal to expire
        import time
        time.sleep(2)

        # Attempt to finalize the proposal
        self.governance.finalize_proposal(proposal_id)
        proposal = self.governance.get_proposal(proposal_id)
        self.assertEqual(proposal['status'], "Completed")  # Should be completed since it was voted on

    def test_get_all_proposals(self):
        """Test retrieving all proposals."""
        self.governance.create_proposal("Proposal 1", "Description 1", "admin", 3600, "Technical")
        self.governance.create_proposal("Proposal 2", "Description 2", "admin", 3600, "Technical")
        
        proposals = self.governance.get_all_proposals()
        self.assertEqual(len(proposals), 2)

if __name__ == "__main__":
    unittest.main()
