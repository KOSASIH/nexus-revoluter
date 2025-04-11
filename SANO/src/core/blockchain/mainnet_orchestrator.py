import requests
import logging
import time
import json
import yaml

class MainnetOrchestrator:
    def __init__(self, config_path):
        self.logger = logging.getLogger("MainnetOrchestrator")
        self.config = self.load_config(config_path)
        self.nodes = self.config['network']['nodes']
        self.blockchain_data = []
        self.current_block = None

    def load_config(self, config_path):
        """Load configuration settings from a YAML file."""
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)

    def register_node(self, node_url):
        """Register a new node in the network."""
        if node_url not in self.nodes:
            self.nodes.append(node_url)
            self.logger.info(f"Node registered: {node_url}")
        else:
            self.logger.warning(f"Node {node_url} is already registered.")

    def synchronize_nodes(self):
        """Synchronize all nodes with the latest blockchain data."""
        for node in self.nodes:
            try:
                response = requests.get(f"{node}/blockchain")
                response.raise_for_status()
                node_data = response.json()
                self.update_blockchain(node_data)
                self.logger.info(f"Synchronized with node: {node}")
            except Exception as e:
                self.logger.error(f"Failed to synchronize with node {node}: {e}")

    def update_blockchain(self, node_data):
        """Update the local blockchain data with data from a node."""
        if node_data['blocks']:
            latest_block = node_data['blocks'][-1]
            if not self.current_block or latest_block['index'] > self.current_block['index']:
                self.current_block = latest_block
                self.blockchain_data.extend(node_data['blocks'])
                self.logger.info(f"Updated blockchain with latest block: {latest_block['index']}")

    def deploy_smart_contract(self, contract_data):
        """Deploy a smart contract to the mainnet."""
        for node in self.nodes:
            try:
                response = requests.post(f"{node}/deploy", json=contract_data)
                response.raise_for_status()
                self.logger.info(f"Smart contract deployed on node: {node}")
            except Exception as e:
                self.logger.error(f"Failed to deploy smart contract on node {node}: {e}")

    def monitor_network(self):
        """Monitor the health of the network and log any issues."""
        while True:
            for node in self.nodes:
                try:
                    response = requests.get(f"{node}/health")
                    response.raise_for_status()
                    health_status = response.json()
                    self.logger.info(f"Node {node} health status: {health_status['status']}")
                except Exception as e:
                    self.logger.error(f"Node {node} is down: {e}")
            time.sleep(self.config['network']['monitor_interval'])

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    orchestrator = MainnetOrchestrator("src/config/settings.yaml")

    # Example usage
    orchestrator.register_node("http://localhost:5000")
    orchestrator.synchronize_nodes()
    orchestrator.deploy_smart_contract({
        "name": "ExampleContract",
        "code": "contract code here"
    })
    orchestrator.monitor_network()
