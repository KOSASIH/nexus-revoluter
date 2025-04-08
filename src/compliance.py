import json
import logging
import sqlite3
from datetime import datetime
import pandas as pd
from sklearn.ensemble import IsolationForest
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Compliance:
    def __init__(self, db_name='compliance.db'):
        # Initialize database connection
        self.conn = sqlite3.connect(db_name)
        self.create_tables()
        self.model = IsolationForest(contamination=0.1)  # Simple ML model for anomaly detection

    def create_tables(self):
        """Create necessary tables in the database for KYC and AML."""
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT PRIMARY KEY,
                    name TEXT,
                    email TEXT,
                    phone TEXT,
                    kyc_verified INTEGER DEFAULT 0,
                    created_at TEXT,
                    kyc_documents TEXT
                )
            ''')
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY,
                    user_id TEXT,
                    value REAL,
                    timestamp TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            ''')
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS activity_log (
                    id INTEGER PRIMARY KEY,
                    user_id TEXT,
                    action TEXT,
                    timestamp TEXT
                )
            ''')

    def register_user(self, user_id, name, email, phone, kyc_documents=None):
        """Register a new user and initiate KYC process."""
        with self.conn:
            self.conn.execute('''
                INSERT INTO users (user_id, name, email, phone, created_at, kyc_documents)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (user_id, name, email, phone, datetime.now().isoformat(), kyc_documents))
        logging.info(f"User  registered: {user_id}")

    def verify_kyc(self, user_id):
        """Verify KYC for a user."""
        with self.conn:
            self.conn.execute('''
                UPDATE users
                SET kyc_verified = 1
                WHERE user_id = ?
            ''', (user_id,))
        logging.info(f"KYC verified for user: {user_id}")

    def log_transaction(self, user_id, value):
        """Log a transaction for a user."""
        with self.conn:
            self.conn.execute('''
                INSERT INTO transactions (user_id, value, timestamp)
                VALUES (?, ?, ?)
            ''', (user_id, value, datetime.now().isoformat()))
        logging.info(f"Transaction logged for user {user_id}: {value}")
        self.log_activity(user_id, f"Transaction of {value} logged.")

    def log_activity(self, user_id, action):
        """Log user activity."""
        with self.conn:
            self.conn.execute('''
                INSERT INTO activity_log (user_id, action, timestamp)
                VALUES (?, ?, ?)
            ''', (user_id, action, datetime.now().isoformat()))

    def monitor_transactions(self):
        """Monitor transactions for suspicious activity using ML."""
        suspicious_transactions = []
        with self.conn:
            cursor = self.conn.execute('SELECT user_id, value FROM transactions')
            data = np.array(cursor.fetchall())
            if data.size > 0:
                # Fit the model on transaction values
                self.model.fit(data[:, 1].reshape(-1, 1))
                predictions = self.model.predict(data[:, 1].reshape(-1, 1))
                for i, prediction in enumerate(predictions):
                    if prediction == -1:  # Anomaly detected
                        suspicious_transactions.append(data[i][0])
                        logging.warning(f"Suspicious activity detected for user {data[i][0]}: Transaction value = {data[i][1]}")
        return suspicious_transactions

    def generate_regulatory_report(self):
        """Generate a regulatory report for compliance."""
        report = {
            'report_generated_at': datetime.now().isoformat(),
            'users': [],
            'suspicious_transactions': self.monitor_transactions()
        }
        with self.conn:
            cursor = self.conn.execute('SELECT * FROM users')
            for row in cursor:
                report['users'].append({
                    'user_id': row[0],
                    'name': row[1],
                    'email': row[2],
                    'phone': row[3],
                    'kyc_verified': bool(row[4]),
                    'created_at': row[5],
                    'kyc_documents': row[6]
                })
        return report

    def save_report_to_file(self, filename='regulatory_report.json'):
        """Save the regulatory report to a JSON file."""
        report = self.generate_regulatory_report()
        with open(filename, 'w') as f:
            json.dump(report, f, indent=4)
        logging.info(f"Regulatory report saved to {filename}")

    def export_report_to_csv(self, filename='regulatory_report.csv'):
        """Export the regulatory report to a CSV file."""
        report = self.generate_regulatory_report()
        users_df = pd.DataFrame(report['users'])
        users_df.to_csv(filename, index=False)
        logging.info(f"Regulatory report exported to {filename}")

# Example usage
if __name__ == "__main__":
    compliance = Compliance()

    # Register users with KYC documents
    compliance.register_user('user1', 'Alice Smith', 'alice@example.com', '123-456-7890', 'doc1.pdf')
    compliance.register_user('user2', 'Bob Johnson', 'bob@example.com', '098-765-4321', 'doc2.pdf')

    # Verify KYC for a user
    compliance.verify_kyc('user1')

    # Log transactions
    compliance.log_transaction('user1', 5000)
    compliance.log_transaction('user1', 15000)  # This should trigger suspicious activity
    compliance.log_transaction('user2', 2000)

    # Generate and save regulatory report
    compliance.save_report_to_file()
    compliance.export_report_to_csv()
