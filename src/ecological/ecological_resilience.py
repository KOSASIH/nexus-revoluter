import logging
import asyncio
from multi_objective import SustainabilityOptimizer
from iot_feed import EcoMonitor
from stellar_sdk import Server, TransactionBuilder, Network, Payment, Asset, Keypair, NotFoundError, BadRequestError

class EcologicalResilience:
    def __init__(self, horizon_url, pi_coin_issuer, master_secret):
        self.optimizer = SustainabilityOptimizer()
        self.monitor = EcoMonitor()
        self.server = Server(horizon_url)
        self.green_asset = Asset("GREEN", pi_coin_issuer)
        self.master_keypair = Keypair.from_secret(master_secret)
        self.logger = logging.getLogger("EcologicalResilience")
        logging.basicConfig(level=logging.INFO)

    async def optimize_impact(self, node_data):
        try:
            eco_plan = await self.optimizer.compute(node_data)
            emissions = await self.monitor.measure(node_data)
            self.logger.info(f"Environmental Plan: {eco_plan}, Emissions: {emissions}")
            return eco_plan
        except Exception as e:
            self.logger.error(f"Error optimizing impact: {e}")
            return None

    async def issue_credit(self, recipient_public, credit_amount):
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
                    asset=self.green_asset,
                    amount=str(credit_amount)
                )
                .build()
            )
            tx.sign(self.master_keypair)
            response = await self.server.submit_transaction(tx)
            self.logger.info(f"Green credit issued: {response['id']}")
            return response['id']
        except (NotFoundError, BadRequestError) as e:
            self.logger.error(f"Transaction failed: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            return None

    async def track_sustainability_metrics(self, node_data):
        try:
            metrics = await self.monitor.get_metrics(node_data)
            self.logger.info(f"Sustainability Metrics: {metrics}")
            return metrics
        except Exception as e:
            self.logger.error(f"Error tracking sustainability metrics: {e}")
            return None

    async def run(self, node_data, recipient_public, credit_amount):
        eco_plan = await self.optimize_impact(node_data)
        if eco_plan:
            await self.issue_credit(recipient_public, credit_amount)
            await self.track_sustainability_metrics(node_data)

# Example usage
if __name__ == "__main__":
    horizon_url = "https://horizon.stellar.org"
    pi_coin_issuer = "GXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    master_secret = "SXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

    ecological_resilience = EcologicalResilience(horizon_url, pi_coin_issuer, master_secret)

    # Sample node data and recipient public key
    node_data = {"location": "City Park", "activity": "Tree Planting"}
    recipient_public = "GXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    credit_amount = 10

    asyncio.run(ecological_resilience.run(node_data, recipient_public, credit_amount))
