from robust_neural import EnvironmentModeler
from adversarial_modeling import OptimizationEngine
from stellar_sdk import Server, TransactionBuilder, Network, Payment, Asset, Keypair
from config import Config
from hashlib import sha256
from logging import getLogger, StreamHandler, Formatter
import json
import time

class ExtremeEnvironmentAdaptor:
    def __init__(self, horizon_url, pi_coin_issuer, master_secret):
        self.modeler = EnvironmentModeler()
        self.engine = OptimizationEngine()
        self.server = Server(horizon_url)
        self.endurance_asset = Asset("ENDURANCE", pi_coin_issuer)
        self.master_keypair = Keypair.from_secret(master_secret)
        self.project_wallet = Config.PROJECT_WALLET_ADDRESS
        self.logger = self.setup_logger()
    
    def setup_logger(self):
        logger = getLogger("ExtremeEnvironmentAdaptor")
        handler = StreamHandler()
        formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel("INFO")
        return logger
    
    def adapt_environment(self, env_data):
        try:
            environment_map = self.modeler.process(env_data)
            optimization_plan = self.engine.optimize(environment_map)
            self.logger.info(f"Environment Map: {json.dumps(environment_map, indent=2)}, Optimization Plan: {json.dumps(optimization_plan, indent=2)}")
            return optimization_plan
        except Exception as e:
            self.logger.error(f"Error adapting environment: {str(e)}")
            raise
    
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
                    asset=self.endurance_asset,
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
            raise
    
    def monitor_transaction(self, transaction_id):
        """Monitor the transaction status until it is confirmed or fails."""
        while True:
            try:
                response = self.server.transactions().get(transaction_id)
                if response['status'] in ['completed', 'failed']:
                    self.logger.info(f"Transaction {transaction_id} status: {response['status']}")
                    return response['status']
                self.logger.info(f"Transaction {transaction_id} is still pending...")
                time.sleep(5)  # Wait before checking again
            except Exception as e:
                self.logger.error(f"Error monitoring transaction {transaction_id}: {str(e)}")
                break

# Example usage
if __name__ == "__main__":
    horizon_url = "https://horizon-testnet.stellar.org"
    pi_coin_issuer = "GABC1234567890"  # Replace with actual issuer
    master_secret = "SXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"  # Replace with actual secret

    adaptor = ExtremeEnvironmentAdaptor(horizon_url, pi_coin_issuer, master_secret)
    env_data = {"temperature": 22, "humidity": 60}  # Example environment data
    optimization_plan = adaptor.adapt_environment(env_data)
    transaction_id = adaptor.allocate_revenue(100)  # Example amount
    adaptor.monitor_transaction(transaction_id)
