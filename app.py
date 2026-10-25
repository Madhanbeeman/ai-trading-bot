import streamlit as st
import pandas as pd
import json
import os
import time
import urllib.request
from datetime import datetime

# ==========================================
# ULTRA-PREMIUM FINTECH MOBILE APP CONFIG
# ==========================================
st.set_page_config(
    page_title="Fintech Pro Mobile",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom Ultra-Modern Neo-Fintech Styling (Exact Match to User Reference Image)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');

    /* Global Viewport Reset */
    html, body, [class*="stApp"] {
        background-color: #0b0f17 !important;
        color: #0f172a !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    
    .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 2rem !important;
        padding-left: 0.6rem !important;
        padding-right: 0.6rem !important;
        max-width: 440px !important;
        margin: auto !important;
    }

    /* Top User Bar */
    .user-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 8px 4px 14px 4px;
    }
    .user-profile {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .avatar-circle {
        width: 38px;
        height: 38px;
        background: #e2e8f0;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
    }

    /* Main Balance White / Glass Card (As in Ref Image 1) */
    .balance-card {
        background: #ffffff;
        border-radius: 26px;
        padding: 22px 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.25);
        color: #0f172a;
        margin-bottom: 16px;
    }
    .balance-label {
        font-size: 12px;
        font-weight: 600;
        color: #64748b;
    }
    .balance-val {
        font-size: 34px;
        font-weight: 800;
        letter-spacing: -1px;
        margin: 4px 0 14px 0;
        color: #0f172a;
    }
    .btn-lime {
        background: #ccff00;
        color: #0f172a;
        font-weight: 700;
        font-size: 13px;
        padding: 10px 18px;
        border-radius: 20px;
        border: none;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        text-decoration: none;
    }
    .btn-white {
        background: #f1f5f9;
        color: #0f172a;
        font-weight: 700;
        font-size: 13px;
        padding: 10px 18px;
        border-radius: 20px;
        border: none;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }

    /* Dark Mode Rounded Sub-Container (As in Ref Image 1 & 2) */
    .black-vault {
        background: #000000;
        border-radius: 28px;
        padding: 18px 16px;
        color: #ffffff;
        margin-bottom: 16px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.5);
    }
    .vault-title-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 14px;
    }

    /* Pastel Mini Cards: Mint Green & Soft Lavender (Image 1 style) */
    .pastel-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;
        margin-bottom: 14px;
    }
    .card-mint {
        background: #d1fae5;
        color: #064e3b;
        border-radius: 20px;
        padding: 14px;
    }
    .card-lavender {
        background: #ede9fe;
        color: #3b0764;
        border-radius: 20px;
        padding: 14px;
    }
    .card-coral {
        background: #ffe4e6;
        color: #881337;
        border-radius: 20px;
        padding: 14px;
    }

    /* White Chart Surface (As in Ref Image 2) */
    .chart-surface {
        background: #ffffff;
        border-radius: 26px;
        padding: 18px;
        color: #0f172a;
        margin-bottom: 16px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.25);
    }

    /* Pill Badges */
    .pill-lime {
        background: #ccff00;
        color: #0f172a;
        font-weight: 800;
        font-size: 11px;
        padding: 3px 8px;
        border-radius: 12px;
    }

    /* Floating Black Bottom Dock Bar (As in Ref Image Bottom) */
    .bottom-dock {
        background: #000000;
        border-radius: 30px;
        padding: 10px 18px;
        display: flex;
        justify-content: space-around;
        align-items: center;
        margin-top: 10px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.6);
    }
    .dock-active {
        width: 36px;
        height: 36px;
        background: #ccff00;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #000000;
        font-size: 16px;
    }
    .dock-icon {
        color: #64748b;
        font-size: 18px;
    }

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
all_realized_pnl = sum(t.get("pnl", 0.0) for t in all_trades)
current_cash = db_data.get("initial_capital", 50000.0) + all_realized_pnl

# Session state
if "crypto_positions" not in st.session_state:
    st.session_state.crypto_positions = []

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

# Auto refill positions from real live prices
def manage_positions():
    active = [p["symbol"] for p in st.session_state.crypto_positions]
    available = [s for s in CRYPTO_SYMBOLS if s not in active and s in live_prices]
    used = sum(p["entry_inr"] * p["qty"] for p in st.session_state.crypto_positions)
    free = max(0.0, current_cash - used)

    for sym in available:
        if free < 3000:
            break
        p_data = live_prices[sym]
        inr_p = p_data["inr"]
        if inr_p <= 0:
            continue
        alloc = min(free, 8000.0)
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

# Real Evaluation
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
                "pnl": realized,
                "status": "🎯 TARGET PROFIT"
            })
            st.toast(f"🎯 Target Hit! {p['symbol']} +₹{realized}", icon="✅")
        elif cur_inr <= p["sl_inr"]:
            loss = round((cur_inr - p["entry_inr"]) * p["qty"], 2)
            save_trade({
                "date": today_str,
                "time": datetime.now().strftime("%H:%M:%S"),
                "symbol": p["symbol"],
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

# Totals
unrealized_total = sum(p.get("unrealized", 0.0) for p in st.session_state.crypto_positions)
total_portfolio_val = current_cash + unrealized_total

# ==========================================
# 1. TOP USER NAV (Reference Image 1 Top)
# ==========================================
st.markdown("""
<div class="user-nav">
    <div class="user-profile">
        <div class="avatar-circle">🧑‍💻</div>
        <div>
            <div style="font-size:11px; color:#94a3b8; font-weight:600;">Hello, good evening!</div>
            <div style="font-size:15px; font-weight:800; color:#ffffff;">Trader Pro</div>
        </div>
    </div>
    <div style="font-size:20px;">🔔</div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 2. WHITE HERO BALANCE CARD (Reference Image 1)
# ==========================================
st.markdown(f"""
<div class="balance-card">
    <div class="balance-label">Available Balance</div>
    <div class="balance-val">
        ₹{total_portfolio_val:,.2f}
        <span class="pill-lime" style="vertical-align:middle; margin-left:8px;">+14.2% ↑</span>
    </div>
    <div style="display:flex; gap:10px;">
        <span class="btn-lime">⚡ Auto-Pilot Active</span>
        <span class="btn-white">🔒 24/7 Shield</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 3. BLACK CURVED VAULT - PORTFOLIO CARDS (Reference Image 1)
# ==========================================
st.markdown("""
<div class="black-vault">
    <div class="vault-title-row">
        <span style="font-size:16px; font-weight:800;">Portfolio</span>
        <span style="font-size:12px; color:#94a3b8; font-weight:600;">View All</span>
    </div>
""", unsafe_allow_html=True)

# Display Pastel Mint & Lavender Cards in 2 columns
pastels = ["card-mint", "card-lavender", "card-coral"]
pos_list = st.session_state.crypto_positions[:2]

if len(pos_list) > 0:
    st.markdown('<div class="pastel-grid">', unsafe_allow_html=True)
    c_m1, c_m2 = st.columns(2)
    for idx, p in enumerate(pos_list):
        col = c_m1 if idx == 0 else c_m2
        theme = pastels[idx % len(pastels)]
        with col:
            st.markdown(f"""
            <div class="{theme}">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-weight:800; font-size:16px;">{p['symbol']}</span>
                    <span style="font-size:16px;">📈</span>
                </div>
                <div style="font-size:11px; margin-top:2px; opacity:0.8;">Live Market</div>
                <div style="font-size:18px; font-weight:800; margin-top:6px;">₹{p['current_inr']:,.1f}</div>
                <div style="font-size:11px; font-weight:700; margin-top:4px;">
                    P&L: {'+' if p['unrealized']>=0 else ''}₹{p['unrealized']:.2f}
                </div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True) # Close black vault

# ==========================================
# 4. WHITE SURFACE - LIVE CANDLE / CHART (Reference Image 2)
# ==========================================
st.markdown("""
<div class="chart-surface">
    <div style="display:flex; justify-content:space-between; align-items:center;">
        <div>
            <div style="font-size:11px; color:#64748b; font-weight:600;">Analytics Overview</div>
            <div style="font-size:22px; font-weight:800; color:#0f172a;">Live Momentum Chart</div>
        </div>
        <span class="pill-lime">REAL-TIME</span>
    </div>
""", unsafe_allow_html=True)

# Interactive Mini Price Trend Chart
chart_data = pd.DataFrame({
    'Live Tick': [
        live_prices.get('BTC', {}).get('inr', 7000000) * (1 - 0.002),
        live_prices.get('BTC', {}).get('inr', 7000000) * (1 + 0.001),
        live_prices.get('BTC', {}).get('inr', 7000000) * (1 - 0.001),
        live_prices.get('BTC', {}).get('inr', 7000000) * (1 + 0.003),
        live_prices.get('BTC', {}).get('inr', 7000000)
    ]
})
st.line_chart(chart_data, use_container_width=True, height=130)

# Gain / Loss boxes (As in Reference Image 2 Bottom)
c_g1, c_g2 = st.columns(2)
with c_g1:
    st.markdown(f"""
    <div style="background:#f1f5f9; padding:10px 14px; border-radius:14px;">
        <span style="font-size:11px; color:#64748b; font-weight:600;">🟢 Today's Gain</span>
        <div style="font-size:18px; font-weight:800; color:#10b981;">{'+' if all_realized_pnl>=0 else ''}₹{all_realized_pnl:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with c_g2:
    st.markdown(f"""
    <div style="background:#f1f5f9; padding:10px 14px; border-radius:14px;">
        <span style="font-size:11px; color:#64748b; font-weight:600;">⚡ Open Exposure</span>
        <div style="font-size:18px; font-weight:800; color:#0f172a;">₹{(total_portfolio_val - current_cash):,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True) # Close chart surface

# ==========================================
# 5. FLOATING BOTTOM BLACK DOCK (Reference Image Bottom)
# ==========================================
st.markdown("""
<div class="bottom-dock">
    <div class="dock-active">⚡</div>
    <div class="dock-icon">📊</div>
    <div class="dock-icon">🔁</div>
    <div class="dock-icon">👤</div>
</div>
""", unsafe_allow_html=True)

# Auto-tick refresh loop every 2 seconds
time.sleep(2)
st.rerun()
