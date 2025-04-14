from multi_objective import SustainabilityPlanner
from spatio_temporal import ImpactEngine
from stellar_sdk import Server, TransactionBuilder, Network, Payment, Asset, Keypair
from config import Config
from hashlib import sha256
from logging import getLogger, StreamHandler, Formatter
import json
import requests

class SustainabilitySynergy:
    def __init__(self, horizon_url, pi_coin_issuer, master_secret):
        self.planner = SustainabilityPlanner()
        self.engine = ImpactEngine()
        self.server = Server(horizon_url)
        self.green_asset = Asset("GREEN", pi_coin_issuer)
        self.master_keypair = Keypair.from_secret(master_secret)
        self.project_wallet = Config.PROJECT_WALLET_ADDRESS
        self.logger = self.setup_logger()
    
    def setup_logger(self):
        logger = getLogger("SustainabilitySynergy")
        handler = StreamHandler()
        formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel("INFO")
        return logger

    def plan_initiatives(self, global_data):
        try:
            sustainability_map = self.planner.process(global_data)
            impact_plan = self.engine.optimize(sustainability_map)
            self.logger.info(f"Sustainability Map: {json.dumps(sustainability_map, indent=2)}, Impact Plan: {json.dumps(impact_plan, indent=2)}")
            return impact_plan
        except Exception as e:
            self.logger.error(f"Error in planning initiatives: {str(e)}")
            return None
    
    def allocate_profits(self, amount):
        try:
            tx = (
                TransactionBuilder(
                    source_account=self.server.load_account(self.master_keypair.public_key),
                    network_passphrase=Network.PUBLIC_NETWORK_PASSPHRASE,
                    base_fee=100
                )
                .append_payment_op(
                    destination=self.project_wallet,
                    asset=self.green_asset,
                    amount=str(amount)
                )
                .build()
            )
            tx.sign(self.master_keypair)
            response = self.server.submit_transaction(tx)
            self.logger.info(f"Profits allocated to {self.project_wallet}: {response['id']}")
            return response['id']
        except Exception as e:
            self.logger.error(f"Error in allocating profits: {str(e)}")
            return None

    def fetch_global_data(self, api_endpoint):
        try:
            response = requests.get(api_endpoint)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            self.logger.error(f"Error fetching global data: {str(e)}")
            return None

    def validate_transaction(self, transaction_id):
        try:
            response = self.server.transactions().get(transaction_id)
            self.logger.info(f"Transaction {transaction_id} validation: {response['status']}")
            return response['status'] == 'completed'
        except Exception as e:
            self.logger.error(f"Error validating transaction {transaction_id}: {str(e)}")
            return False

# Example usage
if __name__ == "__main__":
    horizon_url = "https://horizon.stellar.org"
    pi_coin_issuer = "GABC1234567890"  # Replace with actual issuer
    master_secret = "SXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"  # Replace with actual secret

    synergy = SustainabilitySynergy(horizon_url, pi_coin_issuer, master_secret)
    global_data = synergy.fetch_global_data("https://api.example.com/global_data")
    if global_data:
        impact_plan = synergy.plan_initiatives(global_data)
        if impact_plan:
            transaction_id = synergy.allocate_profits(100)
            if transaction_id:
                is_valid = synergy.validate_transaction(transaction_id)
                print(f"Transaction valid: {is_valid}")
