import unittest
from unittest.mock import patch, MagicMock
import socket
import json
from node import Node  # Assuming your Node class is in a file named node.py

class TestNode(unittest.TestCase):
    def setUp(self):
        """Set up a new Node instance for testing."""
        self.node = Node(host='127.0.0.1', port=5000)
        self.node.start()

    def test_initialization(self):
        """Test the initialization of the Node."""
        self.assertEqual(self.node.host, '127.0.0.1')
        self.assertEqual(self.node.port, 5000)
        self.assertEqual(len(self.node.peers), 0)

    @patch('socket.socket')
    def test_accept_connections(self, mock_socket):
        """Test that the node accepts incoming connections."""
        mock_client_socket = MagicMock()
        mock_socket.return_value.accept.return_value = (mock_client_socket, ('127.0.0.1', 5001))
        
        # Simulate accepting a connection
        self.node.accept_connections()
        mock_socket.return_value.accept.assert_called_once()
        mock_client_socket.recv.assert_called()

    @patch('socket.socket')
    def test_process_message_peer_discovery(self, mock_socket):
        """Test processing a peer discovery message."""
        message = json.dumps({"type": "peer_discovery", "peer": "127.0.0.1:5001"})
        self.node.process_message(message)
        self.assertIn("127.0.0.1:5001", self.node.peers)

    @patch('socket.socket')
    def test_process_message_transaction(self, mock_socket):
        """Test processing a transaction message."""
        transaction = {"type": "transaction", "transaction": {"sender": "Alice", "recipient": "Bob", "amount": 10.0}}
        with patch('logging.info') as mock_logging:
            self.node.process_message(json.dumps(transaction))
            mock_logging.assert_called_with(f"Received transaction: {transaction['transaction']}")

    @patch('socket.socket')
    def test_process_message_broadcast(self, mock_socket):
        """Test processing a broadcast message."""
        message = json.dumps({"type": "broadcast", "message": "Hello, peers!"})
        with patch('logging.info') as mock_logging:
            self.node.process_message(message)
            mock_logging.assert_called_with("Broadcast message received: Hello, peers!")

    @patch('socket.socket')
    def test_broadcast(self, mock_socket):
        """Test broadcasting a message to peers."""
        self.node.peers = ["127.0.0.1:5001"]
        message = json.dumps({"type": "broadcast", "message": "Test broadcast"})
        
        with patch('socket.socket.connect') as mock_connect, patch('socket.socket.sendall') as mock_sendall:
            self.node.broadcast(message)
            mock_connect.assert_called_once_with(('127.0.0.1', 5001))
            mock_sendall.assert_called_once_with(message.encode())

    @patch('socket.socket')
    def test_shutdown(self, mock_socket):
        """Test shutting down the node."""
        with patch('logging.info') as mock_logging:
            self.node.shutdown()
            mock_logging.assert_called_with("Shutting down the node...")
            self.assertRaises(OSError, self.node.server_socket.accept)

if __name__ == '__main__':
    unittest.main()
