import json
import logging
import hashlib
import time
import random
from threading import Thread, Event

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PaymentChannel:
    def __init__(self, party_a: str, party_b: str, capacity: float, multi_sig_required: int = 2):
        self.party_a = party_a
        self.party_b = party_b
        self.capacity = capacity
        self.balance_a = capacity
        self.balance_b = 0.0
        self.channel_id = self.generate_channel_id()
        self.is_open = True
        self.multi_sig_required = multi_sig_required
        self.transaction_history = []
        logging.info(f"Payment channel created between {party_a} and {party_b} with capacity {capacity}.")

    def generate_channel_id(self) -> str:
        """Generate a unique channel ID based on the parties involved."""
        return hashlib.sha256(f"{self.party_a}-{self.party_b}-{time.time()}".encode()).hexdigest()

    def fund_channel(self, amount: float) -> None:
        """Fund the payment channel."""
        if amount > self.capacity:
            raise ValueError("Amount exceeds channel capacity.")
        self.balance_a += amount
        logging.info(f"{self.party_a} funded the channel with {amount}. New balance: {self.balance_a}")

    def make_payment(self, amount: float, from_party: str) -> None:
        """Make a payment through the channel."""
        if not self.is_open:
            raise Exception("Channel is closed.")
        if from_party == self.party_a:
            if amount > self.balance_a:
                raise ValueError("Insufficient balance for payment.")
            self.balance_a -= amount
            self.balance_b += amount
            self.transaction_history.append((time.time(), from_party, amount))
            logging.info(f"{self.party_a} paid {amount} to {self.party_b}.")
        elif from_party == self.party_b:
            if amount > self.balance_b:
                raise ValueError("Insufficient balance for payment.")
            self.balance_b -= amount
            self.balance_a += amount
            self.transaction_history.append((time.time(), from_party, amount))
            logging.info(f"{self.party_b} paid {amount} to {self.party_a}.")
        else:
            raise ValueError("Invalid party.")

    def close_channel(self) -> dict:
        """Close the payment channel and settle the final balance."""
        if not self.is_open:
            raise Exception("Channel is already closed.")
        self.is_open = False
        logging.info(f"Closing channel {self.channel_id}. Final balances: {self.balance_a}, {self.balance_b}")
        return self.settle_on_chain()

    def settle_on_chain(self) -> dict:
        """Mock function to settle the final balance on the blockchain."""
        # Simulate a delay for on-chain settlement
        time.sleep(1)
        logging.info(f"Settling channel {self.channel_id} on-chain.")
        return {
            "channel_id": self.channel_id,
            "final_balance_a": self.balance_a,
            "final_balance_b": self.balance_b,
            "transaction_history": self.transaction_history
        }

    def dispute_resolution(self, timeout: int = 30) -> None:
        """Handle dispute resolution with a timeout."""
        logging.info("Dispute resolution initiated.")
        event = Event()

        def wait_for_resolution():
            event.wait(timeout)
            if not event.is_set():
                logging.warning("Dispute resolution timed out. Channel will be closed.")
                self.close_channel()

        thread = Thread(target=wait_for_resolution)
        thread.start()

        # Simulate some resolution process
        time.sleep(random.randint(1, timeout))
        event.set()
        logging.info("Dispute resolved successfully.")

# Example usage of the PaymentChannel class
if __name__ == "__main__":
    # Create a payment channel between two parties
    channel = PaymentChannel("Alice", "Bob", 100.0)

    # Fund the channel
    channel.fund_channel(50.0)

    # Make payments
    try:
        channel.make_payment(20.0, "Alice")
        channel.make_payment(10.0, "Bob")
    except ValueError as e:
        logging.error(f"Payment error: {e}")

    # Close the channel
    final_settlement = channel.close_channel()
    print(f"Final settlement: {json.dumps(final_settlement, indent=2)}")

    # Simulate dispute resolution
    channel.dispute_resolution()
