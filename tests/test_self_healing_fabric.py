import unittest
from unittest.mock import MagicMock
from self_healing_fabric import SelfHealingFabric
from blockchain import Blockchain
from consensus import Consensus

class TestSelfHealingFabric(unittest.TestCase):
    def setUp(self):
        """Set up the test environment."""
        self.blockchain = Blockchain()
        self.consensus = Consensus()
        self.self_healing_fabric = SelfHealingFabric(self.blockchain, self.consensus)

    def test_fork_resolution(self):
        """Test fork detection and resolution."""
        # Simulate a fork
        self.blockchain.add_block("Block 1")
        self.blockchain.add_block("Block 2")  # Main chain
        self.blockchain.add_block("Block 3")  # Main chain
        self.blockchain.add_block("Fork Block 2")  # Forked chain

        # Mock the consensus method
        self.consensus.resolve_fork = MagicMock(return_value=True)

        # Detect and resolve the fork
        anomalies = [{'type': 'fork', 'block_id': 'Fork Block 2'}]
        self.self_healing_fabric.handle_anomalies(anomalies)

        # Check if the fork was resolved
        self.assertEqual(self.blockchain.get_latest_block(), "Block 3")
        self.consensus.resolve_fork.assert_called_once_with('Fork Block 2')

    def test_node_recovery(self):
        """Test node failure and recovery."""
        # Simulate adding nodes
        self.blockchain.add_node("Node 1")
        self.blockchain.add_node("Node 2")
        self.blockchain.add_node("Node 3")

        # Simulate a node failure
        self.blockchain.fail_node("Node 2")

        # Check the status of the node
        self.assertEqual(self.blockchain.get_node_status("Node 2"), "failed")

        # Mock the reconstruction method
        self.blockchain.reconstruct_node_state = MagicMock()

        # Recover the node
        anomalies = [{'type': 'node_failure', 'node_id': 'Node 2'}]
        self.self_healing_fabric.handle_anomalies(anomalies)

        # Check if the node was recovered
        self.blockchain.reconstruct_node_state.assert_called_once()
        self.assertEqual(self.blockchain.get_node_status("Node 2"), "active")

    def test_51_percent_attack(self):
        """Test handling of a 51% attack."""
        # Simulate a 51% attack
        self.blockchain.add_block("Block 1")
        self.blockchain.add_block("Block 2")
        self.blockchain.add_block("Block 3")
        self.blockchain.add_block("Malicious Block 1")  # Malicious chain

        # Mock the increase difficulty method
        self.consensus.increase_difficulty = MagicMock()

        # Detect the attack
        anomalies = [{'type': 'attack', 'attack_type': '51%'}]
        self.self_healing_fabric.handle_anomalies(anomalies)

        # Check if the difficulty was increased
        self.consensus.increase_difficulty.assert_called_once()

    def test_ddos_attack(self):
        """Test handling of a DDoS attack."""
        # Simulate a DDoS attack
        self.blockchain.add_node("Node 1")
        self.blockchain.add_node("Node 2")
        self.blockchain.add_node("Node 3")
        self.blockchain.simulate_ddos_attack()  # Placeholder for actual DDoS simulation

        # Mock the sharding method
        self.blockchain.shard_network = MagicMock()

        # Detect the attack
        anomalies = [{'type': 'attack', 'attack_type': 'DDoS'}]
        self.self_healing_fabric.handle_anomalies(anomalies)

        # Check if the network was sharded
        self.blockchain.shard_network.assert_called_once()

if __name__ == "__main__":
    unittest.main()
