import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, Any, List
from brokers.base import BaseBroker

class PaperBroker(BaseBroker):
    """
    Simulated Paper Trading Broker.
    Allows zero-risk testing with virtual capital, accurate tracking of PnL,
    stop-loss, targets, and open positions.
    """

    def __init__(self, initial_capital: float = 50000.0):
        self.initial_capital = initial_capital
        self.available_cash = initial_capital
        self.positions: Dict[str, Dict[str, Any]] = {}
        self.order_history: List[Dict[str, Any]] = []
        self.connected = False

    def connect(self) -> bool:
        self.connected = True
        return True

    def get_balance(self) -> Dict[str, float]:
        unrealized_pnl = sum(p.get("unrealized_pnl", 0.0) for p in self.positions.values())
        total_equity = self.available_cash + unrealized_pnl
        return {
            "initial_capital": self.initial_capital,
            "available_cash": round(self.available_cash, 2),
            "unrealized_pnl": round(unrealized_pnl, 2),
            "total_equity": round(total_equity, 2)
        }

    def get_historical_data(self, symbol: str, interval: str = "5m", days: int = 2) -> pd.DataFrame:
        """
        Generates simulated realistic price series for testing or backtesting
        when live data feed is not connected.
        """
        periods = 100
        dates = pd.date_range(end=datetime.now(), periods=periods, freq="5min")
        
        # Synthetic random walk with realistic momentum
        np.random.seed(42)
        base_price = 24500.0 if "NIFTY" in symbol else 500.0
        returns = np.random.normal(0.0002, 0.002, periods)
        prices = base_price * np.exp(np.cumsum(returns))
        
        df = pd.DataFrame({
            "timestamp": dates,
            "open": prices * (1 - np.random.uniform(0.0001, 0.001, periods)),
            "high": prices * (1 + np.random.uniform(0.0005, 0.002, periods)),
            "low": prices * (1 - np.random.uniform(0.0005, 0.002, periods)),
            "close": prices,
            "volume": np.random.randint(1000, 50000, periods)
        })
        return df

    def place_order(self, symbol: str, action: str, quantity: int, price: float = 0.0, order_type: str = "MARKET") -> Dict[str, Any]:
        action = action.upper()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # In paper mode, if price is 0, fetch current synthetic price
        if price <= 0:
            hist = self.get_historical_data(symbol)
            price = float(hist["close"].iloc[-1])

        cost = price * quantity

        if action == "BUY":
            if self.available_cash < cost:
                return {"status": "REJECTED", "message": "Insufficient virtual funds"}

            self.available_cash -= cost
            if symbol in self.positions:
                pos = self.positions[symbol]
                total_qty = pos["quantity"] + quantity
                avg_price = ((pos["entry_price"] * pos["quantity"]) + cost) / total_qty
                pos["quantity"] = total_qty
                pos["entry_price"] = avg_price
            else:
                self.positions[symbol] = {
                    "symbol": symbol,
                    "quantity": quantity,
                    "entry_price": price,
                    "current_price": price,
                    "unrealized_pnl": 0.0,
                    "entry_time": timestamp
                }

        elif action == "SELL":
            if symbol not in self.positions or self.positions[symbol]["quantity"] < quantity:
                return {"status": "REJECTED", "message": "No open position to sell"}

            pos = self.positions[symbol]
            pnl = (price - pos["entry_price"]) * quantity
            self.available_cash += (pos["entry_price"] * quantity) + pnl
            pos["quantity"] -= quantity

            if pos["quantity"] <= 0:
                del self.positions[symbol]

        order_record = {
            "order_id": f"PAPER_{len(self.order_history) + 1}",
            "symbol": symbol,
            "action": action,
            "quantity": quantity,
            "price": round(price, 2),
            "status": "EXECUTED",
            "timestamp": timestamp
        }
        self.order_history.append(order_record)
        return order_record

    def get_open_positions(self) -> List[Dict[str, Any]]:
        return list(self.positions.values())

    def close_all_positions(self) -> List[Dict[str, Any]]:
        closed_orders = []
        for symbol, pos in list(self.positions.items()):
            order = self.place_order(symbol, "SELL", pos["quantity"], pos.get("current_price", pos["entry_price"]))
            closed_orders.append(order)
        return closed_orders
