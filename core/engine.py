import asyncio
from datetime import datetime
from typing import Dict, Any, Optional

from core.config import settings
from brokers.paper_broker import PaperBroker
from brokers.angel_one import AngelOneBroker
from strategies.technical import TechnicalAnalyzer
from ai.analyzer import AIAgentAnalyzer
from bot.telegram_app import TelegramMobileController

class BotEngine:
    """
    Central Engine coordinating Market Data, Technical Indicators,
    AI Analysis, Order Execution, and Mobile Telegram Control.
    """

    def __init__(self):
        # Choose broker based on settings
        if settings.PAPER_TRADING:
            print("[Engine] Initializing in PAPER TRADING (Virtual Capital) mode.")
            self.broker = PaperBroker(initial_capital=settings.INITIAL_PAPER_CAPITAL)
        else:
            print("[Engine] Initializing in LIVE ANGEL ONE TRADING mode.")
            self.broker = AngelOneBroker()

        self.tech_analyzer = TechnicalAnalyzer()
        self.ai_analyzer = AIAgentAnalyzer()
        self.telegram = TelegramMobileController(bot_manager=self)
        self.is_active = True
        self.last_ai_verdict = {
            "decision": "HOLD",
            "confidence": 50,
            "reason": "AI monitoring technical indicators (RSI, EMA, MACD)...",
            "suggested_sl": 0,
            "suggested_target": 0,
            "symbol": settings.DEFAULT_SYMBOL
        }

    async def initialize(self):
        # Connect broker
        self.broker.connect()
        # Start telegram mobile controller
        await self.telegram.start()
        print("[Engine] Bot Engine fully initialized.")

    async def run_analysis_cycle(self, symbol: Optional[str] = None) -> Optional[Dict[str, Any]]:
        target_symbol = symbol or settings.DEFAULT_SYMBOL
        
        # 1. Fetch Candle Data
        df = self.broker.get_historical_data(target_symbol, interval=settings.TIMEFRAME)
        if df.empty or len(df) < 20:
            print(f"[Engine] Insufficient candle data for {target_symbol}")
            return None

        # 2. Compute Technical Indicators
        summary = self.tech_analyzer.get_market_summary(df)
        if not summary:
            return None

        # 3. AI Quantitative Analysis
        ai_verdict = self.ai_analyzer.analyze_market(target_symbol, summary)
        decision = ai_verdict.get("decision", "HOLD")
        confidence = int(ai_verdict.get("confidence", 0))

        print(f"[Engine] {target_symbol} Analysis: {decision} | Confidence: {confidence}% | Reason: {ai_verdict.get('reason')}")

        # 4. Check Risk & Confidence Threshold
        if decision in ["BUY", "SELL"] and confidence >= settings.AI_CONFIDENCE_THRESHOLD:
            # Execute Trade
            current_price = summary["current_price"]
            # Default single lot or fixed quantity
            qty = 15 if "NIFTY" in target_symbol else 1

            order = self.broker.place_order(target_symbol, decision, quantity=qty, price=current_price)
            
            # Send Instant Alert to Mobile Telegram
            alert_msg = (
                f"🚨 *NEW AI TRADE EXECUTED!*\n\n"
                f"• *Symbol:* `{target_symbol}`\n"
                f"• *Action:* *{decision}*\n"
                f"• *Price:* ₹{current_price}\n"
                f"• *Quantity:* {qty}\n"
                f"• *Confidence:* {confidence}%\n"
                f"• *Target:* ₹{ai_verdict.get('suggested_target')}\n"
                f"• *Stop Loss:* ₹{ai_verdict.get('suggested_sl')}\n\n"
                f"🧠 *AI Reason:* {ai_verdict.get('reason')}"
            )
            await self.telegram.send_alert(alert_msg)

        ai_verdict["symbol"] = target_symbol
        self.last_ai_verdict = ai_verdict
        return ai_verdict

    async def background_trading_loop(self, interval_seconds: int = 60):
        """Continuous background trading loop that evaluates markets at set intervals."""
        while True:
            try:
                if self.is_active:
                    await self.run_analysis_cycle()
            except Exception as e:
                print(f"[Engine Loop Error]: {e}")
            await asyncio.sleep(interval_seconds)
