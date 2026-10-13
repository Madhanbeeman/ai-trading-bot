import pyotp
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Any, List
from brokers.base import BaseBroker
from core.config import settings

try:
    from SmartApi import SmartConnect
except ImportError:
    SmartConnect = None

class AngelOneBroker(BaseBroker):
    """
    Angel One SmartAPI Live Broker Adapter.
    Uses Client Code, API Key, PIN, and TOTP for automated daily session login.
    """

    def __init__(self):
        self.api_key = settings.ANGEL_API_KEY
        self.client_code = settings.ANGEL_CLIENT_CODE
        self.password = settings.ANGEL_PASSWORD
        self.totp_key = settings.ANGEL_TOTP_KEY
        self.smart_api = None
        self.connected = False
        self.auth_token = None
        self.feed_token = None

    def connect(self) -> bool:
        if not SmartConnect:
            print("[AngelOne] SmartApi package is not installed. Run: pip install smartapi-python")
            return False

        if not all([self.api_key, self.client_code, self.password, self.totp_key]):
            print("[AngelOne] Missing credentials in .env! Please update ANGEL_* keys.")
            return False

        try:
            self.smart_api = SmartConnect(api_key=self.api_key)
            totp = pyotp.TOTP(self.totp_key).now()
            data = self.smart_api.generateSession(self.client_code, self.password, totp)
            
            if data and data.get("status"):
                self.auth_token = data["data"]["jwtToken"]
                self.feed_token = self.smart_api.getfeedToken()
                self.connected = True
                print(f"[AngelOne] Successfully authenticated for client: {self.client_code}")
                return True
            else:
                print(f"[AngelOne] Authentication failed: {data.get('message')}")
                return False
        except Exception as e:
            print(f"[AngelOne] Connection exception: {e}")
            return False

    def get_balance(self) -> Dict[str, float]:
        if not self.connected:
            return {"available_cash": 0.0, "net": 0.0}
        try:
            funds = self.smart_api.rmsLimit()
            if funds and funds.get("status"):
                net = float(funds["data"].get("net", 0.0))
                available = float(funds["data"].get("availablecash", 0.0))
                return {"available_cash": available, "net": net}
        except Exception as e:
            print(f"[AngelOne] Error fetching balance: {e}")
        return {"available_cash": 0.0, "net": 0.0}

    def get_historical_data(self, symbol: str, interval: str = "FIVE_MINUTE", days: int = 5) -> pd.DataFrame:
        if not self.connected:
            return pd.DataFrame()
        try:
            to_date = datetime.now()
            from_date = to_date - timedelta(days=days)

            historic_param = {
                "exchange": settings.DEFAULT_EXCHANGE,
                "symboltoken": symbol,  # Instrument token
                "interval": interval,
                "fromdate": from_date.strftime("%Y-%m-%d 09:15"),
                "todate": to_date.strftime("%Y-%m-%d 15:30")
            }
            res = self.smart_api.getCandleData(historic_param)
            if res and res.get("status") and res.get("data"):
                df = pd.DataFrame(res["data"], columns=["timestamp", "open", "high", "low", "close", "volume"])
                df["timestamp"] = pd.to_datetime(df["timestamp"])
                for col in ["open", "high", "low", "close", "volume"]:
                    df[col] = pd.to_numeric(df[col])
                return df
        except Exception as e:
            print(f"[AngelOne] Error fetching candle data: {e}")
        return pd.DataFrame()

    def place_order(self, symbol: str, action: str, quantity: int, price: float = 0.0, order_type: str = "MARKET") -> Dict[str, Any]:
        if not self.connected:
            return {"status": "ERROR", "message": "Broker not connected"}

        try:
            order_params = {
                "variety": "NORMAL",
                "tradingsymbol": symbol,
                "symboltoken": symbol,
                "transactiontype": action.upper(),
                "exchange": settings.DEFAULT_EXCHANGE,
                "ordertype": order_type.upper(),
                "producttype": "INTRADAY",
                "duration": "DAY",
                "price": str(price) if order_type.upper() == "LIMIT" else "0",
                "quantity": str(quantity)
            }
            order_id = self.smart_api.placeOrder(order_params)
            return {"status": "SUCCESS", "order_id": order_id, "symbol": symbol, "action": action}
        except Exception as e:
            return {"status": "ERROR", "message": str(e)}

    def get_open_positions(self) -> List[Dict[str, Any]]:
        if not self.connected:
            return []
        try:
            positions = self.smart_api.position()
            if positions and positions.get("status") and positions.get("data"):
                return positions["data"]
        except Exception as e:
            print(f"[AngelOne] Error fetching positions: {e}")
        return []

    def close_all_positions(self) -> List[Dict[str, Any]]:
        positions = self.get_open_positions()
        results = []
        for pos in positions:
            net_qty = int(pos.get("netqty", 0))
            if net_qty != 0:
                action = "SELL" if net_qty > 0 else "BUY"
                res = self.place_order(pos.get("symboltoken"), action, abs(net_qty))
                results.append(res)
        return results
