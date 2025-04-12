import logging
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from web3 import Web3
import json

class GenerativeEconomicPlanner:
    def __init__(self, model_name="gpt2", blockchain_url="https://rpc.pi-network.io", policy_contract_address="0x...Policy", policy_contract_abi=None):
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        self.model = GPT2LMHeadModel.from_pretrained(model_name)
        self.w3 = Web3(Web3.HTTPProvider(blockchain_url))
        self.policy_contract = self.w3.eth.contract(address=policy_contract_address, abi=policy_contract_abi)
        self.logger = self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        logger = logging.getLogger("GenerativeEconomicPlanner")
        return logger

    def generate_policy(self, market_data):
        try:
            prompt = f"Generate economic policy for Pi Coin at $314,159.00 given: {market_data}"
            inputs = self.tokenizer(prompt, return_tensors="pt")
            outputs = self.model.generate(inputs["input_ids"], max_length=200)
            policy = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            self.logger.info("Policy generated successfully.")
            return policy
        except Exception as e:
            self.logger.error(f"Error generating policy: {e}")
            return None

    def apply_policy(self, policy, seller_address, private_key):
        try:
            # Build transaction to update policy on the blockchain
            tx = self.policy_contract.functions.updatePolicy(policy).build_transaction({
                'chainId': self.w3.eth.chain_id,
                'gas': 2000000,
                'gasPrice': self.w3.toWei('50', 'gwei'),
                'nonce': self.w3.eth.getTransactionCount(seller_address),
            })

            # Sign the transaction
            signed_tx = self.w3.eth.account.sign_transaction(tx, private_key)

            # Send the transaction
            tx_hash = self.w3.eth.sendRawTransaction(signed_tx.rawTransaction)
            self.logger.info(f"Transaction sent: {tx_hash.hex()}")

            # Wait for transaction receipt
            receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
            self.logger.info(f"Transaction receipt: {receipt}")
            return receipt
        except Exception as e:
            self.logger.error(f"Error applying policy: {e}")
            return None

# Example usage
if __name__ == "__main__":
    policy_contract_address = "0x...Policy"  # Replace with your contract address
    policy_contract_abi = json.loads('[{"constant":false,"inputs":[{"name":"policy","type":"string"}],"name":"updatePolicy","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]')

    planner = GenerativeEconomicPlanner(policy_contract_address=policy_contract_address, policy_contract_abi=policy_contract_abi)

    market_data = {
        "current_price": 31415900,
        "market_trends": "Increasing demand for Pi Coin in digital transactions.",
        "economic_indicators": "Stable inflation rates and growing user base."
    }

    generated_policy = planner.generate_policy(market_data)
    if generated_policy:
        print(f"Generated Policy: {generated_policy}")

        seller_address = "0x...SellerAddress"  # Replace with the seller's address
        private_key = "0x...PrivateKey"  # Replace with the seller's private key

        receipt = planner.apply_policy(generated_policy, seller_address, private_key)
        if receipt:
            print(f"Policy applied successfully. Transaction receipt: {receipt}")
        else:
            print("Failed to apply policy.")
    else:
        print("Failed to generate policy.")
