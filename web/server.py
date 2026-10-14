import os
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from datetime import datetime
from core.config import settings

def create_app(bot_manager=None) -> FastAPI:
    app = FastAPI(title="AI Trader Real-Time Terminal")

    template_path = os.path.join(os.path.dirname(__file__), "templates", "dashboard.html")

    @app.get("/", response_class=HTMLResponse)
    def render_mobile_dashboard():
        if os.path.exists(template_path):
            with open(template_path, "r", encoding="utf-8") as f:
                return f.read()
        return "<h3>Mobile Dashboard Template Not Found</h3>"

    @app.get("/health")
    def health_check():
        return {
            "healthy": True,
            "is_active": bot_manager.is_active if bot_manager else False,
            "daily_target_reached": bot_manager.daily_target_reached if bot_manager else False
        }

    # ==========================================
    # WEBSOCKET REAL-TIME STREAMING (0ms LAG)
    # ==========================================
    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        await websocket.accept()
        try:
            while True:
                if bot_manager:
                    # Collect real-time payload
                    balance = bot_manager.broker.get_balance()
                    positions = bot_manager.broker.get_open_positions()
                    history = getattr(bot_manager.broker, "order_history", [])
                    ai = bot_manager.last_ai_verdict
                    
                    data = {
                        "type": "TICK",
                        "timestamp": datetime.now().strftime("%H:%M:%S"),
                        "mode": "PAPER" if settings.PAPER_TRADING else "LIVE",
                        "balance": balance,
                        "positions": positions,
                        "history": history[-10:] if history else [],
                        "ai": ai,
                        "daily_stats": {
                            "daily_profit": round(bot_manager.daily_realized_pnl, 2),
                            "daily_target": 200.0,
                            "target_reached": bot_manager.daily_target_reached,
                            "progress_pct": min(100, max(0, round((bot_manager.daily_realized_pnl / 200.0) * 100, 1)))
                        }
                    }
                    await websocket.send_json(data)
                await asyncio.sleep(1) # Stream updates every 1 second
        except WebSocketDisconnect:
            pass
        except Exception as e:
            print(f"[WS Error]: {e}")

    @app.post("/api/analyze")
    async def trigger_analysis():
        if bot_manager:
            res = await bot_manager.run_analysis_cycle()
            return {"status": "success", "result": res}
        return {"status": "error"}

    @app.post("/api/kill")
    def trigger_emergency_kill():
        if bot_manager:
            closed = bot_manager.broker.close_all_positions()
            return {"status": "success", "closed_positions": len(closed)}
        return {"status": "error"}

    return app
