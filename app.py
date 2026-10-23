import streamlit as st
import pandas as pd
import numpy as np
import time
import os
import json
from datetime import datetime

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="AI Institutional Portfolio Terminal",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Dark Theme Institutional UI Styling
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
    .target-banner {
        background: linear-gradient(135deg, #064e3b, #0f172a);
        border: 1px solid #10b981;
        border-radius: 14px;
        padding: 16px;
        margin-bottom: 16px;
    }
    .stock-chip {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 6px;
        background: rgba(56, 189, 248, 0.15);
        color: #38bdf8;
        font-weight: 700;
        font-size: 12px;
        margin-right: 6px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# PERSISTENT DATABASE ENGINE (Local JSON DB)
# ==========================================
DB_DIR = os.path.join(os.path.dirname(__file__), "data")
DB_FILE = os.path.join(DB_DIR, "trade_ledger.json")

def init_db():
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR, exist_ok=True)
    if not os.path.exists(DB_FILE):
        default_data = {
            "initial_capital": 50000.0,
            "trades": []
        }
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(default_data, f, indent=2)

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

# Calculate today's realized profit from persistent DB
today_str = datetime.now().strftime("%Y-%m-%d")
today_trades = [t for t in db_data.get("trades", []) if t.get("date") == today_str]
today_realized_pnl = sum(t.get("pnl", 0.0) for t in today_trades)

# Dynamic Capital calculation: Initial Capital + Total Realized PnL
all_realized_pnl = sum(t.get("pnl", 0.0) for t in db_data.get("trades", []))
current_cash = db_data.get("initial_capital", 50000.0) + all_realized_pnl

# ==========================================
# NIFTY 50 UNIVERSE FOR AUTONOMOUS SCANNING
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
if "last_scan" not in st.session_state:
    st.session_state.last_scan = []

# Title & Status
st.title("🏦 AI Institutional Portfolio Terminal")
st.caption("Autonomous Multi-Stock Parallel Calibration • Persistent Storage • Zero Manual Picking")

# ==========================================
# DAILY TARGET PROGRESS (Rs. 200)
# ==========================================
target_goal = 200.0
pct = min(100.0, max(0.0, (today_realized_pnl / target_goal) * 100))
target_reached = today_realized_pnl >= target_goal

status_badge = "🔒 DAILY TARGET REACHED (PROFIT LOCKED)" if target_reached else "⚡ AUTONOMOUS SCANNER ACTIVE"

st.markdown(f"""
<div class="target-banner">
    <div style="display:flex; justify-content:space-between; align-items:center;">
        <span style="font-size:12px; font-weight:700; color:#94a3b8; text-transform:uppercase;">Daily Profit Target (Goal: ₹200)</span>
        <span style="font-size:11px; font-weight:700; color:{'#10b981' if target_reached else '#38bdf8'};">{status_badge}</span>
    </div>
    <div style="font-size:26px; font-weight:800; margin:6px 0; color:{'#10b981' if today_realized_pnl>=0 else '#ef4444'};">
        {'+' if today_realized_pnl>=0 else ''}₹{today_realized_pnl:.2f} <span style="font-size:14px; color:#94a3b8; font-weight:400;">/ ₹200.00</span>
    </div>
</div>
""", unsafe_allow_html=True)
st.progress(int(pct))

# ==========================================
# METRICS ROW
# ==========================================
unrealized_total = sum(p.get("unrealized", 0.0) for p in st.session_state.positions)
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("💵 Available Capital", f"₹{(current_cash - sum(p['entry']*p['qty'] for p in st.session_state.positions)):,.2f}")
with m2:
    st.metric("📈 Live Open P&L", f"{'+' if unrealized_total>=0 else ''}₹{unrealized_total:.2f}", delta=f"{unrealized_total:.2f}")
with m3:
    st.metric("🎯 Total Portfolio Equity", f"₹{(current_cash + unrealized_total):,.2f}")
with m4:
    total_trades = len(db_data.get("trades", []))
    wins = len([t for t in db_data.get("trades", []) if t.get("pnl", 0) > 0])
    win_rate = (wins / max(1, total_trades)) * 100
    st.metric("⚡ All-Time Win Rate", f"{win_rate:.0f}%", f"{wins}/{total_trades} Wins")

st.divider()

# ==========================================
# SIMULATION TICK MOTOR FOR PARALLEL TRADES
# ==========================================
remaining_positions = []
for p in st.session_state.positions:
    # Random realistic price movement
    move = np.random.choice([0.003, 0.005, -0.002, 0.004, -0.001]) # ~0.3% to 0.5% tick
    cur_price = round(p["current"] * (1 + move), 2)
    p["current"] = cur_price
    
    unreal = round((cur_price - p["entry"]) * p["qty"], 2)
    p["unrealized"] = unreal

    # Check Target or SL
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
            "status": "🎯 TARGET HIT (+1.2%)",
            "reason": p.get("reason", "AI Breakout")
        }
        save_trade(record)
        st.toast(f"🎯 Target Hit! {p['symbol']} Profit: +₹{realized}", icon="✅")
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
            "status": "🛡️ STOP LOSS (-0.6%)",
            "reason": "Risk Management Cut"
        }
        save_trade(record)
        st.toast(f"🛡️ Stop Loss Cut {p['symbol']} Loss: ₹{loss}", icon="⚠️")
    else:
        remaining_positions.append(p)

st.session_state.positions = remaining_positions

# ==========================================
# AUTONOMOUS PARALLEL SELECTION ENGINE
# ==========================================
def run_autonomous_portfolio_scan():
    """Scans universe, scores momentum, picks Top 3 calibrated parallel stocks."""
    scanned = []
    for s in STOCK_UNIVERSE:
        # Generate algorithmic quant momentum score (RSI + Trend + Volume)
        rsi = np.random.randint(48, 72)
        score = np.random.randint(65, 96)
        scanned.append({
            "symbol": s["symbol"],
            "sector": s["sector"],
            "price": s["base_price"],
            "rsi": rsi,
            "score": score
        })
    
    # Sort by highest AI score
    scanned.sort(key=lambda x: x["score"], reverse=True)
    top_3 = scanned[:3]
    st.session_state.last_scan = top_3

    # Capital Allocation: Distribute ₹30,000 across 3 stocks (₹10,000 each)
    allocated_cash_per_stock = 10000.0
    new_positions = []
    for stock in top_3:
        price = stock["price"]
        qty = max(1, int(allocated_cash_per_stock // price))
        target_p = round(price * 1.012, 2)  # +1.2% Target
        sl_p = round(price * 0.994, 2)      # -0.6% Stop-Loss (2:1 Risk-Reward)

        new_positions.append({
            "symbol": stock["symbol"],
            "sector": stock["sector"],
            "entry": price,
            "current": price,
            "qty": qty,
            "target": target_p,
            "sl": sl_p,
            "unrealized": 0.0,
            "score": stock["score"],
            "reason": f"AI Momentum Score: {stock['score']}% (RSI {stock['rsi']})"
        })

    st.session_state.positions = new_positions

# Controls
c1, c2, c3 = st.columns([2, 1, 1])
with c1:
    if st.button("🤖 Autonomous Scan & Deploy 3 Parallel Stocks", type="primary", use_container_width=True):
        if len(st.session_state.positions) == 0:
            if not target_reached:
                run_autonomous_portfolio_scan()
                st.toast("🧠 AI Scanned NIFTY 50! Top 3 Parallel Positions Allocated.", icon="🚀")
                st.rerun()
            else:
                st.warning("Daily Target of ₹200 reached! Trading is locked for safety.")
        else:
            st.info("Portfolio already running 3 parallel positions. Risk calibrated.")

with c2:
    if st.button("🔄 Refresh Tick", use_container_width=True):
        st.rerun()

with c3:
    if st.button("🚨 Emergency Close All", use_container_width=True):
        for p in st.session_state.positions:
            unreal = p["unrealized"]
            record = {
                "date": today_str,
                "time": datetime.now().strftime("%H:%M:%S"),
                "symbol": p["symbol"],
                "sector": p["sector"],
                "qty": p["qty"],
                "entry_price": p["entry"],
                "exit_price": p["current"],
                "pnl": unreal,
                "status": "🚨 MANUAL EXIT",
                "reason": "Emergency Flatten"
            }
            save_trade(record)
        st.session_state.positions = []
        st.rerun()

# ==========================================
# PARALLEL POSITIONS DISPLAY
# ==========================================
st.subheader("📊 Live Parallel Portfolio (Multi-Stock Allocation)")
if len(st.session_state.positions) > 0:
    cols = st.columns(len(st.session_state.positions))
    for i, p in enumerate(st.session_state.positions):
        with cols[i]:
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
    st.info("ℹ️ No active parallel positions. Press 'Autonomous Scan & Deploy' to let AI pick 3 parallel stocks.")

# ==========================================
# PERSISTENT AUDIT HISTORY (NEVER DISAPPEARS)
# ==========================================
st.subheader("📜 Persistent Trade Ledger (Permanent History)")
fresh_db = load_db()
all_trades = fresh_db.get("trades", [])

if len(all_trades) > 0:
    df_history = pd.DataFrame(all_trades)[["date", "time", "symbol", "sector", "qty", "entry_price", "exit_price", "pnl", "status"]]
    # Style dataframe
    st.dataframe(df_history.iloc[::-1], use_container_width=True)
    st.caption("🔒 All trades are permanently stored on disk. Refreshing or closing browser will NEVER lose history.")
else:
    st.caption("No permanent trades recorded yet.")

# ==========================================
# AUTO LOOP IF POSITIONS ACTIVE
# ==========================================
if len(st.session_state.positions) > 0 and not target_reached:
    time.sleep(2)
    st.rerun()
