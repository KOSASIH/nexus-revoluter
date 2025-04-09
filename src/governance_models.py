from decimal import Decimal
from collections import defaultdict
import time

class GovernanceModel:
    """Base class for governance models."""
    def __init__(self):
        self.votes = defaultdict(int)  # Store votes for proposals
        self.proposals = {}  # Dictionary to store proposals with their status
        self.voting_period = 3600  # Voting period in seconds (default: 1 hour)

    def create_proposal(self, proposal):
        """Create a new proposal."""
        self.proposals[proposal] = {
            'status': 'pending',
            'creation_time': time.time(),
            'yes_votes': 0,
            'no_votes': 0
        }
        print(f"Proposal '{proposal}' created.")

    def vote(self, proposal, voter, decision):
        """Vote on a proposal."""
        if proposal not in self.proposals:
            raise ValueError("Proposal does not exist.")
        if self.is_voting_period_expired(proposal):
            raise ValueError("Voting period has expired for this proposal.")
        
        self.votes[(proposal, voter)] = decision
        if decision == 'yes':
            self.proposals[proposal]['yes_votes'] += 1
        elif decision == 'no':
            self.proposals[proposal]['no_votes'] += 1
        print(f"Voter '{voter}' voted '{decision}' on proposal '{proposal}'.")

    def tally_votes(self, proposal):
        """Tally votes for a proposal."""
        if proposal not in self.proposals:
            raise ValueError("Proposal does not exist.")
        return self.proposals[proposal]['yes_votes'], self.proposals[proposal]['no_votes']

    def is_voting_period_expired(self, proposal):
        """Check if the voting period for a proposal has expired."""
        if proposal not in self.proposals:
            raise ValueError("Proposal does not exist.")
        return (time.time() - self.proposals[proposal]['creation_time']) > self.voting_period

class DirectDemocracy(GovernanceModel):
    """Direct Democracy model where all members can vote on every proposal."""
    def __init__(self):
        super().__init__()

    def execute_proposal(self, proposal):
        """Execute a proposal if it passes."""
        if self.is_voting_period_expired(proposal):
            print(f"Voting period expired for proposal '{proposal}'.")
            return
        
        yes_votes, no_votes = self.tally_votes(proposal)
        if yes_votes > no_votes:
            self.proposals[proposal]['status'] = 'executed'
            print(f"Proposal '{proposal}' passed with {yes_votes} yes votes and {no_votes} no votes.")
        else:
            self.proposals[proposal]['status'] = 'failed'
            print(f"Proposal '{proposal}' failed with {no_votes} no votes.")

class RepresentativeDemocracy(GovernanceModel):
    """Representative Democracy model where members elect representatives to vote on their behalf."""
    def __init__(self):
        super().__init__()
        self.representatives = {}  # Mapping of representatives to their constituents

    def elect_representative(self, representative, constituents):
        """Elect a representative for a group of constituents."""
        for constituent in constituents:
            self.representatives[constituent] = representative
        print(f"Representative '{representative}' elected for constituents: {constituents}")

    def vote(self, proposal, voter, decision):
        """Override vote method to allow representatives to vote on behalf of constituents."""
        if voter in self.representatives:
            representative = self.representatives[voter]
            super().vote(proposal, representative, decision)
        else:
            raise ValueError("Voter is not a constituent of any representative.")

class LiquidDemocracy(GovernanceModel):
    """Liquid Democracy model where members can delegate their votes to others."""
    def __init__(self):
        super().__init__()
        self.delegations = {}  # Mapping of voters to their delegates

    def delegate_vote(self, voter, delegate):
        """Delegate vote to another voter."""
        self.delegations[voter] = delegate
        print(f"Voter '{voter}' delegated their vote to '{delegate}'.")

    def vote(self, proposal, voter, decision):
        """Override vote method to allow delegation."""
        if voter in self.delegations:
            delegate = self.delegations[voter]
            super().vote(proposal, delegate, decision)
        else:
            super().vote(proposal, voter, decision)

class DAO(GovernanceModel):
    """Decentralized Autonomous Organization (DAO) model."""
    def __init__(self):
        super().__init__()
        self.members = set()  # Set of DAO members

    def add_member(self, member):
        """Add a new member to the DAO."""
        self.members.add(member)
        print(f"Member '{member}' added to the DAO.")

    def remove_member(self, member):
        """Remove a member from the DAO."""
        self.members.discard(member)
        print(f"Member '{member}' removed from the DAO.")

    def vote(self, proposal, voter, decision):
        """Override vote method to ensure only members can vote."""
        if voter not in self.members:
            raise ValueError("Only DAO members can vote.")
        super().vote(proposal, voter, decision)

    def execute_proposal(self, proposal):
        """Execute a proposal if it passes."""
        if self.is_voting_period_expired(proposal):
            print(f"Voting period expired for proposal '{proposal}'.")
            return
        
        yes_votes, no_votes = self.tally_votes(proposal)
        if yes_votes > no_votes:
            self.proposals[proposal]['status'] = 'executed'
            print(f"Proposal '{proposal}' passed with {yes_votes} yes votes and {no_votes} no votes.")
        else:
            self.proposals[proposal]['status'] = 'failed'
            print(f"Proposal '{proposal}' failed with {no_votes} no votes.")

# Example usage
if __name__ == "__main__":
    # Create a Direct Democracy model
    direct_democracy = DirectDemocracy()
    direct_democracy.create_proposal("Increase block reward")
    direct_democracy.vote("Increase block reward", "Alice", "yes")
    direct_democracy.vote("Increase block reward", "Bob", "no")
    direct_democracy.execute_proposal("Increase block reward")

    # Create a Representative Democracy model
    rep_democracy = RepresentativeDemocracy()
    rep_democracy.elect_representative("Charlie", ["Alice", "Bob"])
    rep_democracy.create_proposal("Change governance model")
    rep_democracy.vote("Change governance model", "Alice", "yes")
    rep_democracy.vote("Change governance model", "Charlie", "no")
    rep_democracy.execute_proposal("Change governance model")

    # Create a Liquid Democracy model
    liquid_democracy = LiquidDemocracy()
    liquid_democracy.create_proposal("Fund community project")
    liquid_democracy.delegate_vote("Alice", "Bob")
    liquid_democracy.vote("Fund community project", "Alice", "yes")  # Alice's vote is delegated to Bob
    liquid_democracy.vote("Fund community project", "Charlie", "no")
    liquid_democracy.execute_proposal("Fund community project")

    # Create a DAO model
    dao = DAO()
    dao.add_member("Alice")
    dao.add_member("Bob")
    dao.create_proposal("Launch new feature")
    dao.vote("Launch new feature", "Alice", "yes")
    dao.vote("Launch new feature", "Bob", "yes")
    dao.execute_proposal("Launch new feature")
