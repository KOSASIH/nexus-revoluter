import unittest
from unittest.mock import patch, MagicMock
import logging
import yaml
from npas.core.synchronizer import NexusPiSynchronizer

class TestNexusPiSynchronizer(unittest.TestCase):
    @patch('npas.core.synchronizer.PiNetworkClient')
    @patch('npas.core.synchronizer.NexusClient')
    @patch('npas.core.synchronizer.AIAnalyzer')
    @patch('npas.core.synchronizer.BlockchainVerifier')
    @patch('npas.utils.metrics_collector.MetricsCollector')
    @patch('npas.utils.logger.setup_logger')
    def setUp(self, mock_setup_logger, mock_metrics_collector, mock_blockchain_verifier, 
              mock_ai_analyzer, mock_nexus_client, mock_pi_network_client):
        # Mock the logger
        self.mock_logger = MagicMock()
        mock_setup_logger.return_value = self.mock_logger
        
        # Mock the metrics collector
        self.mock_metrics = MagicMock()
        mock_metrics_collector.return_value = self.mock_metrics
        
        # Mock the clients and analyzer
        self.mock_pi_client = MagicMock()
        mock_pi_network_client.return_value = self.mock_pi_client
        
        self.mock_nexus_client = MagicMock()
        mock_nexus_client.return_value = self.mock_nexus_client
        
        self.mock_ai_analyzer = MagicMock()
        mock_ai_analyzer.return_value = self.mock_ai_analyzer
        
        self.mock_blockchain_verifier = MagicMock()
        mock_blockchain_verifier.return_value = self.mock_blockchain_verifier
        
        # Create an instance of NexusPiSynchronizer
        self.synchronizer = NexusPiSynchronizer(config_path="npas/config/settings.yaml")

    def test_load_config_success(self):
        """Test successful loading of configuration."""
        self.assertIsNotNone(self.synchronizer.config)
        self.mock_logger.info.assert_called_with("Configuration loaded successfully.")

    @patch('npas.core.synchronizer.NexusClient.get_changes')
    @patch('npas.core.synchronizer.AIAnalyzer.predict_issues')
    @patch('npas.core.synchronizer.PiNetworkClient.apply_change')
    @patch('npas.core.synchronizer.BlockchainVerifier.record_sync')
    def test_sync_cycle_success(self, mock_record_sync, mock_apply_change, mock_predict_issues, mock_get_changes):
        """Test successful synchronization cycle."""
        # Mock the return values
        mock_get_changes.return_value = [{'id': '1', 'content': 'Update code', 'timestamp': 1234567890}]
        mock_predict_issues.return_value = []
        mock_record_sync.return_value = '0x1234567890abcdef'

        self.synchronizer.sync_cycle()

        self.assertEqual(self.mock_nexus_client.get_changes.call_count, 1)
        self.assertEqual(mock_apply_change.call_count, 1)
        self.assertEqual(mock_record_sync.call_count, 1)
        self.mock_logger.info.assert_any_call("Detected 1 changes from Nexus.")
        self.mock_logger.info.assert_any_call("Change synchronized: 1")
        self.mock_logger.info.assert_any_call("Blockchain verification successful: 0x1234567890abcdef")

    @patch('npas.core.synchronizer.NexusClient.get_changes')
    @patch('npas.core.synchronizer.AIAnalyzer.predict_issues')
    def test_sync_cycle_with_issues(self, mock_predict_issues, mock_get_changes):
        """Test synchronization cycle when issues are predicted."""
        # Mock the return values
        mock_get_changes.return_value = [{'id': '1', 'content': 'Update code', 'timestamp': 1234567890}]
        mock_predict_issues.return_value = ['Issue detected']

        self.synchronizer.sync_cycle()

        self.assertEqual(self.mock_nexus_client.get_changes.call_count, 1)
        self.assertEqual(mock_predict_issues.call_count, 1)
        self.mock_logger.warning.assert_called_with("Potential issues detected: ['Issue detected']")

    def test_run_with_keyboard_interrupt(self):
        """Test run method handles KeyboardInterrupt gracefully."""
        with patch('time.sleep', return_value=None):  # Mock sleep to avoid delays
            with self.assertRaises(KeyboardInterrupt):
                self.synchronizer.run(interval=0)  # Set interval to 0 for immediate exit

    @patch('npas.core.synchronizer.NexusClient.get_changes')
    def test_sync_cycle_error_handling(self, mock_get_changes):
        """Test error handling during synchronization cycle."""
        # Mock the return value to raise an exception
        mock_get_changes.side_effect = Exception("Network error")

        self.synchronizer.sync_cycle()

        self.mock_logger.error.assert_called_with("Error during synchronization: Network error")
        self.mock_metrics.record.assert_called_with("sync_errors", 1)

    @patch('npas.core.synchronizer.NexusClient.get_changes')
    def test_run_unexpected_error_handling(self, mock_get_changes):
        """Test run method handles unexpected errors gracefully."""
        mock_get_changes.side_effect = Exception("Unexpected error")
        
        with patch('time.sleep', return_value=None):  # Mock sleep to avoid delays
            self.synchronizer.run(interval=0)  # Set interval to 0 for immediate exit

        self.mock_logger.error.assert_called_with("Unexpected error: Unexpected error")
        self.mock_metrics.record.assert_called_with("unexpected_errors", 1)

if __name__ == "__main__":
    unittest.main()
