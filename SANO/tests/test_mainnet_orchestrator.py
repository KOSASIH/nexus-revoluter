import unittest
from unittest.mock import patch, MagicMock
import logging
import json
import yaml
from mainnet_orchestrator import MainnetOrchestrator  # Assuming the class is in mainnet_orchestrator.py

class TestMainnetOrchestrator(unittest.TestCase):
    def setUp(self):
        """Set up the MainnetOrchestrator instance for testing."""
        self.config_path = "test_config.yaml"
        self.test_config = {
            'network': {
                'nodes': ['http://localhost:5000'],
                'monitor_interval': 5
            }
        }
        with open(self.config_path, 'w') as f:
            yaml.dump(self.test_config, f)

        self.orchestrator = MainnetOrchestrator(self.config_path)

    def tearDown(self):
        """Clean up after tests."""
        import os
        os.remove(self.config_path)

    @patch('requests.get')
    def test_synchronize_nodes(self, mock_get):
        """Test the synchronization of nodes."""
        mock_get.return_value = MagicMock(status_code=200)
        mock_get.return_value.json.return_value = {
            'blocks': [{'index': 1, 'data': 'block data'}]
        }

        self.orchestrator.synchronize_nodes()
        self.assertEqual(len(self.orchestrator.blockchain_data), 1)
        self.assertEqual(self.orchestrator.current_block['index'], 1)

    @patch('requests.get')
    def test_synchronize_nodes_failure(self, mock_get):
        """Test synchronization failure handling."""
        mock_get.side_effect = Exception("Connection error")
        with self.assertLogs(self.orchestrator.logger, level='ERROR') as log:
            self.orchestrator.synchronize_nodes()
            self.assertIn("Failed to synchronize with node http://localhost:5000: Connection error", log.output[0])

    def test_register_node(self):
        """Test registering a new node."""
        new_node = "http://localhost:6000"
        self.orchestrator.register_node(new_node)
        self.assertIn(new_node, self.orchestrator.nodes)

    def test_register_existing_node(self):
        """Test registering an existing node."""
        with self.assertLogs(self.orchestrator.logger, level='WARNING') as log:
            self.orchestrator.register_node("http://localhost:5000")
            self.assertIn("Node http://localhost:5000 is already registered.", log.output[0])

    @patch('requests.post')
    def test_deploy_smart_contract(self, mock_post):
        """Test deploying a smart contract."""
        mock_post.return_value = MagicMock(status_code=200)

        contract_data = {
            "name": "ExampleContract",
            "code": "contract code here"
        }
        self.orchestrator.deploy_smart_contract(contract_data)
        self.assertTrue(mock_post.called)

    @patch('requests.post')
    def test_deploy_smart_contract_failure(self, mock_post):
        """Test smart contract deployment failure handling."""
        mock_post.side_effect = Exception("Deployment error")
        with self.assertLogs(self.orchestrator.logger, level='ERROR') as log:
            self.orchestrator.deploy_smart_contract({"name": "ExampleContract", "code": "contract code here"})
            self.assertIn("Failed to deploy smart contract on node http://localhost:5000: Deployment error", log.output[0])

    @patch('requests.get')
    def test_monitor_network(self, mock_get):
        """Test network monitoring."""
        mock_get.return_value = MagicMock(status_code=200)
        mock_get.return_value.json.return_value = {'status': 'healthy'}

        with patch('time.sleep', return_value=None):  # Mock sleep to avoid delays
            self.orchestrator.monitor_network()
            self.assertTrue(mock_get.called)

    @patch('requests.get')
    def test_monitor_network_failure(self, mock_get):
        """Test network monitoring failure handling."""
        mock_get.side_effect = Exception("Node down")
        with self.assertLogs(self.orchestrator.logger, level='ERROR') as log:
            with patch('time.sleep', return_value=None):  # Mock sleep to avoid delays
                self.orchestrator.monitor_network()
                self.assertIn("Node http://localhost:5000 is down: Node down", log.output[0])

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    unittest.main()
