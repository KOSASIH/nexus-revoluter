import json
import logging
from datetime import datetime
import requests
import matplotlib.pyplot as plt
import sqlite3
import asyncio
import aiohttp
import os

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SustainabilityTracker:
    def __init__(self, db_name='sustainability.db', api_url='https://api.example.com/energy_data'):
        self.data = {
            "energy_consumption": 0,  # in kWh
            "carbon_emissions": 0,     # in kg CO2
            "transactions": [],
        }
        self.db_name = db_name
        self.api_url = api_url
        self.create_database()

    def create_database(self):
        """Create a SQLite database to store transaction data."""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS transactions (
                        id INTEGER PRIMARY KEY,
                        transaction_id TEXT UNIQUE,
                        timestamp TEXT,
                        energy_consumed REAL,
                        carbon_emitted REAL
                    )
                ''')
                conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Database error: {e}")

    def validate_data(self, energy_kwh, emissions_kg):
        """Validate energy and emissions data."""
        if energy_kwh < 0:
            logging.error("Energy consumption cannot be negative.")
            return False
        if emissions_kg < 0:
            logging.error("Carbon emissions cannot be negative.")
            return False
        return True

    def track_energy_consumption(self, energy_kwh):
        """Track energy consumption."""
        self.data["energy_consumption"] += energy_kwh
        logging.info(f"Tracked energy consumption: {energy_kwh} kWh")

    def track_carbon_emissions(self, emissions_kg):
        """Track carbon emissions."""
        self.data["carbon_emissions"] += emissions_kg
        logging.info(f"Tracked carbon emissions: {emissions_kg} kg CO2")

    def log_transaction(self, transaction_id, energy_kwh, emissions_kg):
        """Log a transaction with its energy and emissions data."""
        if not self.validate_transaction_id(transaction_id):
            logging.error(f"Transaction ID '{transaction_id}' is invalid or already exists.")
            return

        if not self.validate_data(energy_kwh, emissions_kg):
            return

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

    def validate_transaction_id(self, transaction_id):
        """Validate transaction ID to ensure uniqueness."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM transactions WHERE transaction_id = ?', (transaction_id,))
            return cursor.fetchone()[0] == 0

    def save_transaction_to_db(self, transaction_record):
        """Save transaction record to the database."""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO transactions (transaction_id, timestamp, energy_consumed, carbon_emitted)
                    VALUES (?, ?, ?, ?)
                ''', (transaction_record["transaction_id"], transaction_record["timestamp"],
                      transaction_record["energy_consumed"], transaction_record["carbon_emitted"]))
                conn.commit()
        except sqlite3.Error as e:
            logging.error(f"Database error while saving transaction: {e}")

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

    async def fetch_external_data(self):
        """Fetch external data for energy sources and emissions asynchronously."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.api_url) as response:
                    response.raise_for_status()
                    data = await response.json()
                    logging.info("Fetched external energy data successfully.")
                    return data
        except aiohttp.ClientError as e:
            logging.error(f"HTTP error occurred: {e}")
        except Exception as e:
            logging.error(f"An error occurred while fetching external data: {e}")

    def run(self):
        """Run the command-line interface for user interaction."""
        while True:
            print("1. Log Transaction")
            print("2. Generate Report")
            print("3. Visualize Data")
            print("4. Fetch External Data")
            print("5. Exit")
            choice = input("Choose an option: ")

            if choice == '1':
                transaction_id = input("Enter transaction ID: ")
                energy_kwh = float(input("Enter energy consumed (kWh): "))
                emissions_kg = float(input("Enter carbon emitted (kg CO2): "))
                self.log_transaction(transaction_id, energy_kwh, emissions_kg)
            elif choice == '2':
                report = self.generate_report()
                print(json.dumps(report, indent=4))
            elif choice == '3':
                self.visualize_data()
            elif choice == '4':
                asyncio.run(self.fetch_external_data())
            elif choice == '5':
                break
            else:
                print("Invalid choice. Please try again.")

# Example usage
if __name__ == "__main__":
    tracker = SustainabilityTracker()
    tracker.run() }
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

    async def fetch_external_data(self):
        """Fetch external data for energy sources and emissions asynchronously."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.api_url) as response:
                    response.raise_for_status()
                    data = await response.json()
                    logging.info("Fetched external energy data successfully.")
                    return data
        except aiohttp.ClientError as e:
            logging.error(f"HTTP error occurred: {e}")
        except Exception as e:
            logging.error(f"An error occurred while fetching external data: {e}")

    def run(self):
        """Run the tracker with a simple command-line interface."""
        while True:
            print("1. Log Transaction")
            print("2. Generate Report")
            print("3. Visualize Data")
            print("4. Fetch External Data")
            print("5. Exit")
            choice = input("Choose an option: ")

            if choice == '1':
                transaction_id = input("Enter transaction ID: ")
                energy_kwh = float(input("Enter energy consumed (kWh): "))
                emissions_kg = float(input("Enter carbon emitted (kg CO2): "))
                self.log_transaction(transaction_id, energy_kwh, emissions_kg)
            elif choice == '2':
                report = self.generate_report()
                print(json.dumps(report, indent=4))
            elif choice == '3':
                self.visualize_data()
            elif choice == '4':
                asyncio.run(self.fetch_external_data())
            elif choice == '5':
                break
            else:
                print("Invalid choice. Please try again.")

# Example usage
if __name__ == "__main__":
    tracker = SustainabilityTracker()
    tracker.run()
