import asyncio
from datetime import datetime
from typing import Dict, Any, Optional

from core.config import settings
from brokers.paper_broker import PaperBroker
from brokers.angel_one import AngelOneBroker
from strategies.technical import TechnicalAnalyzer
from ai.analyzer import AIAgentAnalyzer

class BotEngine:
    """
    Central Engine with:
    - Real-Time Tick Evaluation
    - Fixed Daily Target: Rs. 200 (Profit Lock)
    - Strict Stop-Loss & Target Monitoring
    - 0-ms WebSocket Broadcast State
    """

    def __init__(self):
        if settings.PAPER_TRADING:
            print("[Engine] Initializing in PAPER TRADING mode (Capital: Rs. 50,000).")
            self.broker = PaperBroker(initial_capital=50000.0)
        else:
            print("[Engine] Initializing in LIVE ANGEL ONE TRADING mode.")
            self.broker = AngelOneBroker()

        self.tech_analyzer = TechnicalAnalyzer()
        self.ai_analyzer = AIAgentAnalyzer()
        self.is_active = True
        
        # Daily Target Management
        self.daily_target_amount = 200.0
        self.daily_realized_pnl = 0.0
        self.daily_target_reached = False
        
        self.last_ai_verdict = {
            "decision": "HOLD",
            "confidence": 50,
            "reason": "AI monitoring technical indicators (RSI, EMA, MACD)...",
            "suggested_sl": 0,
            "suggested_target": 0,
            "symbol": settings.DEFAULT_SYMBOL
        }

    async def initialize(self):
        self.broker.connect()
        print("[Engine] Bot Engine fully initialized & Broker connected.")

    def check_position_sl_target(self):
        """Monitors open trades every tick for SL/Target hits."""
        positions = self.broker.get_open_positions()
        for pos in positions:
            symbol = pos["symbol"]
            qty = pos["quantity"]
            entry_price = pos["entry_price"]
            
            # Fetch simulated current price
            hist = self.broker.get_historical_data(symbol)
            cur_price = round(float(hist["close"].iloc[-1]), 2)
            pos["current_price"] = cur_price
            
            # Unrealized PnL
            unrealized = round((cur_price - entry_price) * qty, 2)
            pos["unrealized_pnl"] = unrealized

            target_price = pos.get("target_price", round(entry_price + 15.0, 2))
            sl_price = pos.get("sl_price", round(entry_price - 7.0, 2))

            # 1. Target Hit (PROFIT!)
            if cur_price >= target_price:
                self.broker.place_order(symbol, "SELL", qty, cur_price)
                realized = round((cur_price - entry_price) * qty, 2)
                self.daily_realized_pnl += realized
                print(f"🎯 [TARGET HIT] Sold {symbol} at Rs.{cur_price} | Profit: +Rs.{realized}")
                if self.daily_realized_pnl >= self.daily_target_amount:
                    self.daily_target_reached = True
                    print(f"🔒 [DAILY TARGET REACHED] Daily profit is Rs.{self.daily_realized_pnl}! Trading paused for today.")

            # 2. Stop-Loss Hit (PROTECTION!)
            elif cur_price <= sl_price:
                self.broker.place_order(symbol, "SELL", qty, cur_price)
                loss = round((cur_price - entry_price) * qty, 2)
                self.daily_realized_pnl += loss
                print(f"🛡️ [STOP LOSS HIT] Exited {symbol} at Rs.{cur_price} to prevent bigger loss | Loss: Rs.{loss}")

    async def run_analysis_cycle(self, symbol: Optional[str] = None) -> Optional[Dict[str, Any]]:
        target_symbol = symbol or settings.DEFAULT_SYMBOL
        
        # If daily target already reached, do not take new trades!
        if self.daily_target_reached:
            self.last_ai_verdict = {
                "decision": "HOLD",
                "confidence": 100,
                "reason": f"🎉 Daily target of Rs.{self.daily_target_amount} achieved! Profit is locked. Bot is resting.",
                "suggested_sl": 0,
                "suggested_target": 0,
                "symbol": target_symbol
            }
            return self.last_ai_verdict

        # If already in an open position, manage it, don't overtrade!
        if len(self.broker.get_open_positions()) > 0:
            return self.last_ai_verdict

        # 1. Fetch Candle Data
        df = self.broker.get_historical_data(target_symbol, interval=settings.TIMEFRAME)
        if df.empty or len(df) < 20:
            return None

        # 2. Compute Technical Indicators
        summary = self.tech_analyzer.get_market_summary(df)
        if not summary:
            return None

        # 3. AI Quantitative Analysis
        ai_verdict = self.ai_analyzer.analyze_market(target_symbol, summary)
        decision = ai_verdict.get("decision", "HOLD")
        confidence = int(ai_verdict.get("confidence", 0))

        now_str = datetime.now().strftime('%H:%M:%S')
        print(f"[{now_str}] [AI Analysis] {target_symbol}: {decision} ({confidence}%) - {ai_verdict.get('reason')}")

        # 4. Simple, Clear Target & Stop Loss Setup
        if decision == "BUY" and confidence >= settings.AI_CONFIDENCE_THRESHOLD:
            # Simulated options premium price (around Rs. 150)
            entry_price = 150.0
            qty = 15 # 1 Lot of Nifty
            
            # Target = +15 pts (Profit = Rs. 225)
            # StopLoss = -7 pts (Max Loss = Rs. 105)
            target = round(entry_price + 15.0, 2)
            sl = round(entry_price - 7.0, 2)

            order = self.broker.place_order(target_symbol, "BUY", quantity=qty, price=entry_price)
            if target_symbol in self.broker.positions:
                self.broker.positions[target_symbol]["target_price"] = target
                self.broker.positions[target_symbol]["sl_price"] = sl
            
            ai_verdict["suggested_target"] = target
            ai_verdict["suggested_sl"] = sl
            print(f"[{now_str}] 🚀 [BOUGHT] {target_symbol} at Rs.{entry_price} | Target: Rs.{target} | SL: Rs.{sl}")

        ai_verdict["symbol"] = target_symbol
        self.last_ai_verdict = ai_verdict
        return ai_verdict

    async def background_trading_loop(self, interval_seconds: int = 15):
        print(f"[Engine] Background trading loop active (tick every {interval_seconds}s)")
        while True:
            try:
                if self.is_active:
                    # 1. Check existing positions for SL / Target hits
                    self.check_position_sl_target()
                    # 2. Run AI evaluation for new setups
                    await self.run_analysis_cycle()
            except Exception as e:
                print(f"[Engine Loop Error]: {e}")
            await asyncio.sleep(interval_seconds)
