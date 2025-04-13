import logging
import asyncio
from multi_agent_rl import OpportunityMapper
from fairness_algorithm import EquityAllocator
from stellar_sdk import Server, TransactionBuilder, Network, Payment, Asset, Keypair, TransactionFailedError

class InclusiveOpportunity:
    def __init__(self, horizon_url, pi_coin_issuer, master_secret):
        self.mapper = OpportunityMapper()
        self.allocator = EquityAllocator()
        self.server = Server(horizon_url)
        self.opportunity_asset = Asset("OPPORTUNITY", pi_coin_issuer)
        self.master_keypair = Keypair.from_secret(master_secret)
        self.logger = self.setup_logger()
    
    def setup_logger(self):
        logger = logging.getLogger("InclusiveOpportunity")
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler("inclusive_opportunity.log")
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    async def map_opportunities(self, community_data):
        try:
            opportunity_map = await self.mapper.compute(community_data)
            allocation_plan = self.allocator.distribute(opportunity_map)
            self.logger.info(f"Opportunity Map: {opportunity_map}, Allocation Plan: {allocation_plan}")
            return allocation_plan
        except Exception as e:
            self.logger.error(f"Error mapping opportunities: {e}")
            return None
    
    async def distribute_opportunity(self, recipient_public, token_amount):
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
                    asset=self.opportunity_asset,
                    amount=str(token_amount)
                )
                .build()
            )
            tx.sign(self.master_keypair)
            response = await self.server.submit_transaction(tx)
            self.logger.info(f"Opportunity distributed: {response['id']}")
            return response['id']
        except TransactionFailedError as e:
            self.logger.error(f"Transaction failed: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Error distributing opportunity: {e}")
            return None

    async def track_opportunity(self, opportunity_id):
        try:
            response = await self.server.transactions().transaction(opportunity_id).call()
            self.logger.info(f"Tracking opportunity {opportunity_id}: {response}")
            return response
        except Exception as e:
            self.logger.error(f"Error tracking opportunity {opportunity_id}: {e}")
            return None

    async def report_opportunities(self, community_data):
        allocation_plan = await self.map_opportunities(community_data)
        if allocation_plan:
            self.logger.info(f"Final Allocation Plan: {allocation_plan}")
        else:
            self.logger.warning("No allocation plan generated.")

# Example usage
async def main():
    inclusive_opportunity = InclusiveOpportunity("https://horizon-testnet.stellar.org", "GABC1234567890", "SXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    community_data = {...}  # Replace with actual community data
    await inclusive_opportunity.report_opportunities(community_data)
    recipient_public = "GXYZ1234567890"
    token_amount = 10
    await inclusive_opportunity.distribute_opportunity(recipient_public, token_amount)

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())
