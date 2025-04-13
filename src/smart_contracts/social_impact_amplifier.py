import logging
from stellar_sdk import Server, Keypair, TransactionBuilder, Network, Asset, Payment, ManageData, CreateAccount, SetOptions, ManageData
from stellar_sdk.exceptions import NotFoundError, BadRequestError

class SocialImpactAmplifier:
    def __init__(self, horizon_url, pi_coin_issuer, master_secret):
        self.server = Server(horizon_url)
        self.pi_coin = Asset("PI", pi_coin_issuer)
        self.master_keypair = Keypair.from_secret(master_secret)
        self.logger = logging.getLogger("SocialImpactAmplifier")
        logging.basicConfig(level=logging.INFO)

    def create_project(self, beneficiary_public, goal, project_name):
        """Create a social project with a dedicated account."""
        try:
            master_account = self.server.load_account(self.master_keypair.public_key)
            project_keypair = Keypair.random()

            transaction = (
                TransactionBuilder(
                    source_account=master_account,
                    network_passphrase=Network.PUBLIC_NETWORK_PASSPHRASE,
                    base_fee=100
                )
                .append_create_account_op(
                    destination=project_keypair.public_key,
                    starting_balance="2"
                )
                .append_set_options_op(
                    master_weight=0,
                    low_threshold=2,
                    med_threshold=2,
                    high_threshold=2,
                    signer={"ed25519PublicKey": self.master_keypair.public_key, "weight": 1},
                    signer={"ed25519PublicKey": beneficiary_public, "weight": 1},
                    source=project_keypair.public_key
                )
                .append_manage_data_op(
                    data_name="project_name",
                    data_value=project_name.encode()
                )
                .append_manage_data_op(
                    data_name="goal",
                    data_value=str(goal).encode()
                )
                .build()
            )
            transaction.sign(self.master_keypair)
            response = self.server.submit_transaction(transaction)
            self.logger.info(f"Project created: {response['id']}, Name: {project_name}")
            return response['id'], project_keypair.public_key
        except (NotFoundError, BadRequestError) as e:
            self.logger.error(f"Failed to create project: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            raise

    def donate(self, donor_secret, project_public, amount):
        """Donate Pi Coin to a project."""
        try:
            donor_keypair = Keypair.from_secret(donor_secret)
            donor_account = self.server.load_account(donor_keypair.public_key)

            transaction = (
                TransactionBuilder(
                    source_account=donor_account,
                    network_passphrase=Network.PUBLIC_NETWORK_PASSPHRASE,
                    base_fee=100
                )
                .append_payment_op(
                    destination=project_public,
                    asset=self.pi_coin,
                    amount=str(amount)
                )
                .build()
            )
            transaction.sign(donor_keypair)
            response = self.server.submit_transaction(transaction)
            self.logger.info(f"Donation made: {response['id']}, Amount: {amount}")
            return response['id']
        except (NotFoundError, BadRequestError) as e:
            self.logger.error(f"Failed to donate: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            raise

    def update_project(self, project_public, new_goal=None, new_name=None):
        """Update project details."""
        try:
            project_account = self.server.load_account(project_public)
            transaction = TransactionBuilder(
                source_account=project_account,
                network_passphrase=Network.PUBLIC_NETWORK_PASSPHRASE,
                base_fee=100
            )

            if new_name:
                transaction.append_manage_data_op(
                    data_name="project_name",
                    data_value=new_name.encode()
                )
            if new_goal:
                transaction.append_manage_data_op(
                    data_name="goal",
                    data_value=str(new_goal).encode()
                )

            transaction = transaction.build()
            transaction.sign(self.master_keypair)
            response = self.server.submit_transaction(transaction)
            self.logger.info(f"Project updated: {response['id']}")
            return response['id']
        except (NotFoundError, BadRequestError) as e:
            self.logger.error(f"Failed to update project: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            raise

    def check_project_status(self, project_public):
        """Check the status of a project."""
        try:
            project_account = self server.load_account(project_public)
            project_data = {
                "project_name": None,
                "goal": None,
                "balance": project_account.balances
            }
            for data in project_account.data:
                if data.name == "project_name":
                    project_data["project_name"] = data.value.decode()
                elif data.name == "goal":
                    project_data["goal"] = data.value.decode()

            self.logger.info(f"Project status retrieved: {project_data}")
            return project_data
        except NotFoundError:
            self.logger.error("Project not found.")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error while checking project status: {e}")
            raise

    def withdraw_funds(self, project_secret, amount):
        """Withdraw funds from a project account."""
        try:
            project_keypair = Keypair.from_secret(project_secret)
            project_account = self.server.load_account(project_keypair.public_key)

            transaction = (
                TransactionBuilder(
                    source_account=project_account,
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
            transaction.sign(project_keypair)
            response = self.server.submit_transaction(transaction)
            self.logger.info(f"Funds withdrawn: {response['id']}, Amount: {amount}")
            return response['id']
        except (NotFoundError, BadRequestError) as e:
            self.logger.error(f"Failed to withdraw funds: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error during withdrawal: {e}")
            raise
