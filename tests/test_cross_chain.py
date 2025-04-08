import unittest
from unittest.mock import MagicMock, patch
import json
import uuid
from your_module import IBCModule  # Adjust the import based on your project structure

class TestIBCModule(unittest.TestCase):

    @patch('your_module.IBCClient')  # Mock the IBCClient
    def setUp(self, MockIBCClient):
        self.config = {
            'retryLimit': 3,
            'retryDelay': 1000
        }
        self.ibc_module = IBCModule(self.config)
        self.ibc_module.client = MockIBCClient()
        self.ibc_module.client.sendPacket = MagicMock()
        self.ibc_module.client.acknowledgePacket = MagicMock()

    def test_send_packet_success(self):
        # Arrange
        data = {"message": "Hello from Pi Coin!"}
        destination_chain_id = "destination-chain-id"
        self.ibc_module.client.sendPacket.return_value = {"status": "success"}

        # Act
        result = self.ibc_module.sendPacket(data, destination_chain_id)

        # Assert
        self.ibc_module.client.sendPacket.assert_called_once()
        self.assertEqual(result, {"status": "success"})

    def test_send_packet_failure_retries(self):
        # Arrange
        data = {"message": "Hello from Pi Coin!"}
        destination_chain_id = "destination-chain-id"
        self.ibc_module.client.sendPacket.side_effect = [Exception("Network error"), {"status": "success"}]

        # Act
        result = self.ibc_module.sendPacket(data, destination_chain_id)

        # Assert
        self.assertEqual(self.ibc_module.client.sendPacket.call_count, 2)  # Should retry once
        self.assertEqual(result, {"status": "success"})

    def test_send_packet_failure_exceeds_retries(self):
        # Arrange
        data = {"message": "Hello from Pi Coin!"}
        destination_chain_id = "destination-chain-id"
        self.ibc_module.client.sendPacket.side_effect = Exception("Network error")

        # Act & Assert
        with self.assertRaises(Exception) as context:
            self.ibc_module.sendPacket(data, destination_chain_id)
        self.assertEqual(str(context.exception), "Packet transmission failed after multiple attempts")

    def test_receive_packet(self):
        # Arrange
        packet = {"id": str(uuid.uuid4()), "data": {"message": "Hello!"}}

        # Act
        self.ibc_module.receivePacket(packet)

        # Assert
        self.ibc_module.client.acknowledgePacket.assert_called_once_with(packet["id"])

    def test_acknowledge_packet_success(self):
        # Arrange
        packet_id = str(uuid.uuid4())
        self.ibc_module.client.acknowledgePacket.return_value = {"status": "acknowledged"}

        # Act
        result = self.ibc_module.acknowledgePacket(packet_id)

        # Assert
        self.ibc_module.client.acknowledgePacket.assert_called_once_with(packet_id)
        self.assertEqual(result, {"status": "acknowledged"})

    def test_acknowledge_packet_failure(self):
        # Arrange
        packet_id = str(uuid.uuid4())
        self.ibc_module.client.acknowledgePacket.side_effect = Exception("Acknowledgment error")

        # Act & Assert
        with self.assertRaises(Exception) as context:
            self.ibc_module.acknowledgePacket(packet_id)
        self.assertEqual(str(context.exception), "Packet acknowledgment failed")

if __name__ == '__main__':
    unittest.main()
