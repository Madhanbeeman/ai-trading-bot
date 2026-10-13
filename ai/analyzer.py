import json
import urllib.request
from typing import Dict, Any
from core.config import settings

class AIAgentAnalyzer:
    """
    AI Market Brain using Google Gemini 2.5 Flash via REST API.
    Evaluates real-time market technicals, confidence, and trade validity.
    """

    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.model_name = settings.GEMINI_MODEL or "gemini-2.5-flash"
        self.endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent?key={self.api_key}"

    def analyze_market(self, symbol: str, tech_summary: Dict[str, Any]) -> Dict[str, Any]:
        """
        Submits market technical indicators to Gemini AI and gets a structured decision.
        """
        if not self.api_key or self.api_key == "your_gemini_api_key_here":
            return self._fallback_rule_based_analysis(symbol, tech_summary)

        prompt = f"""
You are an expert Quantitative Algorithmic Trading AI specializing in Indian Stock Market & Options.
Analyze these real-time technical indicators for '{symbol}':

Technical Indicators:
- Current Price: {tech_summary.get('current_price')}
- RSI (14): {tech_summary.get('rsi')}
- EMA 9: {tech_summary.get('ema_9')}
- EMA 21: {tech_summary.get('ema_21')}
- EMA Trend: {tech_summary.get('ema_trend')}
- EMA Bullish Cross: {tech_summary.get('ema_crossover_bullish')}
- EMA Bearish Cross: {tech_summary.get('ema_crossover_bearish')}
- MACD: {tech_summary.get('macd')} | Signal: {tech_summary.get('macd_signal')}
- ATR (Volatility): {tech_summary.get('atr')}
- Volume: {tech_summary.get('volume')}

Evaluate the probability of a profitable setup.
Return ONLY valid JSON matching this exact format:
{{
    "decision": "BUY" | "SELL" | "HOLD",
    "confidence": integer between 0 and 100,
    "suggested_sl": float stop loss price,
    "suggested_target": float target price,
    "reason": "Clear concise 2-sentence explanation of why this decision was made",
    "risk_level": "LOW" | "MEDIUM" | "HIGH"
}}
"""

        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "response_mime_type": "application/json",
                "temperature": 0.2
            }
        }

        try:
            req = urllib.request.Request(
                self.endpoint,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=15) as response:
                result = json.loads(response.read().decode("utf-8"))
                text = result["candidates"][0]["content"]["parts"][0]["text"].strip()
                data = json.loads(text)
                return data
        except Exception as e:
            print(f"[AI] Gemini REST call exception: {e}, using quantitative fallback.")
            return self._fallback_rule_based_analysis(symbol, tech_summary)

    def _fallback_rule_based_analysis(self, symbol: str, tech: Dict[str, Any]) -> Dict[str, Any]:
        price = tech.get("current_price", 100.0)
        rsi = tech.get("rsi", 50.0)
        ema_trend = tech.get("ema_trend", "NEUTRAL")
        atr = tech.get("atr", price * 0.01)

        decision = "HOLD"
        confidence = 50
        reason = "Market consolidating. No clear breakout."
        risk_level = "LOW"

        if ema_trend == "BULLISH" and rsi > 45 and rsi < 68 and tech.get("macd", 0) > tech.get("macd_signal", 0):
            decision = "BUY"
            confidence = 82 if tech.get("ema_crossover_bullish") else 76
            reason = f"Bullish momentum: Price above EMA 21, RSI ({rsi}) healthy, MACD positive."
            risk_level = "LOW"
        elif ema_trend == "BEARISH" and rsi < 55 and rsi > 30 and tech.get("macd", 0) < tech.get("macd_signal", 0):
            decision = "SELL"
            confidence = 80 if tech.get("ema_crossover_bearish") else 75
            reason = f"Bearish momentum: Price below EMA 21, RSI ({rsi}) declining, MACD negative."
            risk_level = "MEDIUM"

        sl = price - (atr * 1.5) if decision == "BUY" else price + (atr * 1.5)
        target = price + (atr * 2.5) if decision == "BUY" else price - (atr * 2.5)

        return {
            "decision": decision,
            "confidence": confidence,
            "suggested_sl": round(sl, 2),
            "suggested_target": round(target, 2),
            "reason": reason,
            "risk_level": risk_level
        }
