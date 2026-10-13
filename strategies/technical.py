import pandas as pd
import numpy as np
from typing import Dict, Any

class TechnicalAnalyzer:
    """Computes technical indicators from OHLCV candle data."""

    @staticmethod
    def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
        if df.empty or len(df) < 20:
            return df

        df = df.copy()

        # Exponential Moving Averages (EMA 9 & 21) using pure pandas
        df["ema_9"] = df["close"].ewm(span=9, adjust=False).mean()
        df["ema_21"] = df["close"].ewm(span=21, adjust=False).mean()

        # Relative Strength Index (RSI 14) using pure pandas
        delta = df["close"].diff()
        gain = delta.where(delta > 0, 0.0)
        loss = -delta.where(delta < 0, 0.0)
        avg_gain = gain.rolling(window=14).mean()
        avg_loss = loss.rolling(window=14).mean()
        rs = avg_gain / (avg_loss + 1e-9)
        df["rsi"] = 100.0 - (100.0 / (1.0 + rs))

        # MACD (12, 26, 9)
        ema_12 = df["close"].ewm(span=12, adjust=False).mean()
        ema_26 = df["close"].ewm(span=26, adjust=False).mean()
        df["macd"] = ema_12 - ema_26
        df["macd_signal"] = df["macd"].ewm(span=9, adjust=False).mean()
        df["macd_diff"] = df["macd"] - df["macd_signal"]

        # Average True Range (ATR 14)
        high_low = df["high"] - df["low"]
        high_close = (df["high"] - df["close"].shift()).abs()
        low_close = (df["low"] - df["close"].shift()).abs()
        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        df["atr"] = tr.rolling(window=14).mean()

        return df

    @classmethod
    def get_market_summary(cls, df: pd.DataFrame) -> Dict[str, Any]:
        """Summarizes the latest indicator values for AI consumption."""
        if df.empty or len(df) < 20:
            return {}

        df = cls.add_indicators(df)
        last = df.iloc[-1]
        prev = df.iloc[-2]

        current_price = float(last["close"])
        ema_9 = float(last["ema_9"])
        ema_21 = float(last["ema_21"])
        rsi = float(last["rsi"])
        atr = float(last["atr"])

        # Determine basic technical trend
        ema_cross_bullish = bool(prev["ema_9"] <= prev["ema_21"] and last["ema_9"] > last["ema_21"])
        ema_cross_bearish = bool(prev["ema_9"] >= prev["ema_21"] and last["ema_9"] < last["ema_21"])

        return {
            "current_price": round(current_price, 2),
            "rsi": round(rsi, 2),
            "ema_9": round(ema_9, 2),
            "ema_21": round(ema_21, 2),
            "ema_trend": "BULLISH" if ema_9 > ema_21 else "BEARISH",
            "ema_crossover_bullish": ema_cross_bullish,
            "ema_crossover_bearish": ema_cross_bearish,
            "macd": round(float(last["macd"]), 3),
            "macd_signal": round(float(last["macd_signal"]), 3),
            "atr": round(atr, 2),
            "volume": int(last["volume"]),
            "price_change_last_candle": round(float(last["close"] - prev["close"]), 2)
        }
