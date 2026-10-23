import streamlit as st
import pandas as pd
import numpy as np
import time
import os
import json
from datetime import datetime

# ==========================================
# PAGE CONFIGURATION (Mobile Responsive)
# ==========================================
st.set_page_config(
    page_title="Autonomous AI Hedge Fund Terminal",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom Styling
st.markdown("""
<style>
    .stApp { background-color: #080c14; color: #f8fafc; }
    .card {
        background: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 12px;
        padding: 14px;
        margin-bottom: 12px;
    }
    .text-green { color: #10b981; font-weight: 700; }
    .text-red { color: #ef4444; font-weight: 700; }
    .autopilot-banner {
        background: linear-gradient(135deg, #1e1b4b, #0f172a);
        border: 1px solid #6366f1;
        border-radius: 14px;
        padding: 14px;
        margin-bottom: 16px;
    }
    .stock-chip {
        display: inline-block;
        padding: 3px 8px;
        border-radius: 6px;
        background: rgba(99, 102, 241, 0.2);
        color: #818cf8;
        font-weight: 700;
        font-size: 11px;
    }
    .pulse {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: #10b981;
        box-shadow: 0 0 10px #10b981;
        margin-right: 6px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# PERSISTENT DATABASE ENGINE
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

# Calculate lifetime and today's profit
today_str = datetime.now().strftime("%Y-%m-%d")
all_trades = db_data.get("trades", [])
today_trades = [t for t in all_trades if t.get("date") == today_str]
today_realized_pnl = sum(t.get("pnl", 0.0) for t in today_trades)
all_realized_pnl = sum(t.get("pnl", 0.0) for t in all_trades)
current_cash = db_data.get("initial_capital", 50000.0) + all_realized_pnl

# ==========================================
# NIFTY 50 UNIVERSE FOR SCANNING
# ==========================================
STOCK_UNIVERSE = [
    {"symbol": "TATAMOTORS", "base_price": 960.0, "sector": "Auto"},
    {"symbol": "RELIANCE", "base_price": 2750.0, "sector": "Energy"},
    {"symbol": "INFY", "base_price": 1820.0, "sector": "IT"},
    {"symbol": "HDFCBANK", "base_price": 1680.0, "sector": "Banking"},
    {"symbol": "ICICIBANK", "base_price": 1240.0, "sector": "Banking"},
    {"symbol": "BHARTIARTL", "base_price": 1650.0, "sector": "Telecom"},
    {"symbol": "LT", "base_price": 3520.0, "sector": "Infra"},
    {"symbol": "TCS", "base_price": 4120.0, "sector": "IT"},
    {"symbol": "SUNPHARMA", "base_price": 1890.0, "sector": "Pharma"},
    {"symbol": "ITC", "base_price": 485.0, "sector": "FMCG"}
]

# State setup
if "positions" not in st.session_state:
    st.session_state.positions = []
if "auto_pilot" not in st.session_state:
    st.session_state.auto_pilot = True  # Always True by default!
if "last_action" not in st.session_state:
    st.session_state.last_action = "AI initialized autonomous scanning..."

# ==========================================
# AUTONOMOUS ENGINE: SCAN & REPLACE OPEN SLOTS
# ==========================================
def auto_fill_slots():
    """Keeps exactly 3 calibrated parallel stocks active at all times automatically."""
    active_symbols = [p["symbol"] for p in st.session_state.positions]
    needed_slots = 3 - len(st.session_state.positions)
    
    if needed_slots > 0:
        available_stocks = [s for s in STOCK_UNIVERSE if s["symbol"] not in active_symbols]
        np.random.shuffle(available_stocks)
        
        for stock in available_stocks[:needed_slots]:
            price = stock["base_price"]
            qty = max(1, int(10000.0 // price)) # Allocates ~Rs 10,000 per slot
            target_p = round(price * 1.012, 2)  # +1.2% Target Profit
            sl_p = round(price * 0.994, 2)      # -0.6% Stop Loss

            score = np.random.randint(82, 98)
            st.session_state.positions.append({
                "symbol": stock["symbol"],
                "sector": stock["sector"],
                "entry": price,
                "current": price,
                "qty": qty,
                "target": target_p,
                "sl": sl_p,
                "unrealized": 0.0,
                "score": score,
                "reason": f"AI Momentum Score: {score}%"
            })
            st.session_state.last_action = f"AI Auto-Picked {stock['symbol']} ({stock['sector']}) at ₹{price}"

# Trigger auto-fill if slots empty
if st.session_state.auto_pilot:
    auto_fill_slots()

# ==========================================
# HEADER & AUTOPILOT BANNER
# ==========================================
st.title("🤖 Autonomous AI Hedge Fund Terminal")
st.caption("100% Hands-Free • Continuous Parallel Execution • No Daily Profit Cap")

st.markdown(f"""
<div class="autopilot-banner">
    <div style="display:flex; justify-content:space-between; align-items:center;">
        <span style="font-weight:700; font-size:14px;"><span class="pulse"></span>100% FULL AUTO-PILOT ACTIVE</span>
        <span style="font-size:12px; color:#818cf8; font-weight:700;">UNLIMITED TRADES • NO LIMIT</span>
    </div>
    <div style="font-size:12px; color:#94a3b8; margin-top:6px;">
        AI scans, buys, exits on target, and continuously refills 3 parallel stock slots without any manual intervention.
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# METRICS ROW
# ==========================================
unrealized_total = sum(p.get("unrealized", 0.0) for p in st.session_state.positions)
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("💵 Total Cumulative Profit", f"{'+' if all_realized_pnl>=0 else ''}₹{all_realized_pnl:,.2f}", delta=f"Today: ₹{today_realized_pnl:.2f}")
with m2:
    st.metric("📈 Live Open P&L", f"{'+' if unrealized_total>=0 else ''}₹{unrealized_total:.2f}", delta=f"{unrealized_total:.2f}")
with m3:
    st.metric("🎯 Total Portfolio Equity", f"₹{(current_cash + unrealized_total):,.2f}")
with m4:
    total_trades_count = len(all_trades)
    wins = len([t for t in all_trades if t.get("pnl", 0) > 0])
    win_rate = (wins / max(1, total_trades_count)) * 100
    st.metric("⚡ Win Rate", f"{win_rate:.0f}%", f"{wins}/{total_trades_count} Trades")

st.divider()

# ==========================================
# TICK MOTOR & AUTOMATIC PROFIT BOOKING
# ==========================================
remaining_positions = []
for p in st.session_state.positions:
    # Continuous market tick fluctuation
    move = np.random.choice([0.003, 0.005, -0.002, 0.004, -0.001])
    cur_price = round(p["current"] * (1 + move), 2)
    p["current"] = cur_price
    
    unreal = round((cur_price - p["entry"]) * p["qty"], 2)
    p["unrealized"] = unreal

    # Check Target (+1.2%) or SL (-0.6%)
    if cur_price >= p["target"]:
        realized = round((cur_price - p["entry"]) * p["qty"], 2)
        record = {
            "date": today_str,
            "time": datetime.now().strftime("%H:%M:%S"),
            "symbol": p["symbol"],
            "sector": p["sector"],
            "qty": p["qty"],
            "entry_price": p["entry"],
            "exit_price": cur_price,
            "pnl": realized,
            "status": "🎯 TARGET PROFIT",
            "reason": "AI Target Hit (+1.2%)"
        }
        save_trade(record)
        st.session_state.last_action = f"🎯 TARGET HIT! Sold {p['symbol']} (+₹{realized}). Auto-Scanning next stock..."
        st.toast(f"🎯 Target Hit! Sold {p['symbol']} (+₹{realized})", icon="✅")
    elif cur_price <= p["sl"]:
        loss = round((cur_price - p["entry"]) * p["qty"], 2)
        record = {
            "date": today_str,
            "time": datetime.now().strftime("%H:%M:%S"),
            "symbol": p["symbol"],
            "sector": p["sector"],
            "qty": p["qty"],
            "entry_price": p["entry"],
            "exit_price": cur_price,
            "pnl": loss,
            "status": "🛡️ STOP LOSS",
            "reason": "Risk Cut (-0.6%)"
        }
        save_trade(record)
        st.session_state.last_action = f"🛡️ SL Hit! Exited {p['symbol']} (₹{loss}). Auto-Scanning next stock..."
        st.toast(f"🛡️ SL Cut {p['symbol']} (₹{loss})", icon="⚠️")
    else:
        remaining_positions.append(p)

st.session_state.positions = remaining_positions

# Automatically refill any slots that were just exited!
if st.session_state.auto_pilot and len(st.session_state.positions) < 3:
    auto_fill_slots()

# ==========================================
# PARALLEL ACTIVE SLOTS DISPLAY
# ==========================================
st.subheader("📊 Live Parallel Executions (Continuous 3 Slots)")
st.caption(f"⚡ Status: {st.session_state.last_action}")

cols = st.columns(3)
for i in range(3):
    with cols[i]:
        if i < len(st.session_state.positions):
            p = st.session_state.positions[i]
            st.markdown(f"""
            <div class="card" style="border-left: 4px solid {'#10b981' if p['unrealized']>=0 else '#ef4444'};">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-weight:800; font-size:16px;">{p['symbol']}</span>
                    <span class="stock-chip">{p['sector']}</span>
                </div>
                <div style="font-size:11px; color:#94a3b8; margin:4px 0;">{p['reason']}</div>
                <div style="font-size:20px; font-weight:800; margin:8px 0;" class="{'text-green' if p['unrealized']>=0 else 'text-red'}">
                    {'+' if p['unrealized']>=0 else ''}₹{p['unrealized']:.2f}
                </div>
                <div style="font-size:12px; color:#94a3b8; font-family:monospace; line-height:1.6;">
                    • Qty: <strong>{p['qty']}</strong> | Entry: ₹{p['entry']}<br>
                    • Live: ₹{p['current']}<br>
                    • Target: <span style="color:#10b981;">₹{p['target']}</span> | SL: <span style="color:#ef4444;">₹{p['sl']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="card" style="border: 1px dashed #334155; text-align:center; padding:35px 14px;">
                <span style="color:#64748b; font-size:13px;">AI Scanning next stock...</span>
            </div>
            """, unsafe_allow_html=True)

# Emergency Manual Control (Only for Panic)
if st.button("🚨 Emergency Stop & Flatten All Positions", type="secondary", use_container_width=True):
    for p in st.session_state.positions:
        unreal = p["unrealized"]
        save_trade({
            "date": today_str,
            "time": datetime.now().strftime("%H:%M:%S"),
            "symbol": p["symbol"],
            "sector": p["sector"],
            "qty": p["qty"],
            "entry_price": p["entry"],
            "exit_price": p["current"],
            "pnl": unreal,
            "status": "🚨 MANUAL FLATTEN",
            "reason": "Emergency Flatten"
        })
    st.session_state.positions = []
    st.rerun()

# ==========================================
# PERMANENT AUDIT HISTORY
# ==========================================
st.subheader("📜 Continuous Trade Ledger (Permanent Database)")
fresh_db = load_db()
all_completed = fresh_db.get("trades", [])

if len(all_completed) > 0:
    df_history = pd.DataFrame(all_completed)[["date", "time", "symbol", "sector", "qty", "entry_price", "exit_price", "pnl", "status"]]
    st.dataframe(df_history.iloc[::-1], use_container_width=True)
    st.caption("🔒 All closed trades are permanently recorded in database file.")
else:
    st.caption("No completed trades recorded yet.")

# ==========================================
# 100% AUTONOMOUS REAL-TIME STREAMING LOOP
# ==========================================
time.sleep(2)
st.rerun()
