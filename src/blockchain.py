import hashlib
import time
import json
from typing import List, Dict, Any, Union
import random
import requests
from flask import Flask, jsonify, request

# Constants
PI_COIN_VALUE = 314159.00  # Fixed value for Pi Coin
TRANSACTION_FEE_PERCENTAGE = 0.01  # 1% transaction fee

class Block:
    def __init__(self, index: int, previous_hash: str, timestamp: float, data: Any, hash: str, nonce: int):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash
        self.nonce = nonce

    def to_dict(self) -> Dict[str, Any]:
        """Convert the block to a dictionary for easy serialization."""
        return {
            "index": self.index,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "data": self.data,
            "hash": self.hash,
            "nonce": self.nonce
        }

class Blockchain:
    def __init__(self):
        self.chain: List[Block] = []
        self.current_transactions: List[Dict[str, Any]] = []
        self.create_genesis_block()
        self.difficulty = 2  # Difficulty for proof of work
        self.wallets: Dict[str, float] = {}  # User wallets

    def create_genesis_block(self):
        """Create the first block in the blockchain."""
        genesis_block = Block(0, "0", time.time(), "Genesis Block", self.hash_block(0, "0", time.time(), "Genesis Block", 0), 0)
        self.chain.append(genesis_block)

    def hash_block(self, index: int, previous_hash: str, timestamp: float, data: Any, nonce: int) -> str:
        """Create a SHA-256 hash of a block."""
        block_string = json.dumps({
            "index": index,
            "previous_hash": previous_hash,
            "timestamp": timestamp,
            "data": data,
            "nonce": nonce
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, previous_hash: str, data: Any) -> (int, str):
        """Simple Proof of Work algorithm."""
        nonce = 0
        hash_value = self.hash_block(len(self.chain), previous_hash, time.time(), data, nonce)
        while not hash_value.startswith('0' * self.difficulty):
            nonce += 1
            hash_value = self.hash_block(len(self.chain), previous_hash, time.time(), data, nonce)
        return nonce, hash_value

    def add_block(self, data: Any) -> Block:
        """Add a new block to the blockchain."""
        previous_block = self.chain[-1]
        nonce, hash_value = self.proof_of_work(previous_block.hash, data)
        new_block = Block(previous_block.index + 1, previous_block.hash, time.time(), data, hash_value, nonce)
        self.chain.append(new_block)
        return new_block

    def add_transaction(self, transaction: Dict[str, Any]) -> None:
        """Add a transaction to the current transactions pool."""
        if transaction['amount'] <= 0:
            raise ValueError("Transaction amount must be positive.")
        
        # Calculate transaction fee
        transaction_fee = transaction['amount'] * TRANSACTION_FEE_PERCENTAGE
        transaction['fee'] = transaction_fee
        transaction['transaction_id'] = random.randint(1000, 9999)  # Simulate a transaction ID
        
        # Update wallets
        self.update_wallets(transaction)
        
        self.current_transactions.append(transaction)

    def update_wallets(self, transaction: Dict[str, Any]) -> None:
        """Update user wallets based on the transaction."""
        sender = transaction['sender']
        recipient = transaction['recipient']
        amount = transaction['amount']
        fee = transaction['fee']

        # Deduct amount + fee from sender
        if sender not in self.wallets:
            self.wallets[sender] = 0
        if self.wallets[sender] < amount + fee:
            raise ValueError("Insufficient funds for transaction.")
        
        self.wallets[sender] -= (amount + fee)
        
        # Add amount to recipient
        if recipient not in self.wallets:
            self.wallets[recipient] = 0
        self.wallets[recipient] += amount

    def validate_chain(self) -> bool:
        """Validate the entire blockchain to ensure integrity."""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != self.hash_block(current_block.index, current_block.previous_hash, current_block.timestamp, current_block.data, current_block.nonce):
                print(f"Invalid hash at block {current_block.index}")
                return False

            if current_block.previous_hash != previous_block.hash:
                print(f"Invalid previous hash at block {current_block.index}")
                return False

        return True

    def get_chain(self) -> List[Dict[str, Any]]:
        """Get the blockchain as a list of dictionaries."""
        return [block.to_dict() for block in self.chain]

    def get_block(self, index: int) -> Union[Block, None]:
        """Get a block by its index."""
        if 0 <= index < len(self.chain):
            return self.chain[index]
        return None

    def __len__(self) -> int:
        """Return the length of the blockchain."""
        return len(self.chain)

    def get_latest_block(self) -> Block:
        """Get the latest block in the blockchain."""
        return self.chain[-1] if self.chain else None

    def print_chain(self) -> None:
        """Print the entire blockchain in a readable format."""
        for block in self.chain:
            print(json.dumps(block.to_dict(), indent=4))

    def create_transaction(self, sender: str, recipient: str, amount: float) -> None:
        """Create a new transaction and add it to the pool."""
        transaction = {
            "sender": sender,
            "recipient": recipient,
            "amount": amount,
            "currency": "Pi"
        }
        self.add_transaction(transaction)

    def mine_block(self) -> Block:
        """Mine a new block with the current transactions."""
        if not self.current_transactions:
            raise ValueError("No transactions to mine.")
        return self.add_block(self.current_transactions)

    def clear_transactions(self) -> None:
        """Clear the current transactions pool."""
        self.current_transactions = []

    def automatic_mining(self) -> None:
        """Automatically mine blocks based on certain conditions."""
        if self.current_transactions:
            self.mine_block()

# Flask app for REST API
app = Flask(__name__)
blockchain = Blockchain()

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    required_fields = ['sender', 'recipient', 'amount']
    if not all(field in values for field in required_fields):
        return 'Missing values', 400
    blockchain.create_transaction(values['sender'], values['recipient'], values['amount'])
    return 'Transaction will be added to the next block', 201

@app.route('/mine', methods=['GET'])
def mine():
    block = blockchain.mine_block()
    response = {
        'message': 'New block mined',
        'index': block.index,
        'transactions': block.data,
        'hash': block.hash
    }
    return jsonify(response), 200

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.get_chain(),
        'length': len(blockchain)
    }
    return jsonify(response), 200

if __name__ == "__main__":
    app.run(debug=True)
