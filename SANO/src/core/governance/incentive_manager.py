import logging
from collections import defaultdict
from datetime import datetime, timedelta

class IncentiveManager:
    def __init__(self, governance_token):
        self.logger = logging.getLogger("IncentiveManager")
        self.governance_token = governance_token  # Reference to the governance token contract
        self.incentives = defaultdict(list)  # Mapping of user addresses to their incentives
        self.performance_data = defaultdict(lambda: {"contributions": 0, "votes": 0})

    def add_performance_data(self, user, contributions, votes):
        """Add performance data for a user."""
        self.performance_data[user]["contributions"] += contributions
        self.performance_data[user]["votes"] += votes
        self.logger.info(f"Performance data updated for {user}: {self.performance_data[user]}")

    def calculate_incentives(self, user):
        """Calculate incentives based on performance data."""
        contributions = self.performance_data[user]["contributions"]
        votes = self.performance_data[user]["votes"]
        incentive_amount = 0

        # Example incentive structure
        if contributions > 1000:
            incentive_amount += contributions * 0.1  # 10% of contributions as incentive
        if votes > 10:
            incentive_amount += votes * 5  # 5 tokens per vote

        self.logger.info(f"Incentives calculated for {user}: {incentive_amount}")
        return incentive_amount

    def distribute_incentives(self, user):
        """Distribute incentives to a user."""
        incentive_amount = self.calculate_incentives(user)
        if incentive_amount > 0:
            self.governance_token.mint(user, incentive_amount)  # Mint tokens for the user
            self.incentives[user].append((datetime.now(), incentive_amount))
            self.logger.info(f"Distributed {incentive_amount} tokens to {user}")
        else:
            self.logger.info(f"No incentives to distribute for {user}")

    def get_incentives_history(self, user):
        """Get the incentive distribution history for a user."""
        return self.incentives[user]

    def adjust_incentive_parameters(self, new_parameters):
        """Adjust incentive parameters based on governance decisions."""
        # This method would be called by the governance system
        # Example: new_parameters could include changes to the incentive structure
        self.logger.info(f"Incentive parameters adjusted: {new_parameters}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Example governance token mockup
    class MockGovernanceToken:
        def __init__(self):
            self.balances = defaultdict(int)

        def mint(self, address, amount):
            self.balances[address] += amount
            print(f"Minted {amount} tokens to {address}. New balance: {self.balances[address]}")

    governance_token = MockGovernanceToken()
    incentive_manager = IncentiveManager(governance_token)

    # Simulate user performance data
    incentive_manager.add_performance_data("0x123", 1500, 12)  # User with contributions and votes
    incentive_manager.distribute_incentives("0x123")  # Distribute incentives to the user

    # Check incentive history
    history = incentive_manager.get_incentives_history("0x123")
    print(f"Incentive history for 0x123: {history}")
