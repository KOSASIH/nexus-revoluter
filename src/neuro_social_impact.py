import logging
import torch
from torch_geometric.nn import GCNConv
from torch_geometric.data import Data
from web3 import Web3
import json

class NeuroSocialImpact:
    def __init__(self, w3_provider, model_path=None):
        self.w3 = Web3(Web3.HTTPProvider(w3_provider))
        self.gnn = GCNConv(in_channels=10, out_channels=1)
        self.logger = self.setup_logging()
        if model_path:
            self.load_model(model_path)

    def setup_logging(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        logger = logging.getLogger("NeuroSocialImpact")
        return logger

    def load_model(self, model_path):
        # Load a pre-trained GNN model if available
        try:
            self.gnn.load_state_dict(torch.load(model_path))
            self.logger.info("Model loaded successfully.")
        except Exception as e:
            self.logger.error(f"Error loading model: {e}")

    def _build_social_graph(self, project_data):
        # Construct a graph from project data
        # Example: project_data should include node features and edge indices
        x = torch.tensor(project_data['features'], dtype=torch.float)  # Node features
        edge_index = torch.tensor(project_data['edges'], dtype=torch.long)  # Edge indices
        return Data(x=x, edge_index=edge_index)

    def predict_impact(self, project_data):
        try:
            graph_data = self._build_social_graph(project_data)
            impact_score = self.gnn(graph_data.x, graph_data.edge_index)
            self.logger.info(f"Predicted impact score: {impact_score.item()}")
            return impact_score.item()
        except Exception as e:
            self.logger.error(f"Error predicting impact: {e}")
            return None

    def allocate_funds(self, project_id, amount, donor_address, private_key):
        try:
            contract = self.w3.eth.contract(address="0x...Charity", abi=...)
            tx = contract.functions.donate(project_id, amount).build_transaction({
                'chainId': self.w3.eth.chain_id,
                'gas': 2000000,
                'gasPrice': self.w3.toWei('50', 'gwei'),
                'nonce': self.w3.eth.getTransactionCount(donor_address),
            })

            # Sign the transaction
            signed_tx = self.w3.eth.account.sign_transaction(tx, private_key)

            # Send the transaction
            tx_hash = self.w3.eth.sendRawTransaction(signed_tx.rawTransaction)
            self.logger.info(f"Transaction sent: {tx_hash.hex()}")

            # Wait for transaction receipt
            receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
            self.logger.info(f"Transaction receipt: {receipt}")
            return receipt
        except Exception as e:
            self.logger.error(f"Error allocating funds: {e}")
            return None

# Example usage
if __name__ == "__main__":
    w3_provider = "https://rpc.pi-network.io"  # Replace with your Ethereum provider
    model_path = "path/to/your/model.pth"  # Replace with your model path

    impact_model = NeuroSocialImpact(w3_provider, model_path)

    # Example project data
    project_data = {
        'features': [[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]],  # Node features
        'edges': [[0, 1], [1, 2], [2, 0]]  # Edge indices
    }

    impact_score = impact_model.predict_impact(project_data)
    if impact_score is not None:
        print(f"Predicted impact score: {impact_score}")

    project_id = 1  # Example project ID
    amount = 100  # Amount to donate
    donor_address = "0x...DonorAddress"  # Replace with the donor's address
    private_key = "0x...PrivateKey"  # Replace with the donor's private key

    receipt = impact_model.allocate_funds(project_id, amount, donor_address, private_key)
    if receipt:
        print(f"Funds allocated successfully. Transaction receipt: {receipt}")
    else:
        print("Failed to allocate funds.")
