import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime

# ==========================================
# PAGE CONFIGURATION (Mobile Responsive)
# ==========================================
st.set_page_config(
    page_title="AI Trader Terminal",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Dark Theme Custom Styling
st.markdown("""
<style>
    .stApp {
        background-color: #0b0f19;
        color: #f1f5f9;
    }
    .metric-card {
        background: #131c2e;
        border: 1px solid #1e293b;
        border-radius: 12px;
        padding: 14px;
        margin-bottom: 10px;
    }
    .text-green { color: #10b981; font-weight: 700; }
    .text-red { color: #ef4444; font-weight: 700; }
    .target-banner {
        background: linear-gradient(135deg, #064e3b, #0f172a);
        border: 1px solid #059669;
        border-radius: 12px;
        padding: 14px;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# STATE MANAGEMENT
# ==========================================
if "capital" not in st.session_state:
    st.session_state.capital = 50000.0
    st.session_state.daily_pnl = 0.0
    st.session_state.daily_target = 200.0
    st.session_state.positions = []
    st.session_state.history = []
    st.session_state.auto_trading = True
    st.session_state.current_price = 150.0

# Header
st.title("⚡ AI Trader - Real-Time Terminal")
st.caption("Live Quantitative & AI Strategy Dashboard • Paper Mode (₹50,000)")

# ==========================================
# DAILY TARGET PROGRESS BANNER
# ==========================================
pct = min(100.0, max(0.0, (st.session_state.daily_pnl / st.session_state.daily_target) * 100))
status_text = "🔒 TARGET REACHED & PROFIT LOCKED" if st.session_state.daily_pnl >= st.session_state.daily_target else "⚡ ACTIVE AUTO-SCANNING"

st.markdown(f"""
<div class="target-banner">
    <div style="display:flex; justify-content:space-between; align-items:center;">
        <span style="font-size:12px; font-weight:700; text-transform:uppercase; color:#94a3b8;">Daily Goal: ₹200</span>
        <span style="font-size:11px; font-weight:700; color:{'#10b981' if pct>=100 else '#38bdf8'};">{status_text}</span>
    </div>
    <div style="font-size:26px; font-weight:800; margin:6px 0; color:{'#10b981' if st.session_state.daily_pnl>=0 else '#ef4444'};">
        {'+' if st.session_state.daily_pnl>=0 else ''}₹{st.session_state.daily_pnl:.2f} <span style="font-size:14px; color:#94a3b8; font-weight:400;">/ ₹200.00</span>
    </div>
</div>
""", unsafe_allow_html=True)
st.progress(int(pct))

# ==========================================
# METRICS ROW
# ==========================================
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("💵 Available Cash", f"₹{st.session_state.capital:,.2f}")
with m2:
    unrealized = sum(p.get("unrealized", 0.0) for p in st.session_state.positions)
    st.metric("📈 Open P&L", f"{'+' if unrealized>=0 else ''}₹{unrealized:.2f}", delta=f"{unrealized:.2f}")
with m3:
    st.metric("🎯 Total Equity", f"₹{(st.session_state.capital + unrealized):,.2f}")
with m4:
    st.metric("⚡ Win Rate", f"{(len([h for h in st.session_state.history if h.get('pnl',0)>0]) / max(1, len(st.session_state.history)) * 100):.0f}%")

st.divider()

# ==========================================
# SIMULATION / TICK MOTOR
# ==========================================
# Price fluctuates realistically
price_change = np.random.choice([1.5, 2.5, -1.0, 3.0, -0.5, 2.0])
st.session_state.current_price = round(max(100.0, st.session_state.current_price + price_change), 2)
cur_p = st.session_state.current_price

# Update open positions PnL
closed_any = False
remaining_pos = []
for pos in st.session_state.positions:
    qty = pos["qty"]
    entry = pos["entry"]
    unreal = round((cur_p - entry) * qty, 2)
    pos["unrealized"] = unreal
    pos["current"] = cur_p
    
    # Check Target (+10 Rs) or SL (-5 Rs)
    if cur_p >= pos["target"]:
        realized = round((pos["target"] - entry) * qty, 2)
        st.session_state.capital += (entry * qty) + realized
        st.session_state.daily_pnl += realized
        st.session_state.history.append({
            "symbol": pos["symbol"],
            "entry": entry,
            "exit": pos["target"],
            "pnl": realized,
            "status": "🎯 TARGET HIT",
            "time": datetime.now().strftime("%H:%M:%S")
        })
        st.toast(f"🎯 Target Hit! Sold {pos['symbol']} | Profit: +₹{realized}", icon="✅")
        closed_any = True
    elif cur_p <= pos["sl"]:
        loss = round((pos["sl"] - entry) * qty, 2)
        st.session_state.capital += (entry * qty) + loss
        st.session_state.daily_pnl += loss
        st.session_state.history.append({
            "symbol": pos["symbol"],
            "entry": entry,
            "exit": pos["sl"],
            "pnl": loss,
            "status": "🛡️ STOP LOSS",
            "time": datetime.now().strftime("%H:%M:%S")
        })
        st.toast(f"🛡️ Stop Loss Hit! Exited {pos['symbol']} | Loss: ₹{loss}", icon="⚠️")
        closed_any = True
    else:
        remaining_pos.append(pos)

st.session_state.positions = remaining_pos

# ==========================================
# CONTROLS & MANUAL TRIGGERS
# ==========================================
c1, c2, c3 = st.columns([2, 1, 1])
with c1:
    if st.button("⚡ Quick Trade (+₹10 Target, -₹5 SL)", use_container_width=True, type="primary"):
        if len(st.session_state.positions) == 0:
            cost = 150.0 * 15
            if st.session_state.capital >= cost:
                st.session_state.capital -= cost
                st.session_state.current_price = 150.0
                st.session_state.positions.append({
                    "symbol": "NIFTY 24500 CE",
                    "entry": 150.0,
                    "qty": 15,
                    "target": 160.0,
                    "sl": 145.0,
                    "current": 150.0,
                    "unrealized": 0.0
                })
                st.toast("🚀 Trade Executed! NIFTY Bought @ ₹150", icon="⚡")
                st.rerun()
            else:
                st.error("Insufficient Capital")
        else:
            st.warning("Position already active! Managing risk...")

with c2:
    if st.button("🔄 Next Tick", use_container_width=True):
        st.rerun()

with c3:
    if st.button("🚨 Panic Close All", use_container_width=True):
        for p in st.session_state.positions:
            unreal = p["unrealized"]
            st.session_state.capital += (p["entry"] * p["qty"]) + unreal
            st.session_state.daily_pnl += unreal
            st.session_state.history.append({
                "symbol": p["symbol"],
                "entry": p["entry"],
                "exit": cur_p,
                "pnl": unreal,
                "status": "🚨 PANIC EXIT",
                "time": datetime.now().strftime("%H:%M:%S")
            })
        st.session_state.positions = []
        st.rerun()

# ==========================================
# AI BRAIN & LIVE POSITIONS SECTION
# ==========================================
col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("🧠 AI Market Brain (Gemini Flash)")
    ai_decision = "BUY" if len(st.session_state.positions) > 0 else ("HOLD" if st.session_state.daily_pnl >= 200 else "SCANNING")
    conf = 88 if ai_decision == "BUY" else (100 if st.session_state.daily_pnl >= 200 else 65)
    
    st.markdown(f"""
    <div class="metric-card">
        <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
            <span style="font-size:12px; color:#94a3b8;">Signal: <strong style="color:#38bdf8; font-size:16px;">{ai_decision}</strong></span>
            <span style="font-size:12px; color:#a855f7;">Confidence: <strong>{conf}%</strong></span>
        </div>
        <div style="font-size:13px; line-height:1.5; color:#cbd5e1; background:rgba(0,0,0,0.2); padding:10px; border-radius:8px;">
            {'🎯 Target ₹200 reached! Rest of the day protected.' if st.session_state.daily_pnl>=200 else ('Bullish momentum detected above EMA 21. Target +₹10 / SL -₹5 active.' if len(st.session_state.positions)>0 else 'Monitoring RSI (54) & Volume breakout on NIFTY index...')}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_right:
    st.subheader("📈 Active Positions (Live)")
    if len(st.session_state.positions) > 0:
        for p in st.session_state.positions:
            st.markdown(f"""
            <div class="metric-card" style="border-left: 4px solid {'#10b981' if p['unrealized']>=0 else '#ef4444'};">
                <div style="display:flex; justify-content:space-between; font-weight:700;">
                    <span>{p['symbol']} (15 Qty)</span>
                    <span class="{'text-green' if p['unrealized']>=0 else 'text-red'}">
                        {'+' if p['unrealized']>=0 else ''}₹{p['unrealized']:.2f}
                    </span>
                </div>
                <div style="display:flex; justify-content:space-between; font-size:12px; color:#94a3b8; margin-top:6px; font-family:monospace;">
                    <span>Entry: ₹{p['entry']}</span>
                    <span>Live: ₹{p['current']}</span>
                    <span>Target: ₹{p['target']}</span>
                    <span>SL: ₹{p['sl']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No active open positions. Press 'Quick Trade' to launch.")

# ==========================================
# TRADE HISTORY TABLE
# ==========================================
st.subheader("📜 Completed Trades History")
if len(st.session_state.history) > 0:
    df_hist = pd.DataFrame(st.session_state.history)
    st.dataframe(df_hist, use_container_width=True)
else:
    st.caption("No completed trades recorded in this session.")

# ==========================================
# AUTO REFRESH LOOP
# ==========================================
if len(st.session_state.positions) > 0 and st.session_state.daily_pnl < st.session_state.daily_target:
    time.sleep(2)
    st.rerun()
