import hashlib
import json
import logging
from typing import Any, Dict, List, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Token:
    def __init__(self, name: str, symbol: str, total_supply: float):
        self.name = name
        self.symbol = symbol
        self.total_supply = total_supply
        self.balances: Dict[str, float] = {}

    def mint(self, address: str, amount: float) -> None:
        """Mint new tokens to an address."""
        if amount <= 0:
            logging.warning("Mint amount must be positive.")
            return
        self.total_supply += amount
        self.balances[address] = self.balances.get(address, 0) + amount
        logging.info(f"Minted {amount} {self.symbol} to {address}. Total supply: {self.total_supply}")

    def transfer(self, from_address: str, to_address: str, amount: float) -> bool:
        """Transfer tokens from one address to another."""
        if amount <= 0:
            logging.warning("Transfer amount must be positive.")
            return False
        if self.balances.get(from_address, 0) < amount:
            logging.warning(f"Insufficient balance for {from_address}.")
            return False
        self.balances[from_address] -= amount
        self.balances[to_address] = self.balances.get(to_address, 0) + amount
        logging.info(f"Transferred {amount} {self.symbol} from {from_address} to {to_address}.")
        return True

class LendingPool:
    def __init__(self, token: Token):
        self.token = token
        self.lenders: Dict[str, float] = {}
        self.borrowers: Dict[str, float] = {}
        self.collateral: Dict[str, float] = {}
        self.interest_rate: float = 0.05  # Base interest rate

    def lend(self, address: str, amount: float) -> None:
        """Lend tokens to the pool."""
        if self.token.transfer(address, self, amount):
            self.lenders[address] = self.lenders.get(address, 0) + amount
            logging.info(f"{address} lent {amount} {self.token.symbol} to the pool.")

    def borrow(self, address: str, amount: float, collateral_amount: float) -> Optional[str]:
        """Borrow tokens from the pool with collateral."""
        if amount <= 0:
            logging.warning("Borrow amount must be positive.")
            return None
        if self.token.balances.get(self, 0) < amount:
            logging.warning("Insufficient liquidity in the pool.")
            return None
        if collateral_amount < amount * 1.5:  # Require 150% collateral
            logging.warning("Insufficient collateral provided.")
            return None

        self.collateral[address] = self.collateral.get(address, 0) + collateral_amount
        self.borrowers[address] = self.borrowers.get(address, 0) + amount
        self.token.transfer(self, address, amount)
        logging.info(f"{address} borrowed {amount} {self.token.symbol} from the pool with collateral.")
        return self.calculate_repayment_amount(address, amount)

    def calculate_repayment_amount(self, address: str, amount: float) -> float:
        """Calculate the total repayment amount including interest."""
        repayment_amount = amount * (1 + self.interest_rate)
        logging.info(f"Total repayment amount for {address} is {repayment_amount} {self.token.symbol}.")
        return repayment_amount

class LiquidityPool:
    def __init__(self, token: Token):
        self.token = token
        self.liquidity_providers: Dict[str, float] = {}
        self.total_liquidity: float = 0.0

    def provide_liquidity(self, address: str, amount: float) -> None:
        """Provide liquidity to the pool."""
        if self.token.transfer(address, self, amount):
            self.liquidity_providers[address] = self.liquidity_providers.get(address, 0) + amount
            self.total_liquidity += amount
            logging.info(f"{address} provided {amount} {self.token.symbol} to the liquidity pool.")

    def withdraw_liquidity(self, address: str, amount: float) -> bool:
        """Withdraw liquidity from the pool."""
        if self.liquidity_providers.get(address, 0) < amount:
            logging.warning(f"Insufficient liquidity for {address}.")
            return False
        self.liquidity_providers[address] -= amount
        self.total_liquidity -= amount
        self.token.transfer(self, address, amount)
        logging.info(f"{address} withdrew {amount} {self.token.symbol} from the liquidity pool.")
        return True

class DeFiPlatform:
    def __init__(self):
        self.tokens: Dict[str, Token] = {}
        self.lending_pools: Dict[str, LendingPool] = {}
        self.liquidity_pools: Dict[str, LiquidityPool] = {}

    def create_token(self, name: str, symbol: str, total_supply: float) -> Token:
        """Create a new token."""
        token = Token(name, symbol, total_supply)
        self.tokens[symbol] = token
        token.mint("admin", total_supply)  # Mint all tokens to admin
        logging.info(f"Created token {name} ({symbol}) with total supply {total_supply}.")
        return token

    def create_lending_pool(self, token_symbol: str) -> LendingPool:
        """Create a new lending pool for a token."""
        token = self.tokens.get(token_symbol)
        if not token:
            logging.warning(f"Token {token_symbol} does not exist.")
            return None
        lending_pool = LendingPool(token)
        self.lending_pools[token_symbol] = lending_pool
        logging.info(f"Created lending pool for {token_symbol}.")
        return lending_pool

    def create_liquidity_pool(self, token_symbol: str) -> LiquidityPool:
        """Create a new liquidity pool for a token."""
        token = self.tokens.get(token_symbol)
        if not token:
            logging.warning(f"Token {token_symbol} does not exist.")
            return None
        liquidity_pool = LiquidityPool(token)
        self.liquidity_pools[token_symbol] = liquidity_pool
        logging.info(f"Created liquidity pool for {token_symbol}.")
        return liquidity_pool

    def save_state(self, filename: str) -> None:
        """Save the current state of the DeFi platform to a file."""
        state = {
            'tokens': {symbol: {'name': token.name, 'total_supply': token.total_supply, 'balances': token.balances}
                       for symbol, token in self.tokens.items()},
            'lending_pools': {symbol: {'lenders': pool.lenders, 'borrowers': pool.borrowers, 'collateral': pool.collateral}
                              for symbol, pool in self.lending_pools.items()},
            'liquidity_pools': {symbol: {'liquidity_providers': pool.liquidity_providers, 'total_liquidity': pool.total_liquidity}
                               for symbol, pool in self.liquidity_pools.items()}
        }
        with open(filename, 'w') as f:
            json.dump(state, f)
        logging.info(f"DeFi platform state saved to {filename}.")

    def load_state(self, filename: str) -> None:
        """Load the DeFi platform state from a file."""
        try:
            with open(filename, 'r') as f:
                state = json.load(f)
                for symbol, token_data in state['tokens'].items():
                    token = Token(token_data['name'], symbol, token_data['total_supply'])
                    token.balances = token_data['balances']
                    self.tokens[symbol] = token
                for symbol, pool_data in state['lending_pools'].items():
                    pool = LendingPool(self.tokens[symbol])
                    pool.lenders = pool_data['lenders']
                    pool.borrowers = pool_data['borrowers']
                    pool.collateral = pool_data['collateral']
                    self.lending_pools[symbol] = pool
                for symbol, pool_data in state['liquidity_pools'].items():
                    pool = LiquidityPool(self.tokens[symbol])
                    pool.liquidity_providers = pool_data['liquidity_providers']
                    pool.total_liquidity = pool_data['total_liquidity']
                    self.liquidity_pools[symbol] = pool
                logging.info(f"DeFi platform state loaded from {filename}.")
        except Exception as e:
            logging.error(f"Failed to load state: {e}")

# Example usage of the DeFiPlatform class
if __name__ == "__main__":
    defi_platform = DeFiPlatform()

    # Create a token
    token = defi_platform.create_token("MyToken", "MTK", 1000000)

    # Create lending and liquidity pools
    lending_pool = defi_platform.create_lending_pool("MTK")
    liquidity_pool = defi_platform.create_liquidity_pool("MTK")

    # Lend tokens
    lending_pool.lend("admin", 1000)

    # Borrow tokens with collateral
    repayment_amount = lending_pool.borrow("user1", 500, 750)  # 150% collateral
    logging.info(f"User  1 needs to repay: {repayment_amount} MTK")

    # Provide liquidity
    liquidity_pool.provide_liquidity("user2", 200)

    # Withdraw liquidity
    liquidity_pool.withdraw_liquidity("user2", 100)

    # Save and load state
    defi_platform.save_state("defi_state.json")
    defi_platform.load_state("defi_state.json")
