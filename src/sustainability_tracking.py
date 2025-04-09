import json
import logging
from datetime import datetime
import requests
import matplotlib.pyplot as plt
import sqlite3

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SustainabilityTracker:
    def __init__(self, db_name='sustainability.db'):
        self.data = {
            "energy_consumption": 0,  # in kWh
            "carbon_emissions": 0,     # in kg CO2
            "transactions": [],
        }
        self.db_name = db_name
        self.create_database()

    def create_database(self):
        """Create a SQLite database to store transaction data."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY,
                transaction_id TEXT,
                timestamp TEXT,
                energy_consumed REAL,
                carbon_emitted REAL
            )
        ''')
        conn.commit()
        conn.close()

    def track_energy_consumption(self, energy_kwh):
        """Track energy consumption."""
        if energy_kwh < 0:
            logging.error("Energy consumption cannot be negative.")
            return
        self.data["energy_consumption"] += energy_kwh
        logging.info(f"Tracked energy consumption: {energy_kwh} kWh")

    def track_carbon_emissions(self, emissions_kg):
        """Track carbon emissions."""
        if emissions_kg < 0:
            logging.error("Carbon emissions cannot be negative.")
            return
        self.data["carbon_emissions"] += emissions_kg
        logging.info(f"Tracked carbon emissions: {emissions_kg} kg CO2")

    def log_transaction(self, transaction_id, energy_kwh, emissions_kg):
        """Log a transaction with its energy and emissions data."""
        self.track_energy_consumption(energy_kwh)
        self.track_carbon_emissions(emissions_kg)
        transaction_record = {
            "transaction_id": transaction_id,
            "timestamp": datetime.now().isoformat(),
            "energy_consumed": energy_kwh,
            "carbon_emitted": emissions_kg,
        }
        self.data["transactions"].append(transaction_record)
        self.save_transaction_to_db(transaction_record)
        logging.info(f"Logged transaction: {transaction_record}")

    def save_transaction_to_db(self, transaction_record):
        """Save transaction record to the database."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO transactions (transaction_id, timestamp, energy_consumed, carbon_emitted)
            VALUES (?, ?, ?, ?)
        ''', (transaction_record["transaction_id"], transaction_record["timestamp"],
              transaction_record["energy_consumed"], transaction_record["carbon_emitted"]))
        conn.commit()
        conn.close()

    def generate_report(self):
        """Generate a sustainability report."""
        report = {
            "total_energy_consumption": self.data["energy_consumption"],
            "total_carbon_emissions": self.data["carbon_emissions"],
            "transactions": self.data["transactions"],
        }
        logging.info("Generated sustainability report.")
        return report

    def save_report_to_file(self, filename='sustainability_report.json'):
        """Save the sustainability report to a JSON file."""
        report = self.generate_report()
        with open(filename, 'w') as f:
            json.dump(report, f, indent=4)
        logging.info(f"Sustainability report saved to {filename}")

    def visualize_data(self):
        """Visualize energy consumption and carbon emissions."""
        labels = ['Energy Consumption (kWh)', 'Carbon Emissions (kg CO2)']
        values = [self.data["energy_consumption"], self.data["carbon_emissions"]]

        plt.bar(labels, values, color=['blue', 'green'])
        plt.title('Sustainability Metrics')
        plt.ylabel('Amount')
        plt.savefig('sustainability_metrics.png')
        plt.show()
        logging.info("Visualized sustainability data.")

    def fetch_external_data(self):
        """Fetch external data for energy sources and emissions."""
        # Example API call (replace with a real API)
        try:
 response = requests.get("https://api.example.com/energy_data")
            if response.status_code == 200:
                data = response.json()
                # Process the data as needed
                logging.info("Fetched external energy data successfully.")
                return data
            else:
                logging.error("Failed to fetch external data.")
        except Exception as e:
            logging.error(f"An error occurred while fetching external data: {e}")

# Example usage
if __name__ == "__main__":
    tracker = SustainabilityTracker()
    tracker.log_transaction("tx12345", energy_kwh=10, emissions_kg=2.5)
    tracker.log_transaction("tx12346", energy_kwh=15, emissions_kg=3.0)
    tracker.visualize_data()
    tracker.save_report_to_file()
    external_data = tracker.fetch_external_data()
    if external_data:
        # Process external data as needed
        pass
