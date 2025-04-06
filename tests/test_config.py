import unittest
from unittest.mock import patch, MagicMock
from config import Config

class TestConfig(unittest.TestCase):

    @patch.dict('os.environ', {
        "NETWORK_NAME": "TestNetwork",
        "NETWORK_PORT": "6000",
        "NETWORK_HOST": "127.0.0.1",
        "MAX_CONNECTIONS": "150",
        "BLOCK_TIME": "5",
        "DIFFICULTY": "3",
        "API_VERSION": "v2",
        "CONSENSUS_INTERVAL": "10",
        "LOG_LEVEL": "DEBUG",
        "DATABASE_URL": "sqlite:///test_network.db",
        "ENABLE_SSL": "True",
        "SSL_CERT_PATH": "test/path/to/cert.pem",
        "SSL_KEY_PATH": "test/path/to/key.pem",
        "MAINTENANCE_MODE": "False"
    })
    def test_config_loading(self):
        """Test that configuration loads correctly from environment variables."""
        Config.validate_config()  # Validate the configuration
        self.assertEqual(Config.NETWORK_NAME, "TestNetwork")
        self.assertEqual(Config.NETWORK_PORT, 6000)
        self.assertEqual(Config.NETWORK_HOST, "127.0.0.1")
        self.assertEqual(Config.MAX_CONNECTIONS, 150)
        self.assertEqual(Config.BLOCK_TIME, 5)
        self.assertEqual(Config.DIFFICULTY, 3)
        self.assertEqual(Config.API_VERSION, "v2")
        self.assertEqual(Config.CONSENSUS_INTERVAL, 10)
        self.assertEqual(Config.LOG_LEVEL, "DEBUG")
        self.assertEqual(Config.DATABASE_URL, "sqlite:///test_network.db")
        self.assertTrue(Config.ENABLE_SSL)
        self.assertEqual(Config.SSL_CERT_PATH, "test/path/to/cert.pem")
        self.assertEqual(Config.SSL_KEY_PATH, "test/path/to/key.pem")
        self.assertFalse(Config.MAINTENANCE_MODE)

    @patch.dict('os.environ', {
        "NETWORK_PORT": "70000"  # Invalid port
    })
    def test_invalid_network_port(self):
        """Test that an invalid network port raises a ValueError."""
        with self.assertRaises(ValueError) as context:
            Config.validate_config()
        self.assertEqual(str(context.exception), "NETWORK_PORT must be between 1 and 65535.")

    @patch.dict('os.environ', {
        "BLOCK_TIME": "-5"  # Invalid block time
    })
    def test_invalid_block_time(self):
        """Test that an invalid block time raises a ValueError."""
        with self.assertRaises(ValueError) as context:
            Config.validate_config()
        self.assertEqual(str(context.exception), "BLOCK_TIME must be a positive integer.")

    @patch.dict('os.environ', {
        "DIFFICULTY": "0"  # Invalid difficulty
    })
    def test_invalid_difficulty(self):
        """Test that an invalid difficulty raises a ValueError."""
        with self.assertRaises(ValueError) as context:
            Config.validate_config()
        self.assertEqual(str(context.exception), "DIFFICULTY must be at least 1.")

    @patch.dict('os.environ', {
        "ENABLE_SSL": "True",
        "SSL_CERT_PATH": "",
        "SSL_KEY_PATH": ""  # SSL paths must be set if SSL is enabled
    })
    def test_ssl_paths_required(self):
        """Test that missing SSL paths when SSL is enabled raises a ValueError."""
        with self.assertRaises(ValueError) as context:
            Config.validate_config()
        self.assertEqual(str(context.exception), "SSL_CERT_PATH and SSL_KEY_PATH must be set if ENABLE_SSL is True.")

if __name__ == '__main__':
    unittest.main()
