import json
import requests
import logging
import time
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CrossChainInteroperability:
    def __init__(self, config_file='config.json'):
        self.blockchain_apis = self.load_config(config_file)

    def load_config(self, config_file):
        """Load blockchain API configuration from a JSON file."""
        with open(config_file, 'r') as file:
            config = json.load(file)
        return config['blockchain_apis']

    def send_asset(self, from_chain: str, to_chain: str, amount: float, recipient_address: str) -> dict:
        """Send assets from one blockchain to another."""
        if from_chain not in self.blockchain_apis or to_chain not in self.blockchain_apis:
            raise ValueError("Unsupported blockchain.")

        logging.info(f"Sending {amount} from {from_chain} to {to_chain} to address {recipient_address}.")
        response = self.send_request(from_chain, amount, recipient_address)

        if response.get("status") == "success":
            logging.info(f"Successfully sent {amount} from {from_chain} to {to_chain}. Transaction ID: {response['transaction_id']}")
            return response
        else:
            logging.error(f"Failed to send asset: {response.get('error')}")
            raise Exception("Asset transfer failed.")

    def send_request(self, chain: str, amount: float, recipient_address: str) -> dict:
        """Send request to the blockchain API to send assets."""
        api_info = self.blockchain_apis[chain]
        url = f"{api_info['url']}/send"  # Example endpoint
        headers = {
            "Authorization": f"Bearer {api_info['api_key']}",
            "Content-Type": "application/json"
        }
        payload = {
            "amount": amount,
            "recipient": recipient_address
        }

        response = self.make_request(url, headers, payload)
        return self.handle_response(response)

    def make_request(self, url: str, headers: dict, payload: dict, retries: int = 3) -> requests.Response:
        """Make an HTTP request with retries."""
        for attempt in range(retries):
            try:
                response = requests.post(url, headers=headers, json=payload)
                response.raise_for_status()  # Raise an error for bad responses
                return response
            except requests.exceptions.RequestException as e:
                logging.error(f"Request failed: {e}. Attempt {attempt + 1} of {retries}.")
                time.sleep(2)  # Wait before retrying
        raise Exception("Max retries exceeded for request.")

    def receive_asset(self, from_chain: str, amount: float, sender_address: str) -> dict:
        """Receive assets from another blockchain."""
        if from_chain not in self.blockchain_apis:
            raise ValueError("Unsupported blockchain.")

        logging.info(f"Receiving {amount} from {from_chain} from address {sender_address}.")
        response = self.mock_receive_request(from_chain, amount, sender_address)

        if response.get("status") == "success":
            logging.info(f"Successfully received {amount} from {from_chain}. Transaction ID: {response['transaction_id']}")
            return response
        else:
            logging.error(f"Failed to receive asset: {response.get('error')}")
            raise Exception("Asset reception failed.")

    def handle_response(self, response) -> dict:
        """Handle API response and return a structured dictionary."""
        if response.status_code == 200:
            return response.json()
        else:
            logging.error(f"API Error: {response.status_code} - {response.text}")
            return {"status": "error", "error": response.text}

    def get_chain_balance(self, chain: str, address: str) -> float:
        """Get the balance of an address on a specific blockchain."""
        if chain not in self.blockchain_apis:
            raise ValueError("Unsupported blockchain.")

        logging.info(f"Retrieving balance for address {address} on {chain}.")
        response = self.make_request(f"{self.blockchain_apis[chain]['url']}/balance", 
                                      {"Authorization": f"Bearer {self.blockchain_apis[chain]['api_key']}"}, 
                                      {"address": address})

        if response.get("status") == "success":
            balance = response['balance']
            logging.info(f"Balance for address {address} on {chain}: {balance}")
            return balance
        else:
            logging.error(f"Failed to retrieve balance: {response.get('error')}")
            raise Exception("Balance retrieval failed.")

    def confirm_transaction(self, chain: str, transaction_id: str, timeout: int = 60) -> bool:
        """Confirm a transaction on the specified blockchain."""
        start_time = time.time()
        while time.time() - start_time < timeout:
            logging.info(f"Checking transaction status for {transaction_id} on {chain}.")
            response = self.make_request(f"{self.blockchain_apis[chain]['url']}/transaction/{transaction_id}", 
                                          {"Authorization": f"Bearer {self.blockchain_apis[chain]['api_key']}"}, 
                                          {})

            if response.get("status") == "success" and response['confirmed']:
                logging.info(f"Transaction {transaction_id} confirmed on {chain}.")
                return True
            time.sleep(5)  # Wait before checking again
        logging.warning(f"Transaction {transaction_id} not confirmed within timeout.")
        return False

    def validate_data(self, price_data: float, target_value: float, tolerance: float = 0.05) -> bool:
        """Validate price data against a target value with a specified tolerance."""
        if not isinstance(price_data, (int, float)):
            logging.error("Invalid price data type. Must be a number.")
            return False
        if price_data < 0:
            logging.error("Price data cannot be negative.")
            return False
        lower_bound = target_value * (1 - tolerance)
        upper_bound = target_value * (1 + tolerance)
        is_valid = lower_bound <= price_data <= upper_bound
        if is_valid:
            logging.info(f"Price data {price_data} is valid within the range of {lower_bound} and {upper_bound}.")
        else:
            logging.warning(f"Price data {price_data} is out of the valid range.")
        return is_valid

# Example usage of the CrossChainInteroperability class
if __name__ == "__main__":
    interoperability = CrossChainInteroperability()

    # Send asset from Ethereum to Binance Smart Chain
    try:
        send_response = interoperability.send_asset("Ethereum", "BinanceSmartChain", 1.5, "recipient_bsc_address")
        print(f"Send Response: {send_response}")
        # Confirm the transaction
        interoperability.confirm_transaction("Ethereum", send_response["transaction_id"])
    except Exception as e:
        print(f"Error: {e}")

    # Receive asset from Bitcoin
    try:
        receive_response = interoperability.receive_asset("Bitcoin", 0.5, "sender_btc_address")
        print(f"Receive Response: {receive_response}")
    except Exception as e:
        print(f"Error: {e}")

    # Get balance on Ethereum
    try:
        balance = interoperability.get_chain_balance("Ethereum", "user_eth_address")
        print(f"Ethereum Balance: {balance}")
    except Exception as e:
        print(f"Error: {e}")

    # Validate price data
    price_data = 314200
    target_value = 314000
    is_valid = interoperability.validate_data(price_data, target_value)
    print(f"Is the price data valid? {is_valid}")
