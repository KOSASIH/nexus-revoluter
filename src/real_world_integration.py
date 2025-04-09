import json
import random
import requests
from datetime import datetime

class IoTDevice:
    def __init__(self, device_id, device_type, location):
        self.device_id = device_id
        self.device_type = device_type  # e.g., 'solar_panel', 'wind_turbine', 'smart_meter'
        self.location = location
        self.data = {}

    def collect_data(self):
        """Simulate data collection from the IoT device."""
        if self.device_type == 'solar_panel':
            self.data = {
                "energy_produced": self.simulate_energy_production(),
                "temperature": self.simulate_temperature(),
                "timestamp": datetime.now().isoformat()
            }
        elif self.device_type == 'wind_turbine':
            self.data = {
                "energy_produced": self.simulate_energy_production(),
                "wind_speed": self.simulate_wind_speed(),
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

    def simulate_temperature(self):
        """Simulate temperature for solar panels."""
        return round(random.uniform(15.0, 35.0), 2)  # Simulated temperature in Celsius

    def simulate_wind_speed(self):
        """Simulate wind speed for wind turbines."""
        return round(random.uniform(0.0, 25.0), 2)  # Simulated wind speed in m/s

class TokenizedAsset:
    def __init__(self, asset_id, asset_type, owner):
        self.asset_id = asset_id
        self.asset_type = asset_type  # e.g., 'real_estate', 'art', 'carbon_credit'
        self.owner = owner
        self.tokenized_value = 0  # Value in tokens

    def tokenize_asset(self, value):
        """Tokenize the asset and set its value."""
        self.tokenized_value = value
        print(f"Asset {self.asset_id} tokenized with value: {self.tokenized_value} tokens.")

    def transfer_ownership(self, new_owner):
        """Transfer ownership of the tokenized asset."""
        self.owner = new_owner
        print(f"Asset {self.asset_id} ownership transferred to: {self.owner}")

class RealWorldIntegration:
    def __init__(self):
        self.iot_devices = []
        self.tokenized_assets = []

    def add_iot_device(self, device):
        """Add an IoT device to the integration system."""
        self.iot_devices.append(device)
        print(f"Added IoT device: {device.device_id}")

    def add_tokenized_asset(self, asset):
        """Add a tokenized asset to the integration system."""
        self.tokenized_assets.append(asset)
        print(f"Added tokenized asset: {asset.asset_id}")

    def collect_iot_data(self):
        """Collect data from all IoT devices."""
        for device in self.iot_devices:
            data = device.collect_data()
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
        print(f"Logged data from device {device_id}: {data}")

    def trade_tokenized_asset(self, asset_id, new_owner):
        """Trade a tokenized asset to a new owner."""
        for asset in self.tokenized_assets:
            if asset.asset_id == asset_id:
                asset.transfer_ownership(new_owner)
                self.record_transaction_on_blockchain(asset_id, new_owner)
                break
        else:
            print(f"Asset {asset_id} not found.")

    def record_transaction_on_blockchain(self, asset_id, new_owner ):
        """Record the transaction on a blockchain for transparency."""
        transaction_data = {
            "asset_id": asset_id,
            "new_owner": new_owner,
            "timestamp": datetime.now().isoformat()
        }
        # Simulate sending transaction data to a blockchain
        response = requests.post("https://blockchain.api/record_transaction", json=transaction_data)
        if response.status_code == 200:
            print(f"Transaction for asset {asset_id} recorded on blockchain.")
        else:
            print(f"Failed to record transaction for asset {asset_id}.")

    def visualize_data(self):
        """Visualize the collected IoT data."""
        try:
            with open("iot_data_log.json", "r") as log_file:
                data_entries = [json.loads(line) for line in log_file.readlines()]
            # Here you can implement a visualization library like matplotlib or seaborn
            print("Data visualization is ready to be implemented.")
        except Exception as e:
            print(f"Error visualizing data: {e}")

# Example usage
if __name__ == "__main__":
    integration = RealWorldIntegration()

    # Add IoT devices
    solar_panel = IoTDevice(device_id="SolarPanel_001", device_type="solar_panel", location="Rooftop")
    wind_turbine = IoTDevice(device_id="WindTurbine_001", device_type="wind_turbine", location="Field")
    smart_meter = IoTDevice(device_id="SmartMeter_001", device_type="smart_meter", location="Home")

    integration.add_iot_device(solar_panel)
    integration.add_iot_device(wind_turbine)
    integration.add_iot_device(smart_meter)

    # Collect data from IoT devices
    integration.collect_iot_data()

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
        print(f"Asset ID: {asset.asset_id}, Owner: {asset.owner}, Value: {asset.tokenized_value} tokens")

    # Visualize the collected data
    integration.visualize_data()
