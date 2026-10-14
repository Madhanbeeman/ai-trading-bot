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
    Central Engine coordinating Market Data, Technical Indicators,
    AI Analysis, Order Execution, and Web Dashboard.
    (100% Web Native - No Telegram dependency/conflicts)
    """

    def __init__(self):
        if settings.PAPER_TRADING:
            print("[Engine] Initializing in PAPER TRADING (Virtual Capital) mode.")
            self.broker = PaperBroker(initial_capital=settings.INITIAL_PAPER_CAPITAL)
        else:
            print("[Engine] Initializing in LIVE ANGEL ONE TRADING mode.")
            self.broker = AngelOneBroker()

        self.tech_analyzer = TechnicalAnalyzer()
        self.ai_analyzer = AIAgentAnalyzer()
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
        self.broker.connect()
        print("[Engine] Bot Engine fully initialized & Broker connected.")

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

        now_str = datetime.now().strftime('%H:%M:%S')
        print(f"[{now_str}] [AI Evaluation] {target_symbol} -> Decision: {decision} | Conf: {confidence}% | Reason: {ai_verdict.get('reason')}")

        # 4. Check Risk & Confidence Threshold
        if decision in ["BUY", "SELL"] and confidence >= settings.AI_CONFIDENCE_THRESHOLD:
            current_price = summary["current_price"]
            trade_price = current_price
            qty = 15
            if current_price > 5000 and settings.PAPER_TRADING:
                trade_price = round(current_price * 0.006, 2)

            order = self.broker.place_order(target_symbol, decision, quantity=qty, price=trade_price)
            print(f"[{now_str}] [TRADE EXECUTED] {decision} {qty} {target_symbol} @ Rs.{trade_price} | Order: {order}")

        ai_verdict["symbol"] = target_symbol
        self.last_ai_verdict = ai_verdict
        return ai_verdict

    async def background_trading_loop(self, interval_seconds: int = 60):
        print(f"[Engine] Background autonomous trading loop active (every {interval_seconds}s)")
        while True:
            try:
                if self.is_active:
                    await self.run_analysis_cycle()
            except Exception as e:
                print(f"[Engine Loop Error]: {e}")
            await asyncio.sleep(interval_seconds)
