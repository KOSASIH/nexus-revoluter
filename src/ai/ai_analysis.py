import pandas as pd
import numpy as np
import logging
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler
import joblib
import smtplib
from email.mime.text import MIMEText

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TransactionAnalyzer:
    def __init__(self, model=None):
        self.model = model if model else IsolationForest(contamination=0.1)  # Default model
        self.scaler = StandardScaler()
        self.transaction_data = pd.DataFrame()

    def ingest_data(self, data: pd.DataFrame) -> None:
        """Ingest transaction data."""
        self.transaction_data = data
        logging.info(f"Data ingested: {len(data)} transactions.")

    def preprocess_data(self) -> pd.DataFrame:
        """Preprocess the transaction data for analysis."""
        if self.transaction_data.empty:
            raise ValueError("No transaction data to preprocess.")

        # Example feature extraction
        features = self.transaction_data[['amount', 'transaction_type', 'timestamp']]
        features['transaction_type'] = features['transaction_type'].astype('category').cat.codes  # Convert categorical to numeric
        features['timestamp'] = pd.to_datetime(features['timestamp']).astype(int) // 10**9  # Convert to seconds since epoch

        # Scale features
        scaled_features = self.scaler.fit_transform(features)
        logging.info("Data preprocessed and features extracted.")
        return scaled_features

    def train_model(self) -> None:
        """Train the anomaly detection model."""
        if self.transaction_data.empty:
            raise ValueError("No transaction data to train the model.")

        X = self.preprocess_data()
        self.model.fit(X)
        logging.info("Anomaly detection model trained.")

    def detect_anomalies(self) -> pd.DataFrame:
        """Detect anomalies in the transaction data."""
        if self.transaction_data.empty:
            raise ValueError("No transaction data to analyze.")

        X = self.preprocess_data()
        predictions = self.model.predict(X)
        self.transaction_data['anomaly'] = predictions
        anomalies = self.transaction_data[self.transaction_data['anomaly'] == -1]
        logging.info(f"Detected {len(anomalies)} anomalies.")
        return anomalies

    def generate_report(self, anomalies: pd.DataFrame) -> None:
        """Generate a report of detected anomalies."""
        if anomalies.empty:
            logging.info("No anomalies detected. No report generated.")
            return

        report = anomalies[['transaction_id', 'amount', 'transaction_type', 'timestamp']]
        report.to_csv('anomaly_report.csv', index=False)
        logging.info(f"Anomaly report generated with {len(anomalies)} entries.")

    def visualize_anomalies(self, anomalies: pd.DataFrame) -> None:
        """Visualize the detected anomalies."""
        plt.figure(figsize=(10, 6))
        plt.scatter(self.transaction_data['timestamp'], self.transaction_data['amount'], c=self.transaction_data['anomaly'], cmap='coolwarm', label='Transactions')
        plt.scatter(anomalies['timestamp'], anomalies['amount'], color='red', label='Anomalies', edgecolor='black')
        plt.title('Transaction Amounts with Detected Anomalies')
        plt.xlabel('Timestamp')
        plt.ylabel('Amount')
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('anomaly_visualization.png')
        plt.show()
        logging.info("Anomaly visualization saved as 'anomaly_visualization.png'.")

    def tune_hyperparameters(self, param_grid: dict) -> None:
        """Tune hyperparameters for the anomaly detection model."""
        X = self.preprocess_data()
        grid_search = GridSearchCV(self.model, param_grid, cv=5)
        grid_search.fit(X)
        self.model = grid_search.best_estimator_
        logging.info(f"Best model parameters: {grid_search.best_params_}")

    def save_model(self, filename: str) -> None:
        """Save the trained model to a file."""
        joblib.dump(self.model, filename)
        logging.info(f"Model saved to {filename}.")

    def load_model(self, filename: str) -> None:
        """Load a trained model from a file."""
        self.model = joblib.load(filename)
        logging.info(f"Model loaded from {filename}.")

    def send_alert(self, anomalies: pd.DataFrame) -> None:
        """Send an alert if anomalies are detected."""
        if anomalies.empty:
            logging.info("No anomalies detected. No alert sent.")
            return

        # Configure your email settings
        sender_email = "your_email@example.com"
        receiver_email = "receiver_email@example.com"
        subject = "Anomaly Detection Alert"
        body = f"Detected {len(anomalies)} anomalies in transaction data. Please check the report."

        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = receiver_email

        try:
            with smtplib.SMTP('smtp.example.com', 587) as server:
                server.starttls()
                server.login(sender_email, "your_password")  # Use environment variables for security
                server.sendmail(sender_email, receiver_email, msg.as_string())
            logging.info("Alert email sent successfully.")
        except Exception as e:
            logging.error(f"Failed to send alert email: {e}")

# Example usage of the TransactionAnalyzer class
if __name__ == "__main__":
    # Create a mock dataset
    data = {
        'transaction_id': range(1, 101),
        'amount': np.random.normal(100, 20, 100).tolist(),  # Normal distribution around 100
        'transaction_type': np.random.choice(['deposit', 'withdrawal'], 100),
        'timestamp': pd.date_range(start='2023-01-01', periods=100, freq='H')
    }
    df = pd.DataFrame(data)

    # Introduce some anomalies
    df.loc[::10, 'amount'] = np.random.normal(500, 50, 10)  # Outliers

    analyzer = TransactionAnalyzer()
    analyzer.ingest_data(df)
    analyzer.train_model()
    anomalies = analyzer.detect_anomalies()
    analyzer.generate_report(anomalies)
    analyzer.visualize_anomalies(anomalies)

    # Hyperparameter tuning example
    param_grid = {
        'n_estimators': [50, 100, 200],
        'max_samples': [0.8, 1.0],
        'contamination': [0.05, 0.1, 0.15]
    }
    analyzer.tune_hyperparameters(param_grid)

    # Save the model
    analyzer.save_model('anomaly_detection_model.pkl')

    # Load the model
    analyzer.load_model('anomaly_detection_model.pkl')

    # Send alert if anomalies are detected
    analyzer.send_alert(anomalies)
