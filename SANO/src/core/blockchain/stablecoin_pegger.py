import ccxt  # Library for interacting with exchanges
from web3 import Web3
import json
import logging
import os
import time

class StablecoinPegger:
    def __init__(self, target_price=314159.00, tolerance=0.05, w3_provider="https://rpc.pi-network.io", exchanges=None):
        self.target_price = target_price
        self.tolerance = tolerance
        self.w3 = Web3(Web3.HTTPProvider(w3_provider))
        self.logger = logging.getLogger("StablecoinPegger")
        self.exchanges = exchanges if exchanges else [ccxt.binance(), ccxt.kraken()]  # Default exchanges
        self.default_account = self.w3.eth.default_account

    def fetch_market_price(self):
        """Fetch the market price of Pi Coin from various exchanges."""
        prices = []
        for exchange in self.exchanges:
            try:
                ticker = exchange.fetch_ticker("PI/USD")
                prices.append(ticker["last"])
            except Exception as e:
                self.logger.error(f"Failed to fetch price from {exchange}: {e}")
        return sum(prices) / len(prices) if prices else None

    def adjust_supply(self, current_price):
        """Adjust the supply of Pi Coin to maintain price stability."""
        if current_price is None:
            self.logger.error("Market price is not available.")
            return
        
        deviation = abs(current_price - self.target_price) / self.target_price
        if deviation > self.tolerance:
            action = "burn" if current_price < self.target_price else "mint"
            amount = deviation * 1000000  # Example: adjust 1M tokens
            self.logger.info(f"Action: {action} {amount} PI for stabilization.")
            self._execute_supply_action(action, amount)

    def _execute_supply_action(self, action, amount):
        """Execute burn/mint through smart contract."""
        contract_address = "0x...PiCoinContract"  # Placeholder
        with open("smart_contracts/stablecoin_abi.json") as f:
            abi = json.load(f)
        
        contract = self.w3.eth.contract(address=contract_address, abi=abi)
        if action == "burn":
            tx = contract.functions.burn(int(amount)).buildTransaction({
                "from": self.default_account,
                "nonce": self.w3.eth.getTransactionCount(self.default_account),
                "gas": 2000000,
                "gasPrice": self.w3.toWei('50', 'gwei')
            })
        else:
            tx = contract.functions.mint(int(amount)).buildTransaction({
                "from": self.default_account,
                "nonce": self.w3.eth.getTransactionCount(self.default_account),
                "gas": 2000000,
                "gasPrice": self.w3.toWei('50', 'gwei')
            })
        
        signed_tx = self.w3.eth.account.sign_transaction(tx, private_key=os.getenv("PRIVATE_KEY"))
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        self.logger.info(f"Transaction {action} sent: {tx_hash.hex()}")
        self.confirm_transaction(tx_hash)

    def confirm_transaction(self, tx_hash):
        """Confirm the transaction on the blockchain."""
        while True:
            try:
                receipt = self.w3.eth.waitForTransactionReceipt(tx_hash, timeout=120)
                if receipt.status == 1:
                    self.logger.info(f"Transaction confirmed: {tx_hash.hex()}")
                    break
                else:
                    self.logger.error(f"Transaction failed: {tx_hash.hex()}")
                    break
            except Exception as e:
                self.logger.warning(f"Waiting for transaction confirmation: {e}")
                time.sleep(5)

    def monitor_market(self, interval=60):
        """Continuously monitor the market price and adjust supply."""
        while True:
            market_price = self.fetch_market_price()
            self.logger.info(f"Market price: {market_price}")
            self.adjust_supply(market_price)
            time.sleep(interval)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    pegger = StablecoinPegger()
    pegger.monitor_market(interval=60)  # Monitor market every 60 seconds
