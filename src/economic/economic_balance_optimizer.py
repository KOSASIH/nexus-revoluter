import asyncio
from multi_agent_rl import BalancePlanner
from game_theoretic import OptimizationEngine
from stellar_sdk import Server, TransactionBuilder, Network, Payment, Asset, Keypair
from config import Config
from hashlib import sha256
from logging import getLogger, StreamHandler, Formatter
from requests.exceptions import RequestException

class EconomicBalanceOptimizer:
    def __init__(self, horizon_url, pi_coin_issuer, master_secret):
        self.planner = BalancePlanner()
        self.engine = OptimizationEngine()
        self.server = Server(horizon_url)
        self.equity_asset = Asset("EQUITY", pi_coin_issuer)
        self.master_keypair = Keypair.from_secret(master_secret)
        self.project_wallet = Config.PROJECT_WALLET_ADDRESS
        self.logger = self.setup_logger()

    def setup_logger(self):
        logger = getLogger("EconomicBalanceOptimizer")
        handler = StreamHandler()
        formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel("INFO")
        return logger

    async def optimize_balance(self, economic_data):
        try:
            balance_map = await self.planner.process(economic_data)
            optimization_plan = await self.engine.distribute(balance_map)
            self.logger.info(f"Balance Map: {balance_map}, Optimization Plan: {optimization_plan}")
            return optimization_plan
        except Exception as e:
            self.logger.error(f"Error optimizing balance: {e}")
            return None

    async def allocate_revenue(self, amount):
        try:
            account = await self.server.load_account(self.master_keypair.public_key)
            tx = (
                TransactionBuilder(
                    source_account=account,
                    network_passphrase=Network.PUBLIC_NETWORK_PASSPHRASE,
                    base_fee=100
                )
                .append_payment_op(
                    destination=self.project_wallet,
                    asset=self.equity_asset,
                    amount=str(amount)
                )
                .build()
            )
            tx.sign(self.master_keypair)
            response = await self.submit_transaction(tx)
            self.logger.info(f"Revenue allocated to {self.project_wallet}: {response['id']}")
            return response['id']
        except RequestException as e:
            self.logger.error(f"Network error during transaction: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Error allocating revenue: {e}")
            return None

    async def submit_transaction(self, transaction):
        try:
            response = await self.server.submit_transaction(transaction)
            return response
        except Exception as e:
            self.logger.error(f"Transaction submission failed: {e}")
            raise

# Example usage
async def main():
    optimizer = EconomicBalanceOptimizer("https://horizon-testnet.stellar.org", "GABCD1234567890", "SXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    economic_data = {"data": "example"}  # Replace with actual economic data
    optimization_plan = await optimizer.optimize_balance(economic_data)
    if optimization_plan:
        await optimizer.allocate_revenue(100)

if __name__ == "__main__":
    asyncio.run(main())
