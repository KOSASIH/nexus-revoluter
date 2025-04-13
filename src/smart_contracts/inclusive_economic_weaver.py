import logging
import time
import asyncio
from stellar_sdk import Server, Keypair, TransactionBuilder, Network, Asset, Account, Payment, ManageData

class InclusiveEconomicWeaver:
    def __init__(self, horizon_url, pi_coin_issuer, master_secret):
        self.server = Server(horizon_url)
        self.pi_coin = Asset("PI", pi_coin_issuer)
        self.master_keypair = Keypair.from_secret(master_secret)
        self.logger = logging.getLogger("InclusiveEconomicWeaver")
        self.target_value = 314159  # Target value $314,159.00 (converted to PI by oracle)
        logging.basicConfig(level=logging.INFO)

    async def issue_loan(self, borrower_public, amount, duration_seconds):
        """Issues a microloan to a user through a multi-signature escrow."""
        try:
            master_account = await self.server.load_account(self.master_keypair.public_key)
            escrow_keypair = Keypair.random()
            escrow_public = escrow_keypair.public_key

            # Create escrow account
            transaction = (
                TransactionBuilder(
                    source_account=master_account,
                    network_passphrase=Network.PUBLIC_NETWORK_PASSPHRASE,
                    base_fee=100
                )
                .append_create_account_op(
                    destination=escrow_public,
                    starting_balance="2"  # Minimum for new account
                )
                .append_payment_op(
                    destination=escrow_public,
                    asset=self.pi_coin,
                    amount=str(amount)
                )
                .append_set_options_op(
                    master_weight=0,
                    low_threshold=2,
                    med_threshold=2,
                    high_threshold=2,
                    signer={"ed25519PublicKey": self.master_keypair.public_key, "weight": 1},
                    signer={"ed25519PublicKey": borrower_public, "weight": 1}
                )
                .append_manage_data_op(
                    data_name="loan_due",
                    data_value=str(int(time.time() + duration_seconds)).encode()
                )
                .build()
            )
            transaction.sign(self.master_keypair)
            response = await self.server.submit_transaction(transaction)
            self.logger.info(f"Loan issued: {response['id']}, Borrower: {borrower_public}, Amount: {amount}")
            return response['id']
        except Exception as e:
            self.logger.error(f"Failed to issue loan: {e}")
            raise

    async def repay_loan(self, escrow_secret, amount):
        """Repays a loan from the escrow account."""
        try:
            escrow_keypair = Keypair.from_secret(escrow_secret)
            escrow_account = await self.server.load_account(escrow_keypair.public_key)

            transaction = (
                TransactionBuilder(
                    source_account=escrow_account,
                    network_passphrase=Network.PUBLIC_NETWORK_PASSPHRASE,
                    base_fee=100
                )
                .append_payment_op(
                    destination=self.master_keypair.public_key,
                    asset=self.pi_coin,
                    amount=str(amount)
                )
                .build()
            )
            transaction.sign(escrow_keypair, self.master_keypair)  # Requires second signature
            response = await self.server.submit_transaction(transaction)
            self.logger.info(f"Loan repaid: {response['id']}, Amount: {amount}")
            return response['id']
        except Exception as e:
            self.logger.error(f"Failed to repay loan: {e}")
            raise

    async def tokenize_asset(self, owner_public, asset_value, metadata):
        """Tokenizes a local asset as a custom asset on Stellar."""
        try:
            master_account = await self.server.load_account(self.master_keypair.public_key)
            asset_keypair = Keypair.random()
            asset_code = f"ASSET{asset_keypair.public_key[-4:]}"

            transaction = (
                TransactionBuilder(
                    source_account=master_account,
                    network_passphrase=Network.PUBLIC_NETWORK_PASSPHRASE,
                    base_fee=100
                )
                .append_create_account_op(
                    destination=asset_keypair.public_key,
                    starting_balance="2"
                )
                .append_change_trust_op(
                    asset=Asset(asset_code, asset_keypair.public_key),
                    source=owner_public
                )
                .append_payment_op(
                    destination= owner_public,
                    asset=Asset(asset_code, asset_keypair.public_key),
                    amount=str(asset_value)
                )
                .append_manage_data_op(
                    data_name="asset_metadata",
                    data_value=metadata.encode()
                )
                .build()
            )
            transaction.sign(self.master_keypair)
            response = await self.server.submit_transaction(transaction)
            self.logger.info(f"Asset tokenized: {response['id']}, Owner: {owner_public}, Value: {asset_value}")
            return response['id']
        except Exception as e:
            self.logger.error(f"Failed to tokenize asset: {e}")
            raise

    async def get_loan_status(self, escrow_public):
        """Retrieves the status of a loan associated with the given escrow account."""
        try:
            escrow_account = await self.server.load_account(escrow_public)
            loan_due_data = escrow_account.data.get("loan_due")
            if loan_due_data:
                due_time = int(loan_due_data.decode())
                status = "Due" if time.time() > due_time else "Active"
                self.logger.info(f"Loan status for {escrow_public}: {status}, Due Time: {due_time}")
                return status, due_time
            else:
                self.logger.info(f"No loan data found for {escrow_public}.")
                return "No loan data", None
        except Exception as e:
            self.logger.error(f"Failed to retrieve loan status: {e}")
            raise

    async def close_escrow_account(self, escrow_secret):
        """Closes the escrow account after loan repayment or expiration."""
        try:
            escrow_keypair = Keypair.from_secret(escrow_secret)
            escrow_account = await self.server.load_account(escrow_keypair.public_key)

            transaction = (
                TransactionBuilder(
                    source_account=escrow_account,
                    network_passphrase=Network.PUBLIC_NETWORK_PASSPHRASE,
                    base_fee=100
                )
                .append_account_merge_op(destination=self.master_keypair.public_key)
                .build()
            )
            transaction.sign(escrow_keypair)
            response = await self.server.submit_transaction(transaction)
            self.logger.info(f"Escrow account closed: {response['id']}, Escrow: {escrow_keypair.public_key}")
            return response['id']
        except Exception as e:
            self.logger.error(f"Failed to close escrow account: {e}")
            raise
