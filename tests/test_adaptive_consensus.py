import unittest
from unittest.mock import patch
import random

# Assuming the AdaptiveConsensus class is defined in a module named adaptive_consensus
from adaptive_consensus import AdaptiveConsensus

class TestAdaptiveConsensus(unittest.TestCase):
    def setUp(self):
        """Set up a new AdaptiveConsensus instance for testing."""
        self.consensus = AdaptiveConsensus()

    @patch('adaptive_consensus.random.randint')
    @patch('adaptive_consensus.random.uniform')
    def test_adjust_consensus_mechanism(self, mock_uniform, mock_randint):
        """Test the adjustment of the consensus mechanism based on network conditions."""
        
        # Test case 1: High congestion
        mock_randint.return_value = 150  # Simulated latency
        mock_uniform.side_effect = [0, 500, 80]  # Simulated throughput, error rate, congestion
        self.consensus.evaluate_network_conditions()
        self.assertEqual(self.consensus.get_current_mechanism(), "Proof of Authority")

        # Test case 2: High error rate
        mock_randint.return_value = 100  # Simulated latency
        mock_uniform.side_effect = [0, 500, 3]  # Simulated throughput, error rate, congestion
        self.consensus.evaluate_network_conditions()
        self.assertEqual(self.consensus.get_current_mechanism(), "Delegated Proof of Stake")

        # Test case 3: Normal conditions
        mock_randint.return_value = 50  # Simulated latency
        mock_uniform.side_effect = [0, 500, 1]  # Simulated throughput, error rate, congestion
        self.consensus.evaluate_network_conditions()
        self.assertEqual(self.consensus.get_current_mechanism(), "Proof of Stake")

    @patch('adaptive_consensus.random.randint')
    @patch('adaptive_consensus.random.uniform')
    def test_monitor_network_conditions(self, mock_uniform, mock_randint):
        """Test the monitoring of network conditions."""
        mock_randint.return_value = 100  # Simulated latency
        mock_uniform.side_effect = [0, 2, 30]  # Simulated throughput, error rate, congestion

        self.consensus.monitor_network_conditions()
        
        # Check if network conditions are updated
        self.assertEqual(self.consensus.network_conditions["latency"], 100)
        self.assertEqual(self.consensus.network_conditions["throughput"], 0)
        self.assertEqual(self.consensus.network_conditions["error_rate"], 2)
        self.assertEqual(self.consensus.network_conditions["congestion"], 30)

if __name__ == '__main__':
    unittest.main()
