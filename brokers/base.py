from abc import ABC, abstractmethod
from typing import Dict, Any, List

class BaseBroker(ABC):
    """Abstract interface that every broker adapter must implement."""

    @abstractmethod
    def connect(self) -> bool:
        """Authenticate and establish connection with broker."""
        pass

    @abstractmethod
    def get_balance(self) -> Dict[str, float]:
        """Fetch available margin/funds."""
        pass

    @abstractmethod
    def get_historical_data(self, symbol: str, interval: str, days: int = 5) -> Any:
        """Fetch historical candle/OHLCV data for technical analysis."""
        pass

    @abstractmethod
    def place_order(self, symbol: str, action: str, quantity: int, price: float = 0.0, order_type: str = "MARKET") -> Dict[str, Any]:
        """Place buy or sell order."""
        pass

    @abstractmethod
    def get_open_positions(self) -> List[Dict[str, Any]]:
        """Fetch currently active trading positions."""
        pass

    @abstractmethod
    def close_all_positions(self) -> List[Dict[str, Any]]:
        """Emergency Kill-switch: Close all open positions."""
        pass
