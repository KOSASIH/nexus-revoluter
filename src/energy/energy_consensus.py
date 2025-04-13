import asyncio
from deep_rl import EnergyOptimizer
from swarm_intelligence import LoadBalancer
from stellar_sdk import Server, TransactionBuilder, Network, Payment, Asset, Keypair
from hashlib import sha256
from logging import getLogger, StreamHandler, Formatter
import json

class EnergyConsensus:
    def __init__(self, horizon_url, pi_coin_issuer, master_secret):
        self.optimizer = EnergyOptimizer()
        self.balancer = LoadBalancer()
        self.server = Server(horizon_url)
        self.energy_asset = Asset("ENERGY", pi_coin_issuer)
        self.master_keypair = Keypair.from_secret(master_secret)
        self.logger = self.setup_logger()
        self.node_usage = {}

    def setup_logger(self):
        logger = getLogger("EnergyConsensus")
        handler = StreamHandler()
        formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel("INFO")
        return logger

    async def optimize_energy(self, node_data):
        try:
            energy_plan = await self.optimizer.compute(node_data)
            balanced_load = self.balancer.distribute(energy_plan)
            self.logger.info(f"Energy Plan: {json.dumps(energy_plan)}, Load: {balanced_load}")
            return balanced_load
        except Exception as e:
            self.logger.error(f"Error optimizing energy: {str(e)}")
            return None

    async def issue_credit(self, node_public, credit_amount):
        try:
            tx = (
                TransactionBuilder(
                    source_account=self.server.load_account(self.master_keypair.public_key),
                    network_passphrase=Network.PUBLIC_NETWORK_PASSPHRASE,
                    base_fee=100
                )
                .append_payment_op(
                    destination=node_public,
                    asset=self.energy_asset,
                    amount=str(credit_amount)
                )
                .build()
            )
            tx.sign(self.master_keypair)
            response = await self.server.submit_transaction(tx)
            self.logger.info(f"Energy credit issued: {response['id']}")
            return response['id']
        except Exception as e:
            self.logger.error(f"Error issuing credit: {str(e)}")
            return None

    async def track_energy_usage(self, node_id, usage):
        if node_id not in self.node_usage:
            self.node_usage[node_id] = []
        self.node_usage[node_id].append(usage)
        self.logger.info(f"Tracking energy usage for {node_id}: {usage}")

    async def run(self, node_data, node_public, credit_amount):
        balanced_load = await self.optimize_energy(node_data)
        if balanced_load:
            await self.issue_credit(node_public, credit_amount)
            await self.track_energy_usage(node_public, balanced_load)

# Example usage
async def main():
    horizon_url = "https://horizon-testnet.stellar.org"
    pi_coin_issuer = "GXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    master_secret = "SXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    
    energy_consensus = EnergyConsensus(horizon_url, pi_coin_issuer, master_secret)
    node_data = {"node_id": "node_1", "demand": 100}
    node_public = "GXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    credit_amount = 10

    await energy_consensus.run(node_data, node_public, credit_amount)

# To run the example
if __name__ == "__main__":
    asyncio.run(main())
