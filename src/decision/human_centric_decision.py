import asyncio
from neuro_symbolic import DecisionEngine
from multi_objective import AlignmentOrchestrator
from stellar_sdk import Server, TransactionBuilder, Network, Payment, Asset, Keypair
from hashlib import sha256
from logging import getLogger, StreamHandler, Formatter
from datetime import datetime

class HumanCentricDecision:
    def __init__(self, horizon_url, pi_coin_issuer, master_secret):
        self.engine = DecisionEngine()
        self.orchestrator = AlignmentOrchestrator()
        self.server = Server(horizon_url)
        self.decision_asset = Asset("DECISION", pi_coin_issuer)
        self.master_keypair = Keypair.from_secret(master_secret)
        self.logger = self.setup_logger()
        self.decision_history = []

    def setup_logger(self):
        logger = getLogger("HumanCentricDecision")
        handler = StreamHandler()
        formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel("INFO")
        return logger

    async def make_decision(self, proposal_data):
        try:
            decision = self.engine.process(proposal_data)
            aligned_outcome = self.orchestrator.optimize(decision)
            self.logger.info(f"Decision: {decision}, Outcome: {aligned_outcome}")
            self.decision_history.append((datetime.now(), decision, aligned_outcome))
            return aligned_outcome
        except Exception as e:
            self.logger.error(f"Error in making decision: {e}")
            return None

    async def record_decision(self, voter_public, token_amount):
        try:
            tx = (
                TransactionBuilder(
                    source_account=await self.server.load_account(self.master_keypair.public_key),
                    network_passphrase=Network.PUBLIC_NETWORK_PASSPHRASE,
                    base_fee=100
                )
                .append_payment_op(
                    destination=voter_public,
                    asset=self.decision_asset,
                    amount=str(token_amount)
                )
                .build()
            )
            tx.sign(self.master_keypair)
            response = await self.server.submit_transaction(tx)
            self.logger.info(f"Decision token issued: {response['id']}")
            return response['id']
        except Exception as e:
            self.logger.error(f"Error in recording decision: {e}")
            return None

    def get_decision_history(self):
        return self.decision_history

# Example usage
async def main():
    horizon_url = "https://horizon.stellar.org"
    pi_coin_issuer = "GXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    master_secret = "SXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    
    hcd = HumanCentricDecision(horizon_url, pi_coin_issuer, master_secret)
    
    proposal_data = {"example": "data"}
    decision_outcome = await hcd.make_decision(proposal_data)
    
    if decision_outcome:
        voter_public = "GXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
        token_amount = 10
        await hcd.record_decision(voter_public, token_amount)
    
    history = hcd.get_decision_history()
    print(history)

# Run the example
if __name__ == "__main__":
    asyncio.run(main())
