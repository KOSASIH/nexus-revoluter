import logging
from ipfshttpclient import connect
from web3 import Web3
import json

class PARMarketplace:
    def __init__(self, ipfs_node, w3_provider, marketplace_contract_address, marketplace_abi):
        self.ipfs = connect(ipfs_node)
        self.w3 = Web3(Web3.HTTPProvider(w3_provider))
        self.marketplace_contract = self.w3.eth.contract(address=marketplace_contract_address, abi=marketplace_abi)
        self.logger = self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        logger = logging.getLogger("PARMarketplace")
        return logger

    def list_item(self, item_data, seller_address, private_key):
        try:
            # Upload item data to IPFS
            ipfs_hash = self.upload_to_ipfs(item_data)
            self.logger.info(f"Item uploaded to IPFS with hash: {ipfs_hash}")

            # Build transaction to list item on the blockchain
            tx = self.build_list_item_transaction(ipfs_hash, seller_address)

            # Sign and send the transaction
            tx_hash = self.send_transaction(tx, private_key)
            self.logger.info(f"Item listed successfully with transaction hash: {tx_hash.hex()}")
            return tx_hash
        except Exception as e:
            self.logger.error(f"Error listing item: {e}")
            return None

    def upload_to_ipfs(self, item_data):
        try:
            ipfs_hash = self.ipfs.add_json(item_data)
            return ipfs_hash
        except Exception as e:
            self.logger.error(f"Error uploading to IPFS: {e}")
            raise

    def build_list_item_transaction(self, ipfs_hash, seller_address):
        try:
            # Estimate gas for the transaction
            gas_estimate = self.marketplace_contract.functions.listItem(ipfs_hash, 31415900).estimateGas({'from': seller_address})
            tx = self.marketplace_contract.functions.listItem(ipfs_hash, 31415900).build_transaction({
                'chainId': self.w3.eth.chain_id,
                'gas': gas_estimate,
                'gasPrice': self.w3.toWei('50', 'gwei'),
                'nonce': self.w3.eth.getTransactionCount(seller_address),
            })
            return tx
        except Exception as e:
            self.logger.error(f"Error building transaction: {e}")
            raise

    def send_transaction(self, tx, private_key):
        try:
            # Sign the transaction
            signed_tx = self.w3.eth.account.sign_transaction(tx, private_key)

            # Send the transaction
            tx_hash = self.w3.eth.sendRawTransaction(signed_tx.rawTransaction)
            return tx_hash
        except Exception as e:
            self.logger.error(f"Error sending transaction: {e}")
            raise

# Example usage
if __name__ == "__main__":
    ipfs_node = "http://localhost:5001"  # Replace with your IPFS node URL
    w3_provider = "https://your.ethereum.node"  # Replace with your Ethereum node URL
    marketplace_contract_address = "0x...Marketplace"  # Replace with your contract address
    marketplace_abi = json.loads('[{"constant":false,"inputs":[{"name":"ipfsHash","type":"string"},{"name":"price","type":"uint256"}],"name":"listItem","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]')

    marketplace = PARMarketplace(ipfs_node, w3_provider, marketplace_contract_address, marketplace_abi)

    item_data = {
        "name": "Example Item",
        "description": "This is an example item for sale.",
        "image": "http://example.com/image.png",
        "category": "Art"
    }
    seller_address = "0x...SellerAddress"  # Replace with the seller's address
    private_key = " "0x...PrivateKey"  # Replace with the seller's private key

    tx_hash = marketplace.list_item(item_data, seller_address, private_key)
    if tx_hash:
        print(f"Item listed successfully with transaction hash: {tx_hash.hex()}")
    else:
        print("Failed to list item.")
