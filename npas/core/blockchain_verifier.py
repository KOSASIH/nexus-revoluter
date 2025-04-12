from web3 import Web3
import json
import logging
from npas.utils.logger import setup_logger

class BlockchainVerifier:
    def __init__(self, config):
        self.logger = setup_logger("BlockchainVerifier")
        self.w3 = Web3(Web3.HTTPProvider(config["rpc_endpoint"]))
        self.contract_address = config["contract_address"]
        self.load_contract()
        self.account = config["account"]
        self.private_key = config["private_key"]
        self.logger.info("Blockchain Verifier initialized.")

    def load_contract(self):
        """Load the smart contract ABI and create a contract instance."""
        try:
            with open("npas/core/smart_contracts/sync_verifier.json") as f:
                self.abi = json.load(f)
            self.contract = self.w3.eth.contract(address=self.contract_address, abi=self.abi)
            self.logger.info("Smart contract loaded successfully.")
        except FileNotFoundError:
            self.logger.error("Smart contract ABI file not found.")
            raise
        except json.JSONDecodeError:
            self.logger.error("Error decoding the smart contract ABI JSON.")
            raise

    def record_sync(self, change):
        """Record synchronization changes on the blockchain."""
        try:
            tx = self.contract.functions.recordSync(
                change["id"],
                change["content"],
                int(change["timestamp"])
            ).build_transaction({
                "from": self.account,
                "nonce": self.w3.eth.get_transaction_count(self.account),
                "gas": 200000,
                "gasPrice": self.w3.to_wei("20", "gwei")
            })
            signed_tx = self.w3.eth.account.sign_transaction(tx, self.private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            self.logger.info(f"Transaction recorded: {tx_hash.hex()}")
            return tx_hash.hex()
        except ValueError as e:
            self.logger.error(f"Value error while recording to blockchain: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Error recording to blockchain: {e}")
            return None

    def check_transaction_status(self, tx_hash):
        """Check the status of a transaction on the blockchain."""
        try:
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            if receipt.status == 1:
                self.logger.info(f"Transaction {tx_hash} confirmed.")
                return True
            else:
                self.logger.warning(f"Transaction {tx_hash} failed.")
                return False
        except Exception as e:
            self.logger.error(f"Error checking transaction status: {e}")
            return None

if __name__ == "__main__":
    config = {
        "rpc_endpoint": "https://rpc.pi-network.io",  # Placeholder
        "contract_address": "0x...SyncContract",  # Placeholder
        "account": "0x...YourAccount",  # Placeholder
        "private_key": "your_private_key"  # Placeholder
    }
    
    verifier = BlockchainVerifier(config)
    
    sample_change = {
        "id": "1",
        "content": "code update",
        "timestamp": 1634567890
    }
    
    tx_hash = verifier.record_sync(sample_change)
    if tx_hash:
        print(f"Transaction hash: {tx_hash}")
        # Check the transaction status
        status = verifier.check_transaction_status(tx_hash)
        if status is not None:
            print(f"Transaction status: {'Confirmed' if status else 'Failed'}")
