import json
import logging
import numpy as np
import pandas as pd
import requests
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AIMarketPredictions:
    def __init__(self):
        self.data = None
        self.model = None

    def fetch_market_data(self, symbol, start_date, end_date):
        """Fetch market data from an external API."""
        url = f"https://api.example.com/marketdata?symbol={symbol}&start={start_date}&end={end_date}"
        response = requests.get(url)
        if response.status_code == 200:
            self.data = pd.DataFrame(response.json())
            logging.info(f"Market data fetched for {symbol}.")
        else:
            logging.error("Failed to fetch market data.")
            return None

    def preprocess_data(self):
        """Preprocess the market data for analysis."""
        if self.data is None:
            logging.error("No data to preprocess.")
            return False
        self.data['Date'] = pd.to_datetime(self.data['Date'])
        self.data.set_index('Date', inplace=True)
        self.data['Returns'] = self.data['Close'].pct_change()
        self.data.dropna(inplace=True)
        logging.info("Market data preprocessed.")
        return True

    def train_model(self):
        """Train a machine learning model on the market data."""
        if self.data is None:
            logging.error("No data to train on.")
            return False
        X = self.data[['Open', 'High', 'Low', 'Volume']]
        y = self.data['Close'].shift(-1).dropna()
        X = X[:-1]  # Align X with y
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)

        predictions = self.model.predict(X_test)
        rmse = np.sqrt(mean_squared_error(y_test, predictions))
        logging.info(f"Model trained with RMSE: {rmse:.2f}")
        return rmse

    def make_prediction(self, input_data):
        """Make a market prediction based on input data."""
        if self.model is None:
            logging.error("Model is not trained.")
            return None
        prediction = self.model.predict(np.array(input_data).reshape(1, -1))
        logging.info(f"Prediction made: {prediction[0]}")
        return prediction[0]

    def visualize_predictions(self):
        """Visualize historical data and predictions."""
        if self.data is None:
            logging.error("No data to visualize.")
            return False
        plt.figure(figsize=(14, 7))
        plt.plot(self.data['Close'], label='Historical Prices', color='blue')
        plt.title('Market Price History')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.show()
        logging.info("Visualization displayed.")
        return True

    def backtest_strategy(self, initial_investment=1000):
        """Backtest a simple trading strategy based on predictions."""
        if self.data is None:
            logging.error("No data to backtest.")
            return False
        self.data['Predicted'] = self.model.predict(self.data[['Open', 'High', 'Low', 'Volume']])
        self.data['Signal'] = np.where(self.data['Predicted'] > self.data['Close'], 1, 0)  # Buy signal
        self.data['Position'] = self.data['Signal'].shift(1)  # Shift to avoid lookahead bias
        self.data['Strategy_Returns'] = self.data['Returns'] * self.data['Position']
        self.data['Cumulative_Strategy_Returns'] = (1 + self.data['Strategy_Returns']).cumprod()

        total_return = initial_investment * self.data['Cumulative_Strategy_Returns'].iloc[-1]
        logging.info(f"Backtest completed. Total return: ${total_return:.2f}")
        return total_return

# Example usage
if __name__ == "__main__":
    ai_market_predictions = AIMarketPredictions()
    ai_market_predictions.fetch_market_data("AAPL", "2022-01-01", "2023-01-01")
    ai_market_predictions.preprocess_data()
    rmse = ai_market_predictions.train_model()
    print(f"Model RMSE: {rmse:.2f}")

    # Make a prediction
    input_data = [150, 155, 145, 1000000]  # Example input data: Open, High, Low, Volume
    prediction = ai_market_predictions.make_prediction(input_data)
    print(f"Predicted next closing price: {prediction:.2f}")

    # Visualize predictions
    ai_market_predictions.visualize_predictions()

    # Backtest strategy
    total_return = ai_market_predictions.backtest_strategy()
    print(f"Total return from backtesting: ${total_return:.2f}")
