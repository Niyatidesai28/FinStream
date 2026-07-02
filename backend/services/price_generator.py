import random
from datetime import datetime, timezone
from typing import Dict

from models.schemas import StockPrice

# Starting reference prices for each simulated symbol.
INITIAL_PRICES: Dict[str, float] = {
    "AAPL": 195.50,
    "MSFT": 415.20,
    "TSLA": 248.75,
    "NVDA": 925.30,
}


class PriceGenerator:
    """Generates a simulated random-walk price feed for a fixed set of symbols."""

    def __init__(self, initial_prices: Dict[str, float] = None):
        seed = initial_prices or INITIAL_PRICES
        self._reference_prices: Dict[str, float] = dict(seed)
        self._current_prices: Dict[str, float] = dict(seed)

    @staticmethod
    def _random_walk(price: float) -> float:
        volatility = max(price * 0.004, 0.05)
        delta = random.uniform(-volatility, volatility)
        new_price = price + delta
        return max(new_price, 0.01)

    def _build_price(self, symbol: str, current: float) -> StockPrice:
        reference = self._reference_prices[symbol]
        change = round(current - reference, 2)
        change_percent = round((change / reference) * 100, 2) if reference else 0.0
        return StockPrice(
            symbol=symbol,
            price=round(current, 2),
            previous_close=reference,
            change=change,
            change_percent=change_percent,
            updated_at=datetime.now(timezone.utc),
        )

    def tick(self) -> Dict[str, StockPrice]:
        """Advance every symbol by one random-walk step and return the new prices."""
        result: Dict[str, StockPrice] = {}
        for symbol, current in self._current_prices.items():
            new_price = round(self._random_walk(current), 2)
            self._current_prices[symbol] = new_price
            result[symbol] = self._build_price(symbol, new_price)
        return result

    def snapshot(self) -> Dict[str, StockPrice]:
        """Return the current prices without advancing the simulation."""
        return {
            symbol: self._build_price(symbol, current)
            for symbol, current in self._current_prices.items()
        }

    def symbols(self):
        return list(self._current_prices.keys())


# Singleton instance shared across the application.
price_generator = PriceGenerator()
