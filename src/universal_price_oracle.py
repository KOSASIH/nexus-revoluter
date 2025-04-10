import requests
import logging
import asyncio
import aiohttp
from time import sleep
from collections import defaultdict
from interoperability import validate_data
from governance import apply_penalty
from cachetools import TTLCache

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class UniversalPriceOracle:
    def __init__(self, target_value=314159.00, fetch_interval=60):
        self.target_value = target_value
        self.fetch_interval = fetch_interval
        self.price_sources = [
            'https://api.binance.com/api/v3/ticker/price?symbol=PICUSDT',  # Example for Pi Coin on Binance
            'https://api.coinbase.com/v2/prices/PI-USD/spot',  # Example for Pi Coin on Coinbase
            # Add more sources as needed
        ]
        self.price_data = defaultdict(list)
        self.cache = TTLCache(maxsize=100, ttl=300)  # Cache for 5 minutes

    async def fetch_price_from_source(self, session, source):
        """Fetch price data from a single source asynchronously."""
        try:
            async with session.get(source) as response:
                response.raise_for_status()
                data = await response.json()
                price = float(data['price'])  # Adjust based on the API response structure
                self.price_data[source].append(price)
                logging.info(f"Fetched price from {source}: {price}")
        except Exception as e:
            logging.error(f"Error fetching data from {source}: {e}")

    async def fetch_price_data(self):
        """Fetch price data from all sources asynchronously."""
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch_price_from_source(session, source) for source in self.price_sources]
            await asyncio.gather(*tasks)

    def validate_prices(self):
        """Validate the fetched prices against the target value."""
        for source, prices in self.price_data.items():
            if prices:
                average_price = sum(prices) / len(prices)
                if not validate_data(average_price, self.target_value):
                    logging.warning(f"Price from {source} deviates from target value. Average: {average_price}")
                    apply_penalty(source)  # Apply penalty for deviation

    def aggregate_prices(self):
        """Aggregate prices from all sources."""
        all_prices = []
        for prices in self.price_data.values():
            all_prices.extend(prices)
        if all_prices:
            average_price = sum(all_prices) / len(all_prices)
            logging.info(f"Aggregated average price: {average_price}")
            return average_price
        return None

    def run(self):
        """Main loop to continuously fetch and validate prices."""
        while True:
            asyncio.run(self.fetch_price_data())
            self.validate_prices()
            aggregated_price = self.aggregate_prices()
            if aggregated_price:
                # Here you can implement further logic, e.g., updating a database or notifying other services
                logging.info(f"Current aggregated price for Pi Coin: {aggregated_price}")
            sleep(self.fetch_interval)  # Fetch data every specified interval

if __name__ == "__main__":
    oracle = UniversalPriceOracle()
    oracle.run()
