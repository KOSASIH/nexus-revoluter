import unittest
from unittest.mock import patch, MagicMock
from satellite_value_network import SatelliteValueNetwork

class TestSatelliteValueNetwork(unittest.TestCase):

    @patch('satellite_value_network.NodeManager')
    @patch('satellite_value_network.QuantumCrypto')
    @patch('satellite_value_network.NotificationManager')
    def setUp(self, mock_notification_manager, mock_quantum_crypto, mock_node_manager):
        # Mock the managers
        self.mock_node_manager = mock_node_manager.return_value
        self.mock_quantum_crypto = mock_quantum_crypto.return_value
        self.mock_notification_manager = mock_notification_manager.return_value

        # Initialize the SatelliteValueNetwork class
        self.satellite_network = SatelliteValueNetwork()

    def test_broadcast_value(self):
        # Mock the nodes and encryption
        self.mock_node_manager.get_all_nodes.return_value = [
            {'id': 'node1', 'user_id': 'user1'},
            {'id': 'node2', 'user_id': 'user2'}
        ]
        self.mock_quantum_crypto.encrypt.return_value = 'encrypted_value'

        # Call broadcast_value
        self.satellite_network.broadcast_value()

        # Check that the value was encrypted
        self.mock_quantum_crypto.encrypt.assert_called_once_with(str(self.satellite_network.target_value))

        # Check that the value was sent to all nodes
        self.mock_notification_manager.send_notification.assert_any_call('user1', 'New Pi Coin value: 314159.0')
        self.mock_notification_manager.send_notification.assert_any_call('user2', 'New Pi Coin value: 314159.0')

    def test_send_value_to_node(self):
        # Mock the notification sending
        self.mock_notification_manager.send_notification = MagicMock()

        # Call send_value_to_node
        self.satellite_network.send_value_to_node({'id': 'node1', 'user_id': 'user1'}, 'encrypted_value')

        # Check that the notification was sent
        self.mock_notification_manager.send_notification.assert_called_once_with('user1', 'New Pi Coin value: 314159.0')

if __name__ == '__main__':
    unittest.main()
