from causal_inference import RiskForecaster
from game_theory import StrategyEngine
from stellar_sdk import Server, TransactionBuilder, Network, Payment, Asset, Keypair
from config import Config
from hashlib import sha256
from logging import getLogger, StreamHandler, Formatter
import json
import requests

class GeopoliticalRiskMitigator:
    def __init__(self, horizon_url, pi_coin_issuer, master_secret):
        self.forecaster = RiskForecaster()
        self.engine = StrategyEngine()
        self.server = Server(horizon_url)
        self.resilience_asset = Asset("RESILIENCE", pi_coin_issuer)
        self.master_keypair = Keypair.from_secret(master_secret)
        self.project_wallet = Config.PROJECT_WALLET_ADDRESS
        self.logger = self.setup_logger()
    
    def setup_logger(self):
        logger = getLogger("GeopoliticalRiskMitigator")
        handler = StreamHandler()
        formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel("INFO")
        return logger
    
    def forecast_risks(self, global_data):
        try:
            risk_map = self.forecaster.predict(global_data)
            strategy_plan = self.engine.respond(risk_map)
            self.logger.info(f"Risk Map: {json.dumps(risk_map, indent=2)}, Strategy Plan: {json.dumps(strategy_plan, indent=2)}")
            return strategy_plan
        except Exception as e:
            self.logger.error(f"Error forecasting risks: {e}")
            return None
    
    def allocate_funds(self, amount):
        try:
            tx = (
                TransactionBuilder(
                    source_account=self.server.load_account(self.master_keypair.public_key),
                    network_passphrase=Network.PUBLIC_NETWORK_PASSPHRASE,
                    base_fee=100
                )
                .append_payment_op(
                    destination=self.project_wallet,
                    asset=self.resilience_asset,
                    amount=str(amount)
                )
                .build()
            )
            tx.sign(self.master_keypair)
            response = self.server.submit_transaction(tx)
            self.logger.info(f"Funds allocated to {self.project_wallet}: {response['id']}")
            return response['id']
        except Exception as e:
            self.logger.error(f"Error allocating funds: {e}")
            return None
    
    def fetch_global_data(self, api_endpoint):
        try:
            response = requests.get(api_endpoint)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            self.logger.error(f"Error fetching global data: {e}")
            return None

    def execute_strategy(self, global_data):
        strategy_plan = self.forecast_risks(global_data)
        if strategy_plan:
            for action in strategy_plan.get('actions', []):
                if action['type'] == 'allocate':
                    self.allocate_funds(action['amount'])
                # Add more action types as needed
        else:
            self.logger.warning("No valid strategy plan generated.")

# Example usage
if __name__ == "__main__":
    horizon_url = "https://horizon-testnet.stellar.org"
    pi_coin_issuer = "GXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    master_secret = "SXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    
    mitigator = GeopoliticalRiskMitigator(horizon_url, pi_coin_issuer, master_secret)
    global_data = mitigator.fetch_global_data("https://api.example.com/global_data")
    mitigator.execute_strategy(global_data)
