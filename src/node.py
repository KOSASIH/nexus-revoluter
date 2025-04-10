import socket
import threading
import json
import logging
import time
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Node:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.peers: List[str] = []  # List of peer nodes
        self.transactions: List[Dict[str, Any]] = []  # Transaction pool
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        logging.info(f"Node started at {self.host}:{self.port}")

    def start(self):
        """Start the node and listen for incoming connections."""
        threading.Thread(target=self.accept_connections, daemon=True).start()
        logging.info("Node is listening for connections...")

    def accept_connections(self):
        """Accept incoming connections from peers."""
        while True:
            try:
                client_socket, address = self.server_socket.accept()
                logging.info(f"Connection from {address} has been established.")
                threading.Thread(target=self.handle_client, args=(client_socket,), daemon=True).start()
            except Exception as e:
                logging.error(f"Error accepting connections: {e}")

    def handle_client(self, client_socket: socket.socket):
        """Handle communication with a connected peer."""
        while True:
            try:
                message = client_socket.recv(1024).decode()
                if not message:
                    break
                self.process_message(message)
            except Exception as e:
                logging.error(f"Error handling client: {e}")
                break
        client_socket.close()

    def process_message(self, message: str):
        """Process incoming messages from peers."""
        try:
            data = json.loads(message)
            message_type = data.get('type')
            if message_type == 'peer_discovery':
                self.add_peer(data['peer'])
            elif message_type == 'transaction':
                self.handle_transaction(data['transaction'])
            elif message_type == 'broadcast':
                self.handle_broadcast(data['message'])
            elif message_type == 'request_transactions':
                self.send_transactions(data['peer'])
            else:
                logging.warning(f"Unknown message type: {message_type}")
        except json.JSONDecodeError:
            logging.error("Received invalid JSON message.")
        except KeyError as e:
            logging.error(f"Received message with missing field: {e}")

    def add_peer(self, peer: str):
        """Add a new peer to the list of peers."""
        if peer not in self.peers:
            self.peers.append(peer)
            logging.info(f"Added new peer: {peer}")
            self.broadcast_peer_discovery(peer)

    def broadcast_peer_discovery(self, peer: str):
        """Broadcast the new peer discovery to existing peers."""
        message = json.dumps({"type": "peer_discovery", "peer": peer})
        self.broadcast(message)

    def handle_transaction(self, transaction: Dict[str, Any]):
        """Handle a new transaction received from a peer."""
        if self.validate_transaction(transaction):
            self.transactions.append(transaction)
            logging.info(f"Received and validated transaction: {transaction}")
            self.broadcast_transaction(transaction)
        else:
            logging.warning(f"Invalid transaction received: {transaction}")

    def validate_transaction(self, transaction: Dict[str, Any]) -> bool:
        """Validate the transaction (placeholder for actual validation logic)."""
        # Implement your validation logic here
        return True

    def broadcast_transaction(self, transaction: Dict[str, Any]):
        """Broadcast a new transaction to all peers."""
        message = json.dumps({"type": "transaction", "transaction": transaction})
        self.broadcast(message)

    def handle_broadcast(self, message: str):
        """Handle a broadcast message from a peer."""
        logging.info(f"Broadcast message received: {message}")

    def send_transactions(self, peer: str):
        """Send the current transaction pool to a peer."""
        message = json.dumps({"type": "transaction_pool", "transactions": self.transactions})
        self.send_message(peer, message)

    def broadcast(self, message: str):
        """Broadcast a message to all connected peers."""
        for peer in self.peers:
            self.send_message(peer, message)

    def send_message(self, peer: str, message: str):
        """Send a message to a specific peer."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock .connect((peer.split(':')[0], int(peer.split(':')[1])))
                sock.sendall(message.encode())
                logging.info(f"Sent message to {peer}")
        except Exception as e:
            logging.error(f"Could not send message to {peer}: {e}")

    def discover_peers(self, peer_list: List[str]):
        """Discover and add peers from a given list."""
        for peer in peer_list:
            self.add_peer(peer)

    def shutdown(self):
        """Gracefully shut down the node."""
        logging.info("Shutting down the node...")
        self.server_socket.close()

# Example usage
if __name__ == "__main__":
    node = Node(host='127.0.0.1', port=5000)
    node.start()

    # Simulate peer discovery
    node.discover_peers(['127.0.0.1:5001', '127.0.0.1:5002'])

    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)  # Sleep to prevent busy waiting
    except KeyboardInterrupt:
        node.shutdown()
