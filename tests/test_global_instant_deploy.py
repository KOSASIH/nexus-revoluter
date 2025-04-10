# tests/test_global_instant_deploy.py

import unittest
from unittest.mock import patch, MagicMock
import json
import asyncio
from global_instant_deploy import GlobalInstantDeploy

class TestGlobalInstantDeploy(unittest.TestCase):
    def setUp(self):
        # Load a sample configuration
        self.config = {
            'cdn_url': 'http://mock-cdn-url.com/distribute'
        }
        self.deployer = GlobalInstantDeploy(self.config)

    @patch('requests.post')
    async def test_distribute_code_success(self, mock_post):
        # Mock the response of the CDN distribution
        mock_post.return_value = MagicMock(status_code=200)
        
        await self.deployer.distribute_code()
        mock_post.assert_called_once_with(self.config['cdn_url'], json={"code": "mainnet_code"})

    @patch('requests.post')
    async def test_distribute_code_failure(self, mock_post):
        # Mock a failed response from the CDN
        mock_post.side_effect = Exception("CDN error")
        
        with self.assertRaises(Exception):
            await self.deployer.distribute_code()

    @patch('blockchain.Blockchain.sync')
    async def test_sync_blockchain_success(self, mock_sync):
        # Mock the successful blockchain sync
        mock_sync.return_value = None
        
        await self.deployer.sync_blockchain()
        mock_sync.assert_called_once()

    @patch('blockchain.Blockchain.sync')
    async def test_sync_blockchain_failure(self, mock_sync):
        # Mock a failed blockchain sync
        mock_sync.side_effect = Exception("Blockchain sync error")
        
        with self.assertRaises(Exception):
            await self.deployer.sync_blockchain()

    @patch('node.NodeManager.auto_configure_nodes')
    async def test_auto_configure_nodes_success(self, mock_auto_configure):
        # Mock the successful node configuration
        mock_auto_configure.return_value = None
        
        await self.deployer.node_manager.auto_configure_nodes()
        mock_auto_configure.assert_called_once()

    @patch('node.NodeManager.auto_configure_nodes')
    async def test_auto_configure_nodes_failure(self, mock_auto_configure):
        # Mock a failed node configuration
        mock_auto_configure.side_effect = Exception("Node configuration error")
        
        with self.assertRaises(Exception):
            await self.deployer.node_manager.auto_configure_nodes()

    @patch('global_instant_deploy.GlobalInstantDeploy.distribute_code')
    @patch('global_instant_deploy.GlobalInstantDeploy.sync_blockchain')
    @patch('global_instant_deploy.GlobalInstantDeploy.node_manager.auto_configure_nodes')
    async def test_deploy_network_success(self, mock_auto_configure, mock_sync, mock_distribute):
        # Mock all methods to simulate a successful deployment
        mock_distribute.return_value = None
        mock_auto_configure.return_value = None
        mock_sync.return_value = None
        
        await self.deployer.deploy_network()

    @patch('global_instant_deploy.GlobalInstantDeploy.distribute_code')
    @patch('global_instant_deploy.GlobalInstantDeploy.sync_blockchain')
    @patch('global_instant_deploy.GlobalInstantDeploy.node_manager.auto_configure_nodes')
    async def test_deploy_network_failure(self, mock_auto_configure, mock_sync, mock_distribute):
        # Mock a failure in the deployment process
        mock_distribute.side_effect = Exception("CDN error")
        
        with self.assertRaises(Exception):
            await self.deployer.deploy_network()

if __name__ == '__main__':
    unittest.main()
