# 🏦 AI Institutional Multi-Stock Trading Terminal

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)

An autonomous, multi-asset quantitative trading terminal engineered with:
- **Zero Manual Stock Picking**: AI scans the entire NIFTY universe and algorithmically picks top setups.
- **Parallel Multi-Stock Calibration**: Capital is allocated equally across 3 distinct sectors to mitigate single-stock risk.
- **Persistent Database (Local JSON Ledger)**: Records never disappear on refresh or session reloads.
- **Strict Risk Management**: 2:1 Risk-Reward Ratio (+1.2% Target / -0.6% Stop-Loss) with an automated Daily Target Lock (₹200 Goal).
- **100% Free Lifetime Hosting**: Deployed on Streamlit Cloud with zero sleep-mode drops.

---

## 🌟 Key Features

### 1. 🧠 Autonomous Parallel Market Scanner
- Evaluates moving average momentum (9 & 21 EMA crossover), Relative Strength Index (RSI), and volume expansion.
- Dynamically allocates ₹10,000 across 3 high-probability stocks simultaneously (e.g., Tata Motors, Reliance, Infosys).

### 2. 🛡️ Professional Capital Preservation
- **Daily Profit Target:** ₹200. Once achieved, the terminal locks profit (`🔒 DAILY TARGET REACHED`) and halts new trades to prevent overtrading.
- **Automated Target / Stop-Loss Engine:**
  - **Target (+1.2%):** Automatically exits in profit.
  - **Stop-Loss (-0.6%):** Automatically cuts risk to protect capital.

### 3. 💾 Persistent Database Ledger
- All closed trades are permanently recorded with timestamp, stock ticker, sector, quantity, entry/exit prices, and net P&L in `data/trade_ledger.json`.

---

## 🚀 Live Dashboard Access

Open your Streamlit Cloud URL on any mobile or desktop browser to monitor and control:
- Live Portfolio Equity & Available Cash
- Parallel Open Position Cards with Tick-by-Tick P&L
- Real-Time AI Confidence Insights
- Full Historical Trade Ledger

---

## 🛠️ Tech Stack
- **Frontend / Terminal:** Streamlit
- **Backend / Engine:** Python 3, Asyncio, Pandas, NumPy
- **Broker Interface:** Angel One SmartAPI Ready & Simulated High-Fidelity Paper Engine
- **Hosting:** Streamlit Cloud (100% Free, Always-On)
