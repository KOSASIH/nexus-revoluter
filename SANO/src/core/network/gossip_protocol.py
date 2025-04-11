import logging
import json
import random
import time
import hashlib
import requests
from collections import defaultdict
from threading import Thread

class GossipProtocol:
    def __init__(self, node_url, peers=None):
        self.logger = logging.getLogger("GossipProtocol")
        self.node_url = node_url
        self.peers = peers if peers else []
        self.message_queue = defaultdict(list)  # Queue for incoming messages
        self.seen_messages = set()  # Track seen messages to avoid duplicates
        self.running = True

    def start(self):
        """Start the gossip protocol."""
        self.logger.info("Starting Gossip Protocol...")
        Thread(target=self.listen_for_messages, daemon=True).start()
        Thread(target=self.gossip_updates, daemon=True).start()

    def stop(self):
        """Stop the gossip protocol."""
        self.running = False
        self.logger.info("Stopping Gossip Protocol...")

    def listen_for_messages(self):
        """Listen for incoming messages from peers."""
        while self.running:
            for peer in self.peers:
                try:
                    response = requests.get(f"{peer}/gossip")
                    if response.status_code == 200:
                        messages = response.json()
                        self.process_messages(messages)
                except Exception as e:
                    self.logger.error(f"Failed to fetch messages from {peer}: {e}")
            time.sleep(5)  # Polling interval

    def process_messages(self, messages):
        """Process incoming messages."""
        for message in messages:
            message_id = message['id']
            if message_id not in self.seen_messages:
                self.seen_messages.add(message_id)
                self.logger.info(f"Processing message: {message}")
                self.message_queue[message['type']].append(message)
                self.propagate_message(message)

    def propagate_message(self, message):
        """Propagate a message to peers."""
        for peer in self.peers:
            try:
                requests.post(f"{peer}/gossip", json=message)
                self.logger.info(f"Message sent to {peer}: {message}")
            except Exception as e:
                self.logger.error(f"Failed to send message to {peer}: {e}")

    def gossip_updates(self):
        """Periodically send updates to peers."""
        while self.running:
            message = self.create_message("update", {"data": "example update"})
            self.propagate_message(message)
            time.sleep(10)  # Gossip interval

    def create_message(self, message_type, data):
        """Create a new message with a unique ID and signature."""
        message_id = self.generate_message_id(data)
        message = {
            "id": message_id,
            "type": message_type,
            "data": data,
            "sender": self.node_url,
            "timestamp": time.time()
        }
        return message

    def generate_message_id(self, data):
        """Generate a unique message ID based on the data."""
        message_string = json.dumps(data, sort_keys=True).encode()
        return hashlib.sha256(message_string).hexdigest()

    def add_peer(self, peer_url):
        """Add a new peer to the gossip protocol."""
        if peer_url not in self.peers:
            self.peers.append(peer_url)
            self.logger.info(f"Peer added: {peer_url}")

    def remove_peer(self, peer_url):
        """Remove a peer from the gossip protocol."""
        if peer_url in self.peers:
            self.peers.remove(peer_url)
            self.logger.info(f"Peer removed: {peer_url}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    node_url = "http://localhost:5000"  # Example node URL
    gossip_protocol = GossipProtocol(node_url)

    # Start the gossip protocol
    gossip_protocol.start()

    # Example usage
    gossip_protocol.add_peer("http://localhost:6000")
    time.sleep(30)  # Let the protocol run for a while

    # Stop the gossip protocol
    gossip_protocol.stop()
