import logging
import random
from node import Node
from adaptive_consensus import AdaptiveConsensus

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SwarmStability:
    def __init__(self, target_value=314159.00, symbol="Pi", total_supply=100000000000):
        self.target_value = target_value  # Target value for Pi Coin
        self.symbol = symbol               # Pi Coin symbol
        self.total_supply = total_supply   # Total supply of Pi Coin
        self.nodes = []                    # List of nodes in the swarm
        self.consensus = AdaptiveConsensus()

    def add_node(self, node_id):
        """Add a new node to the swarm."""
        new_node = Node(node_id)
        self.nodes.append(new_node)
        logging.info(f"Node {node_id} added to the swarm.")

    def communicate(self):
        """Facilitate communication between nodes to adjust supply/liquidity."""
        logging.info("Nodes are communicating to adjust supply/liquidity...")
        for node in self.nodes:
            node.adjust_supply(self.target_value)

    def make_decision(self):
        """Collective decision-making process among nodes."""
        logging.info("Making collective decisions...")
        decisions = [node.decide_action() for node in self.nodes]
        final_decision = self.aggregate_decisions(decisions)
        logging.info(f"Final decision made: {final_decision}")
        return final_decision

    def aggregate_decisions(self, decisions):
        """Aggregate decisions from all nodes."""
        # Simple majority voting for decision aggregation
        decision_count = {}
        for decision in decisions:
            if decision in decision_count:
                decision_count[decision] += 1
            else:
                decision_count[decision] = 1
        # Return the decision with the highest count
        return max(decision_count, key=decision_count.get)

    def adapt_to_market_changes(self, market_conditions):
        """Adapt to global market changes based on conditions."""
        logging.info("Adapting to market changes...")
        for condition in market_conditions:
            self.communicate()
            decision = self.make_decision()
            self.consensus.sync(decision)

# Example usage of the SwarmStability class
if __name__ == "__main__":
    swarm_stability = SwarmStability()
    
    # Adding nodes to the swarm
    for i in range(5):
        swarm_stability.add_node(f"Node-{i+1}")

    # Example market conditions to adapt to
    market_conditions = ['bull_market', 'bear_market', 'high_volatility']
    swarm_stability.adapt_to_market_changes(market_conditions)
