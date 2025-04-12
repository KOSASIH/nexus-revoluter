import numpy as np
import logging
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from npas.utils.logger import setup_logger

class AIAnalyzer:
    def __init__(self, model_path="models/rf_analyzer.pkl"):
        self.logger = setup_logger("AIAnalyzer")
        self.model_path = model_path
        self.model = self.load_model()
        self.logger.info("AI Analyzer initialized.")

    def load_model(self):
        """Load the pre-trained model or initialize a new one if not found."""
        try:
            model = joblib.load(self.model_path)
            self.logger.info("Model loaded successfully.")
            return model
        except FileNotFoundError:
            self.logger.warning("Model not found, initializing a new RandomForestClassifier.")
            return RandomForestClassifier()

    def preprocess_data(self, changes):
        """Transform changes into features for analysis."""
        features = []
        for change in changes:
            feature = [
                len(change.get("content", "")),  # Size of content
                1 if change.get("type") == "code" else 0,  # Change type
                change.get("timestamp", 0)  # Change time
            ]
            features.append(feature)
        return np.array(features)

    def train_model(self, X, y):
        """Train the Random Forest model with provided features and labels."""
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        self.logger.info("Model trained successfully.")
        
        # Evaluate the model
        predictions = self.model.predict(X_test)
        report = classification_report(y_test, predictions)
        self.logger.info(f"Model evaluation report:\n{report}")

        # Save the trained model
        joblib.dump(self.model, self.model_path)
        self.logger.info("Model saved successfully.")

    def predict_issues(self, changes):
        """Predict potential issues from changes."""
        if not changes:
            return []
        
        try:
            features = self.preprocess_data(changes)
            predictions = self.model.predict(features)
            issues = [change for change, pred in zip(changes, predictions) if pred == 1]
            return issues
        except Exception as e:
            self.logger.error(f"Error in AI prediction: {e}")
            return []

if __name__ == "__main__":
    analyzer = AIAnalyzer()
    
    # Sample changes for testing
    sample_changes = [
        {"id": "1", "content": "code update", "type": "code", "timestamp": 1634567890},
        {"id": "2", "content": "doc update", "type": "doc", "timestamp": 1634567891},
        {"id": "3", "content": "critical bug fix", "type": "code", "timestamp": 1634567892},
        {"id": "4", "content": "minor text change", "type": "doc", "timestamp": 1634567893}
    ]
    
    # Assuming we have labels for training (1 for issues, 0 for no issues)
    labels = [1, 0, 1, 0]  # Example labels for the sample changes

    # Train the model (this should be done with a larger dataset in practice)
    analyzer.train_model(analyzer.preprocess_data(sample_changes), labels)

    # Predict issues
    issues = analyzer.predict_issues(sample_changes)
    print(f"Issues detected: {issues}")
