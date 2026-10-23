import asyncio
import time
from core.engine import BotEngine

async def run_forever():
    print("[Background Runner] Starting 24/7 Trading Engine...")
    engine = BotEngine()
    await engine.initialize()
    await engine.background_trading_loop(interval_seconds=10)

if __name__ == "__main__":
    while True:
        try:
            asyncio.run(run_forever())
        except Exception as e:
            print(f"[Runner Crash Recovery]: {e}. Restarting in 5s...")
            time.sleep(5)
