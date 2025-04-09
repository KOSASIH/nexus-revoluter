import json
import logging
from datetime import datetime
from uuid import uuid4
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DecentralizedEconomy:
    def __init__(self):
        self.users = {}  # Store user data
        self.marketplaces = {}  # Store marketplace data
        self.transactions = []  # Store transaction records
        self.proposals = []  # Store governance proposals
        self.tokens = {}  # Store token data

    def register_user(self, username, initial_balance):
        """Register a new user in the decentralized economy."""
        if username in self.users:
            logging.error("Username already exists.")
            return False
        user_id = str(uuid4())
        self.users[username] = {
            "user_id": user_id,
            "balance": initial_balance,
            "transactions": [],
            "voting_power": 1,  # Simple voting power for governance
            "tokens": 0  # Initial token balance
        }
        logging.info(f"User   registered: {username} with balance {initial_balance}")
        return True

    def create_marketplace(self, marketplace_name):
        """Create a new decentralized marketplace."""
        if marketplace_name in self.marketplaces:
            logging.error("Marketplace already exists.")
            return False
        self.marketplaces[marketplace_name] = {
            "items": {},
            "transactions": []
        }
        logging.info(f"Marketplace created: {marketplace_name}")
        return True

    def list_item(self, marketplace_name, item_name, price, seller_username):
        """List an item for sale in a marketplace."""
        if marketplace_name not in self.marketplaces:
            logging.error("Marketplace does not exist.")
            return False
        if seller_username not in self.users:
            logging.error("Seller does not exist.")
            return False
        item_id = str(uuid4())
        self.marketplaces[marketplace_name]["items"][item_id] = {
            "item_name": item_name,
            "price": price,
            "seller": seller_username
        }
        logging.info(f"Item listed: {item_name} for {price} in {marketplace_name}")
        return item_id

    def purchase_item(self, marketplace_name, item_id, buyer_username):
        """Purchase an item from a marketplace."""
        if marketplace_name not in self.marketplaces:
            logging.error("Marketplace does not exist.")
            return False
        if buyer_username not in self.users:
            logging.error("Buyer does not exist.")
            return False
        item = self.marketplaces[marketplace_name]["items"].get(item_id)
        if not item:
            logging.error("Item does not exist.")
            return False
        if self.users[buyer_username]["balance"] < item["price"]:
            logging.error("Insufficient balance.")
            return False

        # Process the transaction
        self.users[buyer_username]["balance"] -= item["price"]
        self.users[item["seller"]]["balance"] += item["price"]
        transaction_record = {
            "transaction_id": str(uuid4()),
            "item_name": item["item_name"],
            "price": item["price"],
            "buyer": buyer_username,
            "seller": item["seller"],
            "timestamp": datetime.now().isoformat()
        }
        self.transactions.append(transaction_record)
        self.marketplaces[marketplace_name]["transactions"].append(transaction_record)
        self.users[buyer_username]["transactions"].append(transaction_record)
        self.users[item["seller"]]["transactions"].append(transaction_record)

        logging.info(f"Transaction completed: {transaction_record}")
        return transaction_record

    def propose_change(self, proposal_text, proposer_username):
        """Propose a change to the economy or marketplace rules."""
        if proposer_username not in self.users:
            logging.error("Proposer does not exist.")
            return False
        proposal_id = str(uuid4())
        proposal = {
            "proposal_id": proposal_id,
            "text": proposal_text,
            "votes": 0,
            "proposer": proposer_username,
            "timestamp": datetime.now().isoformat()
        }
        self.proposals.append(proposal)
        logging.info(f"Proposal created: {proposal}")
        return proposal_id

    def vote_on_proposal(self, proposal_id, voter_username):
        """Vote on a governance proposal."""
        if voter_username not in self.users:
            logging.error("Voter does not exist.")
            return False
        proposal = next((p for p in self.proposals if p["proposal_id"] == proposal_id), None)
        if not proposal:
            logging.error("Proposal does not exist.")
            return False
        proposal["votes"] += self.users[voter_username]["voting_power"]
        logging.info(f"{voter_username} voted on proposal {proposal_id}. Total votes: {proposal['votes']}")
        return True

    def generate_report(self):
        """Generate a report of the decentralized economy."""
        report = {
            "total_users": len(self.users),
            "total_marketplaces": len(self.marketplaces),
            "total_transactions": len(self.transactions),
            "total_proposals": len(self.proposals),
            "transactions": self.transactions,
            "proposals": self.proposals
        }
        logging.info("Generated decentralized economy report.")
        return report

    def save_report_to_file(self, filename='decentralized_economy_report.json'):
        """Save the economy report to a JSON file."""
        report = self.generate_report()
        with open(filename, 'w') as f:
            json.dump(report, f, indent=4)
        logging.info(f"Decentralized economy report saved to {filename}")

    def create_token(self, token_name, token_supply):
        """Create a new token in the economy."""
        if token_name in self.tokens:
            logging.error("Token already exists.")
            return False
        token_id = str(uuid4())
        self.tokens[token_name] = {
            "token_id": token_id,
            "token_name": token_name,
            "token_supply": token_supply
        }
        logging.info(f"Token created: {token_name} with supply {token_supply}")
        return token_id

    def distribute_tokens(self, token_name, recipient_username, amount):
        """Distribute tokens to a user."""
        if token_name not in self.tokens:
            logging.error("Token does not exist.")
            return False
        if recipient_username not in self.users:
            logging.error("Recipient does not exist.")
            return False
        if amount > self.tokens[token_name]["token_supply"]:
            logging.error("Insufficient token supply.")
            return False

        self.users[recipient_username]["tokens"] += amount
        self.tokens[token_name]["token_supply"] -= amount
        logging.info(f"Tokens distributed: {amount} {token_name} to {recipient_username}")
        return True

    def analyze_user_behavior(self):
        """Analyze user behavior using machine learning."""
        # Load transaction data into a Pandas DataFrame
        df = pd.DataFrame(self.transactions)

        # Define features and target variable
        X = df[["buyer", "seller", "price"]]
        y = df["timestamp"]

        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train a linear regression model
        model = LinearRegression()
        model.fit(X_train, y_train)

        # Make predictions on the testing set
        predictions = model.predict(X_test)

        # Evaluate the model using mean squared error
        mse = mean_squared_error(y_test, predictions)
        logging.info(f"Mean squared error: {mse}")
        return mse

# Example usage
if __name__ == "__main__":
    economy = DecentralizedEconomy()
    economy.register_user("alice", initial_balance=100)
    economy.register_user("bob", initial_balance=50)
    economy.create_marketplace("Art Marketplace")
    item_id = economy.list_item("Art Marketplace", "Mona Lisa", price=30, seller_username="alice")
    transaction = economy.purchase_item("Art Marketplace", item_id, buyer_username="bob")
    proposal_id = economy.propose_change("Increase transaction fee to support more features", "alice")
    economy.vote_on_proposal(proposal_id, "bob")
    economy.save_report_to_file()
    token_id = economy.create_token("Art Token", token_supply=1000)
    economy.distribute_tokens("Art Token", "alice", 100)
    economy.analyze_user_behavior()
