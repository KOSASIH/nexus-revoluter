import unittest
from unittest.mock import patch, MagicMock
from swarm_stability import SwarmStability

class TestSwarmStability(unittest.TestCase):

    @patch('swarm_stability.Node')
    @patch('swarm_stability.AdaptiveConsensus')
    def setUp(self, mock_adaptive_consensus, mock_node):
        # Mock the Node and AdaptiveConsensus classes
        self.mock_node = mock_node
        self.mock_adaptive_consensus = mock_adaptive_consensus.return_value

        # Initialize the SwarmStability class
        self.swarm_stability = SwarmStability()

    def test_add_node(self):
        # Call add_node
        self.swarm_stability.add_node("Node-1")

        # Check that the node was added
        self.assertEqual(len(self.swarm_stability.nodes), 1)
        self.assertEqual(self.swarm_stability.nodes[0].node_id, "Node-1")

    def test_communicate(self):
        # Mock the adjust_supply method of the Node class
        mock_node_instance = self.mock_node.return_value
        self.swarm_stability.add_node("Node-1")
        self.swarm_stability.add_node("Node-2")

        # Call communicate
        self.swarm_stability.communicate()

        # Check that adjust_supply was called for each node
        mock_node_instance.adjust_supply.assert_called_with(self.swarm_stability.target_value)

    def test_make_decision(self):
        # Mock the decide_action method of the Node class
        mock_node_instance = self.mock_node.return_value
        mock_node_instance.decide_action.side_effect = ["increase_supply", "decrease_supply", "increase_supply"]

        self.swarm_stability.add_node("Node-1")
        self.swarm_stability.add_node("Node-2")
        self.swarm_stability.add_node("Node-3")

        # Call make_decision
        final_decision = self.swarm_stability.make_decision()

        # Check that the final decision is the most common one
        self.assertEqual(final_decision, "increase_supply")

    def test_aggregate_decisions(self):
        decisions = ["increase_supply", "decrease_supply", "increase_supply", "increase_supply", "decrease_supply"]
        
        # Call aggregate_decisions
        final_decision = self.swarm_stability.aggregate_decisions(decisions)

        # Check that the final decision is the most common one
        self.assertEqual(final_decision, "increase_supply")

    def test_adapt_to_market_changes(self):
        # Mock the methods used in adapt_to_market_changes
        self.swarm_stability.add_node("Node-1")
        self.swarm_stability.add_node("Node-2")

        with patch.object(self.swarm_stability, 'communicate') as mock_communicate, \
             patch.object(self.swarm_stability, 'make_decision', return_value="adjust_supply") as mock_make_decision:
            
            market_conditions = ['bull_market', 'bear_market']
            self.swarm_stability.adapt_to_market_changes(market_conditions)

            # Check that communicate and make_decision were called
            self.assertEqual(mock_communicate.call_count, len(market_conditions))
            self.assertEqual(mock_make_decision.call_count, len(market_conditions))

if __name__ == '__main__':
    unittest.main()
