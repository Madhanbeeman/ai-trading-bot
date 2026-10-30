# ⚡ AI Trading Terminal (Angel One + CoinDCX)

A modern, high-performance modular trading terminal built with Python and Streamlit.

## 🚀 Key Highlights
- **Architecture**: Modular Python architecture (`config/`, `brokers/`, `engine/`, `ui/`).
- **Brokers Supported**: 
  - 📈 **Angel One SmartAPI**: NSE Equities (5x Intraday MIS) + Nifty/Bank Nifty F&O Zero-to-Hero Options.
  - 🇮🇳 **CoinDCX India**: 24/7 Crypto Spot in INR + 10x High-Leverage Perpetual Futures.
- **Timezone**: Native Indian Standard Time (IST) formatting on all live ticks, clocks, and trade logs.
- **UI/UX**: Native mobile fintech design with dark/light themes, pill tabs, live radar pulse, and bottom navigation dock.
- **Paper Capital**: ₹2,000 Initial Grant per broker (₹4,000 Total Initial Balance).

## 📁 Project Structure
```
├── config/             # Settings, constants, and asset pool definitions
├── brokers/            # Real-time market feed adapters (NSE & CoinDCX)
├── engine/             # Paper ledger, order manager, and risk triggers
├── ui/                 # Styling, theme engine, and reusable UI components
├── app.py              # Main terminal orchestrator
├── requirements.txt    # Production dependencies
└── .gitignore          # Environment & local state protection
```
