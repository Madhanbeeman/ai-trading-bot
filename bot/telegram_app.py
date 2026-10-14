import asyncio
from typing import Optional, Callable
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from core.config import settings

class TelegramMobileController:
    """
    Mobile Telegram Controller interface.
    Allows user to monitor, control, start, stop, and emergency-kill trades
    directly from Telegram mobile app with auto-reconnect on network drops.
    """

    def __init__(self, bot_manager=None):
        self.token = settings.TELEGRAM_BOT_TOKEN
        self.chat_id = settings.TELEGRAM_CHAT_ID
        self.bot_manager = bot_manager
        self.app = None
        self.is_running = False

    async def start(self):
        if not self.token or self.token == "your_telegram_bot_token_here":
            print("[Telegram] Bot Token not configured in .env. Mobile alerts disabled.")
            return

        try:
            self.app = ApplicationBuilder().token(self.token).build()

            # Register handlers
            self.app.add_handler(CommandHandler("start", self.cmd_start))
            self.app.add_handler(CommandHandler("status", self.cmd_status))
            self.app.add_handler(CommandHandler("positions", self.cmd_positions))
            self.app.add_handler(CommandHandler("analyze", self.cmd_analyze))
            self.app.add_handler(CommandHandler("kill", self.cmd_kill))
            self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_quick_buttons))

            # Add global error handler to prevent crashing
            self.app.add_error_handler(self.error_handler)

            await self.app.initialize()
            await self.app.start()
            # drop_pending_updates cleans up conflict from prior dead connections
            await self.app.updater.start_polling(drop_pending_updates=True, poll_interval=1.0)
            self.is_running = True
            print("[Telegram] Mobile Bot controller is active and listening for commands!")

            # Send a notification that bot is online
            if self.chat_id:
                try:
                    await self.app.bot.send_message(
                        chat_id=self.chat_id,
                        text="🟢 *Bot Cloud Service is Active & Listening!*",
                        parse_mode="Markdown"
                    )
                except Exception as e:
                    print(f"[Telegram] Initial greeting failed: {e}")

        except Exception as e:
            print(f"[Telegram] Failed to start Telegram polling: {e}")

    async def error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Log errors caused by updates."""
        print(f"[Telegram Error Handler] Exception while handling update: {context.error}")

    async def stop(self):
        if self.app and self.is_running:
            try:
                await self.app.updater.stop()
                await self.app.stop()
                await self.app.shutdown()
            except Exception as e:
                print(f"[Telegram] Error during shutdown: {e}")
            self.is_running = False

    async def send_alert(self, message: str):
        """Sends broadcast alert to user's phone."""
        if not self.app or not self.chat_id:
            return
        try:
            await self.app.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode="Markdown"
            )
        except Exception as e:
            print(f"[Telegram] Error sending alert: {e}")

    # --- Commands ---
    async def cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = [
            ["📊 Status", "📈 Open Positions"],
            ["🧠 AI Analyze Now", "🌐 Web Dashboard"],
            ["🚨 Emergency Kill Switch"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        welcome_text = (
            "🤖 *AI Trading Bot - Mobile Controller*\n\n"
            "வணக்கம்! உங்க Trading Bot Mobile Control Panel தயார்.\n\n"
            f"• Mode: *{'PAPER TRADING (Virtual)' if settings.PAPER_TRADING else 'LIVE TRADING'}*\n"
            f"• Default Symbol: *{settings.DEFAULT_SYMBOL}*\n"
            f"• Confidence Threshold: *{settings.AI_CONFIDENCE_THRESHOLD}%*\n\n"
            "கீழே உள்ள பட்டன்களை பயன்படுத்தி கட்டுப்படுத்தலாம்:"
        )
        if update and update.message:
            await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

    async def cmd_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not self.bot_manager:
            if update and update.message:
                await update.message.reply_text("Bot Engine not attached.")
            return

        balance = self.bot_manager.broker.get_balance()
        mode_str = "🟢 PAPER TRADING (Safe)" if settings.PAPER_TRADING else "🔴 LIVE TRADING"
        
        status_msg = (
            f"📊 *Bot Status Report*\n\n"
            f"• Mode: {mode_str}\n"
            f"• Available Cash: ₹{balance.get('available_cash', 0):,}\n"
            f"• Unrealized P&L: ₹{balance.get('unrealized_pnl', 0):,}\n"
            f"• Total Equity: ₹{balance.get('total_equity', balance.get('available_cash', 0)):,}\n"
            f"• Auto-Trading: {'Active ✅' if self.bot_manager.is_active else 'Paused ⏸️'}"
        )
        if update and update.message:
            await update.message.reply_text(status_msg, parse_mode="Markdown")

    async def cmd_positions(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not self.bot_manager:
            return
        positions = self.bot_manager.broker.get_open_positions()
        if not positions:
            if update and update.message:
                await update.message.reply_text("ℹ️ தற்போது எந்த Open Positions-ம் இல்லை.")
            return

        msg = "📈 *Current Open Positions:*\n\n"
        for p in positions:
            msg += (
                f"• *{p.get('symbol')}*\n"
                f"  Qty: {p.get('quantity')} | Entry: ₹{p.get('entry_price')}\n"
                f"  Unrealized PnL: ₹{p.get('unrealized_pnl', 0)}\n\n"
            )
        if update and update.message:
            await update.message.reply_text(msg, parse_mode="Markdown")

    async def cmd_analyze(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update and update.message:
            await update.message.reply_text("⏳ AI Market-ஐ Analyze செய்கிறது... காத்திருக்கவும்.")
        if self.bot_manager:
            res = await self.bot_manager.run_analysis_cycle()
            if res and update and update.message:
                trade_txt = (
                    f"🧠 *AI Analysis Result ({res.get('symbol')}):*\n\n"
                    f"• *Decision:* `{res.get('decision')}`\n"
                    f"• *Confidence:* `{res.get('confidence')}%`\n"
                    f"• *SL:* ₹{res.get('suggested_sl')} | *Target:* ₹{res.get('suggested_target')}\n"
                    f"• *Reason:* {res.get('reason')}\n"
                    f"• *Risk Level:* {res.get('risk_level')}"
                )
                await update.message.reply_text(trade_txt, parse_mode="Markdown")

    async def cmd_kill(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if self.bot_manager:
            closed = self.bot_manager.broker.close_all_positions()
            if update and update.message:
                await update.message.reply_text(f"🚨 *Emergency Kill Triggered!* Closed {len(closed)} open positions.", parse_mode="Markdown")

    async def handle_quick_buttons(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update or not update.message:
            return
        text = update.message.text
        if text == "📊 Status":
            await self.cmd_status(update, context)
        elif text == "📈 Open Positions":
            await self.cmd_positions(update, context)
        elif text == "🧠 AI Analyze Now":
            await self.cmd_analyze(update, context)
        elif text == "🌐 Web Dashboard":
            await update.message.reply_text("🌐 *Mobile Web Dashboard:*\n\nஉங்க Render Cloud Service Dashboard URL-ஐ மொபைல் பிரவுசரில் open செய்து பாருங்கள்!", parse_mode="Markdown")
        elif text == "🚨 Emergency Kill Switch":
            await self.cmd_kill(update, context)
