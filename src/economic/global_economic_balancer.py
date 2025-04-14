from multi_agent import EquityAnalyzer
from predictive_allocation import DistributionEngine
from stellar_sdk import Server, TransactionBuilder, Network, Payment, Asset, Keypair
from config import Config
from hashlib import sha256
from logging import getLogger
import time

class GlobalEconomicBalancer:
    def __init__(self, horizon_url, pi_coin_issuer, master_secret):
        self.analyzer = EquityAnalyzer()
        self.engine = DistributionEngine()
        self.server = Server(horizon_url)
        self.balance_asset = Asset("BALANCE", pi_coin_issuer)
        self.master_keypair = Keypair.from_secret(master_secret)
        self.project_wallet = Config.PROJECT_WALLET_ADDRESS
        self.logger = getLogger("GlobalEconomicBalancer")
    
    def balance_economy(self, economic_data):
        try:
            equity_map = self.analyzer.process(economic_data)
            distribution_plan = self.engine.allocate(equity_map)
            self.logger.info(f"Equity Map: {equity_map}, Distribution Plan: {distribution_plan}")
            return distribution_plan
        except Exception as e:
            self.logger.error(f"Error balancing economy: {e}")
            return None
    
    def allocate_profits(self, amount):
        try:
            # Ensure amount is a valid number
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Amount must be greater than zero.")
            
            # Load the source account
            source_account = self.server.load_account(self.master_keypair.public_key)
            
            # Create transaction
            tx = (
                TransactionBuilder(
                    source_account=source_account,
                    network_passphrase=Network.PUBLIC_NETWORK_PASSPHRASE,
                    base_fee=100
                )
                .append_payment_op(
                    destination=self.project_wallet,
                    asset=self.balance_asset,
                    amount=str(amount)
                )
                .build()
            )
            
            # Sign the transaction
            tx.sign(self.master_keypair)
            
            # Submit the transaction with retry logic
            response = self.submit_transaction_with_retry(tx)
            self.logger.info(f"Profits allocated to {self.project_wallet}: {response['id']}")
            return response['id']
        except Exception as e:
            self.logger.error(f"Error allocating profits: {e}")
            return None

    def submit_transaction_with_retry(self, tx, retries=3, delay=5):
        for attempt in range(retries):
            try:
                response = self.server.submit_transaction(tx)
                return response
            except Exception as e:
                self.logger.warning(f"Transaction submission failed: {e}. Retrying {attempt + 1}/{retries}...")
                time.sleep(delay)
        raise Exception("Transaction submission failed after multiple attempts.")

    def hash_data(self, data):
        """Hash economic data for integrity verification."""
        return sha256(data.encode()).hexdigest()

    def log_economic_data(self, economic_data):
        """Log economic data for auditing purposes."""
        hashed_data = self.hash_data(str(economic_data))
        self.logger.info(f"Logged Economic Data Hash: {hashed_data}")

# Example usage
if __name__ == "__main__":
    horizon_url = "https://horizon.stellar.org"
    pi_coin_issuer = "GXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    master_secret = "SXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    
    balancer = GlobalEconomicBalancer(horizon_url, pi_coin_issuer, master_secret)
    economic_data = {"GDP": 20000, "Inflation": 2.5}  # Example economic data
    balancer.log_economic_data(economic_data)
    distribution_plan = balancer.balance_economy(economic_data)
    if distribution_plan:
        balancer.allocate_profits(1000)  # Example profit allocation
