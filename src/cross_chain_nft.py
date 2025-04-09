import json
import logging
from uuid import uuid4
import requests
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CrossChainNFT:
    def __init__(self):
        self.nfts = {}  # Store NFT data
        self.blockchains = {}  # Store blockchain configurations
        self.event_log = []  # Log of events

    def register_blockchain(self, blockchain_name, api_url):
        """Register a new blockchain for NFT operations."""
        if blockchain_name in self.blockchains:
            logging.error("Blockchain already registered.")
            return False
        self.blockchains[blockchain_name] = {
            "api_url": api_url,
            "nft_contract": None  # Placeholder for NFT contract address
        }
        logging.info(f"Blockchain registered: {blockchain_name}")
        return True

    def mint_nft(self, blockchain_name, owner, metadata):
        """Mint a new NFT on the specified blockchain."""
        if blockchain_name not in self.blockchains:
            logging.error("Blockchain not registered.")
            return False
        nft_id = str(uuid4())
        nft_data = {
            "nft_id": nft_id,
            "owner": owner,
            "metadata": metadata,
            "blockchain": blockchain_name
        }
        self.nfts[nft_id] = nft_data
        self.event_log.append({
            "event": "mint",
            "nft_id": nft_id,
            "owner": owner,
            "timestamp": datetime.now().isoformat()
        })
        logging.info(f"NFT minted: {nft_data}")
        return nft_id

    def transfer_nft(self, nft_id, new_owner):
        """Transfer an NFT to a new owner across blockchains."""
        if nft_id not in self.nfts:
            logging.error("NFT does not exist.")
            return False
        nft_data = self.nfts[nft_id]
        old_owner = nft_data["owner"]
        nft_data["owner"] = new_owner
        self.event_log.append({
            "event": "transfer",
            "nft_id": nft_id,
            "old_owner": old_owner,
            "new_owner": new_owner,
            "timestamp": datetime.now().isoformat()
        })
        logging.info(f"NFT transferred: {nft_id} from {old_owner} to {new_owner}")
        return True

    def get_nft_metadata(self, nft_id):
        """Retrieve metadata for a specific NFT."""
        if nft_id not in self.nfts:
            logging.error("NFT does not exist.")
            return None
        return self.nfts[nft_id]["metadata"]

    def log_event(self, event_type, details):
        """Log an event for auditing purposes."""
        event_record = {
            "event_type": event_type,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.event_log.append(event_record)
        logging.info(f"Event logged: {event_record}")

    def save_event_log(self, filename='event_log.json'):
        """Save the event log to a JSON file."""
        with open(filename, 'w') as f:
            json.dump(self.event_log, f, indent=4)
        logging.info(f"Event log saved to {filename}")

    def fetch_nft_data_from_blockchain(self, blockchain_name, nft_id):
        """Fetch NFT data from the specified blockchain."""
        if blockchain_name not in self.blockchains:
            logging.error("Blockchain not registered.")
            return None
        api_url = self.blockchains[blockchain_name]["api_url"]
        response = requests.get(f"{api_url}/nft/{nft_id}")
        if response.status_code == 200:
            return response.json()
        else:
            logging.error("Failed to fetch NFT data from blockchain.")
            return None

    def batch_mint_nfts(self, blockchain_name, owner, metadata_list):
        """Mint multiple NFTs in a single transaction."""
        nft_ids = []
        for metadata in metadata_list:
            nft_id = self.mint_nft(blockchain_name, owner, metadata)
            if nft_id:
                nft_ids.append(nft_id)
        return nft_ids

    def batch_transfer_nfts(self, nft_ids, new_owner):
        """Transfer multiple NFTs to a new owner."""
        for nft_id in nft_ids:
            self.transfer_nft(nft_id, new_owner)

    def set_royalties(self, nft_id, royalty_percentage):
        """Set royalty percentage for an NFT."""
        if nft_id not in self.nfts:
            logging.error("NFT does not exist.")
            return False
        self.nfts[nft_id]["royalty"] = royalty_percentage
        logging.info(f"Royalty set for NFT {nft_id}: {royalty_percentage}%")
        return True

    def get_royalties(self, nft_id):
        """Get royalty information for an NFT."""
        if nft_id not in self.nfts:
            logging.error("NFT does not exist.")
            return None
        return self.nfts[nft_id].get("royalty", 0)

# Example usage
if __name__ == "__main__":
    cross_chain_nft = CrossChainNFT()
    cross_chain_nft.register_blockchain("Ethereum", "https://api.ethereum.org")
    cross_chain_nft.register_blockchain("Binance Smart Chain", "https://api.bsc.org")
    
    # Mint multiple NFTs
    metadata_list = [
        {"name": "Mona Lisa", "description": "A famous painting by Leonardo da Vinci.", "image": "ipfs://Qm...examplehash"},
        {"name": "Starry Night", "description": "A painting by Vincent van Gogh.", "image": "ipfs://Qm...examplehash2"}
    ]
    nft_ids = cross_chain_nft.batch_mint_nfts("Ethereum", "alice", metadata_list)
    
    # Transfer NFTs
    cross_chain_nft.batch_transfer_nfts(nft_ids, "bob")
    
    # Set royalties
    for nft_id in nft_ids:
        cross_chain_nft.set_royalties(nft_id, 10)  # 10% royalty
    
    # Retrieve NFT metadata
    for nft_id in nft_ids:
        nft_metadata = cross_chain_nft.get_nft_metadata(nft_id)
        print("NFT Metadata:", nft_metadata)
    
    # Save event log
    cross_chain_nft.save_event_log()
