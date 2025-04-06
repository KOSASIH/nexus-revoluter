import os
import unittest
from unittest.mock import patch
from config import Config  # Assuming your config implementation is in a file named config.py

class TestConfig(unittest.TestCase):

    @patch.dict(os.environ, {
        "NETWORK_NAME": "TestNetwork",
        "NETWORK_PORT": "5001",
        "NETWORK_HOST": "127.0.0.1",
        "MAX_CONNECTIONS": "200",
        "BLOCK_TIME": "15",
        "DIFFICULTY": "3",
        "STABLECOIN_VALUE": "314159.26",
        "API_VERSION": "v2",
        "CONSENSUS_INTERVAL": "20",
        "LOG_LEVEL": "DEBUG",
        "LOG_FILE": "test_log.log",
        "DATABASE_URL": "sqlite:///test_pi_network.db",
        "ENABLE_SSL": "True",
        "SSL_CERT_PATH": "test/path/to/cert.pem",
        "SSL_KEY_PATH": "test/path/to/key.pem",
        "MAINTENANCE_MODE": "False"
    })
    def test_config_initialization(self):
        """Test the initialization of the Config class."""
        self.assertEqual(Config.NETWORK_NAME, "TestNetwork")
        self.assertEqual(Config.NETWORK_PORT, 5001)
        self.assertEqual(Config.NETWORK_HOST, "127.0.0.1")
        self.assertEqual(Config.MAX_CONNECTIONS, 200)
        self.assertEqual(Config.BLOCK_TIME, 15)
        self.assertEqual(Config.DIFFICULTY, 3)
        self.assertEqual(Config.STABLECOIN_VALUE, 314159.26)
        self.assertEqual(Config.API_VERSION, "v2")
        self.assertEqual(Config.CONSENSUS_INTERVAL, 20)
        self.assertEqual(Config.LOG_LEVEL, "DEBUG")
        self.assertEqual(Config.LOG_FILE, "test_log.log")
        self.assertEqual(Config.DATABASE_URL, "sqlite:///test_pi_network.db")
        self.assertTrue(Config.ENABLE_SSL)
        self.assertEqual(Config.SSL_CERT_PATH, "test/path/to/cert.pem")
        self.assertEqual(Config.SSL_KEY_PATH, "test/path/to/key.pem")
        self.assertFalse(Config.MAINTENANCE_MODE)

    def test_validate_config(self):
        """Test the validation of the configuration settings."""
        Config.validate_config()  # Should not raise an exception

    def test_validate_config_invalid_port(self):
        """Test validation with an invalid network port."""
        with patch.dict(os.environ, {"NETWORK_PORT": "70000"}):
            with self.assertRaises(ValueError) as context:
                Config.validate_config()
            self.assertEqual(str(context.exception), "NETWORK_PORT must be between 1 and 65535.")

    def test_validate_config_invalid_block_time(self):
        """Test validation with an invalid block time."""
        with patch.dict(os.environ, {"BLOCK_TIME": "0"}):
            with self.assertRaises(ValueError) as context:
                Config.validate_config()
            self.assertEqual(str(context.exception), "BLOCK_TIME must be a positive integer.")

    def test_validate_config_invalid_difficulty(self):
        """Test validation with an invalid difficulty."""
        with patch.dict(os.environ, {"DIFFICULTY": "0"}):
            with self.assertRaises(ValueError) as context:
                Config.validate_config()
            self.assertEqual(str(context.exception), "DIFFICULTY must be at least 1.")

    def test_validate_config_invalid_consensus_interval(self):
        """Test validation with an invalid consensus interval."""
        with patch.dict(os.environ, {"CONSENSUS_INTERVAL": "0"}):
            with self.assertRaises(ValueError) as context:
                Config.validate_config()
            self.assertEqual(str(context.exception), "CONSENSUS_INTERVAL must be a positive integer.")

    def test_validate_config_invalid_stablecoin_value(self):
        """Test validation with an invalid stablecoin value."""
        with patch.dict(os.environ, {"STABLECOIN_VALUE": "-1"}):
            with self.assertRaises(ValueError) as context:
                Config.validate_config()
            self.assertEqual(str(context.exception), "STABLECOIN_VALUE must be a positive number.")

    def test_validate_config_ssl_paths(self):
        """Test validation with SSL enabled but missing paths."""
        with patch.dict(os.environ, {"ENABLE_SSL": "True", "SSL_CERT_PATH": "", "SSL_KEY_PATH": ""}):
            with self.assertRaises(ValueError) as context:
                Config.validate_config()
            self.assertEqual(str(context.exception), "SSL_CERT_PATH and SSL_KEY_PATH must be set if ENABLE_SSL is True.")

if __name__ == '__main__':
    unittest.main()
