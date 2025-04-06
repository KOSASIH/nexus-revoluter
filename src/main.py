import logging
import time
import asyncio
from config import Config
from blockchain import Blockchain
from node import Node
from transaction import TransactionPool
from api import API
from consensus import Consensus
from security import SecurityManager  # New security module
from metrics import Metrics  # New metrics module
from notifications import NotificationService  # New notification service
from load_balancer import LoadBalancer  # New load balancer module

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PiNode:
    def __init__(self):
        self.config = Config()
        self.blockchain = Blockchain()
        self.node = Node(self.config)
        self.transaction_pool = TransactionPool()
        self.api = API(self.config, self.blockchain, self.transaction_pool)
        self.consensus = Consensus(self.blockchain)
        self.security_manager = SecurityManager(self.config)  # Initialize security manager
        self.metrics = Metrics()  # Initialize metrics tracking
        self.notification_service = NotificationService()  # Initialize notification service
        self.load_balancer = LoadBalancer(self.node)  # Initialize load balancer

    async def run_consensus(self):
        """Run the consensus algorithm in an asynchronous loop."""
        while True:
            try:
                await self.consensus.run()  # Run the consensus algorithm
                self.metrics.record_consensus_run()  # Record metrics
                await asyncio.sleep(self.config.CONSENSUS_INTERVAL)  # Wait before the next consensus round
            except Exception as e:
                logger.error(f"Error during consensus: {e}")
                self.notification_service.send_alert(f"Consensus error: {e}")  # Send alert on error

    async def start_services(self):
        """Start the node and API services asynchronously."""
        await self.node.start()  # Start the node's networking capabilities
        await self.api.start()   # Start the API server
        self.metrics.start_monitoring()  # Start metrics monitoring
        self.load_balancer.start()  # Start load balancing

    async def shutdown(self):
        """Gracefully shut down the node and API services."""
        logger.info("Shutting down Pi Node...")
        await self.node.stop()
        await self.api.stop()
        self.metrics.stop_monitoring()  # Stop metrics monitoring
        self.load_balancer.stop()  # Stop load balancing
        self.notification_service.send_alert("Pi Node has been shut down.")  # Notify shutdown

    async def main(self):
        """Main entry point for the Pi Node."""
        logger.info("Starting Pi Node...")
        await self.start_services()  # Start services

        try:
            await self.run_consensus()  # Run consensus in the main loop
        except KeyboardInterrupt:
            await self.shutdown()  # Handle shutdown on keyboard interrupt
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            await self.shutdown()

if __name__ == "__main__":
    pi_node = PiNode()
    asyncio.run(pi_node.main())  # Run the main function using asyncio
