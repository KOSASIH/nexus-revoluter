class DecentralizedInsurance:
    def __init__(self):
        self.pools = {}  # Dictionary to hold insurance pools
        self.contributors = {}  # Track contributors to each pool
        self.claims = {}  # Track claims for each pool

    def create_pool(self, pool_name, initial_contribution):
        """Create a new insurance pool with an initial contribution."""
        if pool_name in self.pools:
            raise ValueError("Pool already exists.")
        self.pools[pool_name] = initial_contribution
        self.contributors[pool_name] = []
        self.claims[pool_name] = []

    def contribute(self, pool_name, amount, contributor):
        """Allow users to contribute to an insurance pool."""
        if pool_name not in self.pools:
            raise ValueError("Pool does not exist.")
        self.pools[pool_name] += amount
        self.contributors[pool_name].append((contributor, amount))

    def submit_claim(self, pool_name, claim_amount, claimant):
        """Submit a claim to the insurance pool."""
        if pool_name not in self.pools:
            raise ValueError("Pool does not exist.")
        self.claims[pool_name].append({"amount": claim_amount, "claimant": claimant, "approved": False})

    def process_claim(self, pool_name, claim_index):
        """Process a claim from the insurance pool based on voting."""
        if pool_name not in self.pools:
            raise ValueError("Pool does not exist.")
        if claim_index >= len(self.claims[pool_name]):
            raise ValueError("Claim does not exist.")

        claim = self.claims[pool_name][claim_index]
        if claim["approved"]:
            raise ValueError("Claim has already been approved.")

        # Voting mechanism for claim approval
        votes = self.vote_on_claim(pool_name, claim)
        if votes > len(self.contributors[pool_name]) / 2:  # Simple majority
            if self.pools[pool_name] >= claim["amount"]:
                self.pools[pool_name] -= claim["amount"]
                claim["approved"] = True
                return True
            else:
                raise ValueError("Insufficient funds in the pool to cover the claim.")
        return False

    def vote_on_claim(self, pool_name, claim):
        """Simulate voting on a claim by contributors."""
        # For simplicity, we randomly decide votes (in a real scenario, this would be user-driven)
        votes = 0
        for contributor, _ in self.contributors[pool_name]:
            if self.random_vote():  # Simulate a random vote
                votes += 1
        return votes

    def random_vote(self):
        """Randomly decide to vote for or against a claim."""
        import random
        return random.choice([True, False])  # Randomly approve or disapprove

# Example usage
if __name__ == "__main__":
    insurance = DecentralizedInsurance()

    # Create a new insurance pool
    insurance.create_pool("Health Insurance", 1000)

    # Contributors add funds to the pool
    insurance.contribute("Health Insurance", 200, "Alice")
    insurance.contribute("Health Insurance", 300, "Bob")

    # Submit a claim
    insurance.submit_claim("Health Insurance", 500, "Alice")

    # Process the claim
    try:
        if insurance.process_claim("Health Insurance", 0):
            print("Claim approved and processed.")
        else:
            print("Claim denied.")
    except ValueError as e:
        print(f"Error: {e}")
