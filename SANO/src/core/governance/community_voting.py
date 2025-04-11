import logging
import time
from collections import defaultdict

class Proposal:
    def __init__(self, proposal_id, description, creator, duration):
        self.proposal_id = proposal_id
        self.description = description
        self.creator = creator
        self.votes = defaultdict(int)  # Mapping of voter address to vote count
        self.start_time = time.time()
        self.duration = duration  # Duration in seconds
        self.executed = False

    def is_active(self):
        return time.time() < self.start_time + self.duration

    def total_votes(self):
        return sum(self.votes.values())

class CommunityVoting:
    def __init__(self, governance_token):
        self.logger = logging.getLogger("CommunityVoting")
        self.proposals = {}
        self.governance_token = governance_token  # Reference to the governance token contract

    def create_proposal(self, proposal_id, description, creator, duration):
        """Create a new proposal."""
        if proposal_id in self.proposals:
            self.logger.error("Proposal ID already exists.")
            return False

        proposal = Proposal(proposal_id, description, creator, duration)
        self.proposals[proposal_id] = proposal
        self.logger.info(f"Proposal created: {proposal_id} by {creator}")
        return True

    def vote(self, proposal_id, voter, vote_count):
        """Vote on a proposal."""
        if proposal_id not in self.proposals:
            self.logger.error("Proposal does not exist.")
            return False

        proposal = self.proposals[proposal_id]
        if not proposal.is_active():
            self.logger.error("Voting period has ended.")
            return False

        # Check if the voter has enough governance tokens
        if self.governance_token.balanceOf(voter) < vote_count:
            self.logger.error("Insufficient governance tokens to vote.")
            return False

        proposal.votes[voter] += vote_count
        self.logger.info(f"{voter} voted {vote_count} on proposal {proposal_id}")
        return True

    def tally_votes(self, proposal_id):
        """Tally votes for a proposal."""
        if proposal_id not in self.proposals:
            self.logger.error("Proposal does not exist.")
            return None

        proposal = self.proposals[proposal_id]
        if proposal.is_active():
            self.logger.error("Voting is still active.")
            return None

        total_votes = proposal.total_votes()
        self.logger.info(f"Total votes for proposal {proposal_id}: {total_votes}")
        return total_votes

    def execute_proposal(self, proposal_id):
        """Execute a proposal if it has passed."""
        if proposal_id not in self.proposals:
            self.logger.error("Proposal does not exist.")
            return False

        proposal = self.proposals[proposal_id]
        if proposal.executed:
            self.logger.error("Proposal has already been executed.")
            return False

        if not proposal.is_active():
            # Logic to execute the proposal goes here
            proposal.executed = True
            self.logger.info(f"Proposal {proposal_id} executed.")
            return True
        else:
            self.logger.error("Proposal is still active.")
            return False

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # Example governance token mockup
    class MockGovernanceToken:
        def __init__(self):
            self.balances = defaultdict(int)

        def balanceOf(self, address):
            return self.balances[address]

        def mint(self, address, amount):
            self.balances[address] += amount

    governance_token = MockGovernanceToken()
    governance_token.mint("0x123", 100)  # Mint tokens for testing

    voting_system = CommunityVoting(governance_token)
    voting_system.create_proposal("1", "Increase block size", "0x123", 3600)  # 1 hour duration
    voting_system.vote("1", "0x123", 10) voting_system.vote("1", "0x123", 10)  # Voting on the proposal
    time.sleep(2)  # Simulate some time passing
    total_votes = voting_system.tally_votes("1")  # Tally votes after voting period
    if total_votes is not None:
        print(f"Total votes for proposal 1: {total_votes}")
    voting_system.execute_proposal("1")  # Attempt to execute the proposal after voting period
    voting_system.execute_proposal("1")  # Attempt to execute again to check for already executed status
