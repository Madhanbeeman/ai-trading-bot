import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from datetime import datetime
from core.config import settings

def create_app(bot_manager=None) -> FastAPI:
    app = FastAPI(title="AI Trader Mobile Engine")

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
            "broker_connected": bot_manager.broker.connected if bot_manager else False
        }

    @app.get("/api/dashboard")
    def get_dashboard_data():
        if not bot_manager:
            return {"status": "uninitialized"}

        balance = bot_manager.broker.get_balance()
        positions = bot_manager.broker.get_open_positions()
        history = getattr(bot_manager.broker, "order_history", [])
        last_ai = getattr(bot_manager, "last_ai_verdict", {
            "decision": "HOLD",
            "confidence": 50,
            "reason": "AI monitoring technical indicators (RSI, EMA, MACD)...",
            "suggested_sl": 0,
            "suggested_target": 0,
            "symbol": settings.DEFAULT_SYMBOL
        })

        return {
            "mode": "PAPER" if settings.PAPER_TRADING else "LIVE",
            "balance": balance,
            "positions": positions,
            "history": history,
            "ai": last_ai,
            "timestamp": datetime.now().isoformat()
        }

    @app.post("/api/analyze")
    async def trigger_analysis():
        if bot_manager:
            res = await bot_manager.run_analysis_cycle()
            bot_manager.last_ai_verdict = res
            return {"status": "success", "result": res}
        return {"status": "error", "message": "Bot not attached"}

    @app.post("/api/kill")
    def trigger_emergency_kill():
        if bot_manager:
            closed = bot_manager.broker.close_all_positions()
            return {"status": "success", "closed_positions": len(closed)}
        return {"status": "error"}

    return app
