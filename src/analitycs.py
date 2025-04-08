import json
import time
from collections import defaultdict
from datetime import datetime
import logging
import sqlite3
import matplotlib.pyplot as plt

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Analytics:
    def __init__(self, db_name='analytics.db'):
        # Initialize data structures to hold analytics data
        self.transaction_data = []
        self.user_engagement = defaultdict(lambda: {'transactions': 0, 'last_active': None})
        self.start_time = time.time()
        
        # Initialize database connection
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        """Create necessary tables in the database."""
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY,
                    user_id TEXT,
                    value REAL,
                    timestamp TEXT
                )
            ''')
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS user_engagement (
                    user_id TEXT PRIMARY KEY,
                    transactions INTEGER,
                    last_active TEXT
                )
            ''')

    def log_transaction(self, transaction):
        """Log a transaction for analytics."""
        self.transaction_data.append(transaction)
        user_id = transaction['user_id']
        self.user_engagement[user_id]['transactions'] += 1
        self.user_engagement[user_id]['last_active'] = datetime.now().isoformat()
        
        # Save transaction to the database
        with self.conn:
            self.conn.execute('''
                INSERT INTO transactions (user_id, value, timestamp)
                VALUES (?, ?, ?)
            ''', (user_id, transaction['value'], transaction['timestamp']))
        
        # Save user engagement to the database
        with self.conn:
            self.conn.execute('''
                INSERT INTO user_engagement (user_id, transactions, last_active)
                VALUES (?, ?, ?)
                ON CONFLICT(user_id) DO UPDATE SET
                    transactions = transactions + 1,
                    last_active = excluded.last_active
            ''', (user_id, 1, self.user_engagement[user_id]['last_active']))
        
        logging.info(f"Transaction logged: {transaction}")

    def get_transaction_metrics(self):
        """Calculate and return transaction metrics."""
        total_transactions = len(self.transaction_data)
        total_value = sum(tx['value'] for tx in self.transaction_data)
        average_value = total_value / total_transactions if total_transactions > 0 else 0
        metrics = {
            'total_transactions': total_transactions,
            'total_value': total_value,
            'average_value': average_value,
            'transaction_volume_over_time': self.get_transaction_volume_over_time()
        }
        return metrics

    def get_transaction_volume_over_time(self, interval='hour'):
        """Get transaction volume over a specified time interval."""
        volume_over_time = defaultdict(float)
        for transaction in self.transaction_data:
            timestamp = transaction['timestamp']
            time_key = self.get_time_key(timestamp, interval)
            volume_over_time[time_key] += transaction['value']
        return dict(volume_over_time)

    def get_time_key(self, timestamp, interval):
        """Get a time key based on the specified interval."""
        dt = datetime.fromisoformat(timestamp)
        if interval == 'hour':
            return dt.strftime('%Y-%m-%d %H:00:00')
        elif interval == 'day':
            return dt.strftime('%Y-%m-%d')
        elif interval == 'month':
            return dt.strftime('%Y-%m')
        else:
            raise ValueError("Unsupported interval. Use 'hour', 'day', or 'month'.")

    def get_user_engagement(self):
        """Return user engagement metrics."""
        return dict(self.user_engagement)

    def generate_report(self):
        """Generate a comprehensive analytics report."""
        report = {
            'report_generated_at': datetime.now().isoformat(),
            'uptime': time.time() - self.start_time,
            'transaction_metrics': self.get_transaction_metrics(),
            'user_engagement': self.get_user_engagement()
        }
        return report

    def save_report_to_file(self, filename='analytics_report.json'):
        """Save the analytics report to a JSON file."""
        report = self.generate_report ()
        with open(filename, 'w') as f:
            json.dump(report, f, indent=4)
        logging.info(f"Report saved to {filename}")

    def visualize_transaction_volume(self, interval='hour'):
        """Visualize transaction volume over time."""
        volume_data = self.get_transaction_volume_over_time(interval)
        times = list(volume_data.keys())
        values = list(volume_data.values())

        plt.figure(figsize=(10, 5))
        plt.plot(times, values, marker='o')
        plt.title(f'Transaction Volume Over Time ({interval})')
        plt.xlabel('Time')
        plt.ylabel('Transaction Volume')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def alert_significant_activity(self, threshold=1000):
        """Check for significant activity and alert if necessary."""
        total_value = sum(tx['value'] for tx in self.transaction_data)
        if total_value > threshold:
            logging.warning(f"Significant activity detected: Total value = {total_value}")

# Example usage
if __name__ == "__main__":
    analytics = Analytics()

    # Simulate logging transactions
    analytics.log_transaction({'user_id': 'user1', 'value': 100, 'timestamp': datetime.now().isoformat()})
    analytics.log_transaction({'user_id': 'user2', 'value': 200, 'timestamp': datetime.now().isoformat()})
    analytics.log_transaction({'user_id': 'user1', 'value': 150, 'timestamp': datetime.now().isoformat()})

    # Generate and save report
    analytics.save_report_to_file()

    # Visualize transaction volume
    analytics.visualize_transaction_volume('hour')

    # Check for significant activity
    analytics.alert_significant_activity(threshold=300)
