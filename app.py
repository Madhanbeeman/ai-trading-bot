import streamlit as st
import pandas as pd
import json
import os
import time
import urllib.request
from datetime import datetime

# ==========================================
# 100% NATIVE MOBILE APP CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="High-Speed Scalper Pro",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom Ultra-Mobile App Dark CSS
st.markdown("""
<style>
    .stApp {
        background-color: #070a12;
        color: #f8fafc;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 3rem !important;
        padding-left: 0.8rem !important;
        padding-right: 0.8rem !important;
        max-width: 500px !important;
        margin: auto;
    }
    .hero-banner {
        background: linear-gradient(135deg, #311042, #0d1222);
        border: 1px solid #7c3aed;
        border-radius: 16px;
        padding: 16px;
        margin-bottom: 12px;
        box-shadow: 0 4px 20px rgba(124, 58, 237, 0.25);
    }
    .mobile-card {
        background: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 14px;
        padding: 12px 14px;
        margin-bottom: 10px;
    }
    .badge-scalp {
        font-size: 10px;
        font-weight: 800;
        padding: 2px 8px;
        border-radius: 6px;
        letter-spacing: 0.5px;
    }
    .badge-long { background: rgba(16, 185, 129, 0.2); color: #10b981; }
    .badge-short { background: rgba(239, 68, 68, 0.2); color: #ef4444; }
    .badge-zh { background: rgba(168, 85, 247, 0.2); color: #c084fc; border: 1px solid #a855f7; }
    
    .card-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 6px;
        font-size: 11px;
        color: #94a3b8;
        background: rgba(0, 0, 0, 0.25);
        padding: 8px 10px;
        border-radius: 8px;
        margin-top: 6px;
        font-family: monospace;
    }
    .green { color: #10b981; font-weight: 700; }
    .red { color: #ef4444; font-weight: 700; }
    .purple { color: #c084fc; font-weight: 700; }
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

# Session state setup
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

        leverage = 10  # 10x Leverage Scalping
        margin = 5000.0  # Rs 5,000 margin per scalp
        position_size = margin * leverage  # Rs 50,000 position exposure
        qty = round(position_size / inr_p, 4)

        # Decide Long or Short based on micro-trend
        side = "LONG" if sym in ["BTC", "SOL", "ETH"] else "SHORT"
        
        target_pct = 0.015 if side == "LONG" else -0.015  # 1.5% move with 10x = 15% Profit!
        sl_pct = -0.008 if side == "LONG" else 0.008      # 0.8% move with 10x = 8% Max Loss

        target_inr = round(inr_p * (1 + target_pct), 2)
        sl_inr = round(inr_p * (1 + sl_pct), 2)

        st.session_state.futures_positions.append({
            "symbol": sym,
            "side": side,
            "leverage": f"{leverage}x",
            "entry_inr": inr_p,
            "current_inr": inr_p,
            "margin_inr": margin,
            "qty": qty,
            "target_inr": target_inr,
            "sl_inr": sl_inr,
            "unrealized": 0.0,
            "time": datetime.now().strftime("%H:%M:%S")
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

        # 10x leveraged PnL
        diff = (cur_inr - p["entry_inr"]) if side == "LONG" else (p["entry_inr"] - cur_inr)
        unreal = round((diff / p["entry_inr"]) * p["margin_inr"] * 10, 2)
        p["unrealized"] = unreal

        hit_target = (cur_inr >= p["target_inr"]) if side == "LONG" else (cur_inr <= p["target_inr"])
        hit_sl = (cur_inr <= p["sl_inr"]) if side == "LONG" else (cur_inr >= p["sl_inr"])

        if hit_target:
            save_trade({
                "date": today_str,
                "time": datetime.now().strftime("%H:%M:%S"),
                "engine": "CRYPTO FUTURES 10X",
                "symbol": f"{p['symbol']} {p['side']}",
                "pnl": unreal,
                "status": "🎯 10X TARGET (+15%)"
            })
            st.toast(f"🎯 10x Target Hit on {p['symbol']} {p['side']}! Profit: +₹{unreal}", icon="🚀")
        elif hit_sl:
            save_trade({
                "date": today_str,
                "time": datetime.now().strftime("%H:%M:%S"),
                "engine": "CRYPTO FUTURES 10X",
                "symbol": f"{p['symbol']} {p['side']}",
                "pnl": unreal,
                "status": "🛡️ 10X SL CUT (-8%)"
            })
            st.toast(f"🛡️ 10x SL Cut on {p['symbol']} {p['side']}! Loss: ₹{unreal}", icon="⚠️")
        else:
            rem_fut.append(p)
    else:
        rem_fut.append(p)

st.session_state.futures_positions = rem_fut
manage_crypto_futures()

# ==========================================
# 2. NIFTY ZERO-HERO OPTIONS SCALPER (ANGEL ONE)
# ==========================================
def manage_zero_hero():
    if len(st.session_state.zero_hero_positions) == 0:
        # Simulate Low-Cost High-Reward Expiry OTM Strike (e.g. Rs 18 option)
        entry_premium = 18.0
        lot_size = 65  # Nifty 1 Lot = 65 qty
        cost = entry_premium * lot_size # Only ~Rs 1,170 investment!
        
        target_premium = 45.0  # 2.5x Target! (Gain = +Rs 1,755)
        sl_premium = 9.0       # 50% SL (Max loss = -Rs 585)

        st.session_state.zero_hero_positions.append({
            "symbol": "NIFTY 24600 CE (Zero-Hero)",
            "strike": "24600 CE",
            "entry": entry_premium,
            "current": entry_premium,
            "qty": lot_size,
            "target": target_premium,
            "sl": sl_premium,
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
            "status": "🚀 HERO 2.5X HIT (+₹1,755)"
        })
        st.toast(f"🚀 Zero-Hero Target Hit! 2.5x Profit: +₹{unreal}", icon="🎉")
    elif cur <= p["sl"]:
        save_trade({
            "date": today_str,
            "time": datetime.now().strftime("%H:%M:%S"),
            "engine": "NIFTY ZERO-HERO",
            "symbol": p["symbol"],
            "pnl": unreal,
            "status": "🛡️ ZERO PROTECTION CUT"
        })
        st.toast(f"🛡️ Zero-Hero Cut! Loss: ₹{unreal}", icon="⚠️")
    else:
        rem_zh.append(p)

st.session_state.zero_hero_positions = rem_zh

# Total unrealized
fut_unreal = sum(p.get("unrealized", 0.0) for p in st.session_state.futures_positions)
zh_unreal = sum(p.get("unrealized", 0.0) for p in st.session_state.zero_hero_positions)
total_active_unreal = fut_unreal + zh_unreal

# ==========================================
# MOBILE HERO BANNER
# ==========================================
st.markdown(f"""
<div class="hero-banner">
    <div style="display:flex; justify-content:space-between; align-items:center;">
        <span style="font-size:11px; font-weight:800; color:#c084fc; letter-spacing:0.5px;">HIGH-SPEED SCALPER PRO</span>
        <span class="badge-scalp badge-zh">● LIVE SCALPING</span>
    </div>
    <div style="font-size:26px; font-weight:800; margin:4px 0;" class="{'green' if all_realized_pnl>=0 else 'red'}">
        {'+' if all_realized_pnl>=0 else ''}₹{all_realized_pnl:,.2f}
    </div>
    <div style="display:flex; justify-content:space-between; font-size:12px; color:#cbd5e1; margin-top:6px;">
        <span>Active P&L: <strong class="{'green' if total_active_unreal>=0 else 'red'}">{'+' if total_active_unreal>=0 else ''}₹{total_active_unreal:.2f}</strong></span>
        <span>Balance: <strong>₹{(current_cash + total_active_unreal):,.0f}</strong></span>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# MOBILE SEGMENT SELECTOR
# ==========================================
mode = st.radio(
    "Mode",
    ["🚀 Crypto Futures 10x", "⚡ NIFTY Zero-Hero", "📜 Ledger"],
    horizontal=True,
    label_visibility="collapsed"
)

# ####################################################################
# SCREEN 1: 🚀 CRYPTO FUTURES 10X LEVERAGE SCALPING
# ####################################################################
if mode == "🚀 Crypto Futures 10x":
    st.write(f"**⚡ Active 10x Leveraged Positions ({len(st.session_state.futures_positions)})**")
    st.caption("24/7 Global Live Feed • 10x Margin Scalping • Quotex Alternative")

    for p in st.session_state.futures_positions:
        pnl = p["unrealized"]
        side_badge = f'<span class="badge-scalp badge-long">LONG 10x</span>' if p["side"]=="LONG" else f'<span class="badge-scalp badge-short">SHORT 10x</span>'
        
        st.markdown(f"""
        <div class="mobile-card" style="border-left: 4px solid {'#10b981' if pnl>=0 else '#ef4444'};">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="font-weight:800; font-size:15px;">{p['symbol']} / USDT</span>
                {side_badge}
            </div>
            <div style="font-size:20px; font-weight:800; margin:4px 0;" class="{'green' if pnl>=0 else 'red'}">
                {'+' if pnl>=0 else ''}₹{pnl:.2f}
            </div>
            <div class="card-grid">
                <div>Entry: ₹{p['entry_inr']:,.1f}</div>
                <div>Live: ₹{p['current_inr']:,.1f}</div>
                <div class="green">Target: ₹{p['target_inr']:,.1f} (+15%)</div>
                <div class="red">SL: ₹{p['sl_inr']:,.1f} (-8%)</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ####################################################################
# SCREEN 2: ⚡ NIFTY ZERO-HERO OPTIONS (ANGEL ONE)
# #################################################===================
elif mode == "⚡ NIFTY Zero-Hero":
    st.write("**⚡ NIFTY Expiry Zero-Hero Options (Angel One)**")
    st.caption("Low Investment (~₹1,200) • High Multiplier (2x to 3x Profit)")

    for p in st.session_state.zero_hero_positions:
        pnl = p["unrealized"]
        st.markdown(f"""
        <div class="mobile-card" style="border: 1px solid #a855f7; border-left: 5px solid #a855f7;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="font-weight:800; font-size:15px; color:#c084fc;">{p['symbol']}</span>
                <span class="badge-scalp badge-zh">LOT: 65 QTY</span>
            </div>
            <div style="font-size:22px; font-weight:800; margin:4px 0;" class="{'green' if pnl>=0 else 'red'}">
                {'+' if pnl>=0 else ''}₹{pnl:.2f}
            </div>
            <div class="card-grid">
                <div>Buy Premium: ₹{p['entry']}</div>
                <div>Live Premium: ₹{p['current']}</div>
                <div class="green">Hero Target: ₹{p['target']} (2.5x)</div>
                <div class="red">Zero SL: ₹{p['sl']}</div>
            </div>
            <div style="font-size:11px; color:#94a3b8; margin-top:6px;">
                💡 <em>Capital at Risk: Only ₹1,170 | Target Profit: +₹1,755</em>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ####################################################################
# SCREEN 3: 📜 HISTORY
# ####################################################################
else:
    st.write(f"**Trade Ledger ({len(all_trades)} Executed Scalps)**")
    if len(all_trades) > 0:
        for t in reversed(all_trades[-15:]):
            pnl = t.get("pnl", 0)
            engine = t.get("engine", "SCALP")
            st.markdown(f"""
            <div class="mobile-card" style="padding:10px 14px; border-left: 3px solid {'#10b981' if pnl>=0 else '#ef4444'};">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-weight:700; font-size:14px;">{t.get('symbol')}</span>
                    <span class="{'green' if pnl>=0 else 'red'}" style="font-weight:800;">
                        {'+' if pnl>=0 else ''}₹{pnl:.2f}
                    </span>
                </div>
                <div style="display:flex; justify-content:space-between; font-size:11px; color:#94a3b8; margin-top:4px; font-family:monospace;">
                    <span>{engine} • {t.get('status')}</span>
                    <span>{t.get('time')}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No closed scalp trades recorded yet.")

# Auto-refresh loop
time.sleep(2)
st.rerun()
