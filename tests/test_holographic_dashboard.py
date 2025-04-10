# test_holographic_dashboard.py

import unittest
from holo_dashboard import HolographicGlobalDashboard
from unittest.mock import MagicMock

class TestHolographicGlobalDashboard(unittest.TestCase):
    def setUp(self):
        self.dashboard = HolographicGlobalDashboard()
        self.dashboard.network_monitor = MagicMock()
        self.dashboard.ar_vr_integration = MagicMock()

    def test_update_dashboard(self):
        """Test updating the dashboard with network data."""
        self.dashboard.network_monitor.get_network_status.return_value = {
            'transactions': 100,
            'nodes': 10,
            'liquidity': 5000
        }
        self.dashboard.update_dashboard()
        self.dashboard.ar_vr_integration.render_transactions.assert_called_once_with(100)
        self.dashboard.ar_vr_integration.render_nodes.assert_called_once_with(10)
        self.dashboard.ar_vr_integration.render_liquidity.assert_called_once_with(5000)
        print("Dashboard update test passed.")

if __name__ == "__main__":
    unittest.main()
