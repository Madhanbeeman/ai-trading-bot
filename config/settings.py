from datetime import datetime, timezone, timedelta
import os

# -------------------------------------------------------------
# 1. TIMEZONE CONFIGURATION (INDIAN STANDARD TIME - IST)
# -------------------------------------------------------------
IST = timezone(timedelta(hours=5, minutes=30))

def get_ist_now():
    """Returns current datetime strictly in Indian Standard Time."""
    return datetime.now(IST)

def format_ist_time():
    return get_ist_now().strftime("%I:%M %p")

def format_ist_clock():
    return get_ist_now().strftime("%I:%M:%S %p")

def format_ist_date():
    return get_ist_now().strftime("%Y-%m-%d")

# -------------------------------------------------------------
# 2. CAPITAL GRANTS (CLEAN ₹2,000 PER BROKER = ₹4,000 TOTAL)
# -------------------------------------------------------------
ANGEL_INITIAL_CAPITAL = 2000.00
COINDCX_INITIAL_CAPITAL = 2000.00
TOTAL_INITIAL_CAPITAL = ANGEL_INITIAL_CAPITAL + COINDCX_INITIAL_CAPITAL

# -------------------------------------------------------------
# 3. STORAGE PATHS
# -------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)
DB_FILE = os.path.join(DATA_DIR, "trade_ledger.json")

# -------------------------------------------------------------
# 4. CANDIDATE ASSET POOLS
# -------------------------------------------------------------

# Angel One: NSE Bluechips (5x Intraday MIS Margin)
ANGEL_STOCKS_POOL = [
    {
        "symbol": "RELIANCE",
        "ticker": "RELIANCE.NS",
        "name": "Reliance Industries",
        "segment": "NSE 5X MIS",
        "base_price": 1196.20,
        "qty_desc": "1 Share (5x)",
        "margin": 239.24,
        "target_mult": 1.025,
        "sl_mult": 0.985
    },
    {
        "symbol": "INFOSYS",
        "ticker": "INFY.NS",
        "name": "Infosys Ltd",
        "segment": "NSE 5X MIS",
        "base_price": 1163.00,
        "qty_desc": "1 Share (5x)",
        "margin": 232.60,
        "target_mult": 1.024,
        "sl_mult": 0.986
    },
    {
        "symbol": "SBIN",
        "ticker": "SBIN.NS",
        "name": "State Bank of India",
        "segment": "NSE 5X MIS",
        "base_price": 945.10,
        "qty_desc": "1 Share (5x)",
        "margin": 189.02,
        "target_mult": 1.026,
        "sl_mult": 0.984
    },
    {
        "symbol": "ICICIBANK",
        "ticker": "ICICIBANK.NS",
        "name": "ICICI Bank Ltd",
        "segment": "NSE 5X MIS",
        "base_price": 1386.90,
        "qty_desc": "1 Share (5x)",
        "margin": 277.38,
        "target_mult": 1.025,
        "sl_mult": 0.985
    }
]

# Angel One: Zero to Hero F&O Options
ANGEL_OPTIONS_POOL = [
    {
        "symbol": "NIFTY 22800 CE",
        "name": "Nifty 50 Call Option",
        "segment": "6X ZERO TO HERO",
        "badge": "HERO CALL",
        "badge_bg": "rgba(16,185,129,0.15)",
        "badge_color": "#10b981",
        "entry_prem": 5.40,
        "lot_desc": "1 Lot (25 Qty)",
        "invested": 135.00,
        "target_prem": 28.00,
        "sl_prem": 1.80,
        "mult": 25
    },
    {
        "symbol": "NIFTY 22700 PE",
        "name": "Nifty 50 Put Option",
        "segment": "HERO REVERSAL",
        "badge": "HERO PUT",
        "badge_bg": "rgba(245,158,11,0.15)",
        "badge_color": "#f59e0b",
        "entry_prem": 7.20,
        "lot_desc": "1 Lot (25 Qty)",
        "invested": 180.00,
        "target_prem": 36.00,
        "sl_prem": 2.50,
        "mult": 25
    },
    {
        "symbol": "BANKNIFTY 52000 CE",
        "name": "Bank Nifty Call Option",
        "segment": "ZERO TO HERO",
        "badge": "BANK CALL",
        "badge_bg": "rgba(168,85,247,0.15)",
        "badge_color": "#c084fc",
        "entry_prem": 9.50,
        "lot_desc": "1 Lot (15 Qty)",
        "invested": 142.50,
        "target_prem": 48.00,
        "sl_prem": 3.50,
        "mult": 15
    }
]

# CoinDCX: 24/7 Spot Holdings in INR
COINDCX_SPOT_POOL = [
    {
        "symbol": "BTC / INR",
        "market": "BTCINR",
        "name": "Bitcoin Spot",
        "segment": "COINDCX SPOT",
        "fallback_price": 8084000.0,
        "cost": 400.00,
        "qty": 0.00005,
        "target_pct": 0.016,
        "sl_pct": -0.010
    },
    {
        "symbol": "ETH / INR",
        "market": "ETHINR",
        "name": "Ethereum Spot",
        "segment": "COINDCX SPOT",
        "fallback_price": 234000.0,
        "cost": 350.00,
        "qty": 0.0015,
        "target_pct": 0.020,
        "sl_pct": -0.012
    },
    {
        "symbol": "SOL / INR",
        "market": "SOLINR",
        "name": "Solana Spot",
        "segment": "COINDCX SPOT",
        "fallback_price": 10110.0,
        "cost": 300.00,
        "qty": 0.0296,
        "target_pct": 0.025,
        "sl_pct": -0.015
    },
    {
        "symbol": "DOGE / INR",
        "market": "DOGEINR",
        "name": "Dogecoin Spot",
        "segment": "COINDCX SPOT",
        "fallback_price": 7.76,
        "cost": 250.00,
        "qty": 32.2,
        "target_pct": 0.035,
        "sl_pct": -0.020
    }
]

# CoinDCX: High Leverage Futures in INR/USDT
COINDCX_FUTURES_POOL = [
    {
        "symbol": "BTC / USDT",
        "market": "BTCINR",
        "name": "Bitcoin Perpetual",
        "segment": "10X LEVERAGE",
        "badge": "10X FUTURES",
        "badge_bg": "rgba(16,185,129,0.15)",
        "badge_color": "#10b981",
        "fallback_price": 8084000.0,
        "margin": 200.0,
        "lev": 10,
        "target_pct": 0.020,
        "sl_pct": -0.012
    },
    {
        "symbol": "SOL / USDT",
        "market": "SOLINR",
        "name": "Solana Perpetual",
        "segment": "10X LEVERAGE",
        "badge": "10X FUTURES",
        "badge_bg": "rgba(56,189,248,0.15)",
        "badge_color": "#38bdf8",
        "fallback_price": 10110.0,
        "margin": 150.0,
        "lev": 10,
        "target_pct": 0.035,
        "sl_pct": -0.018
    },
    {
        "symbol": "ETH / USDT",
        "market": "ETHINR",
        "name": "Ethereum Perpetual",
        "segment": "10X LEVERAGE",
        "badge": "10X FUTURES",
        "badge_bg": "rgba(168,85,247,0.15)",
        "badge_color": "#c084fc",
        "fallback_price": 234000.0,
        "margin": 180.0,
        "lev": 10,
        "target_pct": 0.025,
        "sl_pct": -0.015
    },
    {
        "symbol": "DOGE / USDT",
        "market": "DOGEINR",
        "name": "Dogecoin Scalp",
        "segment": "5X RAPID",
        "badge": "5X SCALP",
        "badge_bg": "rgba(245,158,11,0.15)",
        "badge_color": "#f59e0b",
        "fallback_price": 7.76,
        "margin": 100.0,
        "lev": 5,
        "target_pct": 0.050,
        "sl_pct": -0.025
    }
]
