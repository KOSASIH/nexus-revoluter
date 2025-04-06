import hashlib
import time
import json
from typing import List, Dict, Any, Union

class Block:
    def __init__(self, index: int, previous_hash: str, timestamp: float, data: Any, hash: str):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash

    def to_dict(self) -> Dict[str, Any]:
        """Convert the block to a dictionary for easy serialization."""
        return {
            "index": self.index,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "data": self.data,
            "hash": self.hash
        }

class Blockchain:
    def __init__(self):
        self.chain: List[Block] = []
        self.current_transactions: List[Dict[str, Any]] = []  # Initialize the current transactions pool
        self.create_genesis_block()

    def create_genesis_block(self):
        """Create the first block in the blockchain."""
        genesis_block = Block(0, "0", time.time(), "Genesis Block", self.hash_block(0, "0", time.time(), "Genesis Block"))
        self.chain.append(genesis_block)

    def hash_block(self, index: int, previous_hash: str, timestamp: float, data: Any) -> str:
        """Create a SHA-256 hash of a block."""
        block_string = json.dumps({
            "index": index,
            "previous_hash": previous_hash,
            "timestamp": timestamp,
            "data": data
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def add_block(self, data: Any) -> Block:
        """Add a new block to the blockchain."""
        previous_block = self.chain[-1]
        index = previous_block.index + 1
        timestamp = time.time()
        hash_value = self.hash_block(index, previous_block.hash, timestamp, data)
        new_block = Block(index, previous_block.hash, timestamp, data, hash_value)
        self.chain.append(new_block)
        return new_block

    def add_transaction(self, transaction: Dict[str, Any]) -> None:
        """Add a transaction to the current transactions pool."""
        # Validate the transaction
        if transaction['amount'] <= 0:
            raise ValueError("Transaction amount must be positive.")
        
        # Add the transaction to the current transactions pool
        self.current_transactions.append(transaction)

    def validate_chain(self) -> bool:
        """Validate the entire blockchain to ensure integrity."""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Check if the hash of the current block is correct
            if current_block.hash != self.hash_block(current_block.index, current_block.previous_hash, current_block.timestamp, current_block.data):
                print(f"Invalid hash at block {current_block.index}")
                return False

            # Check if the previous hash of the current block matches the hash of the previous block
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

# Example usage
if __name__ == "__main__":
    blockchain = Blockchain()
    
    # Adding transactions
    blockchain.add_transaction({"sender": "Alice", "recipient": "Bob", "amount": 10.0, "currency": "Pi"})
    blockchain.add_transaction({"sender": "Bob", "recipient": "Charlie", "amount": 5.0, "currency": "Pi"})

    # Add a block with the current transactions
    blockchain.add_block(blockchain.current_transactions)
    blockchain.current_transactions = []  # Clear the transaction pool after adding to the block

    print("Blockchain valid:", blockchain.validate_chain())
    print("Blockchain:")
    blockchain.print_chain()
    print("Total blocks in blockchain:", len(blockchain))
    print("Block at index 1:", blockchain.get_block(1).to_dict() if blockchain.get_block(1) else "Block not found")
