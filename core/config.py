import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # App Settings
    APP_NAME: str = "AITrader"
    DEBUG: bool = False
    
    # Paper Trading
    PAPER_TRADING: bool = os.getenv("PAPER_TRADING", "true").lower() == "true"
    INITIAL_PAPER_CAPITAL: float = float(os.getenv("INITIAL_PAPER_CAPITAL", "50000"))
    
    # Telegram
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_CHAT_ID: str = os.getenv("TELEGRAM_CHAT_ID", "")
    
    # Gemini AI
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    
    # Angel One SmartAPI
    ANGEL_API_KEY: str = os.getenv("ANGEL_API_KEY", "")
    ANGEL_CLIENT_CODE: str = os.getenv("ANGEL_CLIENT_CODE", "")
    ANGEL_PASSWORD: str = os.getenv("ANGEL_PASSWORD", "")
    ANGEL_TOTP_KEY: str = os.getenv("ANGEL_TOTP_KEY", "")
    
    # Risk Management
    MAX_DAILY_LOSS: float = float(os.getenv("MAX_DAILY_LOSS", "2000"))
    MAX_RISK_PER_TRADE_PERCENT: float = float(os.getenv("MAX_RISK_PER_TRADE_PERCENT", "2.0"))
    STOP_LOSS_PERCENT: float = float(os.getenv("STOP_LOSS_PERCENT", "1.0"))
    TARGET_PERCENT: float = float(os.getenv("TARGET_PERCENT", "2.0"))
    AI_CONFIDENCE_THRESHOLD: int = int(os.getenv("AI_CONFIDENCE_THRESHOLD", "75"))
    
    # Trading Defaults
    DEFAULT_SYMBOL: str = os.getenv("DEFAULT_SYMBOL", "NIFTY")
    DEFAULT_EXCHANGE: str = os.getenv("DEFAULT_EXCHANGE", "NSE")
    TIMEFRAME: str = os.getenv("TIMEFRAME", "5m")

settings = Settings()
