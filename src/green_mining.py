import time
import random
import json
import requests
from datetime import datetime

class GreenMining:
    def __init__(self, miner_id, energy_source, carbon_credit_rate):
        self.miner_id = miner_id
        self.energy_source = energy_source  # e.g., 'solar', 'wind', 'hydro'
        self.carbon_credit_rate = carbon_credit_rate  # Carbon credits earned per kWh
        self.energy_consumed = 0  # in kWh
        self.carbon_credits_earned = 0
        self.api_url = "https://api.carboncredits.com"  # Placeholder for carbon credit API

    def mine(self):
        """Simulate the mining process with eco-friendly considerations."""
        start_time = time.time()
        mining_duration = random.randint(1, 5)  # Simulate mining duration in seconds
        time.sleep(mining_duration)  # Simulate time taken to mine a block

        # Calculate energy consumed based on mining duration and energy source
        energy_used = self.calculate_energy_consumed(mining_duration)
        self.energy_consumed += energy_used

        # Calculate carbon credits earned
        credits = self.calculate_carbon_credits(energy_used)
        self.carbon_credits_earned += credits

        # Log mining activity
        self.log_mining_activity(mining_duration, energy_used, credits)

        # Optionally trade carbon credits
        self.trade_carbon_credits(credits)

        return {
            "miner_id": self.miner_id,
            "mining_duration": mining_duration,
            "energy_used": energy_used,
            "carbon_credits_earned": credits,
            "total_carbon_credits": self.carbon_credits_earned
        }

    def calculate_energy_consumed(self, duration):
        """Calculate energy consumed based on the energy source."""
        # Example energy consumption rates (kWh per second)
        energy_rates = {
            'solar': 0.5,
            'wind': 0.3,
            'hydro': 0.4,
            'grid': 1.0  # Non-renewable source
        }
        return energy_rates.get(self.energy_source, 1.0) * duration

    def calculate_carbon_credits(self, energy_used):
        """Calculate carbon credits based on energy consumed."""
        return energy_used * self.carbon_credit_rate

    def log_mining_activity(self, duration, energy_used, credits):
        """Log mining activity to a JSON file."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "miner_id": self.miner_id,
            "mining_duration": duration,
            "energy_used": energy_used,
            "carbon_credits_earned": credits
        }
        with open("mining_activity_log.json", "a") as log_file:
            log_file.write(json.dumps(log_entry) + "\n")

    def trade_carbon_credits(self, credits):
        """Trade carbon credits with an external API."""
        if credits > 0:
            payload = {
                "miner_id": self.miner_id,
                "credits": credits
            }
            response = requests.post(f"{self.api_url}/trade", json=payload)
            if response.status_code == 200:
                print(f"Successfully traded {credits} carbon credits.")
            else:
                print(f"Failed to trade carbon credits: {response.text}")

    def get_status(self):
        """Return the current status of the miner."""
        return {
            "miner_id": self.miner_id,
            "energy_source": self.energy_source,
            "energy_consumed": self.energy_consumed,
            "carbon_credits_earned": self.carbon_credits_earned
        }

# Example usage
if __name__ == "__main__":
    miner = GreenMining(miner_id="Miner_001", energy_source="solar", carbon_credit_rate=0.1)
    
    # Simulate mining for a number of iterations
    for _ in range(5):
        result = miner.mine()
        print(result)

    # Print current status
    print(miner.get_status())
