from sentiment_aware import TrustAnalyzer
from behavioral_rl import RestorationEngine
from stellar_sdk import Server, TransactionBuilder, Network, Payment, Asset, Keypair
from config import Config
from hashlib import sha256
from logging import getLogger, StreamHandler, Formatter
import json
import time

class GlobalTrustRegenerator:
    def __init__(self, horizon_url, pi_coin_issuer, master_secret):
        self.analyzer = TrustAnalyzer()
        self.engine = RestorationEngine()
        self.server = Server(horizon_url)
        self.confidence_asset = Asset("CONFIDENCE", pi_coin_issuer)
        self.master_keypair = Keypair.from_secret(master_secret)
        self.project_wallet = Config.PROJECT_WALLET_ADDRESS
        self.logger = self.setup_logger()
    
    def setup_logger(self):
        logger = getLogger("GlobalTrustRegenerator")
        handler = StreamHandler()
        formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel("INFO")
        return logger
    
    def regenerate_trust(self, community_data):
        try:
            trust_map = self.analyzer.process(community_data)
            restoration_plan = self.engine.restore(trust_map)
            self.logger.info(f"Trust Map: {json.dumps(trust_map, indent=2)}, Restoration Plan: {json.dumps(restoration_plan, indent=2)}")
            return restoration_plan
        except Exception as e:
            self.logger.error(f"Error regenerating trust: {str(e)}")
            return None
    
    def allocate_revenue(self, amount):
        try:
            tx = (
                TransactionBuilder(
                    source_account=self.server.load_account(self.master_keypair.public_key),
                    network_passphrase=Network.PUBLIC_NETWORK_PASSPHRASE,
                    base_fee=100
                )
                .append_payment_op(
                    destination=self.project_wallet,
                    asset=self.confidence_asset,
                    amount=str(amount)
                )
                .build()
            )
            tx.sign(self.master_keypair)
            response = self.server.submit_transaction(tx)
            self.logger.info(f"Revenue allocated to {self.project_wallet}: {response['id']}")
            return response['id']
        except Exception as e:
            self.logger.error(f"Error allocating revenue: {str(e)}")
            return None
    
    def monitor_transactions(self, transaction_id):
        """Monitor the status of a transaction until it is confirmed or fails."""
        while True:
            try:
                response = self.server.transactions().get(transaction_id)
                if response['status'] in ['completed', 'failed']:
                    self.logger.info(f"Transaction {transaction_id} status: {response['status']}")
                    return response['status']
                time.sleep(5)  # Wait before checking again
            except Exception as e:
                self.logger.error(f"Error monitoring transaction {transaction_id}: {str(e)}")
                return None

# Example usage
if __name__ == "__main__":
    horizon_url = "https://horizon-testnet.stellar.org"
    pi_coin_issuer = "GABC1234567890"  # Replace with actual issuer
    master_secret = "SXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"  # Replace with actual secret

    regenerator = GlobalTrustRegenerator(horizon_url, pi_coin_issuer, master_secret)
    community_data = {"example_key": "example_value"}  # Replace with actual community data
    restoration_plan = regenerator.regenerate_trust(community_data)

    if restoration_plan:
        transaction_id = regenerator.allocate_revenue(100)  # Replace with actual amount
        if transaction_id:
            regenerator.monitor_transactions(transaction_id)
