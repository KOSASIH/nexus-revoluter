import asyncio
from graph_rl import SynergyMapper
from swarm_intelligence import UtilizationEngine
from stellar_sdk import Server, TransactionBuilder, Network, Payment, Asset, Keypair
from hashlib import sha256
from logging import getLogger, StreamHandler, Formatter
from datetime import datetime

class ResourceSynergy:
    def __init__(self, horizon_url, pi_coin_issuer, master_secret, project_wallet):
        self.mapper = SynergyMapper()
        self.engine = UtilizationEngine()
        self.server = Server(horizon_url)
        self.resource_asset = Asset("RESOURCE", pi_coin_issuer)
        self.master_keypair = Keypair.from_secret(master_secret)
        self.project_wallet = project_wallet
        self.logger = self.setup_logger()
    
    def setup_logger(self):
        logger = getLogger("ResourceSynergy")
        handler = StreamHandler()
        formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel("INFO")
        return logger

    async def map_resources(self, resource_data):
        try:
            synergy_map = self.mapper.process(resource_data)
            utilization_plan = self.engine.optimize(synergy_map)
            self.logger.info(f"Synergy Map: {synergy_map}, Utilization Plan: {utilization_plan}")
            return utilization_plan
        except Exception as e:
            self.logger.error(f"Error mapping resources: {e}")
            return None
    
    async def allocate_profits(self, amount):
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
                    asset=self.resource_asset,
                    amount=str(amount)
                )
                .build()
            )
            tx.sign(self.master_keypair)
            response = await self.server.submit_transaction(tx)
            self.logger.info(f"Profits allocated to {self.project_wallet}: {response['id']}")
            return response['id']
        except Exception as e:
            self.logger.error(f"Error allocating profits: {e}")
            return None

    async def monitor_transactions(self, transaction_id):
        try:
            while True:
                response = await self.server.transactions().transaction(transaction_id).call()
                self.logger.info(f"Transaction Status: {response['status']}")
                if response['status'] in ['completed', 'failed']:
                    break
                await asyncio.sleep(5)  # Check every 5 seconds
        except Exception as e:
            self.logger.error(f"Error monitoring transaction {transaction_id}: {e}")

    async def run(self, resource_data, amount):
        utilization_plan = await self.map_resources(resource_data)
        if utilization_plan:
            transaction_id = await self.allocate_profits(amount)
            if transaction_id:
                await self.monitor_transactions(transaction_id)

# Example usage
if __name__ == "__main__":
    horizon_url = "https://horizon.stellar.org"
    pi_coin_issuer = "GXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    master_secret = "SXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    project_wallet = "GXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    
    resource_data = {...}  # Your resource data here
    amount = 100  # Amount to allocate

    resource_synergy = ResourceSynergy(horizon_url, pi_coin_issuer, master_secret, project_wallet)
    asyncio.run(resource_synergy.run(resource_data, amount))
