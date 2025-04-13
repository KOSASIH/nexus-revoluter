import logging
from stellar_sdk import Server, Keypair, TransactionBuilder, Network, Asset, ChangeTrust, ManageData, NotFoundError, BadRequestError

class MetaverseGateway:
    def __init__(self, horizon_url, pi_coin_issuer, master_secret):
        self.server = Server(horizon_url)
        self.pi_coin = Asset("PI", pi_coin_issuer)
        self.master_keypair = Keypair.from_secret(master_secret)
        self.logger = logging.getLogger("MetaverseGateway")
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def create_virtual_asset(self, owner_public, value, metadata):
        """Create a virtual asset as a custom asset."""
        try:
            master_account = self.server.load_account(self.master_keypair.public_key)
            asset_keypair = Keypair.random()
            asset_code = f"VASSET{asset_keypair.public_key[-4:]}"

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
                    destination=owner_public,
                    asset=Asset(asset_code, asset_keypair.public_key),
                    amount=str(value)
                )
                .append_manage_data_op(
                    data_name="virtual_metadata",
                    data_value=metadata.encode()
                )
                .build()
            )
            transaction.sign(self.master_keypair)
            response = self.server.submit_transaction(transaction)
            self.logger.info(f"Virtual asset created: {response['id']}, Owner: {owner_public}")
            return response['id']
        except (NotFoundError, BadRequestError) as e:
            self.logger.error(f"Failed to create virtual asset: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            raise

    def transfer_virtual_asset(self, seller_secret, buyer_public, asset_code, issuer_public, amount):
        """Transfer a virtual asset to the buyer."""
        try:
            seller_keypair = Keypair.from_secret(seller_secret)
            seller_account = self.server.load_account(seller_keypair.public_key)

            transaction = (
                TransactionBuilder(
                    source_account=seller_account,
                    network_passphrase=Network.PUBLIC_NETWORK_PASSPHRASE,
                    base_fee=100
                )
                .append_payment_op(
                    destination=buyer_public,
                    asset=Asset(asset_code, issuer_public),
                    amount=str(amount)
                )
                .append_payment_op(
                    destination=seller_keypair.public_key,
                    asset=self.pi_coin,
                    amount=str(amount),
                    source=buyer_public
                )
                .build()
            )
            transaction.sign(seller_keypair)
            response = self.server.submit_transaction(transaction)
            self.logger.info(f"Virtual asset transferred: {response['id']}, Buyer: {buyer_public}")
            return response['id']
        except (NotFoundError, BadRequestError) as e:
            self.logger.error(f"Failed to transfer asset: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            raise

    def get_asset_info(self, asset_code, issuer_public):
        """Retrieve information about a specific asset."""
        try:
            asset = Asset(asset_code, issuer_public)
            # Here you can add logic to fetch and return asset details
            self.logger.info(f"Asset info retrieved: {asset_code} issued by {issuer_public}")
            return asset
        except Exception as e:
            self.logger.error(f"Failed to retrieve asset info: {e}")
            raise

    def list_assets(self, owner_public):
        """List all assets owned by a specific account."""
        try:
            account = self.server.load_account(owner_public)
            assets = account.balances
            self.logger.info(f"Assets listed for owner: {owner_public}")
            return assets
        except Exception as e:
            self.logger.error(f"Failed to list assets: {e}")
            raise

# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    gateway = MetaverseGateway("https://horizon.st ellar.org", "GABCD1234567890", "S3CR3T_MASTER_KEY")
    owner_public_key = "GXYZ1234567890"
    asset_value = 100
    asset_metadata = "This is a virtual asset."

    # Create a virtual asset
    asset_id = gateway.create_virtual_asset(owner_public_key, asset_value, asset_metadata)
    print(f"Created virtual asset with ID: {asset_id}")

    # Transfer the virtual asset
    seller_secret_key = "S3CR3T_SELLER_KEY"
    buyer_public_key = "GABC9876543210"
    transfer_amount = 50
    transfer_id = gateway.transfer_virtual_asset(seller_secret_key, buyer_public_key, "VASSET1234", "GABCD1234567890", transfer_amount)
    print(f"Transferred virtual asset with ID: {transfer_id}")

    # Get asset info
    asset_info = gateway.get_asset_info("VASSET1234", "GABCD1234567890")
    print(f"Retrieved asset info: {asset_info}")

    # List assets owned by a specific account
    owned_assets = gateway.list_assets(owner_public_key)
    print(f"Assets owned by {owner_public_key}: {owned_assets}")
