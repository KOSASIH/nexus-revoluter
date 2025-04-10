# test_network_monitor.py

import unittest
from monitoring import NetworkMonitor

class TestNetworkMonitor(unittest.TestCase):
    def setUp(self):
        self.network_monitor = NetworkMonitor()

    def test_get_network_status(self):
        """Test retrieving network status."""
        status = self.network_monitor.get_network_status()
        self.assertIn('transactions', status)
        self.assertIn('nodes', status)
        self.assertIn('liquidity', status)
        print("Network status test passed.")

if __name__ == "__main__":
    unittest.main()
