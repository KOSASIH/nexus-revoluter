import logging
import requests
import time
import numpy as np
from collections import defaultdict
from threading import Thread

class LatencyOptimizer:
    def __init__(self, nodes=None):
        self.logger = logging.getLogger("LatencyOptimizer")
        self.nodes = nodes if nodes else []
        self.latency_data = defaultdict(list)  # Store latency measurements
        self.alert_threshold = 200  # Threshold in milliseconds for alerts
        self.running = True

    def start(self):
        """Start the latency optimization process."""
        self.logger.info("Starting Latency Optimizer...")
        Thread(target=self.measure_latency, daemon=True).start()
        Thread(target=self.optimize_routing, daemon=True).start()

    def stop(self):
        """Stop the latency optimization process."""
        self.running = False
        self.logger.info("Stopping Latency Optimizer...")

    def measure_latency(self):
        """Measure latency to each node in the network."""
        while self.running:
            for node in self.nodes:
                latency = self.ping_node(node)
                if latency is not None:
                    self.latency_data[node].append(latency)
                    self.logger.info(f"Measured latency for {node}: {latency} ms")
                    self.check_alerts(node, latency)
            time.sleep(10)  # Measurement interval

    def ping_node(self, node):
        """Ping a node and return the latency in milliseconds."""
        try:
            start_time = time.time()
            response = requests.get(f"{node}/ping", timeout=2)
            response.raise_for_status()
            latency = (time.time() - start_time) * 1000  # Convert to milliseconds
            return latency
        except Exception as e:
            self.logger.error(f"Failed to ping {node}: {e}")
            return None

    def check_alerts(self, node, latency):
        """Check if latency exceeds the alert threshold."""
        if latency > self.alert_threshold:
            self.logger.warning(f"High latency alert for {node}: {latency} ms")

    def optimize_routing(self):
        """Optimize data routing based on latency measurements."""
        while self.running:
            for node in self.nodes:
                if self.latency_data[node]:
                    avg_latency = np.mean(self.latency_data[node])
                    self.logger.info(f"Average latency for {node}: {avg_latency:.2f} ms")
                    # Implement routing logic based on average latency
                    # For example, update routing tables or notify other components
            time.sleep(30)  # Optimization interval

    def add_node(self, node):
        """Add a new node to the optimization process."""
        if node not in self.nodes:
            self.nodes.append(node)
            self.logger.info(f"Node added for latency optimization: {node}")

    def remove_node(self, node):
        """Remove a node from the optimization process."""
        if node in self.nodes:
            self.nodes.remove(node)
            self.logger.info(f"Node removed from latency optimization: {node}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    nodes = ["http://localhost:5000", "http://localhost:6000"]  # Example nodes
    latency_optimizer = LatencyOptimizer(nodes)

    # Start the latency optimization process
    latency_optimizer.start()

    # Example usage
    time.sleep(60)  # Let the optimizer run for a while

    # Stop the latency optimization process
    latency_optimizer.stop()
