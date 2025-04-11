import requests
import logging
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from textblob import TextBlob
import matplotlib.pyplot as plt
import yaml

class MarketAnalyzer:
    def __init__(self, config_path):
        self.logger = logging.getLogger("MarketAnalyzer")
        self.config = self.load_config(config_path)
        self.market_data = None

    def load_config(self, config_path):
        """Load configuration settings from a YAML file."""
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)

    def fetch_market_data(self):
        """Fetch real-time market data for Pi Coin from various exchanges."""
        try:
            response = requests.get(self.config['market']['data_endpoint'])
            response.raise_for_status()
            self.market_data = response.json()
            self.logger.info("Market data fetched successfully.")
        except Exception as e:
            self.logger.error(f"Failed to fetch market data: {e}")

    def calculate_technical_indicators(self):
        """Calculate technical indicators for market analysis."""
        if self.market_data is None:
            self.logger.error("Market data is not available.")
            return None

        df = pd.DataFrame(self.market_data)
        df['SMA_20'] = df['price'].rolling(window=20).mean()  # 20-day Simple Moving Average
        df['SMA_50'] = df['price'].rolling(window=50).mean()  # 50-day Simple Moving Average
        df['RSI'] = self.calculate_rsi(df['price'], 14)  # 14-day RSI
        self.logger.info("Technical indicators calculated.")
        return df

    def calculate_rsi(self, prices, period):
        """Calculate the Relative Strength Index (RSI)."""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def perform_sentiment_analysis(self, text_data):
        """Perform sentiment analysis on social media or news data."""
        analysis = TextBlob(text_data)
        sentiment = analysis.sentiment.polarity
        self.logger.info(f"Sentiment analysis completed with polarity: {sentiment}")
        return sentiment

    def predict_price(self):
        """Predict future price movements using linear regression."""
        if self.market_data is None:
            self.logger.error("Market data is not available for prediction.")
            return None

        df = pd.DataFrame(self.market_data)
        df['time'] = np.arange(len(df))  # Create a time variable
        model = LinearRegression()
        model.fit(df[['time']], df['price'])
        future_time = np.array([[len(df) + i] for i in range(1, 6)])  # Predict next 5 time points
        predictions = model.predict(future_time)
        self.logger.info("Price prediction completed.")
        return predictions

    def plot_market_data(self):
        """Visualize market data and technical indicators."""
        if self.market_data is None:
            self.logger.error("Market data is not available for plotting.")
            return

        df = pd.DataFrame(self.market_data)
        plt.figure(figsize=(14, 7))
        plt.plot(df['timestamp'], df['price'], label='Price', color='blue')
        plt.plot(df['timestamp'], df['SMA_20'], label='20-day SMA', color='orange')
        plt.plot(df['timestamp'], df['SMA_50'], label='50-day SMA', color='green')
        plt.title('Pi Coin Market Data')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.show()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    analyzer = MarketAnalyzer
