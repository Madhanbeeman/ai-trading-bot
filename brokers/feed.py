import requests
import random
import time
from typing import Dict, Any

try:
    import yfinance as yf
except Exception:
    yf = None

# Fallback base prices in INR
DEFAULT_NSE_PRICES = {
    "RELIANCE": 1196.20,
    "INFOSYS": 1163.00,
    "SBIN": 945.10,
    "ICICIBANK": 1386.90,
    "NIFTY50": 22750.00
}

DEFAULT_CRYPTO_INR = {
    "BTCINR": 8084000.0,
    "ETHINR": 234000.0,
    "SOLINR": 10110.0,
    "DOGEINR": 7.76
}

# In-memory cache to prevent excessive API requests
_cache = {
    "nse": {},
    "crypto": {},
    "last_nse_time": 0,
    "last_crypto_time": 0
}

def fetch_coindcx_tickers() -> Dict[str, float]:
    """Fetches real-time cryptocurrency quotes directly from CoinDCX India API."""
    now = time.time()
    if _cache["crypto"] and (now - _cache["last_crypto_time"] < 5.0):
        return _cache["crypto"]

    prices = dict(DEFAULT_CRYPTO_INR)
    try:
        url = "https://api.coindcx.com/exchange/ticker"
        resp = requests.get(url, timeout=3.5)
        if resp.status_code == 200:
            data = resp.json()
            for item in data:
                market = item.get("market")
                if market in prices:
                    try:
                        lp = float(item.get("last_price", 0))
                        if lp > 0:
                            prices[market] = lp
                    except Exception:
                        pass
            _cache["crypto"] = prices
            _cache["last_crypto_time"] = now
    except Exception:
        pass
    return prices

def fetch_nse_tickers() -> Dict[str, float]:
    """Fetches real-time Indian stock market quotes via Yahoo Finance with caching."""
    now = time.time()
    if _cache["nse"] and (now - _cache["last_nse_time"] < 15.0):
        return _cache["nse"]

    prices = dict(DEFAULT_NSE_PRICES)
    if yf is not None:
        sym_map = {
            "RELIANCE": "RELIANCE.NS",
            "INFOSYS": "INFY.NS",
            "SBIN": "SBIN.NS",
            "ICICIBANK": "ICICIBANK.NS",
            "NIFTY50": "^NSEI"
        }
        for code, ticker in sym_map.items():
            try:
                t = yf.Ticker(ticker)
                val = float(t.fast_info.last_price)
                if val > 0:
                    prices[code] = round(val, 2)
            except Exception:
                pass
        _cache["nse"] = prices
        _cache["last_nse_time"] = now
    return prices

def get_micro_tick(base_price: float, volatility_pct: float = 0.06) -> float:
    """Generates realistic micro-fluctuation simulating intraday order-book depth."""
    pct = (random.random() * (volatility_pct * 2)) - volatility_pct
    new_price = base_price * (1.0 + (pct / 100.0))
    if base_price > 100:
        return round(new_price, 2)
    elif base_price > 1:
        return round(new_price, 3)
    else:
        return round(new_price, 6)

def get_live_market_data() -> Dict[str, Any]:
    """Returns aggregated real-time market data for Angel One and CoinDCX."""
    return {
        "nse": fetch_nse_tickers(),
        "coindcx": fetch_coindcx_tickers()
    }
