import json
import logging
from typing import List, Dict, Any
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Proposal:
    def __init__(self, proposal_id: int, title: str, description: str, creator: str, duration: int, category: str):
        self.proposal_id = proposal_id
        self.title = title
        self.description = description
        self.creator = creator
        self.votes: Dict[str, bool] = {}  # User address -> Vote (True for Yes, False for No)
        self.total_votes = 0
        self.yes_votes = 0
        self.no_votes = 0
        self.status = "Pending"  # Status can be Pending, Active, or Completed
        self.created_at = datetime.now()
        self.expires_at = self.created_at + timedelta(seconds=duration)
        self.category = category

    def vote(self, user: str, support: bool, weight: int = 1) -> None:
        """Cast a vote on the proposal with optional weight."""
        if user in self.votes:
            logging.warning(f"User  {user} has already voted on proposal {self.proposal_id}.")
            return
        self.votes[user] = support
        self.total_votes += weight
        if support:
            self.yes_votes += weight
        else:
            self.no_votes += weight
        logging.info(f"User  {user} voted {'Yes' if support else 'No'} on proposal {self.proposal_id}.")

    def finalize(self) -> None:
        """Finalize the proposal based on the voting results."""
        if self.total_votes < 3:  # Example quorum requirement
            self.status = "Rejected"
            logging.info(f"Proposal {self.proposal_id} has been rejected due to insufficient votes.")
            return

        if self.yes_votes > self.no_votes:
            self.status = "Completed"
            logging.info(f"Proposal {self.proposal_id} has been approved.")
        else:
            self.status = "Completed"
            logging.info(f"Proposal {self.proposal_id} has been rejected.")

    def is_active(self) -> bool:
        """Check if the proposal is still active for voting."""
        return datetime.now() < self.expires_at

class Governance:
    def __init__(self):
        self.proposals: Dict[int, Proposal] = {}
        self.next_proposal_id = 1

    def create_proposal(self, title: str, description: str, creator: str, duration: int, category: str) -> int:
        """Create a new governance proposal."""
        proposal = Proposal(self.next_proposal_id, title, description, creator, duration, category)
        self.proposals[self.next_proposal_id] = proposal
        logging.info(f"Created proposal {self.next_proposal_id}: {title} in category {category}")
        self.next_proposal_id += 1
        return proposal.proposal_id

    def vote_on_proposal(self, proposal_id: int, user: str, support: bool, weight: int = 1) -> None:
        """Vote on a specific proposal."""
        if proposal_id not in self.proposals:
            logging.warning(f"Proposal {proposal_id} does not exist.")
            return
        proposal = self.proposals[proposal_id]
        if not proposal.is_active():
            logging.warning(f"Proposal {proposal_id} is no longer active for voting.")
            return
        proposal.vote(user, support, weight)

    def finalize_proposal(self, proposal_id: int) -> None:
        """Finalize a proposal after voting is complete."""
        if proposal_id not in self.proposals:
            logging.warning(f"Proposal {proposal_id} does not exist.")
            return
        proposal = self.proposals[proposal_id]
        if proposal.is_active():
            logging.warning(f"Proposal {proposal_id} is still active and cannot be finalized yet.")
            return
        proposal.finalize()

    def get_proposal(self, proposal_id: int) -> Dict[str, Any]:
        """Get details of a specific proposal."""
        if proposal_id not in self.proposals:
            logging.warning(f"Proposal {proposal_id} does not exist.")
            return {}
        proposal = self.proposals[proposal_id]
        return {
            "proposal_id": proposal.proposal_id,
            "title": proposal.title,
            "description": proposal.description,
            "creator": proposal.creator,
            "total_votes": proposal.total_votes,
            "yes_votes": proposal.yes_votes,
            "no_votes": proposal.no_votes,
            "status": proposal.status,
            "votes": proposal.votes,
            "expires_at": proposal.expires_at.isoformat(),
            "category": proposal.category
        }

    def get_all_proposals(self) -> List[Dict[str, Any]]:
        """Get a list of all proposals."""
        return [self.get_proposal(proposal_id) for proposal_id in self.proposals]

# Example usage of the Governance class
if __name__ == "__main__":
    governance = Governance()

    # Create proposals
    proposal_id1 = governance.create_proposal("Increase Block Size", "Proposal to increase the block size to 2MB.", "admin", 3600, "Technical")
    proposal_id2 = governance.create_proposal("Implement Staking", "Proposal to implement staking rewards for users.", "admin", 7200, "Economic")

    # Users vote on proposals
    governance.vote_on_proposal(proposal_id1, "user1", True, weight=2)
    governance.vote_on_proposal(proposal_id1, "user2", False, weight=1)
    governance.vote_on_proposal(proposal_id2, "user1", True, weight=3)

    # Finalize proposals
    governance.finalize_proposal(proposal_id1)
    governance.finalize_proposal(proposal_id2)

    # Get proposal details
    print(json.dumps(governance.get_all_proposals(), indent=4))
