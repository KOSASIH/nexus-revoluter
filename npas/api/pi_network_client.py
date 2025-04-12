import requests
import logging
from npas.utils.logger import setup_logger
from npas.utils.error_handler import handle_api_error

class PiNetworkClient:
    def __init__(self, config):
        self.logger = setup_logger("PiNetworkClient")
        self.endpoints = {
            "main_site": config["main_site"],
            "wallet": config["wallet"],
            "ecosystem": config["ecosystem"]
        }
        self.api_key = config["api_key"]
        self.logger.info("PiNetworkClient initialized with endpoints: %s", self.endpoints)

    def apply_change(self, change):
        """Apply changes to the Pi Network endpoints."""
        try:
            for name, endpoint in self.endpoints.items():
                response = requests.post(
                    f"{endpoint}/api/sync",
                    json=change,
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    timeout=10
                )
                response.raise_for_status()
                self.logger.info(f"Change applied to {name}: {change['id']}")
        except requests.Timeout:
            self.logger.error("Request timed out while applying change.")
            raise
        except requests.ConnectionError:
            self.logger.error("Connection error occurred while applying change.")
            raise
        except requests.HTTPError as e:
            handle_api_error(e, self.logger)
            raise
        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            raise

    def get_status(self):
        """Fetch the status of the Pi Network."""
        try:
            response = requests.get(
                f"{self.endpoints['main_site']}/api/status",
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=10
            )
            response.raise_for_status()
            status = response.json()
            self.logger.info("Fetched status from Pi Network: %s", status)
            return status
        except requests.RequestException as e:
            handle_api_error(e, self.logger)
            return None

if __name__ == "__main__":
    config = {
        "main_site": "https://minepi.com",
        "wallet": "https://wallet.pinet.com",
        "ecosystem": "https://ecosystem.pinet.com",
        "api_key": "your_api_key"  # Placeholder
    }
    
    client = PiNetworkClient(config)
    
    sample_change = {"id": "1", "content": "code update"}
    try:
        client.apply_change(sample_change)
        status = client.get_status()
        if status:
            print(f"Pi Network Status: {status}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
