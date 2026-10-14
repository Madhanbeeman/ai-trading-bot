import asyncio
import uvicorn
import os
import urllib.request
from core.engine import BotEngine
from web.server import create_app

async def self_keep_alive(port: int, interval_seconds: int = 300):
    """Pings localhost/health periodically so cloud background task never idles out."""
    await asyncio.sleep(10)
    url = f"http://127.0.0.1:{port}/health"
    while True:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "RenderKeepAlive/1.0"})
            with urllib.request.urlopen(req, timeout=10):
                pass
        except Exception:
            pass
        await asyncio.sleep(interval_seconds)

async def main():
    port = int(os.getenv("PORT", 8000))

    # 1. Initialize Bot Engine
    engine = BotEngine()
    await engine.initialize()

    # 2. Setup FastAPI App
    app = create_app(bot_manager=engine)

    # 3. Start background trading loop
    trading_task = asyncio.create_task(engine.background_trading_loop(interval_seconds=60))

    # 4. Start keep-alive pinger (keeps free tier alive)
    keep_alive_task = asyncio.create_task(self_keep_alive(port=port, interval_seconds=300))

    # 5. Start Uvicorn Server
    config = uvicorn.Config(app=app, host="0.0.0.0", port=port, log_level="info")
    server = uvicorn.Server(config)

    print(f"[Server] Mobile Web Terminal running on port {port}!")
    try:
        await server.serve()
    finally:
        trading_task.cancel()
        keep_alive_task.cancel()

if __name__ == "__main__":
    asyncio.run(main())
