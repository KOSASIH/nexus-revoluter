import logging
import json
from typing import List, Dict, Any
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Member:
    def __init__(self, address: str):
        self.address = address
        self.votes = 0

class Proposal:
    def __init__(self, title: str, description: str, proposer: str, duration: int):
        self.title = title
        self.description = description
        self.proposer = proposer
        self.votes_for = 0
        self.votes_against = 0
        self.voters = set()  # Track who has voted
        self.expiration = datetime.now() + timedelta(days=duration)  # Set expiration date

    def is_expired(self) -> bool:
        """Check if the proposal has expired."""
        return datetime.now() > self.expiration

class DAO:
    def __init__(self):
        self.members: Dict[str, Member] = {}
        self.proposals: List[Proposal] = []
        self.treasury: float = 0.0
        self.quorum: int = 2  # Minimum votes required for a proposal to pass

    def add_member(self, address: str) -> None:
        """Add a new member to the DAO."""
        if address in self.members:
            logging.warning(f"Member {address} already exists.")
            return
        self.members[address] = Member(address)
        logging.info(f"Member {address} added to the DAO.")

    def remove_member(self, address: str) -> None:
        """Remove a member from the DAO."""
        if address not in self.members:
            logging.warning(f"Member {address} does not exist.")
            return
        del self.members[address]
        logging.info(f"Member {address} removed from the DAO.")

    def create_proposal(self, title: str, description: str, proposer: str, duration: int) -> None:
        """Create a new proposal."""
        if proposer not in self.members:
            logging.warning(f"Proposer {proposer} is not a member of the DAO.")
            return
        proposal = Proposal(title, description, proposer, duration)
        self.proposals.append(proposal)
        logging.info(f"Proposal '{title}' created by {proposer} with duration {duration} days.")

    def vote(self, proposal_title: str, voter_address: str, vote: str) -> None:
        """Vote on a proposal."""
        if voter_address not in self.members:
            logging.warning(f"Voter {voter_address} is not a member of the DAO.")
            return

        proposal = next((p for p in self.proposals if p.title == proposal_title), None)
        if not proposal:
            logging.warning(f"Proposal '{proposal_title}' does not exist.")
            return

        if proposal.is_expired():
            logging.warning(f"Proposal '{proposal_title}' has expired.")
            return

        if voter_address in proposal.voters:
            logging.warning(f"Member {voter_address} has already voted on proposal '{proposal_title}'.")
            return

        if vote.lower() == 'for':
            proposal.votes_for += 1
        elif vote.lower() == 'against':
            proposal.votes_against += 1
        else:
            logging.warning("Vote must be 'for' or 'against'.")
            return

        proposal.voters.add(voter_address)
        logging.info(f"Member {voter_address} voted '{vote}' on proposal '{proposal_title}'.")

    def get_proposal_results(self, proposal_title: str) -> Dict[str, Any]:
        """Get the results of a proposal."""
        proposal = next((p for p in self.proposals if p.title == proposal_title), None)
        if not proposal:
            logging.warning(f"Proposal '{proposal_title}' does not exist.")
            return {}

        results = {
            'title': proposal.title,
            'description': proposal.description,
            'votes_for': proposal.votes_for,
            'votes_against': proposal.votes_against,
            'proposer': proposal.proposer,
            'voters': list(proposal.voters),
            'expired': proposal.is_expired()
        }
        logging.info(f"Results for proposal '{proposal_title}': {results}")
        return results

    def deposit_funds(self, amount: float) -> None:
        """Deposit funds into the DAO treasury."""
        if amount <= 0:
            logging.warning("Deposit amount must be positive.")
            return
        self.treasury += amount
        logging.info(f"Deposited {amount} to the DAO treasury. Total treasury: {self.treasury}")

    def withdraw_funds(self, amount: float) -> None:
        """Withdraw funds from the DAO treasury."""
        if amount <= 0:
            logging.warning("Withdrawal amount must be positive.")
            return
        if amount > self.treasury:
            logging.warning("Insufficient funds in the treasury.")
            return
        self.treasury -= amount
        logging.info(f"Withdrew {amount} from the DAO treasury. Total treasury: {self.treasury}")

    def save_state(self, filename: str) -> None:
        """Save the current state of the DAO to a file."""
        state = {
            'members': list(self.members.keys()),
            'proposals': [
                {
                    'title': p.title,
                    'description': p.description,
                    'proposer': p.proposer,
                    'votes_for': p.votes_for,
                    'votes_against': p.votes_against,
                    'voters': list(p.voters),
                    'expiration': p.expiration.isoformat()
                } for p in self.proposals
            ],
            'treasury': self.treasury
        }
        with open(filename, 'w') as f:
            json.dump(state, f)
        logging.info(f"DAO state saved to {filename}.")

    def load_state(self, filename: str) -> None:
        """Load the DAO state from a file."""
        with open(filename, 'r') as f:
            state = json.load(f)
            self.members = {address: Member(address) for address in state['members']}
            self.treasury = state['treasury']
            self.proposals = []
            for p in state['proposals']:
                proposal = Proposal(p['title'], p['description'], p['proposer'], 0)  # Duration is not loaded
                proposal.votes_for = p['votes_for']
                proposal.votes_against = p['votes_against']
                proposal.voters = set(p['voters'])
                proposal.expiration = datetime.fromisoformat(p['expiration'])
                self.proposals.append(proposal)
            logging.info(f"DAO state loaded from {filename}.")

# Example usage of the DAO class
if __name__ == "__main__":
    dao = DAO()

    # Add members
    dao.add_member("0x123")
    dao.add_member("0x456")

    # Create a proposal
    dao.create_proposal("Increase Budget", "Proposal to increase the budget for project X.", "0x123", duration=7)

    # Vote on the proposal
    dao.vote("Increase Budget", "0x123", "for")
    dao.vote("Increase Budget", "0x456", "against")

    # Get proposal results
    results = dao.get_proposal_results("Increase Budget")
    print(results)

    # Manage treasury
    dao.deposit_funds(1000)
    dao.withdraw_funds(500)

    # Save and load state
    dao.save_state("dao_state.json")
    dao.load_state("dao_state.json")
