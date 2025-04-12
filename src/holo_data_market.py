import logging
from holochain import HolochainClient
from web3 import Web3
import json

class HoloDataMarket:
    def __init__(self, holo_endpoint, w3_provider, contract_address, contract_abi):
        self.holo = HolochainClient(holo_endpoint)
        self.w3 = Web3(Web3.HTTPProvider(w3_provider))
        self.contract = self.w3.eth.contract(address=contract_address, abi=contract_abi)
        self.logger = self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        logger = logging.getLogger("HoloDataMarket")
        return logger

    def store_data(self, data, zk_proof, seller_address, private_key):
        try:
            # Verify the zero-knowledge proof
            if not self.verify_zk_proof(zk_proof):
                self.logger.error("Invalid zero-knowledge proof.")
                return None

            # Store data in Holochain
            holo_hash = self.holo.store(data)
            self.logger.info(f"Data stored in Holochain with hash: {holo_hash}")

            # Build transaction to list data on the blockchain
            tx = self.contract.functions.listData(holo_hash, zk_proof).build_transaction({
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
            self.logger.error(f"Error storing data: {e}")
            return None

    def verify_zk_proof(self, zk_proof):
        # Placeholder for zero-knowledge proof verification logic
        # Implement the actual verification logic here
        return True  # Assume proof is valid for demonstration

# Example usage
if __name__ == "__main__":
    holo_endpoint = "http://localhost:8888"  # Replace with your Holochain endpoint
    w3_provider = "https://rpc.pi-network.io"  # Replace with your Ethereum provider
    contract_address = "0x...DataMarket"  # Replace with your contract address
    contract_abi = json.loads('[{"constant":false,"inputs":[{"name":"holoHash","type":"string"},{"name":"zkProof","type":"string"}],"name":"listData","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]')

    market = HoloDataMarket(holo_endpoint, w3_provider, contract_address, contract_abi)

    data = {"key": "value"}  # Example data to store
    zk_proof = "example_zk_proof"  # Replace with actual zero-knowledge proof
    seller_address = "0x...SellerAddress"  # Replace with the seller's address
    private_key = "0x...PrivateKey"  # Replace with the seller's private key

    receipt = market.store_data(data, zk_proof, seller_address, private_key)
    if receipt:
        print(f"Data stored and transaction completed. Receipt: {receipt}")
    else:
        print("Failed to store data.")
