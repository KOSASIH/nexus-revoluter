import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

class AIFraudDetection:
    def __init__(self):
        self.model = self.load_fraud_detection_model()
        self.transaction_history = []  # Store transaction history for analysis

    def load_fraud_detection_model(self):
        """Load a pre-trained model for fraud detection or train a new one if not available."""
        try:
            model = joblib.load('fraud_detection_model.pkl')  # Load the model from a file
            print("Fraud detection model loaded successfully.")
            return model
        except FileNotFoundError:
            print("Model not found. Training a new model.")
            return self.train_model()

    def train_model(self):
        """Train a new fraud detection model using a mock dataset."""
        # Generate a mock dataset for demonstration purposes
        data = {
            'amount': np.random.uniform(1, 1000, 1000),
            'transaction_type': np.random.choice(['transfer', 'withdrawal', 'deposit'], 1000),
            'is_fraud': np.random.choice([0, 1], 1000, p=[0.95, 0.05])  # 5% fraud cases
        }
        df = pd.DataFrame(data)

        # Convert categorical variable to numerical
        df['transaction_type'] = df['transaction_type'].map({'transfer': 0, 'withdrawal': 1, 'deposit': 2})

        # Split the dataset into features and target
        X = df[['amount', 'transaction_type']]
        y = df['is_fraud']

        # Split into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train a Random Forest Classifier
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # Evaluate the model
        y_pred = model.predict(X_test)
        print(classification_report(y_test, y_pred))

        # Save the trained model
        joblib.dump(model, 'fraud_detection_model.pkl')
        print("New fraud detection model trained and saved.")

        return model

    def detect_fraud(self, transaction):
        """Analyze the transaction using the model."""
        # Prepare the transaction data for prediction
        transaction_data = np.array([[transaction['amount'], transaction['transaction_type']]])
        prediction = self.model.predict(transaction_data)

        # Log the transaction for history
        self.transaction_history.append(transaction)

        return bool(prediction[0])  # Return True if fraud is detected

# Example usage
if __name__ == "__main__":
    fraud_detector = AIFraudDetection()

    # Simulate a transaction
    transaction = {
        'amount': 500,
        'transaction_type': 0  # 0 for transfer, 1 for withdrawal, 2 for deposit
    }

    # Detect fraud
    is_fraud = fraud_detector.detect_fraud(transaction)
    print(f"Fraud detected: {is_fraud}")
