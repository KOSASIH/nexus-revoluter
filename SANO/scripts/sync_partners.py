import requests
import json
import logging
import os
import time
from utils.logger import CustomLogger

# Constants
PARTNERS_CONFIG_FILE = 'config/partners.json'
LOG_FILE = 'logs/sync_partners.log'
SYNC_INTERVAL = 60  # Sync every 60 seconds
EMAIL_NOTIFICATIONS = True
ADMIN_EMAIL = 'admin@example.com'

class PartnerSync:
    def __init__(self, logger):
        self.logger = logger
        self.partners = self.load_partners()

    def load_partners(self):
        """Load partner configurations from a JSON file."""
        if not os.path.exists(PARTNERS_CONFIG_FILE):
            self.logger.error(f"Partners configuration file '{PARTNERS_CONFIG_FILE}' not found.")
            raise FileNotFoundError(f"Configuration file '{PARTNERS_CONFIG_FILE}' not found.")
        
        with open(PARTNERS_CONFIG_FILE, 'r') as file:
            return json.load(file)

    def sync_with_partner(self, partner):
        """Synchronize data with a single partner."""
        try:
            self.logger.info(f"Synchronizing with partner: {partner['name']}")
            response = requests.post(partner['url'], json=partner['data'])
            response.raise_for_status()  # Raise an error for bad responses
            self.logger.info(f"Successfully synchronized with {partner['name']}: {response.json()}")
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error synchronizing with {partner['name']}: {e}")
            if EMAIL_NOTIFICATIONS:
                self.send_email_notification(partner['name'], str(e))

    def send_email_notification(self, partner_name, error_message):
        """Send an email notification about synchronization errors."""
        subject = f"Synchronization Error with {partner_name}"
        body = f"An error occurred while synchronizing with {partner_name}:\n\n{error_message}"
        # Here you would implement the email sending logic
        self.logger.info(f"Email notification sent for {partner_name}.")

    def run(self):
        """Run the synchronization process in a loop."""
        while True:
            for partner in self.partners:
                self.sync_with_partner(partner)
            self.logger.info("Waiting for the next synchronization cycle...")
            time.sleep(SYNC_INTERVAL)

if __name__ == "__main__":
    logger = CustomLogger(__name__)
    partner_sync = PartnerSync(logger)
    try:
        partner_sync.run()
    except KeyboardInterrupt:
        logger.info("Synchronization process interrupted by user.")
