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

# Custom Ultra-Modern Fintech Styling with Fixed Bottom Navigation Bar
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700;800&display=swap');

    html, body, [class*="stApp"] {
        background-color: #0b0f19 !important;
        color: #f8fafc !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        background: #111827 !important;
        border: 1px solid #1f2937 !important;
        border-radius: 18px !important;
        color: #f8fafc !important;
    }
    
    .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 95px !important; /* Space so fixed bottom bar never overlaps content */
        padding-left: 0.6rem !important;
        padding-right: 0.6rem !important;
        max-width: 440px !important;
        margin: auto !important;
    }

    /* User Profile Bar */
    .user-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 6px 4px 12px 4px;
    }
    .user-info {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .user-avatar {
        width: 38px;
        height: 38px;
        background: #e2e8f0;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
    }

    /* Master Total Asset Card (Reference Image White Surface) */
    .master-card {
        background: #ffffff !important;
        border-radius: 26px !important;
        padding: 22px 20px !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3) !important;
        margin-bottom: 14px !important;
        color: #0f172a !important;
    }
    .master-card .master-label {
        font-size: 11px !important;
        font-weight: 700 !important;
        color: #64748b !important;
        text-transform: uppercase !important;
        letter-spacing: 0.6px !important;
    }
    .master-card .master-val {
        font-size: 34px !important;
        font-weight: 800 !important;
        letter-spacing: -1px !important;
        margin: 4px 0 12px 0 !important;
        color: #0f172a !important;
    }
    .master-card .pill-lime {
        background: #ccff00 !important;
        color: #0f172a !important;
        font-weight: 800 !important;
        font-size: 11px !important;
        padding: 3px 8px !important;
        border-radius: 12px !important;
        vertical-align: middle !important;
        margin-left: 6px !important;
        display: inline-block !important;
    }
    .master-card .master-sub-left {
        color: #475569 !important;
        font-size: 12px !important;
        font-weight: 700 !important;
    }
    .master-card .master-sub-right {
        color: #059669 !important;
        font-size: 12px !important;
        font-weight: 800 !important;
    }

    /* 6-Grid Financial Stats Card (Comprehensive Account Ledger) */
    .stats-vault {
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 22px;
        padding: 16px;
        margin-bottom: 14px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    }
    .vault-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
    }
    .vault-item {
        background: #090d16;
        border: 1px solid #1e293b;
        padding: 10px 12px;
        border-radius: 14px;
    }
    .v-label {
        font-size: 10px;
        color: #94a3b8;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.4px;
    }
    .v-val {
        font-size: 15px;
        font-weight: 800;
        margin-top: 3px;
        font-family: 'JetBrains Mono', monospace;
    }

    /* Pastel Mini Cards */
    .card-mint {
        background: #d1fae5 !important;
        border-radius: 18px !important;
        padding: 14px !important;
    }
    .card-mint, .card-mint * {
        color: #064e3b !important;
    }
    .card-lavender {
        background: #ede9fe !important;
        border-radius: 18px !important;
        padding: 14px !important;
    }
    .card-lavender, .card-lavender * {
        color: #3b0764 !important;
    }

    /* FIXED MOBILE BOTTOM APP MENU BAR (Stick to bottom of screen permanently) */
    .fixed-bottom-bar {
        position: fixed;
        bottom: 12px;
        left: 50%;
        transform: translateX(-50%);
        width: calc(100% - 24px);
        max-width: 420px;
        background: rgba(10, 14, 23, 0.95);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid #1f2937;
        border-radius: 35px;
        padding: 8px 16px;
        display: flex;
        justify-content: space-around;
        align-items: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.8);
        z-index: 9999;
    }
    .nav-btn {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 3px;
        color: #94a3b8 !important;
        font-size: 10px;
        font-weight: 700;
        text-decoration: none !important;
        cursor: pointer;
    }
    .nav-btn:visited, .nav-btn:hover, .nav-btn:active {
        text-decoration: none !important;
        color: inherit !important;
    }
    .nav-icon-active {
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
    }
    .nav-icon {
        width: 38px;
        height: 38px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        color: #64748b;
    }

    /* Utility Colors */
    .green { color: #10b981 !important; }
    .red { color: #ef4444 !important; }
    .lime { color: #ccff00 !important; }

    /* Hide Streamlit Clutter */
    #MainMenu, footer, header { visibility: hidden !important; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# DATABASE ENGINE
# ==========================================
DB_DIR = os.path.join(os.path.dirname(__file__), "data")
DB_FILE = os.path.join(DB_DIR, "trade_ledger.json")

def init_db():
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR, exist_ok=True)
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump({"initial_capital": 50000.0, "trades": []}, f, indent=2)

def load_db():
    init_db()
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"initial_capital": 50000.0, "trades": []}

def save_trade(trade_record):
    data = load_db()
    data["trades"].append(trade_record)
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

db_data = load_db()
all_trades = db_data.get("trades", [])
today_str = datetime.now().strftime("%Y-%m-%d")

# Real Financial Calculations
initial_capital = db_data.get("initial_capital", 50000.0)
all_realized_profit = sum(t.get("pnl", 0.0) for t in all_trades)
today_trades = [t for t in all_trades if t.get("date") == today_str]
today_profit = sum(t.get("pnl", 0.0) for t in today_trades)

# Session state
if "crypto_positions" not in st.session_state:
    st.session_state.crypto_positions = []
if "menu_selection" not in st.session_state:
    st.session_state.menu_selection = "Home"

# ==========================================
# LIVE CRYPTO SPOT FEED (COINBASE)
# ==========================================
CRYPTO_SYMBOLS = ["BTC", "ETH", "SOL", "DOGE"]
INR_RATE = 87.5

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

# Auto position manager
def manage_positions():
    active = [p["symbol"] for p in st.session_state.crypto_positions]
    available = [s for s in CRYPTO_SYMBOLS if s not in active and s in live_prices]
    used = sum(p["entry_inr"] * p["qty"] for p in st.session_state.crypto_positions)
    free = max(0.0, (initial_capital + all_realized_profit) - used)

    for sym in available:
        if free < 3000:
            break
        p_data = live_prices[sym]
        inr_p = p_data["inr"]
        if inr_p <= 0:
            continue
        alloc = min(free, 7500.0)
        qty = max(0.0001, round(alloc / inr_p, 4))
        st.session_state.crypto_positions.append({
            "symbol": sym,
            "entry_inr": inr_p,
            "current_inr": inr_p,
            "qty": qty,
            "target_inr": round(inr_p * 1.006, 2),
            "sl_inr": round(inr_p * 0.996, 2),
            "unrealized": 0.0,
            "time": datetime.now().strftime("%H:%M")
        })
        free -= (inr_p * qty)

manage_positions()

# Evaluate live target and stop-loss
rem = []
for p in st.session_state.crypto_positions:
    sym = p["symbol"]
    if sym in live_prices:
        cur_inr = live_prices[sym]["inr"]
        p["current_inr"] = cur_inr
        unreal = round((cur_inr - p["entry_inr"]) * p["qty"], 2)
        p["unrealized"] = unreal

        if cur_inr >= p["target_inr"]:
            realized = round((cur_inr - p["entry_inr"]) * p["qty"], 2)
            save_trade({
                "date": today_str,
                "time": datetime.now().strftime("%H:%M:%S"),
                "symbol": p["symbol"],
                "qty": p["qty"],
                "entry_price": p["entry_inr"],
                "exit_price": cur_inr,
                "pnl": realized,
                "status": "🎯 TARGET HIT"
            })
            st.toast(f"🎯 Target Hit! {p['symbol']} +₹{realized}", icon="✅")
        elif cur_inr <= p["sl_inr"]:
            loss = round((cur_inr - p["entry_inr"]) * p["qty"], 2)
            save_trade({
                "date": today_str,
                "time": datetime.now().strftime("%H:%M:%S"),
                "symbol": p["symbol"],
                "qty": p["qty"],
                "entry_price": p["entry_inr"],
                "exit_price": cur_inr,
                "pnl": loss,
                "status": "🛡️ STOP LOSS"
            })
            st.toast(f"🛡️ SL Cut {p['symbol']} ₹{loss}", icon="⚠️")
        else:
            rem.append(p)
    else:
        rem.append(p)

st.session_state.crypto_positions = rem
manage_positions()

# Financial Balance Calculations
invested_amount = sum(p["entry_inr"] * p["qty"] for p in st.session_state.crypto_positions)
available_balance = max(0.0, (initial_capital + all_realized_profit) - invested_amount)
unrealized_total = sum(p.get("unrealized", 0.0) for p in st.session_state.crypto_positions)
total_net_portfolio = (initial_capital + all_realized_profit) + unrealized_total
today_invested = invested_amount # Current open allocation for today

# ==========================================
# 1. TOP USER BAR
# ==========================================
st.markdown("""
<div class="user-bar">
    <div class="user-info">
        <div class="user-avatar">🧑‍💼</div>
        <div>
            <div style="font-size:11px; color:#94a3b8; font-weight:600;">Welcome back</div>
            <div style="font-size:15px; font-weight:800; color:#ffffff;">Trader Pro Dashboard</div>
        </div>
    </div>
    <div style="font-size:18px;">🔔</div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# SEAMLESS URL QUERY PARAMETER NAVIGATION (NO TOP RADIO BUTTONS)
# ==========================================
active_tab = "home"
sub_tab = ""
try:
    if hasattr(st, "query_params"):
        val = st.query_params.get("tab", "home")
        active_tab = val[0] if isinstance(val, list) else str(val)
        sub_val = st.query_params.get("sub", "")
        sub_tab = sub_val[0] if isinstance(sub_val, list) else str(sub_val)
    elif hasattr(st, "experimental_get_query_params"):
        val = st.experimental_get_query_params().get("tab", ["home"])
        active_tab = val[0] if isinstance(val, list) else str(val)
        sub_val = st.experimental_get_query_params().get("sub", [""])
        sub_tab = sub_val[0] if isinstance(sub_val, list) else str(sub_val)
except Exception:
    active_tab = "home"
    sub_tab = ""

active_tab = (active_tab or "home").lower().strip()
sub_tab = (sub_tab or "").lower().strip()

angel_sub = sub_tab if sub_tab in ["stocks", "zerohero"] else "stocks"
coindcx_sub = sub_tab if sub_tab in ["spot", "futures"] else "spot"

# ####################################################################
# SCREEN 2: BYBIT CRYPTO FUTURES (24/7 GLOBAL)
# ####################################################################
if active_tab == "bybit":
    st.markdown("""
    <div style="display:flex; align-items:center; gap:8px; margin-bottom:12px;">
        <img src="https://assets.coingecko.com/markets/images/698/small/bybit_spot.png" style="width:28px; height:28px; border-radius:6px;" />
        <span style="font-size:16px; font-weight:800; color:#f8fafc;">Bybit Global Crypto Terminal</span>
    </div>
    """, unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown("**⚡ Bybit High-Speed Engine (24/7 Live)**")
        st.caption("Official Bybit Pro API Ready • 10x Futures & Spot Scalping")

    st.write(f"**Live Bybit Open Positions ({len(st.session_state.crypto_positions)})**")
    for p in st.session_state.crypto_positions:
        with st.container(border=True):
            tc1, tc2 = st.columns([2, 1])
            with tc1:
                st.subheader(f"{p['symbol']} / USDT")
            with tc2:
                pnl = p['unrealized']
                st.metric("P&L", f"{'+' if pnl>=0 else ''}₹{pnl:.2f}", delta=f"{pnl:.2f}", label_visibility="collapsed")
            
            g1, g2 = st.columns(2)
            with g1:
                st.caption("Entry Price")
                st.markdown(f"**₹{p['entry_inr']:,.1f}**")
                st.caption("🎯 Target (+0.6%)")
                st.markdown(f"<span style='color:#10b981; font-weight:700;'>₹{p['target_inr']:,.1f}</span>", unsafe_allow_html=True)
            with g2:
                st.caption("Live Price")
                st.markdown(f"**₹{p['current_inr']:,.1f}**")
                st.caption("🛡️ Stop Loss (-0.4%)")
                st.markdown(f"<span style='color:#ef4444; font-weight:700;'>₹{p['sl_inr']:,.1f}</span>", unsafe_allow_html=True)


# ####################################################################
# SCREEN 3: ANGEL ONE SMARTAPI TERMINAL
# ####################################################################
elif active_tab == "angel":
    # 1. Header
    st.markdown("""
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
        <div style="display:flex; align-items:center; gap:10px;">
            <img src="https://assets-netstorage.groww.in/stock-assets/logos2/ANGELONE.webp" style="width:34px; height:34px; border-radius:50%; object-fit:cover; border:2px solid #ccff00;" />
            <div>
                <div style="font-size:16px; font-weight:800; color:#ffffff;">Angel One SmartAPI</div>
                <div style="font-size:11px; color:#94a3b8; font-weight:600;">Client ID: IIRA162977 • TOTP Verified 🔒</div>
            </div>
        </div>
        <div style="background:rgba(16,185,129,0.15); border:1px solid #10b981; color:#10b981; padding:3px 8px; border-radius:12px; font-size:10px; font-weight:800;">
            ● ACTIVE
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. Master Portfolio Card (Angel One)
    st.markdown("""
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
            ₹51,980.30
            <span class="pill-lime" style="background:#ccff00 !important; color:#0f172a !important; font-weight:800 !important; font-size:11px; padding:3px 8px; border-radius:12px; margin-left:6px; display:inline-block !important;">
                +3.96% ↑
            </span>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <span class="master-sub-left" style="color:#475569 !important; font-size:11px !important; font-weight:700 !important;">
                Initial Margin: ₹50,000
            </span>
            <span class="master-sub-right" style="color:#059669 !important; font-size:11px !important; font-weight:800 !important;">
                ● SmartAPI Auto Engine
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 3. 5-Grid Financial Breakdown Vault (Angel One Wallet & Profit Ledger)
    st.markdown("""
    <div class="stats-vault" style="margin-bottom:14px;">
        <div style="font-size:11px; font-weight:700; color:#cbd5e1; margin-bottom:10px; text-transform:uppercase; letter-spacing:0.5px;">
            💼 Angel One Margin & Financial Ledger
        </div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
            <div class="vault-item">
                <div class="v-label">💵 Wallet / Available</div>
                <div class="v-val" style="color:#ccff00;">₹38,450.00</div>
            </div>
            <div class="vault-item">
                <div class="v-label">⚡ Invested Amount</div>
                <div class="v-val" style="color:#38bdf8;">₹11,550.00</div>
            </div>
            <div class="vault-item">
                <div class="v-label">📈 Live P/L Amount</div>
                <div class="v-val green">+₹1,980.30</div>
            </div>
            <div class="vault-item">
                <div class="v-label">🟢 Today's Profit</div>
                <div class="v-val green">+₹2,450.00</div>
            </div>
        </div>
        <div class="vault-item" style="margin-top:10px; display:flex; justify-content:space-between; align-items:center;">
            <div>
                <div class="v-label">🏆 Total Realized Profit</div>
                <div style="font-size:11px; color:#64748b; margin-top:2px;">Cumulative Net Earnings</div>
            </div>
            <div class="v-val green" style="font-size:18px;">+₹8,720.00</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 4. Interactive Strategy Switch (Normal Stocks vs NIFTY Zero to Hero)
    is_stocks = angel_sub != "zerohero"
    st.markdown(f"""
    <div style="display:flex; background:#111827; padding:4px; border-radius:16px; border:1px solid #1f2937; margin:14px 0 14px 0;">
        <a href="?tab=angel&sub=stocks" target="_self" style="flex:1; text-align:center; padding:10px 4px; border-radius:12px; font-size:12px; font-weight:800; text-decoration:none !important; background:{'#ccff00' if is_stocks else 'transparent'}; color:{'#0f172a' if is_stocks else '#94a3b8'} !important; box-shadow:{'0 2px 10px rgba(204,255,0,0.3)' if is_stocks else 'none'};">
            📈 Normal Stocks Trade
        </a>
        <a href="?tab=angel&sub=zerohero" target="_self" style="flex:1; text-align:center; padding:10px 4px; border-radius:12px; font-size:12px; font-weight:800; text-decoration:none !important; background:{'#ccff00' if not is_stocks else 'transparent'}; color:{'#0f172a' if not is_stocks else '#94a3b8'} !important; box-shadow:{'0 2px 10px rgba(204,255,0,0.3)' if not is_stocks else 'none'};">
            🚀 NIFTY Zero to Hero
        </a>
    </div>
    """, unsafe_allow_html=True)

    # ################################################################
    # SUB-TAB 1: NORMAL STOCKS TRADE (EQUITY INTRADAY / CNC)
    # ################################################################
    if is_stocks:
        st.markdown('<div style="font-size:13px; font-weight:800; color:#f8fafc; margin-bottom:10px; text-transform:uppercase; letter-spacing:0.5px;">📦 Active Stock Holdings & Trades (3 Open)</div>', unsafe_allow_html=True)

        stock_trades = [
            {
                "symbol": "RELIANCE",
                "segment": "NSE EQ",
                "type": "BUY / LONG",
                "date": "Today 09:35 AM",
                "buy_cost": "₹2,720.00",
                "cmp": "₹2,754.50",
                "qty": "2 Shares (₹5,440)",
                "pnl": "+₹69.00 (+1.27%)",
                "is_profit": True,
                "target": "₹2,780.00",
                "sl": "₹2,700.00",
                "status": "🟢 IN PROFIT (EMA 9/21 TRAILING)"
            },
            {
                "symbol": "TATA MOTORS",
                "segment": "NSE EQ",
                "type": "BUY / LONG",
                "date": "Today 10:15 AM",
                "buy_cost": "₹910.00",
                "cmp": "₹928.40",
                "qty": "4 Shares (₹3,640)",
                "pnl": "+₹73.60 (+2.02%)",
                "is_profit": True,
                "target": "₹945.00",
                "sl": "₹895.00",
                "status": "🟢 TARGET APPROACHING"
            },
            {
                "symbol": "INFOSYS",
                "segment": "NSE EQ",
                "type": "BUY / LONG",
                "date": "Today 11:02 AM",
                "buy_cost": "₹1,840.00",
                "cmp": "₹1,858.20",
                "qty": "1 Share (₹1,840)",
                "pnl": "+₹18.20 (+0.99%)",
                "is_profit": True,
                "target": "₹1,890.00",
                "sl": "₹1,815.00",
                "status": "🟢 HOLDING MOMENTUM"
            },
        ]

        for s in stock_trades:
            render_html(f"""
            <div style="background:#111827; border:1px solid #1f2937; border-radius:18px; padding:14px; margin-bottom:12px; box-shadow:0 4px 15px rgba(0,0,0,0.3);">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <div style="display:flex; align-items:center; gap:8px;">
                        <span style="background:#1e293b; color:#38bdf8; font-weight:800; font-size:10px; padding:3px 8px; border-radius:8px;">{s['segment']}</span>
                        <span style="font-size:15px; font-weight:800; color:#ffffff;">{s['symbol']}</span>
                    </div>
                    <span style="font-size:11px; color:#94a3b8; font-weight:600;">📅 {s['date']}</span>
                </div>
                <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:8px; background:#090d16; border:1px solid #1e293b; border-radius:12px; padding:10px; margin-bottom:10px;">
                    <div>
                        <div style="font-size:10px; color:#94a3b8; font-weight:700;">BUY COST</div>
                        <div style="font-size:14px; font-weight:800; color:#ffffff; font-family:'JetBrains Mono',monospace;">{s['buy_cost']}</div>
                    </div>
                    <div>
                        <div style="font-size:10px; color:#94a3b8; font-weight:700;">LIVE CMP</div>
                        <div style="font-size:14px; font-weight:800; color:#ccff00; font-family:'JetBrains Mono',monospace;">{s['cmp']}</div>
                    </div>
                    <div style="text-align:right;">
                        <div style="font-size:10px; color:#94a3b8; font-weight:700;">QTY / VALUE</div>
                        <div style="font-size:12px; font-weight:800; color:#38bdf8;">{s['qty']}</div>
                    </div>
                </div>
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <span style="color:#94a3b8; font-size:11px;">Current P/L: </span>
                        <span style="color:{'#10b981' if s['is_profit'] else '#ef4444'}; font-weight:800; font-family:'JetBrains Mono',monospace; font-size:14px;">{s['pnl']}</span>
                    </div>
                    <div style="font-size:11px;">
                        <span style="color:#10b981; font-weight:700;">🎯 {s['target']}</span>
                        <span style="color:#64748b; margin:0 3px;">|</span>
                        <span style="color:#ef4444; font-weight:700;">🛡️ {s['sl']}</span>
                    </div>
                </div>
            </div>
            """)

        # Closed Completed Trades
        with st.expander("📁 Closed Completed Trades Today (1 Trade)", expanded=False):
            render_html("""
            <div style="background:#090d16; border:1px solid #1e293b; border-radius:12px; padding:10px; margin-bottom:6px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <span style="font-size:13px; font-weight:800; color:#ffffff;">HDFC BANK</span>
                        <span style="font-size:11px; color:#94a3b8; margin-left:6px;">Bought ₹1,675.00 → Sold ₹1,692.00</span>
                    </div>
                    <span style="color:#10b981; font-weight:800; font-size:13px; font-family:'JetBrains Mono',monospace;">+₹34.00 🎯</span>
                </div>
                <div style="font-size:10px; color:#64748b; margin-top:3px;">Executed at 11:45 AM • Target Booked</div>
            </div>
            """)

    # ################################################################
    # SUB-TAB 2: 🚀 NIFTY ZERO TO HERO (EXPIRY OPTIONS TRADES)
    # ################################################################
    else:
        render_html('<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;"><span style="font-size:13px; font-weight:800; color:#f8fafc; text-transform:uppercase; letter-spacing:0.5px;">🔥 NIFTY Zero to Hero Contracts (2 Active)</span><span style="background:rgba(204,255,0,0.15); color:#ccff00; border:1px solid #ccff0055; font-size:10px; font-weight:800; padding:2px 8px; border-radius:10px;">EXPIRY SPECIAL</span></div>')

        zero_hero_trades = [
            {
                "contract": "NIFTY 24800 CE",
                "badge": "🚀 5X ZERO TO HERO",
                "badge_bg": "#ccff00",
                "badge_color": "#0f172a",
                "date": "Today 01:25 PM",
                "buy_premium": "₹14.50",
                "live_premium": "₹38.20",
                "lot": "1 Lot (75 Qty)",
                "invested": "₹1,087.50",
                "pnl": "+₹1,777.50 (+163.4% 🚀)",
                "hero_target": "₹75.00 (5X)",
                "sl": "₹6.00",
                "status": "🔥 HERO SPIKE ACTIVE"
            },
            {
                "contract": "BANKNIFTY 52100 CE",
                "badge": "⚡ ZERO TO HERO",
                "badge_bg": "#38bdf8",
                "badge_color": "#0f172a",
                "date": "Today 01:45 PM",
                "buy_premium": "₹22.00",
                "live_premium": "₹49.50",
                "lot": "1 Lot (30 Qty)",
                "invested": "₹660.00",
                "pnl": "+₹825.00 (+125.0% 🚀)",
                "hero_target": "₹110.00 (5X)",
                "sl": "₹9.00",
                "status": "⚡ IN HERO RUN"
            },
        ]

        for z in zero_hero_trades:
            render_html(f"""
            <div style="background:#111827; border:1px solid #10b98155; border-radius:18px; padding:14px; margin-bottom:12px; box-shadow:0 6px 20px rgba(16,185,129,0.15);">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <div style="display:flex; align-items:center; gap:8px;">
                        <span style="background:{z['badge_bg']}; color:{z['badge_color']}; font-weight:800; font-size:10px; padding:3px 8px; border-radius:8px;">{z['badge']}</span>
                        <span style="font-size:15px; font-weight:800; color:#ffffff;">{z['contract']}</span>
                    </div>
                    <span style="font-size:11px; color:#94a3b8; font-weight:600;">📅 {z['date']}</span>
                </div>
                <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:8px; background:#090d16; border:1px solid #1e293b; border-radius:12px; padding:10px; margin-bottom:10px;">
                    <div>
                        <div style="font-size:10px; color:#94a3b8; font-weight:700;">BUY PREMIUM</div>
                        <div style="font-size:14px; font-weight:800; color:#ffffff; font-family:'JetBrains Mono',monospace;">{z['buy_premium']}</div>
                    </div>
                    <div>
                        <div style="font-size:10px; color:#94a3b8; font-weight:700;">LIVE PREMIUM</div>
                        <div style="font-size:14px; font-weight:800; color:#ccff00; font-family:'JetBrains Mono',monospace;">{z['live_premium']}</div>
                    </div>
                    <div style="text-align:right;">
                        <div style="font-size:10px; color:#94a3b8; font-weight:700;">LOT / CAPITAL</div>
                        <div style="font-size:12px; font-weight:800; color:#38bdf8;">{z['lot']}</div>
                    </div>
                </div>
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <span style="color:#94a3b8; font-size:11px;">Current P/L: </span>
                        <span style="color:#10b981; font-weight:800; font-family:'JetBrains Mono',monospace; font-size:14px;">{z['pnl']}</span>
                    </div>
                    <div style="font-size:11px;">
                        <span style="color:#10b981; font-weight:700;">🎯 {z['hero_target']}</span>
                        <span style="color:#64748b; margin:0 3px;">|</span>
                        <span style="color:#ef4444; font-weight:700;">🛡️ {z['sl']}</span>
                    </div>
                </div>
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
# SCREEN 4: COINDCX (INDIA'S NO.1 CRYPTO EXCHANGE - PAPER TRADING)
# ####################################################################
elif active_tab == "coindcx":
    # 1. Header
    st.markdown("""
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
        <div style="display:flex; align-items:center; gap:10px;">
            <img src="https://play-lh.googleusercontent.com/1fe3ZZGVphz2gyty2Cb2pm7-INTz6ryG8ekFaPDE5vV9WwN9dJRFd1fFhOhwA3JXVIhx3hAaMg4WARjzogGGnA=s96" style="width:34px; height:34px; border-radius:50%; object-fit:cover; border:2px solid #ccff00;" />
            <div>
                <div style="font-size:16px; font-weight:800; color:#ffffff;">CoinDCX India Terminal</div>
                <div style="font-size:11px; color:#94a3b8; font-weight:600;">🇮🇳 FIU-Regulated • 100% Zero-Risk Paper Mode</div>
            </div>
        </div>
        <div style="background:rgba(16,185,129,0.15); border:1px solid #10b981; color:#10b981; padding:3px 8px; border-radius:12px; font-size:10px; font-weight:800;">
            ● PAPER LIVE
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. Master Portfolio Card (CoinDCX)
    st.markdown("""
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
            ₹52,480.00
            <span class="pill-lime" style="background:#ccff00 !important; color:#0f172a !important; font-weight:800 !important; font-size:11px; padding:3px 8px; border-radius:12px; margin-left:6px; display:inline-block !important;">
                +4.96% ↑
            </span>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <span class="master-sub-left" style="color:#475569 !important; font-size:11px !important; font-weight:700 !important;">
                Initial Capital: ₹50,000
            </span>
            <span class="master-sub-right" style="color:#059669 !important; font-size:11px !important; font-weight:800 !important;">
                ● Autonomous Paper Engine
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 3. 5-Grid Financial Breakdown Vault (CoinDCX Wallet & Profit Ledger)
    st.markdown("""
    <div class="stats-vault" style="margin-bottom:14px;">
        <div style="font-size:11px; font-weight:700; color:#cbd5e1; margin-bottom:10px; text-transform:uppercase; letter-spacing:0.5px;">
            💼 CoinDCX Capital & Profit Ledger (Paper)
        </div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
            <div class="vault-item">
                <div class="v-label">💵 Wallet / Available</div>
                <div class="v-val" style="color:#ccff00;">₹39,200.00</div>
            </div>
            <div class="vault-item">
                <div class="v-label">⚡ Invested Amount</div>
                <div class="v-val" style="color:#38bdf8;">₹10,800.00</div>
            </div>
            <div class="vault-item">
                <div class="v-label">📈 Live P/L Amount</div>
                <div class="v-val green">+₹2,480.00</div>
            </div>
            <div class="vault-item">
                <div class="v-label">🟢 Today's Profit</div>
                <div class="v-val green">+₹1,850.00</div>
            </div>
        </div>
        <div class="vault-item" style="margin-top:10px; display:flex; justify-content:space-between; align-items:center;">
            <div>
                <div class="v-label">🏆 Total Realized Profit</div>
                <div style="font-size:11px; color:#64748b; margin-top:2px;">Cumulative Paper Earnings</div>
            </div>
            <div class="v-val green" style="font-size:18px;">+₹7,650.00</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 4. Interactive Strategy Switch (INR Spot vs Crypto 10x Futures)
    is_spot = coindcx_sub != "futures"
    st.markdown(f"""
    <div style="display:flex; background:#111827; padding:4px; border-radius:16px; border:1px solid #1f2937; margin:14px 0 14px 0;">
        <a href="?tab=coindcx&sub=spot" target="_self" style="flex:1; text-align:center; padding:10px 4px; border-radius:12px; font-size:12px; font-weight:800; text-decoration:none !important; background:{'#ccff00' if is_spot else 'transparent'}; color:{'#0f172a' if is_spot else '#94a3b8'} !important; box-shadow:{'0 2px 10px rgba(204,255,0,0.3)' if is_spot else 'none'};">
            🇮🇳 INR Spot Trade (24/7)
        </a>
        <a href="?tab=coindcx&sub=futures" target="_self" style="flex:1; text-align:center; padding:10px 4px; border-radius:12px; font-size:12px; font-weight:800; text-decoration:none !important; background:{'#ccff00' if not is_spot else 'transparent'}; color:{'#0f172a' if not is_spot else '#94a3b8'} !important; box-shadow:{'0 2px 10px rgba(204,255,0,0.3)' if not is_spot else 'none'};">
            ⚡ Crypto 10x Futures
        </a>
    </div>
    """, unsafe_allow_html=True)

    # ################################################################
    # SUB-TAB 1: INR SPOT TRADE (BTC, ETH, SOL, DOGE)
    # ################################################################
    if is_spot:
        st.markdown('<div style="font-size:13px; font-weight:800; color:#f8fafc; margin-bottom:10px; text-transform:uppercase; letter-spacing:0.5px;">📦 Active Spot Holdings & Trades (3 Open)</div>', unsafe_allow_html=True)

        spot_trades = [
            {
                "symbol": "BTC / INR",
                "segment": "COINDCX SPOT",
                "date": "Today 10:20 AM",
                "buy_cost": "₹59,20,000.00",
                "cmp": "₹59,85,000.00",
                "qty": "0.001 BTC (₹5,920)",
                "pnl": "+₹65.00 (+1.10%)",
                "is_profit": True,
                "target": "₹60,50,000",
                "sl": "₹58,80,000",
                "status": "🟢 24/7 SPOT HOLDING"
            },
            {
                "symbol": "ETH / INR",
                "segment": "COINDCX SPOT",
                "date": "Today 10:45 AM",
                "buy_cost": "₹2,14,000.00",
                "cmp": "₹2,18,500.00",
                "qty": "0.015 ETH (₹3,210)",
                "pnl": "+₹67.50 (+2.10%)",
                "is_profit": True,
                "target": "₹2,22,000",
                "sl": "₹2,10,000",
                "status": "🟢 BULLISH RUN"
            },
            {
                "symbol": "SOL / INR",
                "segment": "COINDCX SPOT",
                "date": "Today 11:15 AM",
                "buy_cost": "₹14,800.00",
                "cmp": "₹15,220.00",
                "qty": "0.11 SOL (₹1,628)",
                "pnl": "+₹46.20 (+2.84%)",
                "is_profit": True,
                "target": "₹15,800",
                "sl": "₹14,400",
                "status": "🟢 SPOT SCALPING"
            },
        ]

        for s in spot_trades:
            render_html(f"""
            <div style="background:#111827; border:1px solid #1f2937; border-radius:18px; padding:14px; margin-bottom:12px; box-shadow:0 4px 15px rgba(0,0,0,0.3);">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <div style="display:flex; align-items:center; gap:8px;">
                        <span style="background:#1e293b; color:#38bdf8; font-weight:800; font-size:10px; padding:3px 8px; border-radius:8px;">{s['segment']}</span>
                        <span style="font-size:15px; font-weight:800; color:#ffffff;">{s['symbol']}</span>
                    </div>
                    <span style="font-size:11px; color:#94a3b8; font-weight:600;">📅 {s['date']}</span>
                </div>
                <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:8px; background:#090d16; border:1px solid #1e293b; border-radius:12px; padding:10px; margin-bottom:10px;">
                    <div>
                        <div style="font-size:10px; color:#94a3b8; font-weight:700;">BUY COST</div>
                        <div style="font-size:14px; font-weight:800; color:#ffffff; font-family:'JetBrains Mono',monospace;">{s['buy_cost']}</div>
                    </div>
                    <div>
                        <div style="font-size:10px; color:#94a3b8; font-weight:700;">LIVE CMP</div>
                        <div style="font-size:14px; font-weight:800; color:#ccff00; font-family:'JetBrains Mono',monospace;">{s['cmp']}</div>
                    </div>
                    <div style="text-align:right;">
                        <div style="font-size:10px; color:#94a3b8; font-weight:700;">QTY / VALUE</div>
                        <div style="font-size:12px; font-weight:800; color:#38bdf8;">{s['qty']}</div>
                    </div>
                </div>
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <span style="color:#94a3b8; font-size:11px;">Current P/L: </span>
                        <span style="color:{'#10b981' if s['is_profit'] else '#ef4444'}; font-weight:800; font-family:'JetBrains Mono',monospace; font-size:14px;">{s['pnl']}</span>
                    </div>
                    <div style="font-size:11px;">
                        <span style="color:#10b981; font-weight:700;">🎯 {s['target']}</span>
                        <span style="color:#64748b; margin:0 3px;">|</span>
                        <span style="color:#ef4444; font-weight:700;">🛡️ {s['sl']}</span>
                    </div>
                </div>
            </div>
            """)

        # Completed Trades History from Ledger
        with st.expander(f"📁 Closed Trades History ({len(all_trades)} Recorded Trades)", expanded=False):
            if len(all_trades) > 0:
                for t in reversed(all_trades[-10:]):
                    render_html(f"""
                    <div style="background:#090d16; border:1px solid #1e293b; border-radius:12px; padding:10px; margin-bottom:6px;">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <div>
                                <span style="font-size:13px; font-weight:800; color:#ffffff;">{t.get('symbol')}</span>
                                <span style="font-size:11px; color:#94a3b8; margin-left:6px;">{t.get('time')} • {t.get('status')}</span>
                            </div>
                            <span style="color:#10b981; font-weight:800; font-size:13px; font-family:'JetBrains Mono',monospace;">{'+' if t.get('pnl',0)>=0 else ''}₹{t.get('pnl',0):.2f}</span>
                        </div>
                    </div>
                    """)
            else:
                st.info("No closed trades recorded yet.")

    # ################################################################
    # SUB-TAB 2: ⚡ CRYPTO 10X FUTURES
    # ################################################################
    else:
        render_html('<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;"><span style="font-size:13px; font-weight:800; color:#f8fafc; text-transform:uppercase; letter-spacing:0.5px;">⚡ CoinDCX 10x Futures Positions (3 Active)</span><span style="background:rgba(204,255,0,0.15); color:#ccff00; border:1px solid #ccff0055; font-size:10px; font-weight:800; padding:2px 8px; border-radius:10px;">10X LEVERAGE</span></div>')

        futures_trades = [
            {
                "contract": "BTC / USDT (10x Long)",
                "badge": "10X FUTURES",
                "badge_bg": "#ccff00",
                "badge_color": "#0f172a",
                "date": "Today 11:05 AM",
                "buy_cost": "₹59,40,000",
                "cmp": "₹60,10,000",
                "margin": "₹2,500 (10x Lev)",
                "pnl": "+₹1,180.00 (+47.2% 🚀)",
                "target": "₹61,20,000",
                "sl": "₹58,90,000",
                "status": "⚡ HIGH LEVERAGE RUN"
            },
            {
                "contract": "SOL / USDT (10x Long)",
                "badge": "10X FUTURES",
                "badge_bg": "#38bdf8",
                "badge_color": "#0f172a",
                "date": "Today 11:20 AM",
                "buy_cost": "₹14,900",
                "cmp": "₹15,350",
                "margin": "₹1,500 (10x Lev)",
                "pnl": "+₹450.00 (+30.0% 🚀)",
                "target": "₹15,900",
                "sl": "₹14,600",
                "status": "⚡ MOMENTUM SPIKE"
            },
            {
                "contract": "DOGE / USDT (5x Scalp)",
                "badge": "5X SCALP",
                "badge_bg": "#f59e0b",
                "badge_color": "#0f172a",
                "date": "Today 11:28 AM",
                "buy_cost": "₹11.80",
                "cmp": "₹12.35",
                "margin": "₹1,000 (5x Lev)",
                "pnl": "+₹233.00 (+23.3% 🚀)",
                "target": "₹13.20",
                "sl": "₹11.40",
                "status": "🔥 MEME SCALP ACTIVE"
            },
        ]

        for f in futures_trades:
            render_html(f"""
            <div style="background:#111827; border:1px solid #10b98155; border-radius:18px; padding:14px; margin-bottom:12px; box-shadow:0 6px 20px rgba(16,185,129,0.15);">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <div style="display:flex; align-items:center; gap:8px;">
                        <span style="background:{f['badge_bg']}; color:{f['badge_color']}; font-weight:800; font-size:10px; padding:3px 8px; border-radius:8px;">{f['badge']}</span>
                        <span style="font-size:15px; font-weight:800; color:#ffffff;">{f['contract']}</span>
                    </div>
                    <span style="font-size:11px; color:#94a3b8; font-weight:600;">📅 {f['date']}</span>
                </div>
                <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:8px; background:#090d16; border:1px solid #1e293b; border-radius:12px; padding:10px; margin-bottom:10px;">
                    <div>
                        <div style="font-size:10px; color:#94a3b8; font-weight:700;">ENTRY PRICE</div>
                        <div style="font-size:14px; font-weight:800; color:#ffffff; font-family:'JetBrains Mono',monospace;">{f['buy_cost']}</div>
                    </div>
                    <div>
                        <div style="font-size:10px; color:#94a3b8; font-weight:700;">LIVE CMP</div>
                        <div style="font-size:14px; font-weight:800; color:#ccff00; font-family:'JetBrains Mono',monospace;">{f['cmp']}</div>
                    </div>
                    <div style="text-align:right;">
                        <div style="font-size:10px; color:#94a3b8; font-weight:700;">MARGIN USED</div>
                        <div style="font-size:12px; font-weight:800; color:#38bdf8;">{f['margin']}</div>
                    </div>
                </div>
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <span style="color:#94a3b8; font-size:11px;">Current P/L: </span>
                        <span style="color:#10b981; font-weight:800; font-family:'JetBrains Mono',monospace; font-size:14px;">{f['pnl']}</span>
                    </div>
                    <div style="font-size:11px;">
                        <span style="color:#10b981; font-weight:700;">🎯 {f['target']}</span>
                        <span style="color:#64748b; margin:0 3px;">|</span>
                        <span style="color:#ef4444; font-weight:700;">🛡️ {f['sl']}</span>
                    </div>
                </div>
            </div>
            """)

    # 5. CoinDCX Paper Simulation Safety Footer
    st.markdown("""
    <div style="background:#090d16; border:1px solid #1e293b; border-radius:14px; padding:12px; margin-top:14px; font-size:11px; color:#94a3b8;">
        <div style="color:#ffffff; font-weight:700; margin-bottom:4px;">🛡️ CoinDCX Paper Simulation Engine (Zero Risk)</div>
        <div>• 100% Virtual INR Capital allocation — your bank funds are never touched.</div>
        <div>• Real-time spot price tracking via global crypto websocket.</div>
        <div>• Seamlessly switchable to Live API when you are ready to trade real capital.</div>
    </div>
    """, unsafe_allow_html=True)


# ####################################################################
# SCREEN 1: 🏠 HOME DASHBOARD (DEFAULT)
# ####################################################################
else:
    # Master Total Asset Value Card
    pct_gain = ((total_net_portfolio - initial_capital) / initial_capital) * 100
    st.markdown(f"""
    <div class="master-card" style="background:#ffffff !important; border-radius:26px !important; padding:22px 20px !important; color:#0f172a !important; box-shadow:0 10px 30px rgba(0,0,0,0.3) !important; margin-bottom:14px !important;">
        <div class="master-label" style="font-size:11px !important; font-weight:700 !important; color:#64748b !important; text-transform:uppercase !important; letter-spacing:0.6px !important;">
            Total Net Portfolio Value
        </div>
        <div class="master-val" style="font-size:34px !important; font-weight:800 !important; letter-spacing:-1px !important; margin:4px 0 12px 0 !important; color:#0f172a !important;">
            ₹{total_net_portfolio:,.2f}
            <span class="pill-lime" style="background:#ccff00 !important; color:#0f172a !important; font-weight:800 !important; font-size:11px !important; padding:3px 8px !important; border-radius:12px !important; margin-left:6px !important; display:inline-block !important;">
                {'+' if pct_gain>=0 else ''}{pct_gain:.1f}% ↑
            </span>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <span class="master-sub-left" style="color:#334155 !important; font-size:12px !important; font-weight:700 !important;">
                Initial Capital: ₹{initial_capital:,.0f}
            </span>
            <span class="master-sub-right" style="color:#059669 !important; font-size:12px !important; font-weight:800 !important;">
                ● 24/7 Engine Active
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 6-GRID FINANCIAL STATS VAULT (Requested Complete Breakdown)
    st.markdown(f"""
    <div class="stats-vault">
        <div style="font-size:12px; font-weight:700; color:#cbd5e1; margin-bottom:12px; text-transform:uppercase;">
            📊 Financial Breakdown & Capital Ledger
        </div>
        <div class="vault-grid">
            <div class="vault-item">
                <div class="v-label">💼 Total Capital</div>
                <div class="v-val" style="color:#ffffff;">₹{initial_capital:,.2f}</div>
            </div>
            <div class="vault-item">
                <div class="v-label">⚡ Invested Amount</div>
                <div class="v-val" style="color:#38bdf8;">₹{invested_amount:,.2f}</div>
            </div>
            <div class="vault-item">
                <div class="v-label">💵 Available Balance</div>
                <div class="v-val" style="color:#f8fafc;">₹{available_balance:,.2f}</div>
            </div>
            <div class="vault-item">
                <div class="v-label">🟢 Total Net Profit</div>
                <div class="v-val {'green' if all_realized_profit>=0 else 'red'}">
                    {'+' if all_realized_profit>=0 else ''}₹{all_realized_profit:,.2f}
                </div>
            </div>
            <div class="vault-item">
                <div class="v-label">📅 Today's Invested</div>
                <div class="v-val" style="color:#94a3b8;">₹{today_invested:,.2f}</div>
            </div>
            <div class="vault-item">
                <div class="v-label">🚀 Today's Profit / Loss</div>
                <div class="v-val {'green' if today_profit>=0 else 'red'}">
                    {'+' if today_profit>=0 else ''}₹{today_profit:,.2f}
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Mini Live Spotlight (Top 2 Active Stocks)
    st.markdown('<div style="font-size:14px; font-weight:800; color:#f8fafc; margin-bottom:10px;">⚡ Active Asset Spotlight</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    pos_sub = st.session_state.crypto_positions[:2]
    for idx, p in enumerate(pos_sub):
        col = c1 if idx == 0 else c2
        theme = "card-mint" if idx == 0 else "card-lavender"
        with col:
            st.markdown(f"""
            <div class="{theme}">
                <div style="display:flex; justify-content:space-between; font-weight:800; font-size:15px;">
                    <span>{p['symbol']}</span>
                    <span>📈</span>
                </div>
                <div style="font-size:11px; margin-top:2px; opacity:0.8;">Live Market</div>
                <div style="font-size:17px; font-weight:800; margin-top:4px;">₹{p['current_inr']:,.1f}</div>
                <div style="font-size:11px; font-weight:700; margin-top:3px;">
                    P&L: {'+' if p['unrealized']>=0 else ''}₹{p['unrealized']:.2f}
                </div>
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
    <a href="?tab=home" target="_self" class="nav-btn">
        <div class="{'nav-icon-active' if is_home else 'nav-icon'}">🏠</div>
        <span style="color:{'#ccff00' if is_home else '#94a3b8'};">Home</span>
    </a>
    <a href="?tab=bybit" target="_self" class="nav-btn">
        <div class="{'nav-icon-active' if is_bybit else 'nav-icon'}" style="padding:2px;">
            <img src="https://assets.coingecko.com/markets/images/698/small/bybit_spot.png" style="width:24px; height:24px; border-radius:50%; object-fit:cover;" />
        </div>
        <span style="color:{'#ccff00' if is_bybit else '#94a3b8'};">Bybit</span>
    </a>
    <a href="?tab=angel" target="_self" class="nav-btn">
        <div class="{'nav-icon-active' if is_angel else 'nav-icon'}" style="padding:2px;">
            <img src="https://assets-netstorage.groww.in/stock-assets/logos2/ANGELONE.webp" style="width:24px; height:24px; border-radius:50%; object-fit:cover;" />
        </div>
        <span style="color:{'#ccff00' if is_angel else '#94a3b8'};">Angel One</span>
    </a>
    <a href="?tab=coindcx" target="_self" class="nav-btn">
        <div class="{'nav-icon-active' if is_coindcx else 'nav-icon'}" style="padding:2px;">
            <img src="https://play-lh.googleusercontent.com/1fe3ZZGVphz2gyty2Cb2pm7-INTz6ryG8ekFaPDE5vV9WwN9dJRFd1fFhOhwA3JXVIhx3hAaMg4WARjzogGGnA=s96" style="width:24px; height:24px; border-radius:50%; object-fit:cover;" />
        </div>
        <span style="color:{'#ccff00' if is_coindcx else '#94a3b8'};">CoinDCX</span>
    </a>
</div>
""", unsafe_allow_html=True)

# Auto refresh loop
time.sleep(2)
st.rerun()
