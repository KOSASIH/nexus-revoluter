class LiquidDemocracy:
    def __init__(self):
        self.delegates = {}  # Maps users to their delegates
        self.votes = {}      # Maps proposals to votes
        self.user_votes = {} # Maps users to their voting power
        self.proposals = []  # List of proposals

    def delegate_vote(self, user, delegate):
        """Delegate the user's vote to another user."""
        if user == delegate:
            raise ValueError("User cannot delegate vote to themselves.")
        self.delegates[user] = delegate

    def revoke_delegation(self, user):
        """Revoke the user's delegation."""
        if user in self.delegates:
            del self.delegates[user]

    def get_delegate(self, user):
        """Get the delegate for a user."""
        return self.delegates.get(user, user)  # Return the user if no delegate is set

    def create_proposal(self, proposal):
        """Create a new proposal."""
        self.proposals.append(proposal)
        self.votes[proposal] = {}

    def vote(self, user, proposal, vote_value):
        """Vote on a proposal."""
        if proposal not in self.proposals:
            raise ValueError("Proposal does not exist.")
        
        # Get the user's effective delegate
        effective_delegate = self.get_delegate(user)
        
        # Record the vote
        self.votes[proposal][effective_delegate] = vote_value

    def tally_votes(self, proposal):
        """Tally votes for a proposal."""
        if proposal not in self.proposals:
            raise ValueError("Proposal does not exist.")
        
        tally = {}
        for delegate, vote in self.votes[proposal].items():
            if vote not in tally:
                tally[vote] = 0
            tally[vote] += 1  # Count votes

        return tally

    def get_user_votes(self, user):
        """Get the votes cast by a user."""
        user_votes = {}
        for proposal, votes in self.votes.items():
            if user in votes:
                user_votes[proposal] = votes[user]
        return user_votes

# Example usage
if __name__ == "__main__":
    democracy = LiquidDemocracy()
    
    # Create proposals
    democracy.create_proposal("Increase funding for education")
    democracy.create_proposal("Implement universal basic income")

    # Delegate votes
    democracy.delegate_vote("Alice", "Bob")
    democracy.delegate_vote("Charlie", "Alice")

    # Vote on proposals
    democracy.vote("Alice", "Increase funding for education", "Yes")
    democracy.vote("Bob", "Increase funding for education", "No")  # Bob votes directly
    democracy.vote("Charlie", "Increase funding for education", "Yes")  # Charlie's vote goes to Alice

    # Tally votes
    tally = democracy.tally_votes("Increase funding for education")
    print(f"Tally for 'Increase funding for education': {tally}")

    # Get user votes
    user_votes = democracy.get_user_votes("Charlie")
    print(f"Charlie's votes: {user_votes}")
