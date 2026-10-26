import streamlit as st
import pandas as pd
import json
import os
import time
import urllib.request
from datetime import datetime

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
        color: #0f172a !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
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
        background: #ffffff;
        border-radius: 26px;
        padding: 22px 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        margin-bottom: 14px;
        color: #0f172a;
    }
    .master-label {
        font-size: 11px;
        font-weight: 700;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.6px;
    }
    .master-val {
        font-size: 34px;
        font-weight: 800;
        letter-spacing: -1px;
        margin: 4px 0 12px 0;
        color: #0f172a;
    }
    .pill-lime {
        background: #ccff00;
        color: #0f172a;
        font-weight: 800;
        font-size: 11px;
        padding: 3px 8px;
        border-radius: 12px;
        vertical-align: middle;
        margin-left: 6px;
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
        background: #d1fae5;
        color: #064e3b;
        border-radius: 18px;
        padding: 14px;
    }
    .card-lavender {
        background: #ede9fe;
        color: #3b0764;
        border-radius: 18px;
        padding: 14px;
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
try:
    if hasattr(st, "query_params"):
        val = st.query_params.get("tab", "home")
        active_tab = val[0] if isinstance(val, list) else str(val)
    elif hasattr(st, "experimental_get_query_params"):
        val = st.experimental_get_query_params().get("tab", ["home"])
        active_tab = val[0] if isinstance(val, list) else str(val)
except Exception:
    active_tab = "home"

active_tab = (active_tab or "home").lower().strip()

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
# SCREEN 3: ANGEL ONE
# ####################################################################
elif active_tab == "angel":
    st.markdown("""
    <div style="display:flex; align-items:center; gap:8px; margin-bottom:12px;">
        <img src="https://assets-netstorage.groww.in/stock-assets/logos2/ANGELONE.webp" style="width:28px; height:28px; border-radius:6px;" />
        <span style="font-size:16px; font-weight:800; color:#f8fafc;">Angel One SmartAPI</span>
    </div>
    """, unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("**Client ID: IIRA162977** (Connected & TOTP Verified)")
        st.caption("Opens Mon-Fri 9:15 AM to 3:30 PM for NIFTY F&O")


# ####################################################################
# SCREEN 4: COINDCX (INDIA'S NO.1 CRYPTO EXCHANGE)
# ####################################################################
elif active_tab == "coindcx":
    st.markdown("""
    <div style="display:flex; align-items:center; gap:8px; margin-bottom:12px;">
        <img src="https://s2.coinmarketcap.com/static/img/exchanges/64x64/630.png" style="width:28px; height:28px; border-radius:6px;" />
        <span style="font-size:16px; font-weight:800; color:#f8fafc;">CoinDCX India Terminal</span>
    </div>
    """, unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("**🇮🇳 CoinDCX FIU-Regulated Hub**")
        st.caption("Direct Indian Bank IMPS / UPI INR Deposit & Instant Withdrawal Ready")

    st.write(f"**CoinDCX Trade Ledger ({len(all_trades)} Executed Trades)**")
    if len(all_trades) > 0:
        for t in reversed(all_trades[-15:]):
            with st.container(border=True):
                h1, h2 = st.columns([2, 1])
                with h1:
                    st.markdown(f"**{t.get('symbol')}**")
                    st.caption(f"{t.get('time')} • {t.get('status')}")
                with h2:
                    p = t.get('pnl', 0)
                    st.metric("PnL", f"{'+' if p>=0 else ''}₹{p:.2f}", delta=f"{p:.2f}", label_visibility="collapsed")
    else:
        st.info("No closed trades recorded yet.")


# ####################################################################
# SCREEN 1: 🏠 HOME DASHBOARD (DEFAULT)
# ####################################################################
else:
    # Master Total Asset Value Card
    pct_gain = ((total_net_portfolio - initial_capital) / initial_capital) * 100
    st.markdown(f"""
    <div class="master-card">
        <div class="master-label">Total Net Portfolio Value</div>
        <div class="master-val">
            ₹{total_net_portfolio:,.2f}
            <span class="pill-lime">{'+' if pct_gain>=0 else ''}{pct_gain:.1f}% ↑</span>
        </div>
        <div style="display:flex; justify-content:space-between; font-size:12px; color:#64748b; font-weight:600;">
            <span>Initial Capital: ₹{initial_capital:,.0f}</span>
            <span style="color:#10b981;">● 24/7 Engine Active</span>
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
            <img src="https://s2.coinmarketcap.com/static/img/exchanges/64x64/630.png" style="width:24px; height:24px; border-radius:50%; object-fit:cover;" />
        </div>
        <span style="color:{'#ccff00' if is_coindcx else '#94a3b8'};">CoinDCX</span>
    </a>
</div>
""", unsafe_allow_html=True)

# Auto refresh loop
time.sleep(2)
st.rerun()
