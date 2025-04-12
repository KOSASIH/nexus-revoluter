import time
import yaml
import logging
from npas.api.pi_network_client import PiNetworkClient
from npas.api.nexus_client import NexusClient
from npas.core.ai_analyzer import AIAnalyzer
from npas.core.blockchain_verifier import BlockchainVerifier
from npas.utils.logger import setup_logger
from npas.utils.metrics_collector import MetricsCollector

class NexusPiSynchronizer:
    def __init__(self, config_path="npas/config/settings.yaml"):
        self.logger = setup_logger("NexusPiSynchronizer")
        self.metrics = MetricsCollector()
        self.load_config(config_path)
        
        self.pi_client = PiNetworkClient(self.config["pi_network"])
        self.nexus_client = NexusClient(self.config["nexus_revoluter"])
        self.ai_analyzer = AIAnalyzer()
        self.blockchain_verifier = BlockchainVerifier(self.config["blockchain"])
    
    def load_config(self, config_path):
        """Load configuration from a YAML file."""
        try:
            with open(config_path, "r") as f:
                self.config = yaml.safe_load(f)
            self.logger.info("Configuration loaded successfully.")
        except Exception as e:
            self.logger.error(f"Failed to load configuration: {e}")
            raise

    def sync_cycle(self):
        """Run a synchronization cycle."""
        self.logger.info("Starting synchronization cycle...")
        try:
            # Step 1: Fetch changes from nexus-revoluter
            nexus_changes = self.nexus_client.get_changes()
            self.metrics.record("nexus_changes_detected", len(nexus_changes))
            self.logger.info(f"Detected {len(nexus_changes)} changes from Nexus.")

            # Step 2: Analyze changes with AI
            issues = self.ai_analyzer.predict_issues(nexus_changes)
            if issues:
                self.logger.warning(f"Potential issues detected: {issues}")
                self.metrics.record("issues_predicted", len(issues))
                return
            
            # Step 3: Synchronize changes to Pi Network
            for change in nexus_changes:
                self.pi_client.apply_change(change)
                self.logger.info(f"Change synchronized: {change['id']}")
                self.metrics.record("changes_synced", 1)
                
                # Step 4: Verify on blockchain
                tx_hash = self.blockchain_verifier.record_sync(change)
                self.logger.info(f"Blockchain verification successful: {tx_hash}")
            
            self.logger.info("Synchronization cycle completed successfully.")
        except Exception as e:
            self.logger.error(f"Error during synchronization: {e}")
            self.metrics.record("sync_errors", 1)

    def run(self, interval=60):
        """Run NPAS continuously."""
        self.logger.info("NPAS started...")
        while True:
            try:
                self.sync_cycle()
                self.metrics.report()
                time.sleep(interval)
            except KeyboardInterrupt:
                self.logger.info("NPAS stopped by user.")
                break
            except Exception as e:
                self.logger.error(f"Unexpected error: {e}")
                self.metrics.record("unexpected_errors", 1)
                time.sleep(interval)  # Wait before retrying

if __name__ == "__main__":
    try:
        synchronizer = NexusPiSynchronizer()
        synchronizer.run()
    except Exception as e:
        logging.error(f"Failed to start NexusPiSynchronizer: {e}")
