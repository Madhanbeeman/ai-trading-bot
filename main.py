import asyncio
import uvicorn
import os
from core.engine import BotEngine
from web.server import create_app

async def main():
    # 1. Initialize Bot Engine
    engine = BotEngine()
    await engine.initialize()

    # 2. Setup FastAPI App
    app = create_app(bot_manager=engine)

    # 3. Start background trading scheduler task
    trading_task = asyncio.create_task(engine.background_trading_loop(interval_seconds=60))

    # 4. Start Uvicorn Server
    port = int(os.getenv("PORT", 8000))
    config = uvicorn.Config(app=app, host="0.0.0.0", port=port, log_level="info")
    server = uvicorn.Server(config)

    print(f"[Server] Bot Server is live on port {port}!")
    try:
        await server.serve()
    finally:
        trading_task.cancel()
        await engine.telegram.stop()

if __name__ == "__main__":
    asyncio.run(main())
