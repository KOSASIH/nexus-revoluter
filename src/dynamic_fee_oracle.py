import numpy as np
import logging
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler

class DynamicFeeOracle:
    def __init__(self):
        self.model = self._build_lstm_model()
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.logger = self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        logger = logging.getLogger("DynamicFeeOracle")
        return logger

    def _build_lstm_model(self):
        model = Sequential()
        model.add(LSTM(50, return_sequences=True, input_shape=(10, 1)))
        model.add(LSTM(50))
        model.add(Dense(1))
        model.compile(optimizer="adam", loss="mse")
        return model

    def train_model(self, historical_data):
        try:
            # Normalize the historical data
            scaled_data = self.scaler.fit_transform(historical_data)
            X, y = self._create_dataset(scaled_data)
            self.model.fit(X, y, epochs=100, batch_size=32, verbose=1)
            self.logger.info("Model training complete.")
        except Exception as e:
            self.logger.error(f"Error during model training: {e}")

    def _create_dataset(self, data):
        X, y = [], []
        for i in range(len(data) - 10):
            X.append(data[i:i + 10])
            y.append(data[i + 10])
        return np.array(X), np.array(y)

    def predict_fee(self, network_metrics):
        try:
            # Normalize the input metrics
            data = np.array(network_metrics).reshape(-1, 1)
            scaled_data = self.scaler.transform(data)
            scaled_data = scaled_data.reshape(1, 10, 1)
            fee = self.model.predict(scaled_data)[0][0]
            return max(self.scaler.inverse_transform([[fee]])[0][0], 0.01)  # Ensure minimum fee
        except Exception as e:
            self.logger.error(f"Error during fee prediction: {e}")
            return 0.01  # Fallback to minimum fee

# Example usage
if __name__ == "__main__":
    oracle = DynamicFeeOracle()
    
    # Example historical data for training (replace with actual data)
    historical_data = np.random.rand(100, 1)  # Simulated historical network metrics
    oracle.train_model(historical_data)

    # Example network metrics for prediction
    network_metrics = [0.1, 0.2, 0.15, 0.3, 0.25, 0.2, 0.15, 0.1, 0.05, 0.2]
    predicted_fee = oracle.predict_fee(network_metrics)
    print(f"Predicted Fee: {predicted_fee}")
