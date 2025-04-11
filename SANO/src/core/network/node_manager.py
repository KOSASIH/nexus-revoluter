import logging
import requests
import time
import json
from collections import defaultdict
from threading import Thread

class NodeManager:
    def __init__(self):
        self.logger = logging.getLogger("NodeManager")
        self.nodes = {}  # Dictionary to hold node information
        self.health_status = defaultdict(lambda: {"status": "unknown", "last_checked": None})
        self.load_balancer = LoadBalancer(self)

    def register_node(self, node_url):
        """Register a new node in the network."""
        if node_url not in self.nodes:
            self.nodes[node_url] = {"url": node_url, "load": 0}
            self.logger.info(f"Node registered: {node_url}")
        else:
            self.logger.warning(f"Node {node_url} is already registered.")

    def deregister_node(self, node_url):
        """Deregister a node from the network."""
        if node_url in self.nodes:
            del self.nodes[node_url]
            self.logger.info(f"Node deregistered: {node_url}")
        else:
            self.logger.warning(f"Node {node_url} is not registered.")

    def monitor_nodes(self, interval=60):
        """Continuously monitor the health of nodes."""
        while True:
            for node_url in self.nodes:
                self.check_node_health(node_url)
            time.sleep(interval)

    def check_node_health(self, node_url):
        """Check the health of a node."""
        try:
            response = requests.get(f"{node_url}/health")
            response.raise_for_status()
            health_data = response.json()
            self.health_status[node_url]["status"] = health_data.get("status", "unknown")
            self.health_status[node_url]["last_checked"] = time.time()
            self.logger.info(f"Node {node_url} health status: {self.health_status[node_url]['status']}")
        except Exception as e:
            self.health_status[node_url]["status"] = "down"
            self.logger.error(f"Node {node_url} is down: {e}")

    def get_health_report(self):
        """Get a report of the health status of all nodes."""
        return self.health_status

    def distribute_load(self, request_data):
        """Distribute requests among nodes based on their current load and health status."""
        node_url = self.load_balancer.get_best_node()
        if node_url:
            try:
                response = requests.post(f"{node_url}/process", json=request_data)
                return response.json()
            except Exception as e:
                self.logger.error(f"Failed to process request on node {node_url}: {e}")
                return None
        else:
            self.logger.error("No available nodes to process the request.")
            return None

class LoadBalancer:
    def __init__(self, node_manager):
        self.node_manager = node_manager

    def get_best_node(self):
        """Select the best node based on health and load."""
        available_nodes = [
            node for node, status in self.node_manager.health_status.items()
            if status["status"] == "healthy"
        ]
        if not available_nodes:
            return None
        # Sort nodes by load (ascending)
        available_nodes.sort(key=lambda node: self.node_manager.nodes[node]["load"])
        return available_nodes[0]

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    node_manager = NodeManager()

    # Start monitoring nodes in a separate thread
    monitor_thread = Thread(target=node_manager.monitor_nodes, daemon=True)
    monitor_thread.start()

    # Example usage
    node_manager.register_node("http://localhost:5000")
    node_manager.register_node("http://localhost:6000")

    # Simulate a request distribution
    request_data = {"data": "example"}
    response = node_manager.distribute_load(request_data)
    print(f"Response from node: {response}")

    # Get health report
    health_report = node_manager.get_health_report()
    print(f"Health Report: {health_report}")
