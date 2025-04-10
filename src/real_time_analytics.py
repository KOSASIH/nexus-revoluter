import time
import random
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

class RealTimeAnalytics:
    def __init__(self):
        self.transaction_data = []  # List to store transaction data
        self.transaction_volume = defaultdict(int)  # Dictionary to track transaction volume by type
        self.transaction_times = []  # List to store transaction timestamps

    def log_transaction(self, transaction):
        """Log a transaction and its details."""
        self.transaction_data.append(transaction)
        self.transaction_volume[transaction['type']] += transaction['amount']
        self.transaction_times.append(time.time())

    def analyze_trends(self):
        """Analyze transaction data for trends."""
        total_transactions = len(self.transaction_data)
        total_volume = sum(tx['amount'] for tx in self.transaction_data)
        average_volume = total_volume / total_transactions if total_transactions > 0 else 0

        return {
            "total_transactions": total_transactions,
            "total_volume": total_volume,
            "average_volume": average_volume,
            "transaction_volume_by_type": dict(self.transaction_volume)
        }

    def detect_anomalies(self):
        """Detect anomalies in transaction data."""
        if len(self.transaction_times) < 10:
            return []  # Not enough data to analyze

        # Calculate the time differences between transactions
        time_diffs = np.diff(self.transaction_times)
        mean_diff = np.mean(time_diffs)
        std_diff = np.std(time_diffs)

        # Identify anomalies based on a threshold (e.g., 3 standard deviations from the mean)
        anomalies = [i for i, diff in enumerate(time_diffs) if diff > mean_diff + 3 * std_diff]
        return anomalies

    def visualize_trends(self):
        """Visualize transaction trends using matplotlib."""
        if not self.transaction_data:
            print("No transaction data to visualize.")
            return

        # Prepare data for visualization
        transaction_types = list(self.transaction_volume.keys())
        volumes = list(self.transaction_volume.values())

        plt.figure(figsize=(10, 5))
        plt.bar(transaction_types, volumes, color='blue')
        plt.xlabel('Transaction Types')
        plt.ylabel('Total Volume')
        plt.title('Transaction Volume by Type')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def report(self):
        """Continuously report trends and anomalies."""
        while True:
            trends = self.analyze_trends()
            anomalies = self.detect_anomalies()
            print(f"Current Trends: {trends}")
            if anomalies:
                print(f"Anomalies detected at indices: {anomalies}")
            self.visualize_trends()
            time.sleep(60)  # Report every minute

# Example usage
if __name__ == "__main__":
    analytics = RealTimeAnalytics()

    # Simulate logging transactions
    for _ in range(100):
        transaction = {
            "type": random.choice(["transfer", "stake", "reward"]),
            "amount": random.uniform(1, 100)
        }
        analytics.log_transaction(transaction)

    # Start reporting trends
    analytics.report()
