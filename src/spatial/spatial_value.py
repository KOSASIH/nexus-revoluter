import logging
import asyncio
from torch_geometric.nn import GCNConv
from multi_agent_rl import AllocationAdjuster
from stellar_sdk import Server, TransactionBuilder, Network, Payment, Keypair, Asset, NotFoundError, BadRequestError

class SpatialValue:
    def __init__(self, horizon_url, pi_coin_issuer, master_secret):
        self.mapper = GCNConv(in_channels=128, out_channels=64)
        self.adjuster = AllocationAdjuster()
        self.server = Server(horizon_url)
        self.pi_coin = Asset("PI", pi_coin_issuer)
        self.master_keypair = Keypair.from_secret(master_secret)
        self.logger = self.setup_logger()
    
    def setup_logger(self):
        logger = logging.getLogger("SpatialValue")
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler('spatial_value.log')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    async def map_needs(self, geo_data):
        try:
            value_map = self.mapper(geo_data)
            allocation_plan = self.adjuster.optimize(value_map)
            self.logger.info(f"Value Map: {value_map}, Allocation Plan: {allocation_plan}")
            return allocation_plan
        except Exception as e:
            self.logger.error(f"Error in mapping needs: {e}")
            return None
    
    async def distribute_value(self, recipient_public, amount):
        try:
            account = await self.server.load_account(self.master_keypair.public_key)
            tx = (
                TransactionBuilder(
                    source_account=account,
                    network_passphrase=Network.PUBLIC_NETWORK_PASSPHRASE,
                    base_fee=100
                )
                .append_payment_op(
                    destination=recipient_public,
                    asset=self.pi_coin,
                    amount=str(amount)
                )
                .build()
            )
            tx.sign(self.master_keypair)
            response = await self.server.submit_transaction(tx)
            self.logger.info(f"Value distributed: {response['id']}")
            return response['id']
        except NotFoundError:
            self.logger.error("Recipient account not found.")
            return None
        except BadRequestError as e:
            self.logger.error(f"Bad request error: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Error in distributing value: {e}")
            return None

    async def run(self, geo_data, recipient_public, amount):
        allocation_plan = await self.map_needs(geo_data)
        if allocation_plan:
            transaction_id = await self.distribute_value(recipient_public, amount)
            return allocation_plan, transaction_id
        return None, None

# Example usage
if __name__ == "__main__":
    horizon_url = "https://horizon.stellar.org"
    pi_coin_issuer = "GXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    master_secret = "SXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

    spatial_value = SpatialValue(horizon_url, pi_coin_issuer, master_secret)

    geo_data = ...  # Your geo data here
    recipient_public = "GXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    amount = 10

    loop = asyncio.get_event_loop()
    allocation_plan, transaction_id = loop.run_until_complete(spatial_value.run(geo_data, recipient_public, amount))
    print(f"Allocation Plan: {allocation_plan}, Transaction ID: {transaction_id}")
