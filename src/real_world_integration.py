import json
import random
import requests
import asyncio
import logging
from datetime import datetime
import matplotlib.pyplot as plt
import yaml

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load configuration from a YAML file
def load_config():
    with open("config.yaml", "r") as file:
        return yaml.safe_load(file)

class IoTDevice:
    def __init__(self, device_id, device_type, location):
        self.device_id = device_id
        self.device_type = device_type  # e.g., 'solar_panel', 'wind_turbine', 'smart_meter'
        self.location = location
        self.data = {}

    async def collect_data(self):
        """Simulate data collection from the IoT device asynchronously."""
        await asyncio.sleep(random.uniform(0.1, 0.5))  # Simulate network delay
        if self.device_type in ['solar_panel', 'wind_turbine']:
            self.data = {
                "energy_produced": self.simulate_energy_production(),
                "timestamp": datetime.now().isoformat()
            }
        elif self.device_type == 'smart_meter':
            self.data = {
                "energy_consumed": self.simulate_energy_consumption(),
                "timestamp": datetime.now().isoformat()
            }
        return self.data

    def simulate_energy_production(self):
        """Simulate energy production based on device type."""
        return round(random.uniform(0.5, 5.0), 2)  # Simulated energy production in kWh

    def simulate_energy_consumption(self):
        """Simulate energy consumption for smart meters."""
        return round(random.uniform(0.1, 3.0), 2)  # Simulated energy consumption in kWh

class TokenizedAsset:
    def __init__(self, asset_id, asset_type, owner):
        self.asset_id = asset_id
        self.asset_type = asset_type  # e.g., 'real_estate', 'art', 'carbon_credit'
        self.owner = owner
        self.tokenized_value = 0  # Value in tokens

    def tokenize_asset(self, value):
        """Tokenize the asset and set its value."""
        self.tokenized_value = value
        logging.info(f"Asset {self.asset_id} tokenized with value: {self.tokenized_value} tokens.")

    def transfer_ownership(self, new_owner):
        """Transfer ownership of the tokenized asset."""
        self.owner = new_owner
        logging.info(f"Asset {self.asset_id} ownership transferred to: {self.owner}")

class RealWorldIntegration:
    def __init__(self, config):
        self.iot_devices = []
        self.tokenized_assets = []
        self.api_url = config['blockchain_api_url']

    def add_iot_device(self, device):
        """Add an IoT device to the integration system."""
        self.iot_devices.append(device)
        logging.info(f"Added IoT device: {device.device_id}")

    def add_tokenized_asset(self, asset):
        """Add a tokenized asset to the integration system."""
        self.tokenized_assets.append(asset)
        logging.info(f"Added tokenized asset: {asset.asset_id}")

    async def collect_iot_data(self):
        """Collect data from all IoT devices asynchronously."""
        tasks = [device.collect_data() for device in self.iot_devices]
        results = await asyncio.gather(*tasks)
        for device, data in zip(self.iot_devices, results):
            self.log_iot_data(device.device_id, data)

    def log_iot_data(self, device_id, data):
        """Log IoT data to a JSON file."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "device_id": device_id,
            "data": data
        }
        with open("iot_data_log.json", "a") as log_file:
            log_file.write(json.dumps(log_entry) + "\n")
        logging.info(f"Logged data from device {device_id}: {data}")

    def trade_tokenized_asset(self, asset _id, new_owner):
        """Trade a tokenized asset to a new owner."""
        for asset in self.tokenized_assets:
            if asset.asset_id == asset_id:
                asset.transfer_ownership(new_owner)
                self.record_transaction_on_blockchain(asset_id, new_owner)
                break
        else:
            logging.warning(f"Asset {asset_id} not found.")

    def record_transaction_on_blockchain(self, asset_id, new_owner):
        """Record the asset transfer on the blockchain."""
        payload = {
            "asset_id": asset_id,
            "new_owner": new_owner,
            "timestamp": datetime.now().isoformat()
        }
        try:
            response = requests.post(self.api_url, json=payload)
            response.raise_for_status()  # Raise an error for bad responses
            logging.info(f"Successfully recorded transaction for asset {asset_id} to new owner {new_owner}.")
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to record transaction on blockchain: {e}")

    def visualize_data(self):
        """Visualize the collected IoT data."""
        timestamps = []
        energy_values = []
        for device in self.iot_devices:
            if device.data:
                timestamps.append(device.data['timestamp'])
                if device.device_type in ['solar_panel', 'wind_turbine']:
                    energy_values.append(device.data['energy_produced'])
                elif device.device_type == 'smart_meter':
                    energy_values.append(device.data['energy_consumed'])

        plt.figure(figsize=(10, 5))
        plt.plot(timestamps, energy_values, marker='o')
        plt.title('IoT Device Data Visualization')
        plt.xlabel('Timestamp')
        plt.ylabel('Energy (kWh)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def aggregate_data(self):
        """Aggregate data from IoT devices for better insights."""
        total_energy_produced = 0
        total_energy_consumed = 0
        for device in self.iot_devices:
            if device.device_type == 'solar_panel' or device.device_type == 'wind_turbine':
                total_energy_produced += device.data.get('energy_produced', 0)
            elif device.device_type == 'smart_meter':
                total_energy_consumed += device.data.get('energy_consumed', 0)
        logging.info(f"Total Energy Produced: {total_energy_produced} kWh")
        logging.info(f"Total Energy Consumed: {total_energy_consumed} kWh")

# Example usage
if __name__ == "__main__":
    config = load_config()
    integration = RealWorldIntegration(config)

    # Add IoT devices
    solar_panel = IoTDevice(device_id="SolarPanel_001", device_type="solar_panel", location="Rooftop")
    wind_turbine = IoTDevice(device_id="WindTurbine_001", device_type="wind_turbine", location="Field")
    smart_meter = IoTDevice(device_id="SmartMeter_001", device_type="smart_meter", location="Home")

    integration.add_iot_device(solar_panel)
    integration.add_iot_device(wind_turbine)
    integration.add_iot_device(smart_meter)

    # Collect data from IoT devices asynchronously
    asyncio.run(integration.collect_iot_data())

    # Aggregate data for insights
    integration.aggregate_data()

    # Add tokenized assets
    carbon_credit_asset = TokenizedAsset(asset_id="CarbonCredit_001", asset_type="carbon_credit", owner="Miner_001")
    real_estate_asset = TokenizedAsset(asset_id="RealEstate_001", asset_type="real_estate", owner="Investor_001")

    integration.add_tokenized_asset(carbon_credit_asset)
    integration.add_tokenized_asset(real_estate_asset)

    # Tokenize assets
    carbon_credit_asset.tokenize_asset(value=100)
    real_estate_asset.tokenize_asset(value=500)

    # Trade tokenized asset
    integration.trade_tokenized_asset(asset_id="CarbonCredit_001", new_owner="Miner_002")
    integration.trade_tokenized_asset(asset_id="RealEstate_001", new_owner="Investor_002")

    # Log the final state of tokenized assets
    for asset in integration.tokenized_assets:
        logging.info(f"Asset ID: {asset.asset_id}, Owner: {asset.owner}, Value: {asset.tokenized_value} tokens")

    # Visualize the collected data
    integration.visualize_data()
