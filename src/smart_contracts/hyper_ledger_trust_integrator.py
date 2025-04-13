import logging
import time
from stellar_sdk import Server, Keypair, TransactionBuilder, Network, Asset, Payment, NotFoundError

class HyperledgerTrustIntegrator:
    def __init__(self, horizon_url, pi_coin_issuer, master_secret):
        self.server = Server(horizon_url)
        self.pi_coin = Asset("PI", pi_coin_issuer)
        self.master_keypair = Keypair.from_secret(master_secret)
        self.logger = logging.getLogger("HyperledgerTrustIntegrator")
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(handler)

    def initiate_cross_chain_transfer(self, sender_secret, recipient_public, amount, target_chain):
        """Initiate cross-chain transfer using escrow."""
        try:
            sender_keypair = Keypair.from_secret(sender_secret)
            sender_account = self.server.load_account(sender_keypair.public_key)
            escrow_keypair = Keypair.random()

            transaction = (
                TransactionBuilder(
                    source_account=sender_account,
                    network_passphrase=Network.PUBLIC_NETWORK_PASSPHRASE,
                    base_fee=100
                )
                .append_create_account_op(
                    destination=escrow_keypair.public_key,
                    starting_balance="2"
                )
                .append_payment_op(
                    destination=escrow_keypair.public_key,
                    asset=self.pi_coin,
                    amount=str(amount)
                )
                .append_set_options_op(
                    master_weight=0,
                    low_threshold=2,
                    med_threshold=2,
                    high_threshold=2,
                    signer={"ed25519PublicKey": self.master_keypair.public_key, "weight": 1},
                    signer={"ed25519PublicKey": sender_keypair.public_key, "weight": 1}
                )
                .append_manage_data_op(
                    data_name="target_chain",
                    data_value=target_chain.encode()
                )
                .build()
            )
            transaction.sign(sender_keypair)
            response = self.server.submit_transaction(transaction)
            self.logger.info(f"Cross-chain transfer initiated: {response['id']}, Target: {target_chain}")
            return response['id'], escrow_keypair.secret
        except Exception as e:
            self.logger.error(f"Failed to initiate transfer: {e}")
            raise

    def complete_cross_chain_transfer(self, escrow_secret, recipient_public):
        """Complete cross-chain transfer."""
        try:
            escrow_keypair = Keypair.from_secret(escrow_secret)
            escrow_account = self.server.load_account(escrow_keypair.public_key)

            transaction = (
                TransactionBuilder(
                    source_account=escrow_account,
                    network_passphrase=Network.PUBLIC_NETWORK_PASSPHRASE,
                    base_fee=100
                )
                .append_payment_op(
                    destination=recipient_public,
                    asset=self.pi_coin,
                    amount=str(escrow_account.balances[0].balance)
                )
                .build()
            )
            transaction.sign(escrow_keypair, self.master_keypair)
            response = self.server.submit_transaction(transaction)
            self.logger.info(f"Cross-chain transfer completed: {response['id']}, Recipient: {recipient_public}")
            return response['id']
        except Exception as e:
            self.logger.error(f"Failed to complete transfer: {e}")
            raise

    def monitor_transaction(self, transaction_id):
        """Monitor the status of a transaction."""
        try:
            while True:
                response = self.server.transactions().transaction(transaction_id)
                self.logger.info(f"Transaction {transaction_id} status: {response['status']}")
                if response['status'] in ['completed', 'failed']:
                    break
                time.sleep(5)  # Wait before checking again
        except NotFoundError:
            self.logger.warning(f"Transaction {transaction_id} not found.")
        except Exception as e:
            self.logger.error(f"Error monitoring transaction: {e}")

    def get_account_balance(self, public_key):
        """Retrieve the balance of an account."""
        try:
            account = self.server.load_account(public_key)
            balances = {balance['asset_code']: balance['balance'] for balance in account.balances}
            self.logger.info(f"Account {public_key} balances: {balances}")
            return balances
        except Exception as e:
            self.logger.error(f"Failed to retrieve account balance: {e}")
            raise
