import os
import logging
from typing import Optional

class Config:
    # Network settings
    NETWORK_NAME: str = os.getenv("NETWORK_NAME", "PiNetwork")
    NETWORK_PORT: int = int(os.getenv("NETWORK_PORT", 5000))
    NETWORK_HOST: str = os.getenv("NETWORK_HOST", "0.0.0.0")
    MAX_CONNECTIONS: int = int(os.getenv("MAX_CONNECTIONS", 100))

    # Blockchain settings
    BLOCK_TIME: int = int(os.getenv("BLOCK_TIME", 10))  # Time in seconds to create a new block
    DIFFICULTY: int = int(os.getenv("DIFFICULTY", 2))    # Difficulty level for mining
    STABLECOIN_VALUE: float = float(os.getenv("STABLECOIN_VALUE", 314159.00))  # Value of Pi Coin as a stablecoin
    COIN_SYMBOL: str = "Pi"  # Symbol for Pi Coin

    # API settings
    API_VERSION: str = os.getenv("API_VERSION", "v1")
    API_ENDPOINT: str = os.getenv("API_ENDPOINT", f"http://{NETWORK_HOST}:{NETWORK_PORT}/api/{API_VERSION}")

    # Consensus settings
    CONSENSUS_INTERVAL: int = int(os.getenv("CONSENSUS_INTERVAL", 15))  # Time in seconds between consensus rounds

    # Logging settings
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
    LOG_FILE: str = os.getenv("LOG_FILE", "nexus_revoluter.log")  # Log file path

    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///pi_network.db")  # Default to SQLite

    # Security settings
    ENABLE_SSL: bool = bool(os.getenv("ENABLE_SSL", False))  # Enable SSL for API
    SSL_CERT_PATH: Optional[str] = os.getenv("SSL_CERT_PATH", "path/to/cert.pem")
    SSL_KEY_PATH: Optional[str] = os.getenv("SSL_KEY_PATH", "path/to/key.pem")

    # Other settings
    MAINTENANCE_MODE: bool = bool(os.getenv("MAINTENANCE_MODE", False))  # Enable maintenance mode

    @classmethod
    def validate_config(cls):
        """Validate the configuration settings."""
        if cls.NETWORK_PORT < 1 or cls.NETWORK_PORT > 65535:
            raise ValueError("NETWORK_PORT must be between 1 and 65535.")
        if cls.BLOCK_TIME <= 0:
            raise ValueError("BLOCK_TIME must be a positive integer.")
        if cls.DIFFICULTY < 1:
            raise ValueError("DIFFICULTY must be at least 1.")
        if cls.CONSENSUS_INTERVAL <= 0:
            raise ValueError("CONSENSUS_INTERVAL must be a positive integer.")
        if cls.STABLECOIN_VALUE <= 0:
            raise ValueError("STABLECOIN_VALUE must be a positive number.")
        if cls.ENABLE_SSL and (not cls.SSL_CERT_PATH or not cls.SSL_KEY_PATH):
            raise ValueError("SSL_CERT_PATH and SSL_KEY_PATH must be set if ENABLE_SSL is True.")

    @classmethod
    def display_config(cls):
        """Display the current configuration settings."""
        print("Current Configuration:")
        print(f"Network Name: {cls.NETWORK_NAME}")
        print(f"Network Host: {cls.NETWORK_HOST}")
        print(f"Network Port: {cls.NETWORK_PORT}")
        print(f"Max Connections: {cls.MAX_CONNECTIONS}")
        print(f"Block Time: {cls.BLOCK_TIME} seconds")
        print(f"Difficulty: {cls.DIFFICULTY}")
        print(f"Stablecoin Value: ${cls.STABLECOIN_VALUE:.2f} ({cls.COIN_SYMBOL})")
        print(f"API Endpoint: {cls.API_ENDPOINT}")
        print(f"Consensus Interval: {cls.CONSENSUS_INTERVAL} seconds")
        print(f"Log Level: {cls.LOG_LEVEL}")
        print(f"Log File: {cls.LOG_FILE}")
        print(f"Database URL: {cls.DATABASE_URL}")
        print(f"SSL Enabled: {cls.ENABLE_SSL}")
        print(f"SSL Certificate Path: {cls.SSL_CERT_PATH}")
        print(f"SSL Key Path: {cls.SSL_KEY_PATH}")
        print(f"Maintenance Mode: {cls.MAINTENANCE_MODE}")

    @classmethod
    def setup_logging(cls):
        """Setup logging configuration."""
        logging.basicConfig(
            filename=cls.LOG_FILE,
            level=cls.LOG_LEVEL,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

# Example usage
if __name__ == "__main__":
    try:
        Config.validate_config()  # Validate configuration before use
        Config.setup_logging()     # Setup logging
        Config.display_config()    # Display the configuration
    except ValueError as e:
        logging.error(f"Configuration error: {e}")
