import streamlit as st
import pandas as pd
import json
import os
import time
import urllib.request
from datetime import datetime

# ==========================================
# 100% PURE PITCH-BLACK OLED MOBILE APP CONFIG
# ==========================================
st.set_page_config(
    page_title="Scalper Pro Mobile",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom Ultra-Clean OLED Dark Theme CSS
st.markdown("""
<style>
    /* Full Black Background */
    html, body, [class*="stApp"] {
        background-color: #030712 !important;
        color: #f9fafb !important;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", Roboto, sans-serif !important;
    }
    
    .block-container {
        padding: 0.8rem !important;
        max-width: 450px !important;
        margin: auto !important;
    }

    /* Top Portfolio Banner */
    .top-hero {
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 18px;
        padding: 18px;
        margin-bottom: 14px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.6);
    }
    .hero-label {
        font-size: 11px;
        color: #9ca3af;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 0.8px;
    }
    .hero-profit {
        font-size: 32px;
        font-weight: 900;
        margin: 6px 0;
        letter-spacing: -0.5px;
    }
    .hero-sub-bar {
        display: flex;
        justify-content: space-around;
        background: #0b0f19;
        padding: 8px 12px;
        border-radius: 10px;
        margin-top: 10px;
        font-size: 12px;
        font-weight: 600;
    }

    /* Simple Clean Trading Card */
    .trade-card {
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 16px;
        padding: 14px;
        margin-bottom: 12px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.4);
    }
    .trade-card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 6px;
    }
    .asset-name {
        font-size: 16px;
        font-weight: 800;
        color: #ffffff;
    }
    .pnl-live {
        font-size: 24px;
        font-weight: 900;
        margin: 6px 0;
    }
    .pill-badge {
        font-size: 10px;
        font-weight: 800;
        padding: 3px 8px;
        border-radius: 6px;
    }

    /* 4-Box Clear Metrics */
    .metric-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 8px;
        margin-top: 10px;
        background: #030712;
        padding: 10px;
        border-radius: 12px;
    }
    .metric-box {
        font-size: 11px;
        color: #9ca3af;
        line-height: 1.4;
    }
    .metric-val {
        font-size: 13px;
        font-weight: 800;
        color: #f3f4f6;
        display: block;
        margin-top: 2px;
        font-family: monospace;
    }

    /* Colors */
    .green { color: #10b981 !important; }
    .red { color: #ef4444 !important; }
    .purple { color: #a855f7 !important; }
    .gold { color: #f59e0b !important; }

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
# 1. CRYPTO FUTURES 10X SCALPING ENGINE
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

        leverage = 10
        margin = 5000.0
        position_size = margin * leverage
        qty = round(position_size / inr_p, 4)

        side = "LONG" if sym in ["BTC", "SOL", "ETH"] else "SHORT"
        target_pct = 0.015 if side == "LONG" else -0.015
        sl_pct = -0.008 if side == "LONG" else 0.008

        target_inr = round(inr_p * (1 + target_pct), 2)
        sl_inr = round(inr_p * (1 + sl_pct), 2)

        st.session_state.futures_positions.append({
            "symbol": sym,
            "side": side,
            "entry_inr": inr_p,
            "current_inr": inr_p,
            "margin_inr": margin,
            "qty": qty,
            "target_inr": target_inr,
            "sl_inr": sl_inr,
            "unrealized": 0.0,
            "time": datetime.now().strftime("%H:%M")
        })
        free -= margin

manage_crypto_futures()

# Evaluate Crypto Futures Live
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
                "status": "🎯 TARGET HIT (+15%)"
            })
            st.toast(f"🎯 Target on {p['symbol']} {p['side']}! +₹{unreal}", icon="🚀")
        elif hit_sl:
            save_trade({
                "date": today_str,
                "time": datetime.now().strftime("%H:%M:%S"),
                "engine": "CRYPTO 10X",
                "symbol": f"{p['symbol']} {p['side']}",
                "pnl": unreal,
                "status": "🛡️ SL CUT (-8%)"
            })
            st.toast(f"🛡️ SL on {p['symbol']} {p['side']}! ₹{unreal}", icon="⚠️")
        else:
            rem_fut.append(p)
    else:
        rem_fut.append(p)

st.session_state.futures_positions = rem_fut
manage_crypto_futures()

# ==========================================
# 2. NIFTY ZERO-HERO OPTIONS SCALPER
# ==========================================
def manage_zero_hero():
    if len(st.session_state.zero_hero_positions) == 0:
        entry_premium = 18.0
        lot_size = 65
        st.session_state.zero_hero_positions.append({
            "symbol": "NIFTY 24600 CE",
            "entry": entry_premium,
            "current": entry_premium,
            "qty": lot_size,
            "target": 45.0, # 2.5x Hero Target
            "sl": 9.0,     # Stop loss
            "unrealized": 0.0,
            "time": datetime.now().strftime("%H:%M")
        })

manage_zero_hero()

# Evaluate Zero-Hero
rem_zh = []
for p in st.session_state.zero_hero_positions:
    cur = p["current"]
    unreal = round((cur - p["entry"]) * p["qty"], 2)
    p["unrealized"] = unreal

    if cur >= p["target"]:
        save_trade({
            "date": today_str,
            "time": datetime.now().strftime("%H:%M:%S"),
            "engine": "NIFTY ZERO-HERO",
            "symbol": p["symbol"],
            "pnl": unreal,
            "status": "🚀 2.5X HERO HIT (+₹1,755)"
        })
        st.toast(f"🚀 Zero-Hero Target! +₹{unreal}", icon="🎉")
    elif cur <= p["sl"]:
        save_trade({
            "date": today_str,
            "time": datetime.now().strftime("%H:%M:%S"),
            "engine": "NIFTY ZERO-HERO",
            "symbol": p["symbol"],
            "pnl": unreal,
            "status": "🛡️ ZERO SL CUT"
        })
        st.toast(f"🛡️ Zero-Hero Cut! ₹{unreal}", icon="⚠️")
    else:
        rem_zh.append(p)

st.session_state.zero_hero_positions = rem_zh

# Total Active P&L
fut_unreal = sum(p.get("unrealized", 0.0) for p in st.session_state.futures_positions)
zh_unreal = sum(p.get("unrealized", 0.0) for p in st.session_state.zero_hero_positions)
total_active_unreal = fut_unreal + zh_unreal

# ==========================================
# 📱 TOP PORTFOLIO HERO BANNER
# ==========================================
st.markdown(f"""
<div class="top-hero">
    <div class="hero-label">Total Realized Profit (மொத்த லாபம்)</div>
    <div class="hero-profit {'green' if all_realized_pnl>=0 else 'red'}">
        {'+' if all_realized_pnl>=0 else ''}₹{all_realized_pnl:,.2f}
    </div>
    <div class="hero-sub-bar">
        <span>Active Live P&L: <strong class="{'green' if total_active_unreal>=0 else 'red'}">{'+' if total_active_unreal>=0 else ''}₹{total_active_unreal:.2f}</strong></span>
        <span>Balance: <strong>₹{(current_cash + total_active_unreal):,.0f}</strong></span>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 🔀 BIG THUMB-FRIENDLY SEGMENT SWITCHER
# ==========================================
tab_choice = st.radio(
    "Nav",
    ["🚀 Crypto 10x Scalping", "⚡ Nifty Zero-Hero", "📜 Trade Ledger"],
    horizontal=True,
    label_visibility="collapsed"
)

# ####################################################################
# SCREEN 1: 🚀 CRYPTO FUTURES 10X SCALPING
# ####################################################################
if tab_choice == "🚀 Crypto 10x Scalping":
    st.write(f"**⚡ Live 10x Scalping Trades ({len(st.session_state.futures_positions)})**")

    for p in st.session_state.futures_positions:
        pnl = p["unrealized"]
        side_color = "#10b981" if p["side"]=="LONG" else "#ef4444"
        side_bg = "rgba(16, 185, 129, 0.2)" if p["side"]=="LONG" else "rgba(239, 68, 68, 0.2)"
        
        st.markdown(f"""
        <div class="trade-card" style="border-left: 5px solid {side_color};">
            <div class="trade-card-header">
                <div>
                    <span class="asset-name">{p['symbol']}</span>
                    <span style="font-size:12px; color:#9ca3af; margin-left:4px;">USDT</span>
                </div>
                <span class="pill-badge" style="background:{side_bg}; color:{side_color};">{p['side']} 10X</span>
            </div>
            
            <div class="pnl-live {'green' if pnl>=0 else 'red'}">
                {'+' if pnl>=0 else ''}₹{pnl:.2f}
            </div>

            <div class="metric-grid">
                <div class="metric-box">
                    வாங்கிய விலை (Entry)
                    <span class="metric-val">₹{p['entry_inr']:,.1f}</span>
                </div>
                <div class="metric-box">
                    சந்தை விலை (Live)
                    <span class="metric-val">₹{p['current_inr']:,.1f}</span>
                </div>
                <div class="metric-box">
                    🎯 Target (விற்பனை)
                    <span class="metric-val green">₹{p['target_inr']:,.1f} (+15%)</span>
                </div>
                <div class="metric-box">
                    🛡️ Stop Loss (பாதுகாப்பு)
                    <span class="metric-val red">₹{p['sl_inr']:,.1f} (-8%)</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ####################################################################
# SCREEN 2: ⚡ NIFTY ZERO-HERO OPTIONS
# ####################################################################
elif tab_choice == "⚡ Nifty Zero-Hero":
    st.write("**⚡ NIFTY Zero-Hero Options (Angel One)**")
    st.caption("முதலீடு வெறும் ₹1,170 | Target லாபம்: +₹1,755 (2.5x Multiplier)")

    for p in st.session_state.zero_hero_positions:
        pnl = p["unrealized"]
        st.markdown(f"""
        <div class="trade-card" style="border: 1px solid #7c3aed; border-left: 5px solid #a855f7;">
            <div class="trade-card-header">
                <span class="asset-name" style="color:#c084fc;">{p['symbol']}</span>
                <span class="pill-badge" style="background:rgba(168, 85, 247, 0.2); color:#c084fc;">1 LOT (65 QTY)</span>
            </div>
            
            <div class="pnl-live {'green' if pnl>=0 else 'red'}">
                {'+' if pnl>=0 else ''}₹{pnl:.2f}
            </div>

            <div class="metric-grid">
                <div class="metric-box">
                    வாங்கிய பிரீமியம்
                    <span class="metric-val">₹{p['entry']}</span>
                </div>
                <div class="metric-box">
                    தற்போதைய பிரீமியம்
                    <span class="metric-val">₹{p['current']}</span>
                </div>
                <div class="metric-box">
                    🎯 Hero Target
                    <span class="metric-val purple">₹{p['target']} (2.5x)</span>
                </div>
                <div class="metric-box">
                    🛡️ Zero Stop-Loss
                    <span class="metric-val red">₹{p['sl']}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ####################################################################
# SCREEN 3: 📜 HISTORY / LEDGER
# ####################################################################
else:
    st.write(f"**Trade Ledger ({len(all_trades)} Executed Trades)**")
    if len(all_trades) > 0:
        for t in reversed(all_trades[-15:]):
            pnl = t.get("pnl", 0)
            engine = t.get("engine", "TRADE")
            st.markdown(f"""
            <div class="trade-card" style="padding:10px 14px; border-left: 4px solid {'#10b981' if pnl>=0 else '#ef4444'};">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-weight:800; font-size:15px;">{t.get('symbol')}</span>
                    <span class="{'green' if pnl>=0 else 'red'}" style="font-weight:900; font-size:16px;">
                        {'+' if pnl>=0 else ''}₹{pnl:.2f}
                    </span>
                </div>
                <div style="display:flex; justify-content:space-between; font-size:11px; color:#9ca3af; margin-top:4px; font-family:monospace;">
                    <span>{engine} • {t.get('status')}</span>
                    <span>{t.get('time')}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No closed trades recorded yet.")

# Auto-refresh loop
time.sleep(2)
st.rerun()
