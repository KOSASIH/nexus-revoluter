import socket
import threading
import json
import logging
import time
import hashlib
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Block:
    def __init__(self, index: int, previous_hash: str, transactions: List[Dict[str, Any]], timestamp: float, nonce: int = 0):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.timestamp = timestamp
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        block_string = json.dumps(self.__dict__, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def mine_block(self, difficulty: int):
        """Mine a block by finding a hash that starts with a number of zeros equal to the difficulty."""
        prefix_str = '0' * difficulty
        while not self.hash.startswith(prefix_str):
            self.nonce += 1
            self.hash = self.calculate_hash()
        logging.info(f"Block mined: {self.hash}")

class Node:
    def __init__(self, host: str, port: int, difficulty: int = 2):
        self.host = host
        self.port = port
        self.difficulty = difficulty
        self.peers: List[str] = []  # List of peer nodes
        self.transactions: List[Dict[str, Any]] = []  # Transaction pool
        self.chain: List[Block] = []  # Blockchain
        self.create_genesis_block()  # Create the genesis block
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        logging.info(f"Node started at {self.host}:{self.port}")

    def create_genesis_block(self):
        """Create the first block in the blockchain."""
        genesis_block = Block(0, "0", [], time.time())
        self.chain.append(genesis_block)
        logging.info("Genesis block created.")

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
            elif message_type == 'block':
                self.handle_block(data['block'])
            elif message_type == 'request_chain':
                self.send_chain(data['peer'])
            else:
                logging.warning(f"Unknown message type: {message_type}")
        except json.JSONDecodeError:
            logging.error("Received invalid JSON message.")
        except KeyError as e:
            logging.error(f"Received message with missing field: {e}")

    def add_peer(self, peer: str):
        """Add a new peer to the list of peers."""
        if peer not in self.peers :
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

    def handle_block(self, block: Dict[str, Any]):
        """Handle a new block received from a peer."""
        if self.validate_block(block):
            self.chain.append(Block(**block))
            logging.info(f"New block added to the chain: {block}")
        else:
            logging.warning(f"Invalid block received: {block}")

    def validate_block(self, block: Dict[str, Any]) -> bool:
        """Validate the block (placeholder for actual validation logic)."""
        # Implement your validation logic here
        return True

    def send_chain(self, peer: str):
        """Send the current blockchain to a peer."""
        message = json.dumps({"type": "blockchain", "chain": [block.__dict__ for block in self.chain]})
        self.send_message(peer, message)

    def broadcast(self, message: str):
        """Broadcast a message to all connected peers."""
        for peer in self.peers:
            self.send_message(peer, message)

    def send_message(self, peer: str, message: str):
        """Send a message to a specific peer."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((peer.split(':')[0], int(peer.split(':')[1])))
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

    def mine_pending_transactions(self):
        """Mine all pending transactions and create a new block."""
        if not self.transactions:
            logging.info("No transactions to mine.")
            return
        new_block = Block(len(self.chain), self.chain[-1].hash, self.transactions, time.time())
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        self.transactions = []  # Clear the transaction pool
        logging.info(f"New block mined and added to the chain: {new_block.hash}")

# Example usage
if __name__ == "__main__":
    node = Node(host='127.0.0.1', port=5000, difficulty=2)
    node.start()

    # Simulate peer discovery
    node.discover_peers(['127.0.0.1:5001', '127.0.0.1:5002'])

    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)  # Sleep to prevent busy waiting
    except KeyboardInterrupt:
        node.shutdown()
