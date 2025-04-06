import unittest
from unittest.mock import AsyncMock, patch
from main import PiNode  # Assuming your main code is in a file named main.py

class TestPiNode(unittest.TestCase):

    @patch('main.Node')
    @patch('main.API')
    @patch('main.Blockchain')
    @patch('main.TransactionPool')
    @patch('main.Consensus')
    @patch('main.SecurityManager')
    @patch('main.Metrics')
    @patch('main.NotificationService')
    @patch('main.LoadBalancer')
    def setUp(self, MockLoadBalancer, MockNotificationService, MockMetrics, MockSecurityManager,
               MockConsensus, MockTransactionPool, MockBlockchain, MockAPI, MockNode):
        """Set up the PiNode instance for testing."""
        self.node = PiNode()
        self.node.node = MockNode.return_value
        self.node.api = MockAPI.return_value
        self.node.blockchain = MockBlockchain.return_value
        self.node.transaction_pool = MockTransactionPool.return_value
        self.node.consensus = MockConsensus.return_value
        self.node.security_manager = MockSecurityManager.return_value
        self.node.metrics = MockMetrics.return_value
        self.node.notification_service = MockNotificationService.return_value
        self.node.load_balancer = MockLoadBalancer.return_value

    @patch('asyncio.sleep', new_callable=AsyncMock)
    async def test_run_consensus(self, mock_sleep):
        """Test the run_consensus method."""
        self.node.consensus.run = AsyncMock()
        await self.node.run_consensus()
        self.node.consensus.run.assert_called()
        mock_sleep.assert_called()

    @patch('asyncio.sleep', new_callable=AsyncMock)
    async def test_start_services(self, mock_sleep):
        """Test the start_services method."""
        await self.node.start_services()
        self.node.node.start.assert_called()
        self.node.api.start.assert_called()
        self.node.metrics.start_monitoring.assert_called()
        self.node.load_balancer.start.assert_called()

    @patch('asyncio.sleep', new_callable=AsyncMock)
    async def test_shutdown(self, mock_sleep):
        """Test the shutdown method."""
        await self.node.shutdown()
        self.node.node.stop.assert_called()
        self.node.api.stop.assert_called()
        self.node.metrics.stop_monitoring.assert_called()
        self.node.load_balancer.stop.assert_called()
        self.node.notification_service.send_alert.assert_called_with("Pi Node has been shut down.")

    @patch('asyncio.run', new_callable=AsyncMock)
    async def test_main(self, mock_run):
        """Test the main method."""
        await self.node.main()
        self.node.start_services.assert_called()
        self.node.run_consensus.assert_called()

if __name__ == '__main__':
    unittest.main()
