import asyncio
from deep_rl import FlowOptimizer
from multi_objective import AllocationEngine
from stellar_sdk import Server, TransactionBuilder, Network, Payment, Asset, Keypair
from hashlib import sha256
from logging import getLogger, StreamHandler, Formatter
from datetime import datetime

class FinancialFlowOptimizer:
    def __init__(self, horizon_url, pi_coin_issuer, master_secret, project_wallet):
        self.optimizer = FlowOptimizer()
        self.engine = AllocationEngine()
        self.server = Server(horizon_url)
        self.flow_asset = Asset("FLOW", pi_coin_issuer)
        self.master_keypair = Keypair.from_secret(master_secret)
        self.project_wallet = project_wallet
        self.logger = self.setup_logger()
    
    def setup_logger(self):
        logger = getLogger("FinancialFlowOptimizer")
        handler = StreamHandler()
        formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel("INFO")
        return logger

    async def optimize_flow(self, sector_data):
        try:
            flow_plan = await self.optimizer.compute(sector_data)
            allocation_plan = self.engine.distribute(flow_plan)
            self.logger.info(f"Flow Plan: {flow_plan}, Allocation: {allocation_plan}")
            return allocation_plan
        except Exception as e:
            self.logger.error(f"Error optimizing flow: {e}")
            return None
    
    async def allocate_to_project(self, amount):
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
                    asset=self.flow_asset,
                    amount=str(amount)
                )
                .build()
            )
            tx.sign(self.master_keypair)
            response = await self.server.submit_transaction(tx)
            self.logger.info(f"Funds allocated to {self.project_wallet}: {response['id']}")
            return response['id']
        except Exception as e:
            self.logger.error(f"Error allocating funds: {e}")
            return None

    async def monitor_transaction(self, transaction_id):
        try:
            while True:
                response = await self.server.transactions().transaction(transaction_id).call()
                if response['status'] in ['completed', 'failed']:
                    self.logger.info(f"Transaction {transaction_id} status: {response['status']}")
                    break
                await asyncio.sleep(5)  # Check every 5 seconds
        except Exception as e:
            self.logger.error(f"Error monitoring transaction {transaction_id}: {e}")

# Example usage
async def main():
    optimizer = FinancialFlowOptimizer(
        horizon_url="https://horizon.stellar.org",
        pi_coin_issuer="GABC1234567890",
        master_secret="SXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        project_wallet="GXYZ1234567890"
    )
    
    sector_data = {...}  # Your sector data here
    allocation_plan = await optimizer.optimize_flow(sector_data)
    
    if allocation_plan:
        transaction_id = await optimizer.allocate_to_project(amount=100)
        if transaction_id:
            await optimizer.monitor_transaction(transaction_id)

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())
