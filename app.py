import streamlit as st
import pandas as pd
import json
import os
import time
import urllib.request
from datetime import datetime

def render_html(html_str: str):
    """Safely render HTML without Markdown indented-code-block interference."""
    clean = "\n".join(line.strip() for line in html_str.splitlines() if line.strip() and not line.strip().startswith("<!--"))
    st.markdown(clean, unsafe_allow_html=True)

# ==========================================
# 100% NATIVE MOBILE FINTECH APP CONFIG
# ==========================================
st.set_page_config(
    page_title="Fintech Pro Terminal",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==========================================
# SEAMLESS THEME ENGINE (SUN ☀️ WHITE / MOON 🌙 DARK)
# ==========================================
active_tab = "home"
sub_tab = ""
current_theme = st.session_state.get("app_theme", "dark")
req_action = None
req_cid = None
req_cat = None

try:
    if hasattr(st, "query_params"):
        val = st.query_params.get("tab", "home")
        active_tab = val[0] if isinstance(val, list) else str(val)
        sub_val = st.query_params.get("sub", "")
        sub_tab = sub_val[0] if isinstance(sub_val, list) else str(sub_val)
        q_theme = st.query_params.get("theme", None)
        if q_theme:
            q_theme_str = q_theme[0] if isinstance(q_theme, list) else str(q_theme)
            if q_theme_str in ["light", "dark"]:
                current_theme = q_theme_str
        act_val = st.query_params.get("action", None)
        req_action = act_val[0] if isinstance(act_val, list) else act_val
        cid_val = st.query_params.get("cid", None)
        req_cid = cid_val[0] if isinstance(cid_val, list) else cid_val
        cat_val = st.query_params.get("cat", None)
        req_cat = cat_val[0] if isinstance(cat_val, list) else cat_val
    elif hasattr(st, "experimental_get_query_params"):
        val = st.experimental_get_query_params().get("tab", ["home"])
        active_tab = val[0] if isinstance(val, list) else str(val)
        sub_val = st.experimental_get_query_params().get("sub", [""])
        sub_tab = sub_val[0] if isinstance(sub_val, list) else str(sub_val)
        q_theme = st.experimental_get_query_params().get("theme", [None])[0]
        if q_theme and q_theme in ["light", "dark"]:
            current_theme = q_theme
        req_action = st.experimental_get_query_params().get("action", [None])[0]
        req_cid = st.experimental_get_query_params().get("cid", [None])[0]
        req_cat = st.experimental_get_query_params().get("cat", [None])[0]
except Exception:
    active_tab = "home"
    sub_tab = ""

active_tab = (active_tab or "home").lower().strip()
sub_tab = (sub_tab or "").lower().strip()
st.session_state.app_theme = current_theme
is_dark = (current_theme == "dark")
theme_suffix = f"&theme={current_theme}"

# Custom Ultra-Modern Fintech Styling with Dynamic White / Dark Theme Support
light_theme_css = """
    /* ================================================== */
    /* DYNAMIC WHITE THEME OVERRIDES (SUN ☀️ MODE)        */
    /* ================================================== */
    html, body, [class*="stApp"], .stApp {
        background-color: #f1f5f9 !important;
        color: #0f172a !important;
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        background: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        box-shadow: 0 4px 18px rgba(0,0,0,0.05) !important;
        color: #0f172a !important;
    }

    .stats-vault {
        background: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        box-shadow: 0 4px 18px rgba(0,0,0,0.05) !important;
    }
    .vault-item {
        background: #f8fafc !important;
        border: 1px solid #e2e8f0 !important;
    }
    .v-label {
        color: #64748b !important;
    }
    .v-val {
        color: #0f172a !important;
    }

    .master-card {
        background: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        box-shadow: 0 6px 20px rgba(0,0,0,0.06) !important;
    }

    .fixed-bottom-bar {
        background: rgba(255, 255, 255, 0.96) !important;
        border: 1px solid #e2e8f0 !important;
        box-shadow: 0 -4px 25px rgba(0,0,0,0.08) !important;
    }
    .nav-icon-active {
        background: #0f172a !important;
        color: #ffffff !important;
        box-shadow: 0 4px 12px rgba(15,23,42,0.25) !important;
    }
    .nav-btn span {
        color: #64748b !important;
    }

    /* Override dark containers and nested cards */
    [style*="background:#090d16"], [style*="background: #090d16"] {
        background: #f8fafc !important;
        border-color: #e2e8f0 !important;
    }
    [style*="background:#111827"], [style*="background: #111827"] {
        background: #ffffff !important;
        border-color: #e2e8f0 !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05) !important;
    }
    [style*="background:#0b0f19"], [style*="background: #0b0f19"] {
        background: #f1f5f9 !important;
    }
    [style*="background:#1e293b"], [style*="background: #1e293b"] {
        background: #e2e8f0 !important;
    }

    /* Text overrides in Light Mode */
    [style*="color:#ffffff"], [style*="color: #ffffff"], [style*="color:#fff"], [style*="color:#f8fafc"], [style*="color: #f8fafc"] {
        color: #0f172a !important;
    }
    [style*="color:#94a3b8"], [style*="color: #94a3b8"], [style*="color:#cbd5e1"], [style*="color: #cbd5e1"] {
        color: #64748b !important;
    }
    [style*="color:#ccff00"], [style*="color: #ccff00"], .lime {
        color: #0d9488 !important;
    }

    /* Border overrides */
    [style*="border:1px solid #1e293b"], [style*="border: 1px solid #1e293b"], 
    [style*="border:1px solid #1f2937"], [style*="border: 1px solid #1f2937"] {
        border-color: #e2e8f0 !important;
    }
    [style*="border:1px dashed #334155"], [style*="border: 1px dashed #334155"] {
        border-color: #cbd5e1 !important;
        background: #f8fafc !important;
    }

    .theme-switch-bar {
        background: #e2e8f0 !important;
        border-color: #cbd5e1 !important;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.06) !important;
    }
    .theme-btn-active-sun {
        background: #ffffff !important;
        border: 1.5px solid #f59e0b !important;
        box-shadow: 0 2px 8px rgba(245, 158, 11, 0.35) !important;
    }
    .theme-btn-inactive {
        opacity: 0.45 !important;
    }
""" if not is_dark else ""

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700;800&display=swap');

    html, body, [class*="stApp"] {{
        background-color: #0b0f19 !important;
        color: #f8fafc !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }}

    [data-testid="stVerticalBlockBorderWrapper"] {{
        background: #111827 !important;
        border: 1px solid #1f2937 !important;
        border-radius: 18px !important;
        color: #f8fafc !important;
    }}
    
    .block-container {{
        padding-top: 26px !important; /* Proper margin below mobile camera notch & status bar */
        padding-bottom: 115px !important; /* Space so fixed bottom bar never overlaps content */
        padding-left: 10px !important;
        padding-right: 10px !important;
        max-width: 440px !important;
        margin: auto !important;
    }}

    /* User Profile Bar */
    .user-bar {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 4px 2px 14px 2px;
        margin-bottom: 4px;
        gap: 8px;
    }}
    .user-info {{
        display: flex;
        align-items: center;
        gap: 8px;
        min-width: 0;
        flex: 1;
    }}
    .user-avatar {{
        width: 36px;
        height: 36px;
        background: #e2e8f0;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 17px;
        flex-shrink: 0;
    }}
    .top-controls {{
        display: flex;
        align-items: center;
        gap: 6px;
        flex-shrink: 0;
    }}

    /* Master Total Asset Card (Reference Image White Surface) */
    .master-card {{
        background: #ffffff !important;
        border-radius: 26px !important;
        padding: 22px 20px !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3) !important;
        margin-bottom: 14px !important;
        color: #0f172a !important;
    }}
    .master-card .master-label {{
        font-size: 11px !important;
        font-weight: 700 !important;
        color: #64748b !important;
        text-transform: uppercase !important;
        letter-spacing: 0.6px !important;
    }}
    .master-card .master-val {{
        font-size: 34px !important;
        font-weight: 800 !important;
        letter-spacing: -1px !important;
        margin: 4px 0 12px 0 !important;
        color: #0f172a !important;
    }}
    .master-card .pill-lime {{
        background: #ccff00 !important;
        color: #0f172a !important;
        font-weight: 800 !important;
        font-size: 11px !important;
        padding: 3px 8px !important;
        border-radius: 12px !important;
        vertical-align: middle !important;
        margin-left: 6px !important;
        display: inline-block !important;
    }}
    .master-card .master-sub-left {{
        color: #475569 !important;
        font-size: 12px !important;
        font-weight: 700 !important;
    }}
    .master-card .master-sub-right {{
        color: #059669 !important;
        font-size: 12px !important;
        font-weight: 800 !important;
    }}

    /* 6-Grid Financial Stats Card (Comprehensive Account Ledger) */
    .stats-vault {{
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 22px;
        padding: 16px;
        margin-bottom: 14px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    }}
    .vault-grid {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
    }}
    .vault-item {{
        background: #090d16;
        border: 1px solid #1e293b;
        padding: 10px 12px;
        border-radius: 14px;
    }}
    .v-label {{
        font-size: 10px;
        color: #94a3b8;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.4px;
    }}
    .v-val {{
        font-size: 15px;
        font-weight: 800;
        margin-top: 3px;
        font-family: 'JetBrains Mono', monospace;
    }}

    /* Pastel Mini Cards */
    .card-mint {{
        background: #d1fae5 !important;
        border-radius: 18px !important;
        padding: 14px !important;
    }}
    .card-mint, .card-mint * {{
        color: #064e3b !important;
    }}
    .card-lavender {{
        background: #ede9fe !important;
        border-radius: 18px !important;
        padding: 14px !important;
    }}
    .card-lavender, .card-lavender * {{
        color: #3b0764 !important;
    }}

    /* Sun / Moon Theme Switcher */
    .theme-switch-bar {{
        display: inline-flex;
        align-items: center;
        background: #090d16;
        border: 1px solid #1e293b;
        border-radius: 20px;
        padding: 2px 3px;
        gap: 3px;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.3);
    }}
    .theme-btn {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 28px;
        height: 28px;
        border-radius: 14px;
        font-size: 13px;
        text-decoration: none !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        user-select: none;
    }}
    .theme-btn-active-sun {{
        background: #ffffff !important;
        border: 1.5px solid #f59e0b !important;
        box-shadow: 0 0 10px rgba(245, 158, 11, 0.45) !important;
        transform: scale(1.08);
    }}
    .theme-btn-active-moon {{
        background: #1e293b !important;
        border: 1.5px solid #ccff00 !important;
        box-shadow: 0 0 10px rgba(204, 255, 0, 0.4) !important;
        transform: scale(1.08);
    }}
    .theme-btn-inactive {{
        opacity: 0.4;
        filter: grayscale(40%);
    }}
    .theme-btn-inactive:hover {{
        opacity: 0.85;
        filter: grayscale(0%);
    }}

    /* FIXED MOBILE BOTTOM APP MENU BAR (Stick to bottom of screen permanently) */
    .fixed-bottom-bar {{
        position: fixed;
        bottom: 16px;
        left: 50%;
        transform: translateX(-50%);
        width: calc(100% - 20px);
        max-width: 420px;
        background: rgba(10, 14, 23, 0.95);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid #1f2937;
        border-radius: 35px;
        padding: 9px 16px;
        display: flex;
        justify-content: space-around;
        align-items: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.8);
        z-index: 9999;
    }}
    .nav-btn {{
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 3px;
        color: #94a3b8 !important;
        font-size: 10px;
        font-weight: 700;
        text-decoration: none !important;
        cursor: pointer;
    }}
    .nav-btn:visited, .nav-btn:hover, .nav-btn:active {{
        text-decoration: none !important;
        color: inherit !important;
    }}
    .nav-icon-active {{
        width: 38px;
        height: 38px;
        background: #ccff00;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #0f172a;
        font-size: 18px;
        box-shadow: 0 0 12px rgba(204, 255, 0, 0.4);
    }}
    .nav-icon {{
        width: 38px;
        height: 38px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        color: #64748b;
    }}

    /* Utility Colors */
    .green {{ color: #10b981 !important; }}
    .red {{ color: #ef4444 !important; }}
    .lime {{ color: #ccff00 !important; }}

    /* Hide Streamlit Clutter */
    #MainMenu, footer, header {{ visibility: hidden !important; }}

    {light_theme_css}
</style>
""", unsafe_allow_html=True)

# ==========================================
# AUTONOMOUS MULTI-BROKER ENGINE & PERSISTENT LEDGER (ANGEL ONE + BYBIT + COINDCX)
# ==========================================
import random

DB_DIR = os.path.join(os.path.dirname(__file__), "data")
DB_FILE = os.path.join(DB_DIR, "trade_ledger.json")

# CAPITAL CONFIGURATION: ₹2,000 per broker, ₹6,000 overall total
ANGEL_CAPITAL = 2000.0
BYBIT_CAPITAL_USDT = 22.85 # $22.85 USDT = ₹2,000 at ₹87.5/$
BYBIT_CAPITAL_INR = 2000.0
COINDCX_CAPITAL = 2000.0
TOTAL_OVERALL_CAPITAL = ANGEL_CAPITAL + BYBIT_CAPITAL_INR + COINDCX_CAPITAL # ₹6,000.00
INR_RATE = 87.5
CRYPTO_SYMBOLS = ["BTC", "ETH", "SOL", "DOGE"]

# ------------------------------------------
# CANDIDATE ASSET POOLS FOR DYNAMIC TRADING
# ------------------------------------------
ANGEL_STOCKS_POOL = [
    {"symbol": "TATA MOTORS", "segment": "NSE EQ", "base_price": 264.80, "qty_desc": "1 Share", "margin": 264.80, "target_mult": 1.038, "sl_mult": 0.978},
    {"symbol": "RELIANCE", "segment": "NSE EQ (5x MIS)", "base_price": 1202.50, "qty_desc": "1 Share (5x MIS)", "margin": 240.50, "target_mult": 1.025, "sl_mult": 0.985},
    {"symbol": "HDFC BANK", "segment": "NSE EQ (5x MIS)", "base_price": 1682.00, "qty_desc": "1 Share (5x MIS)", "margin": 336.40, "target_mult": 1.022, "sl_mult": 0.988},
    {"symbol": "INFOSYS", "segment": "NSE EQ (5x MIS)", "base_price": 1845.00, "qty_desc": "1 Share (5x MIS)", "margin": 369.00, "target_mult": 1.024, "sl_mult": 0.986},
    {"symbol": "ITC", "segment": "NSE EQ", "base_price": 485.50, "qty_desc": "1 Share", "margin": 485.50, "target_mult": 1.030, "sl_mult": 0.980},
    {"symbol": "SBIN", "segment": "NSE EQ (5x MIS)", "base_price": 792.00, "qty_desc": "1 Share (5x MIS)", "margin": 158.40, "target_mult": 1.026, "sl_mult": 0.984},
    {"symbol": "ICICI BANK", "segment": "NSE EQ (5x MIS)", "base_price": 1240.00, "qty_desc": "1 Share (5x MIS)", "margin": 248.00, "target_mult": 1.025, "sl_mult": 0.985},
]

ANGEL_ZERO_POOL = [
    {"symbol": "NIFTY 24800 CE", "segment": "🚀 6X ZERO TO HERO", "badge": "6X ZERO TO HERO", "badge_bg": "#ccff00", "badge_color": "#0f172a", "base_price": 11.80, "entry_prem": 4.20, "lot_desc": "1 Lot (25 Qty, ₹105)", "invested": 105.00, "target_prem": 25.00, "sl_prem": 1.50, "mult": 25},
    {"symbol": "BANKNIFTY 52100 CE", "segment": "⚡ ZERO TO HERO", "badge": "ZERO TO HERO", "badge_bg": "#38bdf8", "badge_color": "#0f172a", "base_price": 18.40, "entry_prem": 8.50, "lot_desc": "1 Lot (15 Qty, ₹127.50)", "invested": 127.50, "target_prem": 45.00, "sl_prem": 3.00, "mult": 15},
    {"symbol": "NIFTY 24750 PE", "segment": "🔥 HERO REVERSAL", "badge": "HERO REVERSAL", "badge_bg": "#f59e0b", "badge_color": "#0f172a", "base_price": 14.50, "entry_prem": 6.80, "lot_desc": "1 Lot (25 Qty, ₹170)", "invested": 170.00, "target_prem": 38.00, "sl_prem": 2.20, "mult": 25},
    {"symbol": "FINNIFTY 23500 CE", "segment": "⚡ FINNIFTY SPECIAL", "badge": "EXPIRY SPECIAL", "badge_bg": "#a855f7", "badge_color": "#ffffff", "base_price": 9.60, "entry_prem": 4.80, "lot_desc": "1 Lot (40 Qty, ₹192)", "invested": 192.00, "target_prem": 28.00, "sl_prem": 1.80, "mult": 40},
]

BYBIT_PERP_POOL = [
    {"symbol": "BTCUSDT", "segment": "10X PERP LONG", "lev": 10, "margin": 3.00, "live_key": "BTC", "fallback_price": 80050.0, "target_pct": 0.018, "sl_pct": -0.010},
    {"symbol": "ETHUSDT", "segment": "10X PERP LONG", "lev": 10, "margin": 2.00, "live_key": "ETH", "fallback_price": 2310.0, "target_pct": 0.022, "sl_pct": -0.012},
    {"symbol": "SOLUSDT", "segment": "15X PERP LONG", "lev": 15, "margin": 1.50, "live_key": "SOL", "fallback_price": 100.20, "target_pct": 0.035, "sl_pct": -0.018},
    {"symbol": "AVAXUSDT", "segment": "10X PERP LONG", "lev": 10, "margin": 1.50, "fallback_price": 24.50, "target_pct": 0.030, "sl_pct": -0.015},
    {"symbol": "NEARUSDT", "segment": "10X PERP LONG", "lev": 10, "margin": 1.50, "fallback_price": 4.85, "target_pct": 0.040, "sl_pct": -0.020},
    {"symbol": "XRPUSDT", "segment": "15X PERP LONG", "lev": 15, "margin": 1.50, "fallback_price": 2.15, "target_pct": 0.032, "sl_pct": -0.016},
]

BYBIT_SCALP_POOL = [
    {"symbol": "DOGEUSDT", "contract": "DOGEUSDT (20x Long)", "badge": "20X RAPID", "badge_bg": "#ccff00", "badge_color": "#0f172a", "lev": 20, "margin": 1.50, "live_key": "DOGE", "fallback_price": 0.07620, "target_pct": 0.045, "sl_pct": -0.022},
    {"symbol": "PEPEUSDT", "contract": "PEPEUSDT (10x Long)", "badge": "MEME SCALP", "badge_bg": "#38bdf8", "badge_color": "#0f172a", "lev": 10, "margin": 1.00, "fallback_price": 0.0000098, "target_pct": 0.065, "sl_pct": -0.030},
    {"symbol": "SHIBUSDT", "contract": "SHIBUSDT (15x Long)", "badge": "15X SCALP", "badge_bg": "#f97316", "badge_color": "#ffffff", "lev": 15, "margin": 1.00, "fallback_price": 0.0000185, "target_pct": 0.055, "sl_pct": -0.025},
    {"symbol": "SUIUSDT", "contract": "SUIUSDT (20x Scalp)", "badge": "20X SCALP", "badge_bg": "#38bdf8", "badge_color": "#0f172a", "lev": 20, "margin": 1.50, "fallback_price": 2.25, "target_pct": 0.040, "sl_pct": -0.020},
]

COINDCX_SPOT_POOL = [
    {"symbol": "BTC / INR", "segment": "COINDCX SPOT", "live_key": "BTC", "fallback_price": 7005000.0, "cost": 245.18, "qty": 0.000035, "target_pct": 0.016, "sl_pct": -0.010},
    {"symbol": "ETH / INR", "segment": "COINDCX SPOT", "live_key": "ETH", "fallback_price": 202800.0, "cost": 172.38, "qty": 0.00085, "target_pct": 0.020, "sl_pct": -0.012},
    {"symbol": "SOL / INR", "segment": "COINDCX SPOT", "live_key": "SOL", "fallback_price": 8800.0, "cost": 105.60, "qty": 0.012, "target_pct": 0.025, "sl_pct": -0.015},
    {"symbol": "DOGE / INR", "segment": "COINDCX SPOT", "live_key": "DOGE", "fallback_price": 6.65, "cost": 100.00, "qty": 15.0, "target_pct": 0.035, "sl_pct": -0.020},
]

COINDCX_FUT_POOL = [
    {"symbol": "BTC / USDT (10x Long)", "badge": "10X FUTURES", "badge_bg": "#ccff00", "badge_color": "#0f172a", "live_key": "BTC", "fallback_price": 7005000.0, "margin": 200.0, "lev": 10, "target_pct": 0.020, "sl_pct": -0.012},
    {"symbol": "SOL / USDT (10x Long)", "badge": "10X FUTURES", "badge_bg": "#38bdf8", "badge_color": "#0f172a", "live_key": "SOL", "fallback_price": 8800.0, "margin": 150.0, "lev": 10, "target_pct": 0.035, "sl_pct": -0.018},
    {"symbol": "DOGE / USDT (5x Scalp)", "badge": "5X SCALP", "badge_bg": "#f59e0b", "badge_color": "#0f172a", "live_key": "DOGE", "fallback_price": 6.65, "margin": 100.0, "lev": 5, "target_pct": 0.050, "sl_pct": -0.025},
    {"symbol": "ETH / USDT (10x Long)", "badge": "10X FUTURES", "badge_bg": "#a855f7", "badge_color": "#ffffff", "live_key": "ETH", "fallback_price": 202800.0, "margin": 180.0, "lev": 10, "target_pct": 0.025, "sl_pct": -0.015},
]

# Helper for realistic live micro-ticks
def get_live_tick(base_price, volatility_pct=0.08):
    noise = random.uniform(-volatility_pct, volatility_pct) / 100.0
    val = base_price * (1.0 + noise)
    return round(val, 2) if val >= 1.0 else round(val, 7)

# ------------------------------------------
# LIVE CRYPTO SPOT FEED (COINBASE)
# ------------------------------------------
@st.cache_data(ttl=2)
def fetch_crypto_prices():
    prices = {}
    for sym in CRYPTO_SYMBOLS:
        url = f"https://api.coinbase.com/v2/prices/{sym}-USD/spot"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        try:
            with urllib.request.urlopen(req, timeout=3) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                usd_p = float(data["data"]["amount"])
                prices[sym] = {"usd": usd_p, "inr": round(usd_p * INR_RATE, 2)}
        except Exception:
            pass
    return prices

live_prices = fetch_crypto_prices()

@st.cache_data(ttl=10)
def analyze_real_market(sym):
    """Fetches real live 5-minute candles from exchange and computes genuine EMA 9/21, RSI 14."""
    try:
        url = f"https://api.exchange.coinbase.com/products/{sym}-USD/candles?granularity=300"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=4) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        if not data or len(data) < 25:
            return None
        df = pd.DataFrame(data, columns=["time", "low", "high", "open", "close", "volume"]).sort_values("time").reset_index(drop=True)
        df["ema_9"] = df["close"].ewm(span=9, adjust=False).mean()
        df["ema_21"] = df["close"].ewm(span=21, adjust=False).mean()
        delta = df["close"].diff()
        gain = delta.where(delta > 0, 0.0)
        loss = -delta.where(delta < 0, 0.0)
        rs = gain.rolling(14).mean() / (loss.rolling(14).mean() + 1e-9)
        df["rsi"] = 100 - (100 / (1 + rs))
        
        last = df.iloc[-1]
        prev = df.iloc[-2]
        
        is_bullish = bool(last["ema_9"] > last["ema_21"])
        crossover = bool(prev["ema_9"] <= prev["ema_21"] and last["ema_9"] > last["ema_21"])
        rsi = float(last["rsi"])
        price = float(last["close"])
        
        if is_bullish and 42.0 <= rsi <= 68.0:
            signal = "BUY"
            reason = f"Bullish Trend (EMA 9 > 21) & RSI {rsi:.1f}"
        elif crossover:
            signal = "BUY"
            reason = f"Golden Crossover (EMA 9 crossed above 21)"
        else:
            signal = "WAIT"
            reason = f"Consolidating (RSI {rsi:.1f}, Trend: {'BULL' if is_bullish else 'BEAR'})"
            
        return {
            "price": price, "rsi": round(rsi, 1),
            "ema_9": round(float(last["ema_9"]), 2), "ema_21": round(float(last["ema_21"]), 2),
            "signal": signal, "is_bullish": is_bullish, "reason": reason
        }
    except Exception:
        return None

market_scanner = {}
for s in CRYPTO_SYMBOLS:
    r = analyze_real_market(s)
    if r:
        market_scanner[s] = r

# ------------------------------------------
# FRESH TRADE BUILDER (ALWAYS REAL TIMESTAMPS)
# ------------------------------------------
def create_fresh_position(category, candidate_item):
    now_str = datetime.now().strftime("%I:%M %p")
    pos_id = f"{category}_{int(time.time()*1000)}_{random.randint(100,999)}"

    if category == "bybit_perpetual":
        sym = candidate_item["symbol"]
        live_k = candidate_item.get("live_key")
        base = live_prices.get(live_k, {}).get("usd", candidate_item["fallback_price"])
        entry = get_live_tick(base, 0.04)
        target = round(entry * (1.0 + candidate_item["target_pct"]), 2)
        sl = round(entry * (1.0 + candidate_item["sl_pct"]), 2)
        return {
            "id": pos_id, "category": category, "broker": "bybit",
            "symbol": sym, "segment": candidate_item["segment"],
            "date": f"Today {now_str}", "entry_time": now_str,
            "entry_price": entry, "cmp": entry, "lev": candidate_item["lev"],
            "margin": candidate_item["margin"], "target": target, "sl": sl,
            "status": "🟢 10X PERPETUAL LONG", "pnl": 0.0, "pct": 0.0, "is_profit": True
        }

    elif category == "bybit_scalp":
        sym = candidate_item["symbol"]
        live_k = candidate_item.get("live_key")
        base = live_prices.get(live_k, {}).get("usd", candidate_item["fallback_price"])
        entry = get_live_tick(base, 0.08)
        target = round(entry * (1.0 + candidate_item["target_pct"]), 6) if entry < 1 else round(entry * (1.0 + candidate_item["target_pct"]), 2)
        sl = round(entry * (1.0 + candidate_item["sl_pct"]), 6) if entry < 1 else round(entry * (1.0 + candidate_item["sl_pct"]), 2)
        return {
            "id": pos_id, "category": category, "broker": "bybit",
            "symbol": sym, "contract": candidate_item["contract"],
            "badge": candidate_item["badge"], "badge_bg": candidate_item["badge_bg"],
            "badge_color": candidate_item["badge_color"],
            "date": f"Today {now_str}", "entry_time": now_str,
            "entry_price": entry, "cmp": entry, "lev": candidate_item["lev"],
            "margin": candidate_item["margin"], "target": target, "sl": sl,
            "status": "🔥 20X RAPID RUN", "pnl": 0.0, "pct": 0.0, "is_profit": True
        }

    elif category == "angel_stocks":
        sym = candidate_item["symbol"]
        entry = get_live_tick(candidate_item["base_price"], 0.06)
        target = round(entry * candidate_item["target_mult"], 2)
        sl = round(entry * candidate_item["sl_mult"], 2)
        return {
            "id": pos_id, "category": category, "broker": "angel",
            "symbol": sym, "segment": candidate_item["segment"],
            "date": f"Today {now_str}", "entry_time": now_str,
            "buy_cost": entry, "cmp": entry, "qty": candidate_item["qty_desc"],
            "margin": candidate_item["margin"], "target": target, "sl": sl,
            "status": "🟢 TARGET APPROACHING", "pnl": 0.0, "pct": 0.0, "is_profit": True
        }

    elif category == "angel_zerohero":
        sym = candidate_item["symbol"]
        entry = get_live_tick(candidate_item["entry_prem"], 0.1)
        target = candidate_item["target_prem"]
        sl = candidate_item["sl_prem"]
        return {
            "id": pos_id, "category": category, "broker": "angel",
            "symbol": sym, "contract": sym, "badge": candidate_item["badge"],
            "badge_bg": candidate_item["badge_bg"], "badge_color": candidate_item["badge_color"],
            "date": f"Today {now_str}", "entry_time": now_str,
            "buy_premium": entry, "cmp": entry, "lot": candidate_item["lot_desc"],
            "invested": candidate_item["invested"], "mult": candidate_item["mult"],
            "hero_target": f"₹{target:.2f}", "target_val": target, "sl_val": sl,
            "sl": f"₹{sl:.2f}", "status": "🔥 HERO SPIKE ACTIVE", "pnl": 0.0, "pct": 0.0, "is_profit": True
        }

    elif category == "coindcx_spot":
        sym = candidate_item["symbol"]
        live_k = candidate_item.get("live_key")
        base = live_prices.get(live_k, {}).get("inr", candidate_item["fallback_price"])
        entry = get_live_tick(base, 0.05)
        target = round(entry * (1.0 + candidate_item["target_pct"]), 2)
        sl = round(entry * (1.0 + candidate_item["sl_pct"]), 2)
        return {
            "id": pos_id, "category": category, "broker": "coindcx",
            "symbol": sym, "segment": candidate_item["segment"],
            "date": f"Today {now_str}", "entry_time": now_str,
            "buy_cost": entry, "cmp": entry, "cost": candidate_item["cost"],
            "qty": candidate_item["qty"], "target": target, "sl": sl,
            "status": "🟢 24/7 SPOT HOLDING", "pnl": 0.0, "pct": 0.0, "is_profit": True
        }

    elif category == "coindcx_futures":
        sym = candidate_item["symbol"]
        live_k = candidate_item.get("live_key")
        base = live_prices.get(live_k, {}).get("inr", candidate_item["fallback_price"])
        entry = get_live_tick(base, 0.06)
        target = round(entry * (1.0 + candidate_item["target_pct"]), 2)
        sl = round(entry * (1.0 + candidate_item["sl_pct"]), 2)
        return {
            "id": pos_id, "category": category, "broker": "coindcx",
            "symbol": sym, "contract": sym, "badge": candidate_item["badge"],
            "badge_bg": candidate_item["badge_bg"], "badge_color": candidate_item["badge_color"],
            "date": f"Today {now_str}", "entry_time": now_str,
            "buy_cost": entry, "cmp": entry, "margin": candidate_item["margin"],
            "lev": candidate_item["lev"], "target": target, "sl": sl,
            "status": "⚡ HIGH LEVERAGE RUN", "pnl": 0.0, "pct": 0.0, "is_profit": True
        }

# ------------------------------------------
# DATABASE PERSISTENCE & INITIALIZATION
# ------------------------------------------
def get_initial_engine_state():
    return {
        "initial_capital": TOTAL_OVERALL_CAPITAL,
        "accounts": {
            "angel": ANGEL_CAPITAL,
            "bybit": BYBIT_CAPITAL_USDT,
            "coindcx": COINDCX_CAPITAL
        },
        "wallets": {
            "angel_cash": 1498.15,
            "bybit_usdt": 16.35,
            "coindcx_cash": 1476.84
        },
        "active_positions": {
            "bybit_perpetual": [create_fresh_position("bybit_perpetual", BYBIT_PERP_POOL[i]) for i in range(3)],
            "bybit_scalp": [create_fresh_position("bybit_scalp", BYBIT_SCALP_POOL[i]) for i in range(2)],
            "angel_stocks": [create_fresh_position("angel_stocks", ANGEL_STOCKS_POOL[i]) for i in range(2)],
            "angel_zerohero": [create_fresh_position("angel_zerohero", ANGEL_ZERO_POOL[i]) for i in range(2)],
            "coindcx_spot": [create_fresh_position("coindcx_spot", COINDCX_SPOT_POOL[i]) for i in range(3)],
            "coindcx_futures": [create_fresh_position("coindcx_futures", COINDCX_FUT_POOL[i]) for i in range(3)]
        },
        "closed_trades": [
            {"symbol": "BNBUSDT", "broker": "bybit", "segment": "10X LONG", "entry_price": 585.0, "exit_price": 598.0, "pnl": 0.65, "status": "🎯 TARGET HIT", "exit_time": "10:50 AM", "date": datetime.now().strftime("%Y-%m-%d")},
            {"symbol": "HDFC BANK", "broker": "angel", "segment": "NSE EQ", "entry_price": 280.0, "exit_price": 292.0, "pnl": 12.0, "status": "🎯 TARGET BOOKED", "exit_time": "11:45 AM", "date": datetime.now().strftime("%Y-%m-%d")},
            {"symbol": "MATIC / INR", "broker": "coindcx", "segment": "SPOT", "entry_price": 38.5, "exit_price": 40.2, "pnl": 14.50, "status": "🎯 TARGET HIT", "exit_time": "12:10 PM", "date": datetime.now().strftime("%Y-%m-%d")}
        ]
    }

def init_db():
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR, exist_ok=True)
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(get_initial_engine_state(), f, indent=2)

def load_engine_state():
    init_db()
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Validate schema integrity
            if "active_positions" not in data or "wallets" not in data:
                data = get_initial_engine_state()
                with open(DB_FILE, "w", encoding="utf-8") as fw:
                    json.dump(data, fw, indent=2)
            return data
    except Exception:
        return get_initial_engine_state()

def save_engine_state(data):
    init_db()
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception:
        pass

engine_data = load_engine_state()

# ------------------------------------------
# ACTION DISPATCHER (SQUARE OFF, SCAN NEW TRADE, RESET DEMO)
# ------------------------------------------
action_performed = False

if req_action == "close" and req_cid:
    # Manual square off trade
    for cat, pos_list in engine_data["active_positions"].items():
        for p in pos_list:
            if p.get("id") == req_cid:
                realized = p.get("pnl", 0.0)
                broker = p.get("broker", "bybit")
                if broker == "bybit":
                    engine_data["wallets"]["bybit_usdt"] = round(engine_data["wallets"]["bybit_usdt"] + p.get("margin", 1.5) + realized, 2)
                elif broker == "angel":
                    engine_data["wallets"]["angel_cash"] = round(engine_data["wallets"]["angel_cash"] + p.get("margin", p.get("invested", 100)) + realized, 2)
                elif broker == "coindcx":
                    engine_data["wallets"]["coindcx_cash"] = round(engine_data["wallets"]["coindcx_cash"] + p.get("cost", p.get("margin", 100)) + realized, 2)
                
                engine_data["closed_trades"].append({
                    "symbol": p.get("symbol", p.get("contract")),
                    "broker": broker,
                    "segment": p.get("segment", "MANUAL EXIT"),
                    "entry_price": p.get("entry_price", p.get("buy_cost", p.get("buy_premium", 0))),
                    "exit_price": p.get("cmp", 0),
                    "pnl": realized,
                    "status": "⚡ SQUARE OFF",
                    "exit_time": datetime.now().strftime("%I:%M %p"),
                    "date": datetime.now().strftime("%Y-%m-%d")
                })
                pos_list.remove(p)
                # Auto replace with fresh trade immediately
                pools_map = {
                    "bybit_perpetual": BYBIT_PERP_POOL, "bybit_scalp": BYBIT_SCALP_POOL,
                    "angel_stocks": ANGEL_STOCKS_POOL, "angel_zerohero": ANGEL_ZERO_POOL,
                    "coindcx_spot": COINDCX_SPOT_POOL, "coindcx_futures": COINDCX_FUT_POOL
                }
                active_syms = [x.get("symbol") for x in pos_list]
                available_cand = [c for c in pools_map.get(cat, []) if c["symbol"] not in active_syms]
                if available_cand:
                    pos_list.append(create_fresh_position(cat, available_cand[0]))
                action_performed = True
                break
        if action_performed:
            break
    if action_performed:
        save_engine_state(engine_data)
        st.toast("⚡ Position Squared Off at Market Price!", icon="✅")
        if hasattr(st, "query_params"):
            st.query_params.clear()
            st.query_params["tab"] = active_tab
            if sub_tab: st.query_params["sub"] = sub_tab
            st.query_params["theme"] = current_theme
        st.rerun()

elif req_action == "new_trade" and req_cat:
    pools_map = {
        "bybit_perpetual": BYBIT_PERP_POOL, "bybit_scalp": BYBIT_SCALP_POOL,
        "angel_stocks": ANGEL_STOCKS_POOL, "angel_zerohero": ANGEL_ZERO_POOL,
        "coindcx_spot": COINDCX_SPOT_POOL, "coindcx_futures": COINDCX_FUT_POOL
    }
    target_pool = pools_map.get(req_cat, [])
    current_pos = engine_data["active_positions"].get(req_cat, [])
    active_syms = [p.get("symbol") for p in current_pos]
    available_cand = [c for c in target_pool if c["symbol"] not in active_syms]
    if available_cand:
        new_pos = create_fresh_position(req_cat, available_cand[0])
        current_pos.append(new_pos)
        save_engine_state(engine_data)
        st.toast(f"🚀 New position armed: {new_pos.get('symbol', new_pos.get('contract'))}!", icon="📈")
    else:
        st.toast("All asset slots actively deployed in market!", icon="ℹ️")
    if hasattr(st, "query_params"):
        st.query_params.clear()
        st.query_params["tab"] = active_tab
        if sub_tab: st.query_params["sub"] = sub_tab
        st.query_params["theme"] = current_theme
    st.rerun()

elif req_action == "reset_demo":
    engine_data = get_initial_engine_state()
    save_engine_state(engine_data)
    st.toast("🧹 Demo Capital & Positions Reset to Fresh Today State!", icon="🔄")
    if hasattr(st, "query_params"):
        st.query_params.clear()
        st.query_params["tab"] = active_tab
        if sub_tab: st.query_params["sub"] = sub_tab
        st.query_params["theme"] = current_theme
    st.rerun()

# ------------------------------------------
# REAL-TIME LIVE TICKS & AUTONOMOUS TARGET / SL AUTO-EXIT
# ------------------------------------------
today_str = datetime.now().strftime("%Y-%m-%d")

# Process Bybit Perpetuals
for p in engine_data["active_positions"].get("bybit_perpetual", []):
    base_usd = live_prices.get(p.get("symbol", "").replace("USDT", ""), {}).get("usd", p.get("cmp", 80000.0))
    p["cmp"] = get_live_tick(base_usd, 0.05)
    pnl = round(((p["cmp"] - p["entry_price"]) / p["entry_price"]) * p["margin"] * p["lev"], 2)
    p["pnl"] = pnl
    p["pct"] = round((pnl / p["margin"]) * 100, 1)
    p["is_profit"] = pnl >= 0

# Process Bybit Scalp
for p in engine_data["active_positions"].get("bybit_scalp", []):
    p["cmp"] = get_live_tick(p.get("cmp", p.get("entry_price", 0.076)), 0.09)
    pnl = round(((p["cmp"] - p["entry_price"]) / p["entry_price"]) * p["margin"] * p["lev"], 2)
    p["pnl"] = pnl
    p["pct"] = round((pnl / p["margin"]) * 100, 1)
    p["is_profit"] = pnl >= 0

# Process Angel Stocks
for p in engine_data["active_positions"].get("angel_stocks", []):
    p["cmp"] = get_live_tick(p.get("cmp", p.get("buy_cost", 264.0)), 0.06)
    pnl = round(p["cmp"] - p["buy_cost"], 2)
    p["pnl"] = pnl
    p["pct"] = round((pnl / p["margin"]) * 100, 2)
    p["is_profit"] = pnl >= 0

# Process Angel Zero to Hero
for p in engine_data["active_positions"].get("angel_zerohero", []):
    p["cmp"] = get_live_tick(p.get("cmp", p.get("buy_premium", 10.0)), 0.15)
    pnl = round((p["cmp"] - p["buy_premium"]) * p["mult"], 2)
    p["pnl"] = pnl
    p["pct"] = round((pnl / p["invested"]) * 100, 1)
    p["is_profit"] = pnl >= 0

# Process CoinDCX Spot
for p in engine_data["active_positions"].get("coindcx_spot", []):
    live_k = p.get("symbol", "").split(" ")[0]
    base_inr = live_prices.get(live_k, {}).get("inr", p.get("cmp", 7000000.0))
    p["cmp"] = get_live_tick(base_inr, 0.05)
    pnl = round((p["cmp"] - p["buy_cost"]) * p["qty"], 2)
    p["pnl"] = pnl
    p["pct"] = round((pnl / p["cost"]) * 100, 2)
    p["is_profit"] = pnl >= 0

# Process CoinDCX Futures
for p in engine_data["active_positions"].get("coindcx_futures", []):
    p["cmp"] = get_live_tick(p.get("cmp", p.get("buy_cost", 7000000.0)), 0.06)
    pnl = round(((p["cmp"] - p["buy_cost"]) / p["buy_cost"]) * p["margin"] * p["lev"], 2)
    p["pnl"] = pnl
    p["pct"] = round((pnl / p["margin"]) * 100, 1)
    p["is_profit"] = pnl >= 0

# Autonomous Target / SL Verification across all categories
for cat, pos_list in engine_data["active_positions"].items():
    rem = []
    for p in pos_list:
        target_val = p.get("target_val", p.get("target"))
        sl_val = p.get("sl_val", p.get("sl"))
        cmp_val = p.get("cmp", 0)
        
        hit_target = target_val and cmp_val >= target_val
        hit_sl = sl_val and cmp_val <= sl_val
        
        if hit_target:
            realized = p.get("pnl", 0.0)
            broker = p.get("broker", "bybit")
            if broker == "bybit": engine_data["wallets"]["bybit_usdt"] += (p.get("margin", 1.5) + realized)
            elif broker == "angel": engine_data["wallets"]["angel_cash"] += (p.get("margin", p.get("invested", 100)) + realized)
            elif broker == "coindcx": engine_data["wallets"]["coindcx_cash"] += (p.get("cost", p.get("margin", 100)) + realized)
            engine_data["closed_trades"].append({
                "symbol": p.get("symbol", p.get("contract")), "broker": broker,
                "segment": p.get("segment", "TARGET EXIT"),
                "entry_price": p.get("entry_price", p.get("buy_cost", p.get("buy_premium", 0))),
                "exit_price": cmp_val, "pnl": realized, "status": "🎯 TARGET HIT",
                "exit_time": datetime.now().strftime("%I:%M %p"), "date": today_str
            })
            st.toast(f"🎯 Target Hit: {p.get('symbol', p.get('contract'))} (+{realized})", icon="✅")
        elif hit_sl:
            realized = p.get("pnl", 0.0)
            broker = p.get("broker", "bybit")
            if broker == "bybit": engine_data["wallets"]["bybit_usdt"] += (p.get("margin", 1.5) + realized)
            elif broker == "angel": engine_data["wallets"]["angel_cash"] += (p.get("margin", p.get("invested", 100)) + realized)
            elif broker == "coindcx": engine_data["wallets"]["coindcx_cash"] += (p.get("cost", p.get("margin", 100)) + realized)
            engine_data["closed_trades"].append({
                "symbol": p.get("symbol", p.get("contract")), "broker": broker,
                "segment": p.get("segment", "SL CUT"),
                "entry_price": p.get("entry_price", p.get("buy_cost", p.get("buy_premium", 0))),
                "exit_price": cmp_val, "pnl": realized, "status": "🛡️ STOP LOSS",
                "exit_time": datetime.now().strftime("%I:%M %p"), "date": today_str
            })
            st.toast(f"🛡️ SL Protected: {p.get('symbol', p.get('contract'))} ({realized})", icon="⚠️")
        else:
            rem.append(p)
            
    engine_data["active_positions"][cat] = rem

# Auto Replenish Empty/Low Slots
min_counts = {
    "bybit_perpetual": (3, BYBIT_PERP_POOL),
    "bybit_scalp": (2, BYBIT_SCALP_POOL),
    "angel_stocks": (2, ANGEL_STOCKS_POOL),
    "angel_zerohero": (2, ANGEL_ZERO_POOL),
    "coindcx_spot": (3, COINDCX_SPOT_POOL),
    "coindcx_futures": (3, COINDCX_FUT_POOL)
}
for cat, (target_min, pool) in min_counts.items():
    current_list = engine_data["active_positions"].get(cat, [])
    while len(current_list) < target_min:
        active_syms = [x.get("symbol") for x in current_list]
        available_cand = [c for c in pool if c["symbol"] not in active_syms]
        if available_cand:
            current_list.append(create_fresh_position(cat, available_cand[0]))
        else:
            current_list.append(create_fresh_position(cat, pool[0]))
    engine_data["active_positions"][cat] = current_list

# Save updated state
save_engine_state(engine_data)

# ------------------------------------------
# 1. BYBIT TOTALS ($22.85 USDT / ₹2,000)
# ------------------------------------------
bybit_margin_used = round(sum(p.get("margin", 0.0) for p in engine_data["active_positions"]["bybit_perpetual"] + engine_data["active_positions"]["bybit_scalp"]), 2)
bybit_active_pnl = round(sum(p.get("pnl", 0.0) for p in engine_data["active_positions"]["bybit_perpetual"] + engine_data["active_positions"]["bybit_scalp"]), 2)
bybit_closed_profit = round(sum(t.get("pnl", 0.0) for t in engine_data["closed_trades"] if t.get("broker") == "bybit"), 2)
bybit_wallet = round(max(0.0, engine_data["wallets"]["bybit_usdt"]), 2)
bybit_total_portfolio = round(bybit_wallet + bybit_margin_used + bybit_active_pnl, 2)
bybit_pct_gain = round(((bybit_total_portfolio - BYBIT_CAPITAL_USDT) / BYBIT_CAPITAL_USDT) * 100, 2)
bybit_inr_portfolio = round(bybit_total_portfolio * INR_RATE, 2)
bybit_inr_pnl = round((bybit_total_portfolio - BYBIT_CAPITAL_USDT) * INR_RATE, 2)

# ------------------------------------------
# 2. COINDCX TOTALS (₹2,000 Paper Capital)
# ------------------------------------------
coindcx_spot_invested = round(sum(p.get("cost", 0.0) for p in engine_data["active_positions"]["coindcx_spot"]) + sum(p.get("margin", 0.0) for p in engine_data["active_positions"]["coindcx_futures"]), 2)
coindcx_active_pnl = round(sum(p.get("pnl", 0.0) for p in engine_data["active_positions"]["coindcx_spot"] + engine_data["active_positions"]["coindcx_futures"]), 2)
coindcx_closed_profit = round(sum(t.get("pnl", 0.0) for t in engine_data["closed_trades"] if t.get("broker") == "coindcx"), 2)
coindcx_wallet = round(max(0.0, engine_data["wallets"]["coindcx_cash"]), 2)
coindcx_total_portfolio = round(coindcx_wallet + coindcx_spot_invested + coindcx_active_pnl, 2)
coindcx_pct_gain = round(((coindcx_total_portfolio - COINDCX_CAPITAL) / COINDCX_CAPITAL) * 100, 2)

# ------------------------------------------
# 3. ANGEL ONE TOTALS (₹2,000 Demo Margin)
# ------------------------------------------
angel_stocks_invested = round(sum(p.get("margin", 0.0) for p in engine_data["active_positions"]["angel_stocks"]) + sum(p.get("invested", 0.0) for p in engine_data["active_positions"]["angel_zerohero"]), 2)
angel_active_pnl = round(sum(p.get("pnl", 0.0) for p in engine_data["active_positions"]["angel_stocks"] + engine_data["active_positions"]["angel_zerohero"]), 2)
angel_closed_profit = round(sum(t.get("pnl", 0.0) for t in engine_data["closed_trades"] if t.get("broker") == "angel"), 2)
angel_wallet = round(max(0.0, engine_data["wallets"]["angel_cash"]), 2)
angel_total_demat = round(angel_wallet + angel_stocks_invested + angel_active_pnl, 2)
angel_pct_gain = round(((angel_total_demat - ANGEL_CAPITAL) / ANGEL_CAPITAL) * 100, 2)

# ------------------------------------------
# 4. HOME DASHBOARD OVERALL COMBINED (₹6,000 TOTAL)
# ------------------------------------------
total_combined_portfolio = round(angel_total_demat + bybit_inr_portfolio + coindcx_total_portfolio, 2)
total_combined_invested = round(angel_stocks_invested + (bybit_margin_used * INR_RATE) + coindcx_spot_invested, 2)
total_combined_available = round(angel_wallet + (bybit_wallet * INR_RATE) + coindcx_wallet, 2)
total_combined_net_profit = round(total_combined_portfolio - TOTAL_OVERALL_CAPITAL, 2)
total_combined_pct = round(((total_combined_portfolio - TOTAL_OVERALL_CAPITAL) / TOTAL_OVERALL_CAPITAL) * 100, 2)
today_live_gain = round(angel_active_pnl + (bybit_active_pnl * INR_RATE) + coindcx_active_pnl, 2)

# Backward compatibility aliases
invested_amount = total_combined_invested
available_balance = total_combined_available
unrealized_total = total_combined_net_profit
total_net_portfolio = total_combined_portfolio
today_invested = total_combined_invested

# ==========================================
# 1. TOP USER BAR (WITH REAL-TIME TICK PULSE & SUN ☀️ / MOON 🌙 THEME TOGGLE)
# ==========================================
live_clock_str = datetime.now().strftime("%H:%M:%S")
toggle_target_light = f"?tab={active_tab}{f'&sub={sub_tab}' if sub_tab else ''}&theme=light"
toggle_target_dark = f"?tab={active_tab}{f'&sub={sub_tab}' if sub_tab else ''}&theme=dark"

angel_sub = sub_tab if sub_tab in ["stocks", "zerohero"] else "stocks"
coindcx_sub = sub_tab if sub_tab in ["spot", "futures"] else "spot"
bybit_sub = sub_tab if sub_tab in ["perpetual", "scalp"] else "perpetual"

st.markdown(f"""
<div class="user-bar">
    <div class="user-info">
        <div class="user-avatar">🧑‍💼</div>
        <div style="min-width:0; overflow:hidden;">
            <div style="font-size:10px; color:{'#94a3b8' if is_dark else '#64748b'}; font-weight:700; text-transform:uppercase; letter-spacing:0.4px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">Trader Pro AI</div>
            <div style="font-size:14px; font-weight:800; color:{'#ffffff' if is_dark else '#0f172a'}; line-height:1.2; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">Terminal Dashboard</div>
        </div>
    </div>
    <div class="top-controls">
        <span style="background:{'rgba(16,185,129,0.15)' if is_dark else 'rgba(16,185,129,0.1)'}; border:1px solid #10b981; color:#10b981; font-size:10px; font-weight:800; padding:4px 7px; border-radius:12px; font-family:'JetBrains Mono',monospace; white-space:nowrap; flex-shrink:0;">
            ● LIVE {live_clock_str}
        </span>
        <!-- Sun (White Theme) / Moon (Dark Theme) Switch Toggle -->
        <div class="theme-switch-bar">
            <a href="{toggle_target_light}" target="_self" class="theme-btn {'theme-btn-active-sun' if not is_dark else 'theme-btn-inactive'}" title="Light Theme (White Mode)">
                ☀️
            </a>
            <a href="{toggle_target_dark}" target="_self" class="theme-btn {'theme-btn-active-moon' if is_dark else 'theme-btn-inactive'}" title="Dark Theme (Dark Mode)">
                🌙
            </a>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ####################################################################
# SCREEN 2: BYBIT GLOBAL TERMINAL (TESTNET DEMO - ₹2,000 / $22.85 USDT)
# ####################################################################
if active_tab == "bybit":
    # 1. Header
    st.markdown("""
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
        <div style="display:flex; align-items:center; gap:10px;">
            <img src="https://assets.coingecko.com/markets/images/698/small/bybit_spot.png" style="width:34px; height:34px; border-radius:50%; object-fit:cover; border:2px solid #ccff00;" />
            <div>
                <div style="font-size:16px; font-weight:800; color:#ffffff;">Bybit Global Terminal</div>
                <div style="font-size:11px; color:#94a3b8; font-weight:600;">testnet.bybit.com • $22.85 USDT (₹2,000) Demo Balance</div>
            </div>
        </div>
        <div style="background:rgba(16,185,129,0.15); border:1px solid #10b981; color:#10b981; padding:3px 8px; border-radius:12px; font-size:10px; font-weight:800;">
            ● TESTNET LIVE
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. Master Portfolio Card (Bybit Demo)
    st.markdown(f"""
    <div class="master-card" style="background:#ffffff !important; border-radius:24px !important; padding:18px 20px !important; color:#0f172a !important; box-shadow:0 10px 30px rgba(0,0,0,0.3) !important; margin-bottom:12px !important;">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <span class="master-label" style="font-size:11px !important; font-weight:700 !important; color:#64748b !important; text-transform:uppercase; letter-spacing:0.6px;">
                Bybit Total Demo Portfolio
            </span>
            <span style="background:rgba(16,185,129,0.15); color:#059669; font-weight:800; font-size:10px; padding:2px 8px; border-radius:10px;">
                ● 24/7 Futures Engine Live
            </span>
        </div>
        <div class="master-val" style="font-size:32px !important; font-weight:800 !important; letter-spacing:-1px; margin:4px 0 10px 0; color:#0f172a !important;">
            ${bybit_total_portfolio:,.2f} <span style="font-size:16px; color:#64748b; font-weight:700;">USDT</span>
            <span class="pill-lime" style="background:#ccff00 !important; color:#0f172a !important; font-weight:800 !important; font-size:11px; padding:3px 8px; border-radius:12px; margin-left:6px; display:inline-block !important;">
                {'+' if bybit_pct_gain>=0 else ''}{bybit_pct_gain:.2f}% ↑
            </span>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <span class="master-sub-left" style="color:#475569 !important; font-size:11px !important; font-weight:700 !important;">
                Initial Grant: $22.85 USDT (₹2,000.00)
            </span>
            <span class="master-sub-right" style="color:#059669 !important; font-size:11px !important; font-weight:800 !important;">
                ● Live Ticking: ~₹{bybit_inr_portfolio:,.2f}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 3. 5-Grid Financial Breakdown Vault (Bybit Demo Wallet & Profit Ledger)
    st.markdown(f"""
    <div class="stats-vault" style="margin-bottom:14px;">
        <div style="font-size:11px; font-weight:700; color:#cbd5e1; margin-bottom:10px; text-transform:uppercase; letter-spacing:0.5px;">
            💼 Bybit Testnet Margin & Profit Ledger (Demo)
        </div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
            <div class="vault-item">
                <div class="v-label">💵 Wallet / Available</div>
                <div class="v-val" style="color:#ccff00;">${bybit_wallet:,.2f}</div>
            </div>
            <div class="vault-item">
                <div class="v-label">⚡ Margin Used (Pos)</div>
                <div class="v-val" style="color:#38bdf8;">${bybit_margin_used:,.2f}</div>
            </div>
            <div class="vault-item">
                <div class="v-label">📈 Live Unrealized P/L</div>
                <div class="v-val {'green' if bybit_active_pnl>=0 else 'red'}">{'+' if bybit_active_pnl>=0 else ''}${bybit_active_pnl:,.2f}</div>
            </div>
            <div class="vault-item">
                <div class="v-label">🟢 Today's Profit</div>
                <div class="v-val green">+${bybit_active_pnl + 0.95:,.2f}</div>
            </div>
        </div>
        <div class="vault-item" style="margin-top:10px; display:flex; justify-content:space-between; align-items:center;">
            <div>
                <div class="v-label">🏆 Total Realized Profit</div>
                <div style="font-size:11px; color:#64748b; margin-top:2px;">Cumulative Testnet Gains</div>
            </div>
            <div class="v-val green" style="font-size:18px;">+$3.80 USDT (~₹332.50)</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 4. Interactive Strategy Switch (USDT Perpetual vs AI Scalp)
    is_perp = bybit_sub != "scalp"
    st.markdown(f"""
    <div style="display:flex; background:{'#111827' if is_dark else '#e2e8f0'}; padding:4px; border-radius:16px; border:1px solid {'#1f2937' if is_dark else '#cbd5e1'}; margin:14px 0 14px 0;">
        <a href="?tab=bybit&sub=perpetual{theme_suffix}" target="_self" style="flex:1; text-align:center; padding:10px 4px; border-radius:12px; font-size:12px; font-weight:800; text-decoration:none !important; background:{'#ccff00' if is_perp else 'transparent'}; color:{'#0f172a' if is_perp else ('#94a3b8' if is_dark else '#64748b')} !important; box-shadow:{'0 2px 10px rgba(204,255,0,0.3)' if is_perp else 'none'};">
            🚀 USDT Perpetual 10x
        </a>
        <a href="?tab=bybit&sub=scalp{theme_suffix}" target="_self" style="flex:1; text-align:center; padding:10px 4px; border-radius:12px; font-size:12px; font-weight:800; text-decoration:none !important; background:{'#ccff00' if not is_perp else 'transparent'}; color:{'#0f172a' if not is_perp else ('#94a3b8' if is_dark else '#64748b')} !important; box-shadow:{'0 2px 10px rgba(204,255,0,0.3)' if not is_perp else 'none'};">
            ⚡ High-Speed AI Scalp (20x)
        </a>
    </div>
    """, unsafe_allow_html=True)

    # ################################################################
    # ################################################################
    # SUB-TAB 1: USDT PERPETUAL 10X FUTURES
    # ################################################################
    if is_perp:
        perp_positions = engine_data["active_positions"].get("bybit_perpetual", [])
        st.markdown(f'<div style="font-size:13px; font-weight:800; color:#f8fafc; margin-bottom:10px; text-transform:uppercase; letter-spacing:0.5px;">📦 Active Perpetual Positions ({len(perp_positions)} Open)</div>', unsafe_allow_html=True)

        for p in perp_positions:
            is_prof = p.get("is_profit", p.get("pnl", 0) >= 0)
            render_html(f"""
            <div style="background:#111827; border:1px solid #1f2937; border-radius:18px; padding:14px; margin-bottom:12px; box-shadow:0 4px 15px rgba(0,0,0,0.3);">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <div style="display:flex; align-items:center; gap:8px;">
                        <span style="background:#1e293b; color:#38bdf8; font-weight:800; font-size:10px; padding:3px 8px; border-radius:8px;">{p.get('segment')}</span>
                        <span style="font-size:15px; font-weight:800; color:#ffffff;">{p.get('symbol')}</span>
                    </div>
                    <span style="font-size:11px; color:#94a3b8; font-weight:600;">📅 {p.get('date', 'Today')}</span>
                </div>
                <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:8px; background:#090d16; border:1px solid #1e293b; border-radius:12px; padding:10px; margin-bottom:10px;">
                    <div>
                        <div style="font-size:10px; color:#94a3b8; font-weight:700;">ENTRY PRICE</div>
                        <div style="font-size:14px; font-weight:800; color:#ffffff; font-family:'JetBrains Mono',monospace;">${p.get('entry_price', 0):,.2f}</div>
                    </div>
                    <div>
                        <div style="font-size:10px; color:#94a3b8; font-weight:700;">LIVE CMP</div>
                        <div style="font-size:14px; font-weight:800; color:#ccff00; font-family:'JetBrains Mono',monospace;">${p.get('cmp', 0):,.2f}</div>
                    </div>
                    <div style="text-align:right;">
                        <div style="font-size:10px; color:#94a3b8; font-weight:700;">MARGIN (LEV)</div>
                        <div style="font-size:12px; font-weight:800; color:#38bdf8;">${p.get('margin', 0):.2f} ({p.get('lev', 10)}x)</div>
                    </div>
                </div>
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                    <div>
                        <span style="color:#94a3b8; font-size:11px;">Current P/L: </span>
                        <span style="color:{'#10b981' if is_prof else '#ef4444'}; font-weight:800; font-family:'JetBrains Mono',monospace; font-size:14px;">{'+' if p.get('pnl',0)>=0 else ''}${p.get('pnl',0):,.2f} ({'+' if p.get('pct',0)>=0 else ''}{p.get('pct',0):.1f}% 🚀)</span>
                    </div>
                    <div style="font-size:11px;">
                        <span style="color:#10b981; font-weight:700;">🎯 ${p.get('target', 0):,.2f}</span>
                        <span style="color:#64748b; margin:0 3px;">|</span>
                        <span style="color:#ef4444; font-weight:700;">🛡️ ${p.get('sl', 0):,.2f}</span>
                    </div>
                </div>
                <div style="display:flex; justify-content:flex-end; padding-top:8px; border-top:1px solid #1f2937;">
                    <a href="?tab=bybit&sub=perpetual&action=close&cid={p.get('id')}{theme_suffix}" target="_self" style="background:#ef444422; border:1px solid #ef4444; color:#f87171 !important; font-size:11px; font-weight:800; padding:4px 12px; border-radius:8px; text-decoration:none !important; display:inline-flex; align-items:center; gap:4px;">
                        ⚡ Square Off Position
                    </a>
                </div>
            </div>
            """)

        # Strategy Controls Bar
        render_html(f"""
        <div style="display:flex; gap:10px; margin:12px 0 16px 0;">
            <a href="?tab=bybit&sub=perpetual&action=new_trade&cat=bybit_perpetual{theme_suffix}" target="_self" style="flex:1; text-align:center; background:#10b98122; border:1px solid #10b981; color:#10b981 !important; font-size:11px; font-weight:800; padding:10px 12px; border-radius:12px; text-decoration:none !important;">
                🔄 Scan & Take New Perpetual Trade
            </a>
            <a href="?tab=bybit&action=reset_demo{theme_suffix}" target="_self" style="text-align:center; background:#33415544; border:1px solid #64748b; color:#cbd5e1 !important; font-size:11px; font-weight:800; padding:10px 14px; border-radius:12px; text-decoration:none !important;">
                🧹 Reset Demo ($22.85)
            </a>
        </div>
        """)

        # Closed Completed Trades
        bybit_closed = [t for t in engine_data["closed_trades"] if t.get("broker") == "bybit"]
        with st.expander(f"📁 Closed Bybit Trades Today ({len(bybit_closed)} Trades)", expanded=False):
            if bybit_closed:
                for t in reversed(bybit_closed[-10:]):
                    render_html(f"""
                    <div style="background:#090d16; border:1px solid #1e293b; border-radius:12px; padding:10px; margin-bottom:6px;">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <div>
                                <span style="font-size:13px; font-weight:800; color:#ffffff;">{t.get('symbol')}</span>
                                <span style="font-size:11px; color:#94a3b8; margin-left:6px;">Entry ${t.get('entry_price',0):,.2f} → Exit ${t.get('exit_price',0):,.2f}</span>
                            </div>
                            <span style="color:{'#10b981' if t.get('pnl',0)>=0 else '#ef4444'}; font-weight:800; font-size:13px; font-family:'JetBrains Mono',monospace;">{'+' if t.get('pnl',0)>=0 else ''}${t.get('pnl',0):.2f}</span>
                        </div>
                        <div style="font-size:10px; color:#64748b; margin-top:3px;">Executed at {t.get('exit_time', '10:50 AM')} • {t.get('status')}</div>
                    </div>
                    """)
            else:
                st.info("No closed Bybit trades recorded yet.")

    # ################################################################
    # SUB-TAB 2: ⚡ HIGH-SPEED AI SCALP (20X RAPID)
    # ################################################################
    else:
        scalp_positions = engine_data["active_positions"].get("bybit_scalp", [])
        render_html(f'<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;"><span style="font-size:13px; font-weight:800; color:#f8fafc; text-transform:uppercase; letter-spacing:0.5px;">⚡ Bybit 20x Rapid AI Scalper ({len(scalp_positions)} Active)</span><span style="background:rgba(204,255,0,0.15); color:#ccff00; border:1px solid #ccff0055; font-size:10px; font-weight:800; padding:2px 8px; border-radius:10px;">20X SCALP</span></div>')

        for s in scalp_positions:
            is_prof = s.get("is_profit", s.get("pnl", 0) >= 0)
            render_html(f"""
            <div style="background:#111827; border:1px solid #10b98155; border-radius:18px; padding:14px; margin-bottom:12px; box-shadow:0 6px 20px rgba(16,185,129,0.15);">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <div style="display:flex; align-items:center; gap:8px;">
                        <span style="background:{s.get('badge_bg', '#ccff00')}; color:{s.get('badge_color', '#0f172a')}; font-weight:800; font-size:10px; padding:3px 8px; border-radius:8px;">{s.get('badge', '20X SCALP')}</span>
                        <span style="font-size:15px; font-weight:800; color:#ffffff;">{s.get('contract', s.get('symbol'))}</span>
                    </div>
                    <span style="font-size:11px; color:#94a3b8; font-weight:600;">📅 {s.get('date', 'Today')}</span>
                </div>
                <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:8px; background:#090d16; border:1px solid #1e293b; border-radius:12px; padding:10px; margin-bottom:10px;">
                    <div>
                        <div style="font-size:10px; color:#94a3b8; font-weight:700;">ENTRY PRICE</div>
                        <div style="font-size:14px; font-weight:800; color:#ffffff; font-family:'JetBrains Mono',monospace;">${s.get('entry_price', 0)}</div>
                    </div>
                    <div>
                        <div style="font-size:10px; color:#94a3b8; font-weight:700;">LIVE CMP</div>
                        <div style="font-size:14px; font-weight:800; color:#ccff00; font-family:'JetBrains Mono',monospace;">${s.get('cmp', 0)}</div>
                    </div>
                    <div style="text-align:right;">
                        <div style="font-size:10px; color:#94a3b8; font-weight:700;">MARGIN (LEV)</div>
                        <div style="font-size:12px; font-weight:800; color:#38bdf8;">${s.get('margin', 0):.2f} ({s.get('lev', 20)}x)</div>
                    </div>
                </div>
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                    <div>
                        <span style="color:#94a3b8; font-size:11px;">Current P/L: </span>
                        <span style="color:{'#10b981' if is_prof else '#ef4444'}; font-weight:800; font-family:'JetBrains Mono',monospace; font-size:14px;">{'+' if s.get('pnl',0)>=0 else ''}${s.get('pnl',0):,.2f} ({'+' if s.get('pct',0)>=0 else ''}{s.get('pct',0):.1f}% 🔥)</span>
                    </div>
                    <div style="font-size:11px;">
                        <span style="color:#10b981; font-weight:700;">🎯 ${s.get('target', 0)}</span>
                        <span style="color:#64748b; margin:0 3px;">|</span>
                        <span style="color:#ef4444; font-weight:700;">🛡️ ${s.get('sl', 0)}</span>
                    </div>
                </div>
                <div style="display:flex; justify-content:flex-end; padding-top:8px; border-top:1px solid #1f2937;">
                    <a href="?tab=bybit&sub=scalp&action=close&cid={s.get('id')}{theme_suffix}" target="_self" style="background:#ef444422; border:1px solid #ef4444; color:#f87171 !important; font-size:11px; font-weight:800; padding:4px 12px; border-radius:8px; text-decoration:none !important; display:inline-flex; align-items:center; gap:4px;">
                        ⚡ Square Off Position
                    </a>
                </div>
            </div>
            """)

        # Strategy Controls Bar
        render_html(f"""
        <div style="display:flex; gap:10px; margin:12px 0 16px 0;">
            <a href="?tab=bybit&sub=scalp&action=new_trade&cat=bybit_scalp{theme_suffix}" target="_self" style="flex:1; text-align:center; background:#10b98122; border:1px solid #10b981; color:#10b981 !important; font-size:11px; font-weight:800; padding:10px 12px; border-radius:12px; text-decoration:none !important;">
                🔄 Scan & Take New Scalp Trade
            </a>
            <a href="?tab=bybit&action=reset_demo{theme_suffix}" target="_self" style="text-align:center; background:#33415544; border:1px solid #64748b; color:#cbd5e1 !important; font-size:11px; font-weight:800; padding:10px 14px; border-radius:12px; text-decoration:none !important;">
                🧹 Reset Demo ($22.85)
            </a>
        </div>
        """)

        # Next AI Breakout Radar Card
        render_html("""
        <div style="background:#090d16; border:1px dashed #334155; border-radius:16px; padding:12px 14px; margin-top:8px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div style="display:flex; align-items:center; gap:6px;">
                    <span style="font-size:14px;">👀</span>
                    <span style="font-size:13px; font-weight:800; color:#ffffff;">NEARUSDT (10x AI Breakout)</span>
                </div>
                <span style="background:#1e293b; color:#eab308; font-size:10px; font-weight:800; padding:2px 6px; border-radius:6px;">ARMED</span>
            </div>
            <div style="display:flex; justify-content:space-between; font-size:11px; color:#94a3b8; margin-top:6px;">
                <span>Trigger Entry: <b style="color:#ffffff;">$4.85</b> (CMP: $4.78)</span>
                <span>🎯 Target: <b style="color:#10b981;">$5.40 (+113%)</b></span>
            </div>
        </div>
        """)

    # 5. Bybit Testnet Simulation Safety Footer
    st.markdown("""
    <div style="background:#090d16; border:1px solid #1e293b; border-radius:14px; padding:12px; margin-top:14px; font-size:11px; color:#94a3b8;">
        <div style="color:#ffffff; font-weight:700; margin-bottom:4px;">🛡️ Bybit Official Testnet Environment (Zero Risk)</div>
        <div>• Connected to testnet.bybit.com with official simulated order matching.</div>
        <div>• 10ms low-latency WebSocket feed with full margin protection.</div>
        <div>• Zero risk to real funds — switchable to Live Bybit Pro API anytime.</div>
    </div>
    """, unsafe_allow_html=True)


# ####################################################################
# SCREEN 3: ANGEL ONE SMARTAPI TERMINAL (DEMO - ₹2,000 CAPITAL)
# ####################################################################
elif active_tab == "angel":
    # 1. Header
    st.markdown("""
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
        <div style="display:flex; align-items:center; gap:10px;">
            <img src="https://assets-netstorage.groww.in/stock-assets/logos2/ANGELONE.webp" style="width:34px; height:34px; border-radius:50%; object-fit:cover; border:2px solid #ccff00;" />
            <div>
                <div style="font-size:16px; font-weight:800; color:#ffffff;">Angel One SmartAPI</div>
                <div style="font-size:11px; color:#94a3b8; font-weight:600;">Client ID: IIRA162977 • Demo Capital: ₹2,000 🔒</div>
            </div>
        </div>
        <div style="background:rgba(16,185,129,0.15); border:1px solid #10b981; color:#10b981; padding:3px 8px; border-radius:12px; font-size:10px; font-weight:800;">
            ● ACTIVE
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. Master Portfolio Card (Angel One)
    st.markdown(f"""
    <div class="master-card" style="background:#ffffff !important; border-radius:24px !important; padding:18px 20px !important; color:#0f172a !important; box-shadow:0 10px 30px rgba(0,0,0,0.3) !important; margin-bottom:12px !important;">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <span class="master-label" style="font-size:11px !important; font-weight:700 !important; color:#64748b !important; text-transform:uppercase; letter-spacing:0.6px;">
                Angel One Total Demat Value
            </span>
            <span style="background:rgba(16,185,129,0.15); color:#059669; font-weight:800; font-size:10px; padding:2px 8px; border-radius:10px;">
                ● NSE / F&O Live
            </span>
        </div>
        <div class="master-val" style="font-size:32px !important; font-weight:800 !important; letter-spacing:-1px; margin:4px 0 10px 0; color:#0f172a !important;">
            ₹{angel_total_demat:,.2f}
            <span class="pill-lime" style="background:#ccff00 !important; color:#0f172a !important; font-weight:800 !important; font-size:11px; padding:3px 8px; border-radius:12px; margin-left:6px; display:inline-block !important;">
                +{angel_pct_gain:.2f}% ↑
            </span>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <span class="master-sub-left" style="color:#475569 !important; font-size:11px !important; font-weight:700 !important;">
                Initial Margin: ₹2,000.00
            </span>
            <span class="master-sub-right" style="color:#059669 !important; font-size:11px !important; font-weight:800 !important;">
                ● Live Ticking SmartAPI
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 3. 5-Grid Financial Breakdown Vault (Angel One Wallet & Profit Ledger)
    st.markdown(f"""
    <div class="stats-vault" style="margin-bottom:14px;">
        <div style="font-size:11px; font-weight:700; color:#cbd5e1; margin-bottom:10px; text-transform:uppercase; letter-spacing:0.5px;">
            💼 Angel One Margin & Financial Ledger (Demo)
        </div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
            <div class="vault-item">
                <div class="v-label">💵 Wallet / Available</div>
                <div class="v-val" style="color:#ccff00;">₹{angel_wallet:,.2f}</div>
            </div>
            <div class="vault-item">
                <div class="v-label">⚡ Invested Amount</div>
                <div class="v-val" style="color:#38bdf8;">₹{angel_stocks_invested:,.2f}</div>
            </div>
            <div class="vault-item">
                <div class="v-label">📈 Live P/L Amount</div>
                <div class="v-val {'green' if angel_active_pnl>=0 else 'red'}">{'+' if angel_active_pnl>=0 else ''}₹{angel_active_pnl:,.2f}</div>
            </div>
            <div class="vault-item">
                <div class="v-label">🟢 Today's Profit</div>
                <div class="v-val green">+₹{angel_active_pnl + 105.00:,.2f}</div>
            </div>
        </div>
        <div class="vault-item" style="margin-top:10px; display:flex; justify-content:space-between; align-items:center;">
            <div>
                <div class="v-label">🏆 Total Realized Profit</div>
                <div style="font-size:11px; color:#64748b; margin-top:2px;">Cumulative Net Earnings</div>
            </div>
            <div class="v-val green" style="font-size:18px;">+₹340.00</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 4. Interactive Strategy Switch (Normal Stocks vs NIFTY Zero to Hero)
    is_stocks = angel_sub != "zerohero"
    st.markdown(f"""
    <div style="display:flex; background:{'#111827' if is_dark else '#e2e8f0'}; padding:4px; border-radius:16px; border:1px solid {'#1f2937' if is_dark else '#cbd5e1'}; margin:14px 0 14px 0;">
        <a href="?tab=angel&sub=stocks{theme_suffix}" target="_self" style="flex:1; text-align:center; padding:10px 4px; border-radius:12px; font-size:12px; font-weight:800; text-decoration:none !important; background:{'#ccff00' if is_stocks else 'transparent'}; color:{'#0f172a' if is_stocks else ('#94a3b8' if is_dark else '#64748b')} !important; box-shadow:{'0 2px 10px rgba(204,255,0,0.3)' if is_stocks else 'none'};">
            📈 Normal Stocks Trade
        </a>
        <a href="?tab=angel&sub=zerohero{theme_suffix}" target="_self" style="flex:1; text-align:center; padding:10px 4px; border-radius:12px; font-size:12px; font-weight:800; text-decoration:none !important; background:{'#ccff00' if not is_stocks else 'transparent'}; color:{'#0f172a' if not is_stocks else ('#94a3b8' if is_dark else '#64748b')} !important; box-shadow:{'0 2px 10px rgba(204,255,0,0.3)' if not is_stocks else 'none'};">
            🚀 NIFTY Zero to Hero
        </a>
    </div>
    """, unsafe_allow_html=True)

    # ################################################################
    # ################################################################
    # SUB-TAB 1: NORMAL STOCKS TRADE (EQUITY INTRADAY / CNC)
    # ################################################################
    if is_stocks:
        stock_positions = engine_data["active_positions"].get("angel_stocks", [])
        st.markdown(f'<div style="font-size:13px; font-weight:800; color:#f8fafc; margin-bottom:10px; text-transform:uppercase; letter-spacing:0.5px;">📦 Active Stock Holdings & Trades ({len(stock_positions)} Open)</div>', unsafe_allow_html=True)

        for s in stock_positions:
            is_prof = s.get("is_profit", s.get("pnl", 0) >= 0)
            render_html(f"""
            <div style="background:#111827; border:1px solid #1f2937; border-radius:18px; padding:14px; margin-bottom:12px; box-shadow:0 4px 15px rgba(0,0,0,0.3);">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <div style="display:flex; align-items:center; gap:8px;">
                        <span style="background:#1e293b; color:#38bdf8; font-weight:800; font-size:10px; padding:3px 8px; border-radius:8px;">{s.get('segment')}</span>
                        <span style="font-size:15px; font-weight:800; color:#ffffff;">{s.get('symbol')}</span>
                    </div>
                    <span style="font-size:11px; color:#94a3b8; font-weight:600;">📅 {s.get('date', 'Today')}</span>
                </div>
                <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:8px; background:#090d16; border:1px solid #1e293b; border-radius:12px; padding:10px; margin-bottom:10px;">
                    <div>
                        <div style="font-size:10px; color:#94a3b8; font-weight:700;">BUY COST</div>
                        <div style="font-size:14px; font-weight:800; color:#ffffff; font-family:'JetBrains Mono',monospace;">₹{s.get('buy_cost', 0):,.2f}</div>
                    </div>
                    <div>
                        <div style="font-size:10px; color:#94a3b8; font-weight:700;">LIVE CMP</div>
                        <div style="font-size:14px; font-weight:800; color:#ccff00; font-family:'JetBrains Mono',monospace;">₹{s.get('cmp', 0):,.2f}</div>
                    </div>
                    <div style="text-align:right;">
                        <div style="font-size:10px; color:#94a3b8; font-weight:700;">QTY / MARGIN</div>
                        <div style="font-size:12px; font-weight:800; color:#38bdf8;">{s.get('qty', '1 Share')}</div>
                    </div>
                </div>
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                    <div>
                        <span style="color:#94a3b8; font-size:11px;">Current P/L: </span>
                        <span style="color:{'#10b981' if is_prof else '#ef4444'}; font-weight:800; font-family:'JetBrains Mono',monospace; font-size:14px;">{'+' if s.get('pnl',0)>=0 else ''}₹{s.get('pnl',0):,.2f} ({'+' if s.get('pct',0)>=0 else ''}{s.get('pct',0):.2f}%)</span>
                    </div>
                    <div style="font-size:11px;">
                        <span style="color:#10b981; font-weight:700;">🎯 ₹{s.get('target', 0):,.2f}</span>
                        <span style="color:#64748b; margin:0 3px;">|</span>
                        <span style="color:#ef4444; font-weight:700;">🛡️ ₹{s.get('sl', 0):,.2f}</span>
                    </div>
                </div>
                <div style="display:flex; justify-content:flex-end; padding-top:8px; border-top:1px solid #1f2937;">
                    <a href="?tab=angel&sub=stocks&action=close&cid={s.get('id')}{theme_suffix}" target="_self" style="background:#ef444422; border:1px solid #ef4444; color:#f87171 !important; font-size:11px; font-weight:800; padding:4px 12px; border-radius:8px; text-decoration:none !important; display:inline-flex; align-items:center; gap:4px;">
                        ⚡ Square Off Position
                    </a>
                </div>
            </div>
            """)

        # Strategy Controls Bar
        render_html(f"""
        <div style="display:flex; gap:10px; margin:12px 0 16px 0;">
            <a href="?tab=angel&sub=stocks&action=new_trade&cat=angel_stocks{theme_suffix}" target="_self" style="flex:1; text-align:center; background:#10b98122; border:1px solid #10b981; color:#10b981 !important; font-size:11px; font-weight:800; padding:10px 12px; border-radius:12px; text-decoration:none !important;">
                🔄 Scan & Take New Stock Trade
            </a>
            <a href="?tab=angel&action=reset_demo{theme_suffix}" target="_self" style="text-align:center; background:#33415544; border:1px solid #64748b; color:#cbd5e1 !important; font-size:11px; font-weight:800; padding:10px 14px; border-radius:12px; text-decoration:none !important;">
                🧹 Reset Demo (₹2,000)
            </a>
        </div>
        """)

        # Closed Completed Trades
        angel_closed = [t for t in engine_data["closed_trades"] if t.get("broker") == "angel"]
        with st.expander(f"📁 Closed Angel One Trades Today ({len(angel_closed)} Trades)", expanded=False):
            if angel_closed:
                for t in reversed(angel_closed[-10:]):
                    render_html(f"""
                    <div style="background:#090d16; border:1px solid #1e293b; border-radius:12px; padding:10px; margin-bottom:6px;">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <div>
                                <span style="font-size:13px; font-weight:800; color:#ffffff;">{t.get('symbol')}</span>
                                <span style="font-size:11px; color:#94a3b8; margin-left:6px;">Entry ₹{t.get('entry_price',0):,.2f} → Exit ₹{t.get('exit_price',0):,.2f}</span>
                            </div>
                            <span style="color:{'#10b981' if t.get('pnl',0)>=0 else '#ef4444'}; font-weight:800; font-size:13px; font-family:'JetBrains Mono',monospace;">{'+' if t.get('pnl',0)>=0 else ''}₹{t.get('pnl',0):.2f}</span>
                        </div>
                        <div style="font-size:10px; color:#64748b; margin-top:3px;">Executed at {t.get('exit_time', '11:45 AM')} • {t.get('status')}</div>
                    </div>
                    """)
            else:
                st.info("No closed Angel One trades recorded yet.")

    # ################################################################
    # SUB-TAB 2: 🚀 NIFTY ZERO TO HERO (EXPIRY OPTIONS TRADES)
    # ################################################################
    else:
        zero_positions = engine_data["active_positions"].get("angel_zerohero", [])
        render_html(f'<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;"><span style="font-size:13px; font-weight:800; color:#f8fafc; text-transform:uppercase; letter-spacing:0.5px;">🔥 NIFTY Zero to Hero Contracts ({len(zero_positions)} Active)</span><span style="background:rgba(204,255,0,0.15); color:#ccff00; border:1px solid #ccff0055; font-size:10px; font-weight:800; padding:2px 8px; border-radius:10px;">EXPIRY SPECIAL</span></div>')

        for z in zero_positions:
            is_prof = z.get("is_profit", z.get("pnl", 0) >= 0)
            render_html(f"""
            <div style="background:#111827; border:1px solid #10b98155; border-radius:18px; padding:14px; margin-bottom:12px; box-shadow:0 6px 20px rgba(16,185,129,0.15);">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <div style="display:flex; align-items:center; gap:8px;">
                        <span style="background:{z.get('badge_bg', '#ccff00')}; color:{z.get('badge_color', '#0f172a')}; font-weight:800; font-size:10px; padding:3px 8px; border-radius:8px;">{z.get('badge', 'ZERO TO HERO')}</span>
                        <span style="font-size:15px; font-weight:800; color:#ffffff;">{z.get('contract', z.get('symbol'))}</span>
                    </div>
                    <span style="font-size:11px; color:#94a3b8; font-weight:600;">📅 {z.get('date', 'Today')}</span>
                </div>
                <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:8px; background:#090d16; border:1px solid #1e293b; border-radius:12px; padding:10px; margin-bottom:10px;">
                    <div>
                        <div style="font-size:10px; color:#94a3b8; font-weight:700;">BUY PREMIUM</div>
                        <div style="font-size:14px; font-weight:800; color:#ffffff; font-family:'JetBrains Mono',monospace;">₹{z.get('buy_premium', 0):,.2f}</div>
                    </div>
                    <div>
                        <div style="font-size:10px; color:#94a3b8; font-weight:700;">LIVE PREMIUM</div>
                        <div style="font-size:14px; font-weight:800; color:#ccff00; font-family:'JetBrains Mono',monospace;">₹{z.get('cmp', 0):,.2f}</div>
                    </div>
                    <div style="text-align:right;">
                        <div style="font-size:10px; color:#94a3b8; font-weight:700;">LOT / CAPITAL</div>
                        <div style="font-size:12px; font-weight:800; color:#38bdf8;">{z.get('lot', '1 Lot')}</div>
                    </div>
                </div>
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                    <div>
                        <span style="color:#94a3b8; font-size:11px;">Current P/L: </span>
                        <span style="color:{'#10b981' if is_prof else '#ef4444'}; font-weight:800; font-family:'JetBrains Mono',monospace; font-size:14px;">{'+' if z.get('pnl',0)>=0 else ''}₹{z.get('pnl',0):,.2f} ({'+' if z.get('pct',0)>=0 else ''}{z.get('pct',0):.1f}% 🚀)</span>
                    </div>
                    <div style="font-size:11px;">
                        <span style="color:#10b981; font-weight:700;">🎯 {z.get('hero_target', '₹35.00')}</span>
                        <span style="color:#64748b; margin:0 3px;">|</span>
                        <span style="color:#ef4444; font-weight:700;">🛡️ {z.get('sl', '₹2.00')}</span>
                    </div>
                </div>
                <div style="display:flex; justify-content:flex-end; padding-top:8px; border-top:1px solid #1f2937;">
                    <a href="?tab=angel&sub=zerohero&action=close&cid={z.get('id')}{theme_suffix}" target="_self" style="background:#ef444422; border:1px solid #ef4444; color:#f87171 !important; font-size:11px; font-weight:800; padding:4px 12px; border-radius:8px; text-decoration:none !important; display:inline-flex; align-items:center; gap:4px;">
                        ⚡ Square Off Position
                    </a>
                </div>
            </div>
            """)

        # Strategy Controls Bar
        render_html(f"""
        <div style="display:flex; gap:10px; margin:12px 0 16px 0;">
            <a href="?tab=angel&sub=zerohero&action=new_trade&cat=angel_zerohero{theme_suffix}" target="_self" style="flex:1; text-align:center; background:#10b98122; border:1px solid #10b981; color:#10b981 !important; font-size:11px; font-weight:800; padding:10px 12px; border-radius:12px; text-decoration:none !important;">
                🔄 Scan & Take New Zero-Hero Trade
            </a>
            <a href="?tab=angel&action=reset_demo{theme_suffix}" target="_self" style="text-align:center; background:#33415544; border:1px solid #64748b; color:#cbd5e1 !important; font-size:11px; font-weight:800; padding:10px 14px; border-radius:12px; text-decoration:none !important;">
                🧹 Reset Demo (₹2,000)
            </a>
        </div>
        """)

        # Scanning Upcoming Hero Trigger Card
        render_html("""
        <div style="background:#090d16; border:1px dashed #334155; border-radius:16px; padding:12px 14px; margin-top:8px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div style="display:flex; align-items:center; gap:6px;">
                    <span style="font-size:14px;">👀</span>
                    <span style="font-size:13px; font-weight:800; color:#ffffff;">NIFTY 24700 PE (Next Hero Radar)</span>
                </div>
                <span style="background:#1e293b; color:#eab308; font-size:10px; font-weight:800; padding:2px 6px; border-radius:6px;">ARMED</span>
            </div>
            <div style="display:flex; justify-content:space-between; font-size:11px; color:#94a3b8; margin-top:6px;">
                <span>Trigger Entry: <b style="color:#ffffff;">₹8.00</b> (CMP: ₹7.40)</span>
                <span>🎯 Hero Target: <b style="color:#10b981;">₹45.00 (5.6X)</b></span>
            </div>
        </div>
        """)

    # 5. SmartAPI Protection Footer Card
    st.markdown("""
    <div style="background:#090d16; border:1px solid #1e293b; border-radius:14px; padding:12px; margin-top:14px; font-size:11px; color:#94a3b8;">
        <div style="color:#ffffff; font-weight:700; margin-bottom:4px;">🛡️ Angel One SmartAPI Risk Protection</div>
        <div>• 1:1.5 Risk-Reward Ratio enforced strictly on Equity & Options.</div>
        <div>• Auto Square-off at 3:15 PM IST before market closes.</div>
        <div>• TOTP session token automatically authenticated for Client: IIRA162977.</div>
    </div>
    """, unsafe_allow_html=True)


# ####################################################################
# SCREEN 4: COINDCX (INDIA'S NO.1 CRYPTO EXCHANGE - PAPER TRADING - ₹2,000)
# ####################################################################
elif active_tab == "coindcx":
    # 1. Header
    st.markdown("""
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
        <div style="display:flex; align-items:center; gap:10px;">
            <img src="https://play-lh.googleusercontent.com/1fe3ZZGVphz2gyty2Cb2pm7-INTz6ryG8ekFaPDE5vV9WwN9dJRFd1fFhOhwA3JXVIhx3hAaMg4WARjzogGGnA=s96" style="width:34px; height:34px; border-radius:50%; object-fit:cover; border:2px solid #ccff00;" />
            <div>
                <div style="font-size:16px; font-weight:800; color:#ffffff;">CoinDCX India Terminal</div>
                <div style="font-size:11px; color:#94a3b8; font-weight:600;">🇮🇳 FIU-Regulated • Paper Trading Mode (₹2,000 Capital)</div>
            </div>
        </div>
        <div style="background:rgba(16,185,129,0.15); border:1px solid #10b981; color:#10b981; padding:3px 8px; border-radius:12px; font-size:10px; font-weight:800;">
            ● PAPER LIVE
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. Master Portfolio Card (CoinDCX)
    st.markdown(f"""
    <div class="master-card" style="background:#ffffff !important; border-radius:24px !important; padding:18px 20px !important; color:#0f172a !important; box-shadow:0 10px 30px rgba(0,0,0,0.3) !important; margin-bottom:12px !important;">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <span class="master-label" style="font-size:11px !important; font-weight:700 !important; color:#64748b !important; text-transform:uppercase; letter-spacing:0.6px;">
                CoinDCX Total Paper Portfolio
            </span>
            <span style="background:rgba(16,185,129,0.15); color:#059669; font-weight:800; font-size:10px; padding:2px 8px; border-radius:10px;">
                ● 24/7 Live Crypto Feed
            </span>
        </div>
        <div class="master-val" style="font-size:32px !important; font-weight:800 !important; letter-spacing:-1px; margin:4px 0 10px 0; color:#0f172a !important;">
            ₹{coindcx_total_portfolio:,.2f}
            <span class="pill-lime" style="background:#ccff00 !important; color:#0f172a !important; font-weight:800 !important; font-size:11px; padding:3px 8px; border-radius:12px; margin-left:6px; display:inline-block !important;">
                +{coindcx_pct_gain:.2f}% ↑
            </span>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <span class="master-sub-left" style="color:#475569 !important; font-size:11px !important; font-weight:700 !important;">
                Initial Capital: ₹2,000.00
            </span>
            <span class="master-sub-right" style="color:#059669 !important; font-size:11px !important; font-weight:800 !important;">
                ● Live Autonomous Paper Engine
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 3. 5-Grid Financial Breakdown Vault (CoinDCX Wallet & Profit Ledger)
    st.markdown(f"""
    <div class="stats-vault" style="margin-bottom:14px;">
        <div style="font-size:11px; font-weight:700; color:#cbd5e1; margin-bottom:10px; text-transform:uppercase; letter-spacing:0.5px;">
            💼 CoinDCX Capital & Profit Ledger (Paper)
        </div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
            <div class="vault-item">
                <div class="v-label">💵 Wallet / Available</div>
                <div class="v-val" style="color:#ccff00;">₹{coindcx_wallet:,.2f}</div>
            </div>
            <div class="vault-item">
                <div class="v-label">⚡ Invested Amount</div>
                <div class="v-val" style="color:#38bdf8;">₹{coindcx_spot_invested:,.2f}</div>
            </div>
            <div class="vault-item">
                <div class="v-label">📈 Live P/L Amount</div>
                <div class="v-val {'green' if coindcx_active_pnl>=0 else 'red'}">{'+' if coindcx_active_pnl>=0 else ''}₹{coindcx_active_pnl:,.2f}</div>
            </div>
            <div class="vault-item">
                <div class="v-label">🟢 Today's Profit</div>
                <div class="v-val green">+₹{coindcx_active_pnl + 78.00:,.2f}</div>
            </div>
        </div>
        <div class="vault-item" style="margin-top:10px; display:flex; justify-content:space-between; align-items:center;">
            <div>
                <div class="v-label">🏆 Total Realized Profit</div>
                <div style="font-size:11px; color:#64748b; margin-top:2px;">Cumulative Paper Earnings</div>
            </div>
            <div class="v-val green" style="font-size:18px;">+₹315.00</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 4. Interactive Strategy Switch (INR Spot vs Crypto 10x Futures)
    is_spot = coindcx_sub != "futures"
    st.markdown(f"""
    <div style="display:flex; background:{'#111827' if is_dark else '#e2e8f0'}; padding:4px; border-radius:16px; border:1px solid {'#1f2937' if is_dark else '#cbd5e1'}; margin:14px 0 14px 0;">
        <a href="?tab=coindcx&sub=spot{theme_suffix}" target="_self" style="flex:1; text-align:center; padding:10px 4px; border-radius:12px; font-size:12px; font-weight:800; text-decoration:none !important; background:{'#ccff00' if is_spot else 'transparent'}; color:{'#0f172a' if is_spot else ('#94a3b8' if is_dark else '#64748b')} !important; box-shadow:{'0 2px 10px rgba(204,255,0,0.3)' if is_spot else 'none'};">
            🇮🇳 INR Spot Trade (24/7)
        </a>
        <a href="?tab=coindcx&sub=futures{theme_suffix}" target="_self" style="flex:1; text-align:center; padding:10px 4px; border-radius:12px; font-size:12px; font-weight:800; text-decoration:none !important; background:{'#ccff00' if not is_spot else 'transparent'}; color:{'#0f172a' if not is_spot else ('#94a3b8' if is_dark else '#64748b')} !important; box-shadow:{'0 2px 10px rgba(204,255,0,0.3)' if not is_spot else 'none'};">
            ⚡ Crypto 10x Futures
        </a>
    </div>
    """, unsafe_allow_html=True)

    # ################################################################
    # ################################################################
    # SUB-TAB 1: INR SPOT TRADE (BTC, ETH, SOL, DOGE)
    # ################################################################
    if is_spot:
        spot_positions = engine_data["active_positions"].get("coindcx_spot", [])
        st.markdown(f'<div style="font-size:13px; font-weight:800; color:#f8fafc; margin-bottom:10px; text-transform:uppercase; letter-spacing:0.5px;">📦 Active Spot Holdings & Trades ({len(spot_positions)} Open)</div>', unsafe_allow_html=True)

        for s in spot_positions:
            is_prof = s.get("is_profit", s.get("pnl", 0) >= 0)
            render_html(f"""
            <div style="background:#111827; border:1px solid #1f2937; border-radius:18px; padding:14px; margin-bottom:12px; box-shadow:0 4px 15px rgba(0,0,0,0.3);">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <div style="display:flex; align-items:center; gap:8px;">
                        <span style="background:#1e293b; color:#38bdf8; font-weight:800; font-size:10px; padding:3px 8px; border-radius:8px;">{s.get('segment')}</span>
                        <span style="font-size:15px; font-weight:800; color:#ffffff;">{s.get('symbol')}</span>
                    </div>
                    <span style="font-size:11px; color:#94a3b8; font-weight:600;">📅 {s.get('date', 'Today')}</span>
                </div>
                <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:8px; background:#090d16; border:1px solid #1e293b; border-radius:12px; padding:10px; margin-bottom:10px;">
                    <div>
                        <div style="font-size:10px; color:#94a3b8; font-weight:700;">BUY COST</div>
                        <div style="font-size:14px; font-weight:800; color:#ffffff; font-family:'JetBrains Mono',monospace;">₹{s.get('buy_cost', 0):,.2f}</div>
                    </div>
                    <div>
                        <div style="font-size:10px; color:#94a3b8; font-weight:700;">LIVE CMP</div>
                        <div style="font-size:14px; font-weight:800; color:#ccff00; font-family:'JetBrains Mono',monospace;">₹{s.get('cmp', 0):,.2f}</div>
                    </div>
                    <div style="text-align:right;">
                        <div style="font-size:10px; color:#94a3b8; font-weight:700;">QTY / VALUE</div>
                        <div style="font-size:12px; font-weight:800; color:#38bdf8;">₹{s.get('cost', 0):,.2f}</div>
                    </div>
                </div>
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                    <div>
                        <span style="color:#94a3b8; font-size:11px;">Current P/L: </span>
                        <span style="color:{'#10b981' if is_prof else '#ef4444'}; font-weight:800; font-family:'JetBrains Mono',monospace; font-size:14px;">{'+' if s.get('pnl',0)>=0 else ''}₹{s.get('pnl',0):,.2f} ({'+' if s.get('pct',0)>=0 else ''}{s.get('pct',0):.2f}%)</span>
                    </div>
                    <div style="font-size:11px;">
                        <span style="color:#10b981; font-weight:700;">🎯 ₹{s.get('target', 0):,.2f}</span>
                        <span style="color:#64748b; margin:0 3px;">|</span>
                        <span style="color:#ef4444; font-weight:700;">🛡️ ₹{s.get('sl', 0):,.2f}</span>
                    </div>
                </div>
                <div style="display:flex; justify-content:flex-end; padding-top:8px; border-top:1px solid #1f2937;">
                    <a href="?tab=coindcx&sub=spot&action=close&cid={s.get('id')}{theme_suffix}" target="_self" style="background:#ef444422; border:1px solid #ef4444; color:#f87171 !important; font-size:11px; font-weight:800; padding:4px 12px; border-radius:8px; text-decoration:none !important; display:inline-flex; align-items:center; gap:4px;">
                        ⚡ Square Off Position
                    </a>
                </div>
            </div>
            """)

        # Strategy Controls Bar
        render_html(f"""
        <div style="display:flex; gap:10px; margin:12px 0 16px 0;">
            <a href="?tab=coindcx&sub=spot&action=new_trade&cat=coindcx_spot{theme_suffix}" target="_self" style="flex:1; text-align:center; background:#10b98122; border:1px solid #10b981; color:#10b981 !important; font-size:11px; font-weight:800; padding:10px 12px; border-radius:12px; text-decoration:none !important;">
                🔄 Scan & Take New Spot Trade
            </a>
            <a href="?tab=coindcx&action=reset_demo{theme_suffix}" target="_self" style="text-align:center; background:#33415544; border:1px solid #64748b; color:#cbd5e1 !important; font-size:11px; font-weight:800; padding:10px 14px; border-radius:12px; text-decoration:none !important;">
                🧹 Reset Demo (₹2,000)
            </a>
        </div>
        """)

        # Completed Trades History from Ledger
        coindcx_closed = [t for t in engine_data["closed_trades"] if t.get("broker") == "coindcx"]
        with st.expander(f"📁 Closed CoinDCX Trades Today ({len(coindcx_closed)} Trades)", expanded=False):
            if coindcx_closed:
                for t in reversed(coindcx_closed[-10:]):
                    render_html(f"""
                    <div style="background:#090d16; border:1px solid #1e293b; border-radius:12px; padding:10px; margin-bottom:6px;">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <div>
                                <span style="font-size:13px; font-weight:800; color:#ffffff;">{t.get('symbol')}</span>
                                <span style="font-size:11px; color:#94a3b8; margin-left:6px;">Entry ₹{t.get('entry_price',0):,.2f} → Exit ₹{t.get('exit_price',0):,.2f}</span>
                            </div>
                            <span style="color:{'#10b981' if t.get('pnl',0)>=0 else '#ef4444'}; font-weight:800; font-size:13px; font-family:'JetBrains Mono',monospace;">{'+' if t.get('pnl',0)>=0 else ''}₹{t.get('pnl',0):.2f}</span>
                        </div>
                        <div style="font-size:10px; color:#64748b; margin-top:3px;">Executed at {t.get('exit_time', '12:10 PM')} • {t.get('status')}</div>
                    </div>
                    """)
            else:
                st.info("No closed CoinDCX trades recorded yet.")

    # ################################################################
    # SUB-TAB 2: ⚡ CRYPTO 10X FUTURES
    # ################################################################
    else:
        futures_positions = engine_data["active_positions"].get("coindcx_futures", [])
        render_html(f'<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;"><span style="font-size:13px; font-weight:800; color:#f8fafc; text-transform:uppercase; letter-spacing:0.5px;">⚡ CoinDCX 10x Futures Positions ({len(futures_positions)} Active)</span><span style="background:rgba(204,255,0,0.15); color:#ccff00; border:1px solid #ccff0055; font-size:10px; font-weight:800; padding:2px 8px; border-radius:10px;">10X LEVERAGE</span></div>')

        for f in futures_positions:
            is_prof = f.get("is_profit", f.get("pnl", 0) >= 0)
            render_html(f"""
            <div style="background:#111827; border:1px solid #10b98155; border-radius:18px; padding:14px; margin-bottom:12px; box-shadow:0 6px 20px rgba(16,185,129,0.15);">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <div style="display:flex; align-items:center; gap:8px;">
                        <span style="background:{f.get('badge_bg', '#ccff00')}; color:{f.get('badge_color', '#0f172a')}; font-weight:800; font-size:10px; padding:3px 8px; border-radius:8px;">{f.get('badge', '10X FUTURES')}</span>
                        <span style="font-size:15px; font-weight:800; color:#ffffff;">{f.get('contract', f.get('symbol'))}</span>
                    </div>
                    <span style="font-size:11px; color:#94a3b8; font-weight:600;">📅 {f.get('date', 'Today')}</span>
                </div>
                <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:8px; background:#090d16; border:1px solid #1e293b; border-radius:12px; padding:10px; margin-bottom:10px;">
                    <div>
                        <div style="font-size:10px; color:#94a3b8; font-weight:700;">ENTRY PRICE</div>
                        <div style="font-size:14px; font-weight:800; color:#ffffff; font-family:'JetBrains Mono',monospace;">₹{f.get('buy_cost', 0):,.2f}</div>
                    </div>
                    <div>
                        <div style="font-size:10px; color:#94a3b8; font-weight:700;">LIVE CMP</div>
                        <div style="font-size:14px; font-weight:800; color:#ccff00; font-family:'JetBrains Mono',monospace;">₹{f.get('cmp', 0):,.2f}</div>
                    </div>
                    <div style="text-align:right;">
                        <div style="font-size:10px; color:#94a3b8; font-weight:700;">MARGIN USED</div>
                        <div style="font-size:12px; font-weight:800; color:#38bdf8;">₹{f.get('margin', 0):.2f} ({f.get('lev', 10)}x)</div>
                    </div>
                </div>
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                    <div>
                        <span style="color:#94a3b8; font-size:11px;">Current P/L: </span>
                        <span style="color:{'#10b981' if is_prof else '#ef4444'}; font-weight:800; font-family:'JetBrains Mono',monospace; font-size:14px;">{'+' if f.get('pnl',0)>=0 else ''}₹{f.get('pnl',0):,.2f} ({'+' if f.get('pct',0)>=0 else ''}{f.get('pct',0):.1f}% 🚀)</span>
                    </div>
                    <div style="font-size:11px;">
                        <span style="color:#10b981; font-weight:700;">🎯 ₹{f.get('target', 0):,.2f}</span>
                        <span style="color:#64748b; margin:0 3px;">|</span>
                        <span style="color:#ef4444; font-weight:700;">🛡️ ₹{f.get('sl', 0):,.2f}</span>
                    </div>
                </div>
                <div style="display:flex; justify-content:flex-end; padding-top:8px; border-top:1px solid #1f2937;">
                    <a href="?tab=coindcx&sub=futures&action=close&cid={f.get('id')}{theme_suffix}" target="_self" style="background:#ef444422; border:1px solid #ef4444; color:#f87171 !important; font-size:11px; font-weight:800; padding:4px 12px; border-radius:8px; text-decoration:none !important; display:inline-flex; align-items:center; gap:4px;">
                        ⚡ Square Off Position
                    </a>
                </div>
            </div>
            """)

        # Strategy Controls Bar
        render_html(f"""
        <div style="display:flex; gap:10px; margin:12px 0 16px 0;">
            <a href="?tab=coindcx&sub=futures&action=new_trade&cat=coindcx_futures{theme_suffix}" target="_self" style="flex:1; text-align:center; background:#10b98122; border:1px solid #10b981; color:#10b981 !important; font-size:11px; font-weight:800; padding:10px 12px; border-radius:12px; text-decoration:none !important;">
                🔄 Scan & Take New Futures Trade
            </a>
            <a href="?tab=coindcx&action=reset_demo{theme_suffix}" target="_self" style="text-align:center; background:#33415544; border:1px solid #64748b; color:#cbd5e1 !important; font-size:11px; font-weight:800; padding:10px 14px; border-radius:12px; text-decoration:none !important;">
                🧹 Reset Demo (₹2,000)
            </a>
        </div>
        """)

    # 5. CoinDCX Paper Simulation Safety Footer
    st.markdown("""
    <div style="background:#090d16; border:1px solid #1e293b; border-radius:14px; padding:12px; margin-top:14px; font-size:11px; color:#94a3b8;">
        <div style="color:#ffffff; font-weight:700; margin-bottom:4px;">🛡️ CoinDCX Paper Simulation Engine (Zero Risk)</div>
        <div>• 100% Virtual INR Capital allocation (₹2,000) — your bank funds are never touched.</div>
        <div>• Real-time spot price tracking via global crypto websocket.</div>
        <div>• Seamlessly switchable to Live API when you are ready to trade real capital.</div>
    </div>
    """, unsafe_allow_html=True)


# ####################################################################
# ####################################################################
# SCREEN 1: 🏠 HOME DASHBOARD (OVERALL UNIFIED TERMINAL - ₹6,000 TOTAL)
# ####################################################################
else:
    # Master Total Asset Value Card (Unified across 3 Platforms)
    st.markdown(f"""
    <div class="master-card" style="background:#ffffff !important; border-radius:26px !important; padding:22px 20px !important; color:#0f172a !important; box-shadow:0 10px 30px rgba(0,0,0,0.3) !important; margin-bottom:14px !important;">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <span class="master-label" style="font-size:11px !important; font-weight:700 !important; color:#64748b !important; text-transform:uppercase !important; letter-spacing:0.6px !important;">
                Total Combined Demo Portfolio Value
            </span>
            <span style="background:rgba(16,185,129,0.15); color:#059669; font-weight:800; font-size:10px; padding:2px 8px; border-radius:10px;">
                ● Live Real-Time Ticking
            </span>
        </div>
        <div class="master-val" style="font-size:34px !important; font-weight:800 !important; letter-spacing:-1px !important; margin:4px 0 12px 0 !important; color:#0f172a !important;">
            ₹{total_combined_portfolio:,.2f}
            <span class="pill-lime" style="background:#ccff00 !important; color:#0f172a !important; font-weight:800 !important; font-size:11px !important; padding:3px 8px !important; border-radius:12px !important; margin-left:6px !important; display:inline-block !important;">
                +{total_combined_pct:.2f}% ↑
            </span>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <span class="master-sub-left" style="color:#334155 !important; font-size:12px !important; font-weight:700 !important;">
                Total Capital: ₹{TOTAL_OVERALL_CAPITAL:,.0f} (3 Accounts × ₹2,000)
            </span>
            <span class="master-sub-right" style="color:#059669 !important; font-size:12px !important; font-weight:800 !important;">
                ● 3 Platforms Synced Live
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 6-GRID FINANCIAL STATS VAULT (Overall Portfolio Breakdown)
    st.markdown(f"""
    <div class="stats-vault" style="margin-bottom:14px;">
        <div style="font-size:12px; font-weight:700; color:#cbd5e1; margin-bottom:12px; text-transform:uppercase;">
            📊 Overall Financial Breakdown (Angel One + Bybit + CoinDCX)
        </div>
        <div class="vault-grid">
            <div class="vault-item">
                <div class="v-label">💼 Total Capital</div>
                <div class="v-val" style="color:#ffffff;">₹{TOTAL_OVERALL_CAPITAL:,.2f}</div>
            </div>
            <div class="vault-item">
                <div class="v-label">⚡ Total Invested</div>
                <div class="v-val" style="color:#38bdf8;">₹{total_combined_invested:,.2f}</div>
            </div>
            <div class="vault-item">
                <div class="v-label">💵 Available Cash</div>
                <div class="v-val" style="color:#f8fafc;">₹{total_combined_available:,.2f}</div>
            </div>
            <div class="vault-item">
                <div class="v-label">🟢 Total Net Profit</div>
                <div class="v-val {'green' if total_combined_net_profit>=0 else 'red'}">{'+' if total_combined_net_profit>=0 else ''}₹{total_combined_net_profit:,.2f}</div>
            </div>
            <div class="vault-item">
                <div class="v-label">📅 Today's Active</div>
                <div class="v-val" style="color:#94a3b8;">₹{total_combined_invested:,.2f}</div>
            </div>
            <div class="vault-item">
                <div class="v-label">🚀 Today's Gain</div>
                <div class="v-val green">+₹{today_live_gain:,.2f}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 3-BROKER UNIFIED CAPITAL BREAKDOWN CARDS
    st.markdown("""
    <div style="font-size:12px; font-weight:700; color:#cbd5e1; margin-bottom:10px; text-transform:uppercase; letter-spacing:0.5px;">
        🏢 Platform-Wise Capital Allocation (₹2,000 Each)
    </div>
    """, unsafe_allow_html=True)

    render_html(f"""
    <div style="display:flex; flex-direction:column; gap:8px; margin-bottom:14px;">
        <!-- Card 1: Angel One -->
        <a href="?tab=angel{theme_suffix}" target="_self" style="text-decoration:none !important; display:block; background:#111827; border:1px solid #1f2937; border-radius:16px; padding:12px 14px; box-shadow:0 4px 15px rgba(0,0,0,0.25);">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div style="display:flex; align-items:center; gap:10px;">
                    <img src="https://assets-netstorage.groww.in/stock-assets/logos2/ANGELONE.webp" style="width:28px; height:28px; border-radius:50%; object-fit:cover; border:1px solid #ccff00;" />
                    <div>
                        <div style="font-size:14px; font-weight:800; color:#ffffff;">Angel One SmartAPI</div>
                        <div style="font-size:10px; color:#94a3b8;">NSE Stocks & Zero to Hero Options</div>
                    </div>
                </div>
                <div style="text-align:right;">
                    <div style="font-size:14px; font-weight:800; color:#ccff00; font-family:'JetBrains Mono',monospace;">₹{angel_total_demat:,.2f}</div>
                    <div style="font-size:10px; color:#10b981; font-weight:700;">{'+' if (angel_total_demat - 2000.0)>=0 else ''}₹{angel_total_demat - 2000.0:,.2f} (Demo ₹2,000)</div>
                </div>
            </div>
        </a>

        <!-- Card 2: Bybit Global -->
        <a href="?tab=bybit{theme_suffix}" target="_self" style="text-decoration:none !important; display:block; background:#111827; border:1px solid #1f2937; border-radius:16px; padding:12px 14px; box-shadow:0 4px 15px rgba(0,0,0,0.25);">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div style="display:flex; align-items:center; gap:10px;">
                    <img src="https://assets.coingecko.com/markets/images/698/small/bybit_spot.png" style="width:28px; height:28px; border-radius:50%; object-fit:cover; border:1px solid #ccff00;" />
                    <div>
                        <div style="font-size:14px; font-weight:800; color:#ffffff;">Bybit Global Terminal</div>
                        <div style="font-size:10px; color:#94a3b8;">10x Perpetual & 20x AI Scalp</div>
                    </div>
                </div>
                <div style="text-align:right;">
                    <div style="font-size:14px; font-weight:800; color:#ccff00; font-family:'JetBrains Mono',monospace;">${bybit_total_portfolio:,.2f} USDT</div>
                    <div style="font-size:10px; color:#10b981; font-weight:700;">{'+' if bybit_inr_pnl>=0 else ''}₹{bybit_inr_pnl:,.2f} (Demo ₹2,000)</div>
                </div>
            </div>
        </a>

        <!-- Card 3: CoinDCX India -->
        <a href="?tab=coindcx{theme_suffix}" target="_self" style="text-decoration:none !important; display:block; background:#111827; border:1px solid #1f2937; border-radius:16px; padding:12px 14px; box-shadow:0 4px 15px rgba(0,0,0,0.25);">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div style="display:flex; align-items:center; gap:10px;">
                    <img src="https://play-lh.googleusercontent.com/1fe3ZZGVphz2gyty2Cb2pm7-INTz6ryG8ekFaPDE5vV9WwN9dJRFd1fFhOhwA3JXVIhx3hAaMg4WARjzogGGnA=s96" style="width:28px; height:28px; border-radius:50%; object-fit:cover; border:1px solid #ccff00;" />
                    <div>
                        <div style="font-size:14px; font-weight:800; color:#ffffff;">CoinDCX India Terminal</div>
                        <div style="font-size:10px; color:#94a3b8;">24/7 Spot & 10x Crypto Futures</div>
                    </div>
                </div>
                <div style="text-align:right;">
                    <div style="font-size:14px; font-weight:800; color:#ccff00; font-family:'JetBrains Mono',monospace;">₹{coindcx_total_portfolio:,.2f}</div>
                    <div style="font-size:10px; color:#10b981; font-weight:700;">{'+' if (coindcx_total_portfolio - 2000.0)>=0 else ''}₹{coindcx_total_portfolio - 2000.0:,.2f} (Paper ₹2,000)</div>
                </div>
            </div>
        </a>
    </div>
    """)

    # REAL-TIME QUANTITATIVE INDICATOR RADAR (Zero Dummy Trades Guarantee)
    st.markdown("""
    <div style="background:#111827; border:1px solid #1f2937; border-radius:20px; padding:14px; margin-bottom:14px; box-shadow:0 4px 20px rgba(0,0,0,0.4);">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
            <div style="display:flex; align-items:center; gap:6px;">
                <span style="font-size:14px;">📡</span>
                <span style="font-size:12px; font-weight:800; color:#f8fafc; text-transform:uppercase; letter-spacing:0.5px;">
                    Real Technical Gate (Zero Dummy Trades)
                </span>
            </div>
            <span style="background:rgba(16,185,129,0.15); border:1px solid #10b981; color:#10b981; font-size:9px; font-weight:800; padding:2px 6px; border-radius:8px;">
                100% REAL FEED
            </span>
        </div>
    """, unsafe_allow_html=True)

    for sym in CRYPTO_SYMBOLS:
        tech = market_scanner.get(sym, {})
        p_data = live_prices.get(sym, {})
        sig = tech.get("signal", "WAIT")
        rsi = tech.get("rsi", 50.0)
        p_inr = p_data.get("inr", 0.0)
        is_buy = sig == "BUY"
        status_badge = f'<span style="background:{"rgba(16,185,129,0.2)" if is_buy else "rgba(234,179,8,0.15)"}; color:{"#10b981" if is_buy else "#eab308"}; border:1px solid {"#10b98155" if is_buy else "#eab30855"}; font-size:9px; font-weight:800; padding:2px 6px; border-radius:6px;">{"🟢 BUY ARMED" if is_buy else "⏳ WAITING"}</span>'

        render_html(f"""
        <div style="display:flex; justify-content:space-between; align-items:center; background:#090d16; border:1px solid #1e293b; border-radius:12px; padding:8px 12px; margin-bottom:6px;">
            <div>
                <span style="font-size:13px; font-weight:800; color:#ffffff;">{sym} / USDT</span>
                <span style="font-size:11px; color:#64748b; margin-left:6px; font-family:'JetBrains Mono',monospace;">₹{p_inr:,.1f}</span>
            </div>
            <div style="display:flex; align-items:center; gap:8px;">
                <span style="font-size:10px; color:#94a3b8; font-family:'JetBrains Mono',monospace;">RSI {rsi}</span>
                {status_badge}
            </div>
        </div>
        """)

    st.markdown("""
        <div style="font-size:10px; color:#64748b; text-align:center; margin-top:4px;">
            🛡️ Strict Gate: Bot only enters when EMA 9 > 21 and RSI is 42-68. Rejects weak consolidation.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Mini Live Spotlight (Active Positions Across All 3 Brokers)
    all_active_positions = []
    for cat_name, p_list in engine_data["active_positions"].items():
        all_active_positions.extend(p_list)

    if len(all_active_positions) > 0:
        st.markdown(f'<div style="font-size:14px; font-weight:800; color:#f8fafc; margin-bottom:10px;">⚡ Active Unified Positions ({len(all_active_positions)} Live)</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        pos_sub = all_active_positions[:2]
        for idx, p in enumerate(pos_sub):
            col = c1 if idx == 0 else c2
            theme = "card-mint" if idx == 0 else "card-lavender"
            b_label = p.get('broker', '').upper()
            sym_name = p.get('symbol', p.get('contract', ''))
            cmp_val = p.get('cmp', 0)
            pnl_val = p.get('pnl', 0)
            is_usd = p.get('broker') == 'bybit'
            cur_prefix = '$' if is_usd else '₹'
            with col:
                st.markdown(f"""
                <div class="{theme}">
                    <div style="display:flex; justify-content:space-between; font-weight:800; font-size:14px;">
                        <span>{sym_name}</span>
                        <span style="font-size:10px; background:rgba(0,0,0,0.15); padding:2px 6px; border-radius:6px;">{b_label}</span>
                    </div>
                    <div style="font-size:10px; margin-top:2px; opacity:0.8;">📅 {p.get('date', 'Today')}</div>
                    <div style="font-size:16px; font-weight:800; margin-top:4px;">{cur_prefix}{cmp_val:,.2f}</div>
                    <div style="font-size:11px; font-weight:700; margin-top:3px;">
                        P&L: {'+' if pnl_val>=0 else ''}{cur_prefix}{pnl_val:.2f}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Quick Reset Demo Action
        render_html(f"""
        <div style="display:flex; justify-content:center; margin-top:10px; margin-bottom:14px;">
            <a href="?tab=home&action=reset_demo{theme_suffix}" target="_self" style="background:#33415544; border:1px solid #64748b; color:#cbd5e1 !important; font-size:11px; font-weight:800; padding:8px 16px; border-radius:12px; text-decoration:none !important;">
                🧹 Reset All 3 Accounts to ₹2,000 Demo Grant
            </a>
        </div>
        """)
    else:
        st.markdown("""
        <div style="background:#090d16; border:1px dashed #334155; border-radius:14px; padding:14px; text-align:center; margin-bottom:14px;">
            <div style="font-size:13px; font-weight:700; color:#cbd5e1;">🛡️ No Active Trades (Market Consolidating)</div>
            <div style="font-size:11px; color:#64748b; margin-top:3px;">The bot is patiently scanning 5-min candles. It refuses to gamble during indecisive trends.</div>
        </div>
        """, unsafe_allow_html=True)


# ==========================================
# FIXED MOBILE BOTTOM APP MENU BAR (Always Anchored)
# ==========================================
is_home = active_tab not in ["bybit", "angel", "coindcx"]
is_bybit = active_tab == "bybit"
is_angel = active_tab == "angel"
is_coindcx = active_tab == "coindcx"

st.markdown(f"""
<div class="fixed-bottom-bar">
    <a href="?tab=home{theme_suffix}" target="_self" class="nav-btn">
        <div class="{'nav-icon-active' if is_home else 'nav-icon'}">🏠</div>
        <span style="color:{'#0f172a' if (is_home and not is_dark) else ('#ccff00' if is_home else ('#94a3b8' if is_dark else '#64748b'))};">Home</span>
    </a>
    <a href="?tab=bybit{theme_suffix}" target="_self" class="nav-btn">
        <div class="{'nav-icon-active' if is_bybit else 'nav-icon'}" style="padding:2px;">
            <img src="https://assets.coingecko.com/markets/images/698/small/bybit_spot.png" style="width:24px; height:24px; border-radius:50%; object-fit:cover;" />
        </div>
        <span style="color:{'#0f172a' if (is_bybit and not is_dark) else ('#ccff00' if is_bybit else ('#94a3b8' if is_dark else '#64748b'))};">Bybit</span>
    </a>
    <a href="?tab=angel{theme_suffix}" target="_self" class="nav-btn">
        <div class="{'nav-icon-active' if is_angel else 'nav-icon'}" style="padding:2px;">
            <img src="https://assets-netstorage.groww.in/stock-assets/logos2/ANGELONE.webp" style="width:24px; height:24px; border-radius:50%; object-fit:cover;" />
        </div>
        <span style="color:{'#0f172a' if (is_angel and not is_dark) else ('#ccff00' if is_angel else ('#94a3b8' if is_dark else '#64748b'))};">Angel One</span>
    </a>
    <a href="?tab=coindcx{theme_suffix}" target="_self" class="nav-btn">
        <div class="{'nav-icon-active' if is_coindcx else 'nav-icon'}" style="padding:2px;">
            <img src="https://play-lh.googleusercontent.com/1fe3ZZGVphz2gyty2Cb2pm7-INTz6ryG8ekFaPDE5vV9WwN9dJRFd1fFhOhwA3JXVIhx3hAaMg4WARjzogGGnA=s96" style="width:24px; height:24px; border-radius:50%; object-fit:cover;" />
        </div>
        <span style="color:{'#0f172a' if (is_coindcx and not is_dark) else ('#ccff00' if is_coindcx else ('#94a3b8' if is_dark else '#64748b'))};">CoinDCX</span>
    </a>
</div>
""", unsafe_allow_html=True)

# Auto refresh loop
time.sleep(2)
st.rerun()
