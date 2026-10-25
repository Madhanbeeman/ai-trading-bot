import streamlit as st
import pandas as pd
import json
import os
import time
import urllib.request
from datetime import datetime

# ==========================================
# 100% NATIVE MOBILE APP CONFIG
# ==========================================
st.set_page_config(
    page_title="Scalper Pro Mobile",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Dark Theme CSS (Zero HTML code inside body!)
st.markdown("""
<style>
    .stApp {
        background-color: #030712 !important;
        color: #f9fafb !important;
    }
    .block-container {
        padding: 0.8rem !important;
        max-width: 480px !important;
        margin: auto !important;
    }
    /* Native container borders */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #111827 !important;
        border: 1px solid #1f2937 !important;
        border-radius: 16px !important;
        padding: 12px !important;
        margin-bottom: 10px !important;
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

# Session State
if "futures_positions" not in st.session_state:
    st.session_state.futures_positions = []
if "zero_hero_positions" not in st.session_state:
    st.session_state.zero_hero_positions = []

# ==========================================
# LIVE CRYPTO SPOT FEED (COINBASE)
# ==========================================
FUTURES_SYMBOLS = ["BTC", "ETH", "SOL", "DOGE", "XRP"]
INR_RATE = 87.5

@st.cache_data(ttl=2)
def fetch_crypto_prices():
    prices = {}
    for sym in FUTURES_SYMBOLS:
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

# ==========================================
# 1. CRYPTO 10X SCALPING ENGINE
# ==========================================
def manage_crypto_futures():
    active = [p["symbol"] for p in st.session_state.futures_positions]
    available = [s for s in FUTURES_SYMBOLS if s not in active and s in live_prices]
    used = sum(p["margin_inr"] for p in st.session_state.futures_positions)
    free = max(0.0, current_cash - used)

    for sym in available:
        if free < 5000:
            break
        p_data = live_prices[sym]
        inr_p = p_data["inr"]
        if inr_p <= 0:
            continue

        margin = 5000.0
        leverage = 10
        qty = round((margin * leverage) / inr_p, 4)
        side = "LONG" if sym in ["BTC", "SOL", "ETH"] else "SHORT"

        # Super Quick Scalp Target (+0.4%) & Tight SL (-0.3%)
        target_pct = 0.004 if side == "LONG" else -0.004
        sl_pct = -0.003 if side == "LONG" else 0.003

        st.session_state.futures_positions.append({
            "symbol": sym,
            "side": side,
            "entry_inr": inr_p,
            "current_inr": inr_p,
            "margin_inr": margin,
            "qty": qty,
            "target_inr": round(inr_p * (1 + target_pct), 2),
            "sl_inr": round(inr_p * (1 + sl_pct), 2),
            "unrealized": 0.0,
            "time": datetime.now().strftime("%H:%M")
        })
        free -= margin

manage_crypto_futures()

# Evaluate Crypto Positions
rem_fut = []
for p in st.session_state.futures_positions:
    sym = p["symbol"]
    if sym in live_prices:
        cur_inr = live_prices[sym]["inr"]
        p["current_inr"] = cur_inr
        side = p["side"]

        diff = (cur_inr - p["entry_inr"]) if side == "LONG" else (p["entry_inr"] - cur_inr)
        unreal = round((diff / p["entry_inr"]) * p["margin_inr"] * 10, 2)
        p["unrealized"] = unreal

        hit_target = (cur_inr >= p["target_inr"]) if side == "LONG" else (cur_inr <= p["target_inr"])
        hit_sl = (cur_inr <= p["sl_inr"]) if side == "LONG" else (cur_inr >= p["sl_inr"])

        if hit_target:
            save_trade({
                "date": today_str,
                "time": datetime.now().strftime("%H:%M:%S"),
                "engine": "CRYPTO 10X",
                "symbol": f"{p['symbol']} {p['side']}",
                "pnl": unreal,
                "status": "🎯 TARGET HIT"
            })
            st.toast(f"🎯 Target Hit! {p['symbol']} +₹{unreal}", icon="🚀")
        elif hit_sl:
            save_trade({
                "date": today_str,
                "time": datetime.now().strftime("%H:%M:%S"),
                "engine": "CRYPTO 10X",
                "symbol": f"{p['symbol']} {p['side']}",
                "pnl": unreal,
                "status": "🛡️ SL CUT"
            })
            st.toast(f"🛡️ SL Cut! {p['symbol']} ₹{unreal}", icon="⚠️")
        else:
            rem_fut.append(p)
    else:
        rem_fut.append(p)

st.session_state.futures_positions = rem_fut
manage_crypto_futures()

# ==========================================
# 2. NIFTY ZERO-HERO OPTIONS ENGINE
# ==========================================
def manage_zero_hero():
    if len(st.session_state.zero_hero_positions) == 0:
        st.session_state.zero_hero_positions.append({
            "symbol": "NIFTY 24600 CE",
            "entry": 18.0,
            "current": 18.0,
            "qty": 65,
            "target": 45.0,
            "sl": 9.0,
            "unrealized": 0.0,
            "time": datetime.now().strftime("%H:%M")
        })

manage_zero_hero()

# Total Active P&L
fut_unreal = sum(p.get("unrealized", 0.0) for p in st.session_state.futures_positions)
zh_unreal = sum(p.get("unrealized", 0.0) for p in st.session_state.zero_hero_positions)
total_active_unreal = fut_unreal + zh_unreal

# ==========================================
# 📱 TOP PORTFOLIO BANNER (PURE NATIVE)
# ==========================================
with st.container(border=True):
    col_t1, col_t2 = st.columns([2, 1])
    with col_t1:
        st.caption("TOTAL REALIZED PROFIT (மொத்த லாபம்)")
        profit_delta = f"Live P&L: {'+' if total_active_unreal>=0 else ''}₹{total_active_unreal:.2f}"
        st.metric(
            label="Total Profit",
            value=f"{'+' if all_realized_pnl>=0 else ''}₹{all_realized_pnl:,.2f}",
            delta=profit_delta,
            label_visibility="collapsed"
        )
    with col_t2:
        st.caption("BALANCE")
        st.markdown(f"**₹{(current_cash + total_active_unreal):,.0f}**")
        st.caption("🟢 24/7 AUTO")

# ==========================================
# 🔀 NATIVE SEGMENT SWITCHER
# ==========================================
tab_choice = st.radio(
    "Navigation",
    ["🚀 Crypto 10x Scalping", "⚡ Nifty Zero-Hero", "📜 Trade Ledger"],
    horizontal=True,
    label_visibility="collapsed"
)

# ####################################################################
# SCREEN 1: 🚀 CRYPTO FUTURES 10X SCALPING (PURE NATIVE CARDS)
# ####################################################################
if tab_choice == "🚀 Crypto 10x Scalping":
    st.write(f"**⚡ Live Scalping Slots ({len(st.session_state.futures_positions)})**")

    for p in st.session_state.futures_positions:
        with st.container(border=True):
            # Card Top Header
            ch1, ch2 = st.columns([2, 1])
            with ch1:
                st.subheader(f"{p['symbol']} / USDT")
            with ch2:
                side_label = f"🟢 {p['side']} 10x" if p['side'] == "LONG" else f"🔴 {p['side']} 10x"
                st.markdown(f"**{side_label}**")

            # Big Live PnL
            pnl_val = p['unrealized']
            st.metric(
                label="Unrealized P&L",
                value=f"{'+' if pnl_val>=0 else ''}₹{pnl_val:.2f}",
                delta=f"{'+' if pnl_val>=0 else ''}{pnl_val:.2f}",
                label_visibility="collapsed"
            )

            # 4-Box Clean Grid
            g1, g2 = st.columns(2)
            with g1:
                st.caption("வாங்கிய விலை (Entry)")
                st.markdown(f"**₹{p['entry_inr']:,.1f}**")
                st.caption("🎯 Target (விற்பனை)")
                st.markdown(f"<span style='color:#10b981; font-weight:700;'>₹{p['target_inr']:,.1f}</span>", unsafe_allow_html=True)
            with g2:
                st.caption("சந்தை விலை (Live)")
                st.markdown(f"**₹{p['current_inr']:,.1f}**")
                st.caption("🛡️ Stop Loss (பாதுகாப்பு)")
                st.markdown(f"<span style='color:#ef4444; font-weight:700;'>₹{p['sl_inr']:,.1f}</span>", unsafe_allow_html=True)


# ####################################################################
# SCREEN 2: ⚡ NIFTY ZERO-HERO OPTIONS
# ####################################################################
elif tab_choice == "⚡ Nifty Zero-Hero":
    st.write("**⚡ NIFTY Zero-Hero Options (Angel One)**")
    st.caption("முதலீடு: ~₹1,170 | Target லாபம்: +₹1,755 (2.5x Hero)")

    for p in st.session_state.zero_hero_positions:
        with st.container(border=True):
            st.subheader(p['symbol'])
            st.caption("1 LOT = 65 QTY")

            pnl = p['unrealized']
            st.metric(
                label="Zero-Hero P&L",
                value=f"{'+' if pnl>=0 else ''}₹{pnl:.2f}",
                delta=f"{pnl:.2f}",
                label_visibility="collapsed"
            )

            zg1, zg2 = st.columns(2)
            with zg1:
                st.caption("வாங்கிய பிரீமியம்")
                st.markdown(f"**₹{p['entry']}**")
                st.caption("🎯 Hero Target")
                st.markdown(f"<span style='color:#a855f7; font-weight:700;'>₹{p['target']} (2.5x)</span>", unsafe_allow_html=True)
            with zg2:
                st.caption("சந்தை பிரீமியம்")
                st.markdown(f"**₹{p['current']}**")
                st.caption("🛡️ Zero Stop-Loss")
                st.markdown(f"<span style='color:#ef4444; font-weight:700;'>₹{p['sl']}</span>", unsafe_allow_html=True)


# ####################################################################
# SCREEN 3: 📜 HISTORY / LEDGER
# ####################################################################
else:
    st.write(f"**Trade Ledger ({len(all_trades)} Executed Trades)**")
    if len(all_trades) > 0:
        for t in reversed(all_trades[-15:]):
            pnl = t.get("pnl", 0)
            with st.container(border=True):
                h1, h2 = st.columns([2, 1])
                with h1:
                    st.markdown(f"**{t.get('symbol')}**")
                    st.caption(f"{t.get('engine', 'TRADE')} • {t.get('status')} • {t.get('time')}")
                with h2:
                    st.metric(
                        label="PnL",
                        value=f"{'+' if pnl>=0 else ''}₹{pnl:.2f}",
                        delta=f"{pnl:.2f}",
                        label_visibility="collapsed"
                    )
    else:
        st.info("No closed trades recorded yet.")

# Auto-refresh loop
time.sleep(2)
st.rerun()
