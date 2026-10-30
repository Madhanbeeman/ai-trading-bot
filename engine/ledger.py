import json
import os
import time
import random
from typing import Dict, Any, List

from config.settings import (
    DB_FILE,
    ANGEL_INITIAL_CAPITAL,
    COINDCX_INITIAL_CAPITAL,
    TOTAL_INITIAL_CAPITAL,
    ANGEL_STOCKS_POOL,
    ANGEL_OPTIONS_POOL,
    COINDCX_SPOT_POOL,
    COINDCX_FUTURES_POOL,
    format_ist_time,
    format_ist_date,
    get_ist_now
)
from brokers.feed import get_live_market_data, get_micro_tick

def create_position(category: str, item: Dict[str, Any], market_quotes: Dict[str, Any]) -> Dict[str, Any]:
    """Creates a position with live entry price, target, and stop-loss."""
    now_str = format_ist_time()
    pos_id = f"{category}_{int(time.time() * 1000)}_{random.randint(100, 999)}"

    if category == "angel_stocks":
        code = item["symbol"]
        real_p = market_quotes.get("nse", {}).get(code, item["base_price"])
        entry = round(real_p, 2)
        target = round(entry * item["target_mult"], 2)
        sl = round(entry * item["sl_mult"], 2)
        return {
            "id": pos_id,
            "category": category,
            "broker": "angel",
            "symbol": item["symbol"],
            "name": item["name"],
            "segment": item["segment"],
            "date": f"Today {now_str}",
            "entry_time": now_str,
            "entry_price": entry,
            "cmp": entry,
            "qty_desc": item["qty_desc"],
            "margin": item["margin"],
            "target": target,
            "sl": sl,
            "pnl": 0.0,
            "pct": 0.0,
            "status": "🟢 TARGET APPROACHING"
        }

    elif category == "angel_options":
        entry = get_micro_tick(item["entry_prem"], 0.10)
        target = item["target_prem"]
        sl = item["sl_prem"]
        return {
            "id": pos_id,
            "category": category,
            "broker": "angel",
            "symbol": item["symbol"],
            "name": item["name"],
            "segment": item["segment"],
            "badge": item["badge"],
            "badge_bg": item["badge_bg"],
            "badge_color": item["badge_color"],
            "date": f"Today {now_str}",
            "entry_time": now_str,
            "entry_price": entry,
            "cmp": entry,
            "lot_desc": item["lot_desc"],
            "invested": item["invested"],
            "mult": item["mult"],
            "target": target,
            "sl": sl,
            "pnl": 0.0,
            "pct": 0.0,
            "status": "🔥 HERO SPIKE ACTIVE"
        }

    elif category == "coindcx_spot":
        market = item["market"]
        real_p = market_quotes.get("coindcx", {}).get(market, item["fallback_price"])
        entry = round(real_p, 2)
        target = round(entry * (1.0 + item["target_pct"]), 2)
        sl = round(entry * (1.0 + item["sl_pct"]), 2)
        return {
            "id": pos_id,
            "category": category,
            "broker": "coindcx",
            "symbol": item["symbol"],
            "name": item["name"],
            "segment": item["segment"],
            "date": f"Today {now_str}",
            "entry_time": now_str,
            "entry_price": entry,
            "cmp": entry,
            "cost": item["cost"],
            "qty": item["qty"],
            "target": target,
            "sl": sl,
            "pnl": 0.0,
            "pct": 0.0,
            "status": "🟢 SPOT HOLDING"
        }

    elif category == "coindcx_futures":
        market = item["market"]
        real_p = market_quotes.get("coindcx", {}).get(market, item["fallback_price"])
        entry = round(real_p, 2)
        target = round(entry * (1.0 + item["target_pct"]), 2)
        sl = round(entry * (1.0 + item["sl_pct"]), 2)
        return {
            "id": pos_id,
            "category": category,
            "broker": "coindcx",
            "symbol": item["symbol"],
            "name": item["name"],
            "segment": item["segment"],
            "badge": item["badge"],
            "badge_bg": item["badge_bg"],
            "badge_color": item["badge_color"],
            "date": f"Today {now_str}",
            "entry_time": now_str,
            "entry_price": entry,
            "cmp": entry,
            "margin": item["margin"],
            "lev": item["lev"],
            "target": target,
            "sl": sl,
            "pnl": 0.0,
            "pct": 0.0,
            "status": "⚡ 10X LEVERAGE RUN"
        }

    raise ValueError(f"Unknown category: {category}")

def get_clean_initial_state() -> Dict[str, Any]:
    """Generates initial clean paper ledger with ₹2,000 Angel One + ₹2,000 CoinDCX."""
    quotes = get_live_market_data()

    # Angel One Active Positions
    angel_stocks = [create_position("angel_stocks", ANGEL_STOCKS_POOL[i], quotes) for i in range(2)]
    angel_options = [create_position("angel_options", ANGEL_OPTIONS_POOL[i], quotes) for i in range(2)]
    angel_invested = sum(p["margin"] for p in angel_stocks) + sum(p["invested"] for p in angel_options)
    angel_cash = round(max(0.0, ANGEL_INITIAL_CAPITAL - angel_invested), 2)

    # CoinDCX Active Positions
    coindcx_spot = [create_position("coindcx_spot", COINDCX_SPOT_POOL[i], quotes) for i in range(2)]
    coindcx_futures = [create_position("coindcx_futures", COINDCX_FUTURES_POOL[i], quotes) for i in range(2)]
    coindcx_invested = sum(p["cost"] for p in coindcx_spot) + sum(p["margin"] for p in coindcx_futures)
    coindcx_cash = round(max(0.0, COINDCX_INITIAL_CAPITAL - coindcx_invested), 2)

    return {
        "version": "2.0_clean",
        "initial_capital": TOTAL_INITIAL_CAPITAL,
        "accounts": {
            "angel": ANGEL_INITIAL_CAPITAL,
            "coindcx": COINDCX_INITIAL_CAPITAL
        },
        "wallets": {
            "angel_cash": angel_cash,
            "coindcx_cash": coindcx_cash
        },
        "active_positions": {
            "angel_stocks": angel_stocks,
            "angel_options": angel_options,
            "coindcx_spot": coindcx_spot,
            "coindcx_futures": coindcx_futures
        },
        "closed_trades": []
    }

def save_engine_state(state: Dict[str, Any]) -> None:
    """Safely saves engine state to JSON database file."""
    try:
        os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
    except Exception:
        pass

def load_engine_state() -> Dict[str, Any]:
    """Loads engine state from DB, ensuring schema validity and automatic clean reset."""
    if not os.path.exists(DB_FILE):
        state = get_clean_initial_state()
        save_engine_state(state)
        return state

    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Schema integrity check
            if data.get("version") != "2.0_clean" or "active_positions" not in data or "wallets" not in data:
                state = get_clean_initial_state()
                save_engine_state(state)
                return state
            return data
    except Exception:
        state = get_clean_initial_state()
        save_engine_state(state)
        return state

def reset_engine_state() -> Dict[str, Any]:
    """Forces complete reset of paper trading accounts to fresh ₹2,000 grant."""
    state = get_clean_initial_state()
    save_engine_state(state)
    return state

def clear_trade_history(state: Dict[str, Any]) -> None:
    """Empties the settled trade audit ledger."""
    state["closed_trades"] = []
    save_engine_state(state)

def square_off_position(state: Dict[str, Any], position_id: str) -> bool:
    """Manually squares off an active trade at CMP and credits funds back to wallet."""
    quotes = get_live_market_data()
    for cat, pos_list in state["active_positions"].items():
        for p in pos_list:
            if p["id"] == position_id:
                broker = p.get("broker", "angel")
                realized = p.get("pnl", 0.0)

                # Return principal margin/cost + realized PnL
                if broker == "angel":
                    invested = p.get("margin", p.get("invested", 100.0))
                    state["wallets"]["angel_cash"] = round(state["wallets"]["angel_cash"] + invested + realized, 2)
                elif broker == "coindcx":
                    invested = p.get("cost", p.get("margin", 100.0))
                    state["wallets"]["coindcx_cash"] = round(state["wallets"]["coindcx_cash"] + invested + realized, 2)

                # Add to closed trade audit ledger
                state["closed_trades"].append({
                    "symbol": p["symbol"],
                    "broker": broker,
                    "segment": p.get("segment", "MANUAL EXIT"),
                    "entry_price": p["entry_price"],
                    "exit_price": p["cmp"],
                    "pnl": realized,
                    "status": "⚡ SQUARE OFF",
                    "exit_time": format_ist_time(),
                    "date": format_ist_date()
                })

                pos_list.remove(p)

                # Replenish with fresh candidate from pool
                pools = {
                    "angel_stocks": ANGEL_STOCKS_POOL,
                    "angel_options": ANGEL_OPTIONS_POOL,
                    "coindcx_spot": COINDCX_SPOT_POOL,
                    "coindcx_futures": COINDCX_FUTURES_POOL
                }
                current_syms = [x["symbol"] for x in pos_list]
                candidates = [c for c in pools.get(cat, []) if c["symbol"] not in current_syms]
                if candidates:
                    pos_list.append(create_position(cat, candidates[0], quotes))

                save_engine_state(state)
                return True
    return False

def update_live_ticks_and_triggers(state: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Updates CMP for all active positions and triggers auto-exits on Target or Stop-Loss."""
    quotes = get_live_market_data()
    notifications = []
    today_str = format_ist_date()

    # 1. Update CMP & P&L for Angel Stocks
    for p in state["active_positions"].get("angel_stocks", []):
        sym = p["symbol"]
        real_cmp = quotes.get("nse", {}).get(sym)
        p["cmp"] = round(real_cmp, 2) if real_cmp else get_micro_tick(p["cmp"], 0.05)
        p["pnl"] = round(p["cmp"] - p["entry_price"], 2)
        p["pct"] = round((p["pnl"] / p["margin"]) * 100, 2)

    # 2. Update CMP & P&L for Angel Options
    for p in state["active_positions"].get("angel_options", []):
        p["cmp"] = get_micro_tick(p["cmp"], 0.12)
        p["pnl"] = round((p["cmp"] - p["entry_price"]) * p["mult"], 2)
        p["pct"] = round((p["pnl"] / p["invested"]) * 100, 1)

    # 3. Update CMP & P&L for CoinDCX Spot
    for p in state["active_positions"].get("coindcx_spot", []):
        m = p.get("symbol", "").replace(" / ", "").replace("INR", "INR")
        real_cmp = quotes.get("coindcx", {}).get(m)
        p["cmp"] = round(real_cmp, 2) if real_cmp else get_micro_tick(p["cmp"], 0.05)
        p["pnl"] = round((p["cmp"] - p["entry_price"]) * p["qty"], 2)
        p["pct"] = round((p["pnl"] / p["cost"]) * 100, 2)

    # 4. Update CMP & P&L for CoinDCX Futures
    for p in state["active_positions"].get("coindcx_futures", []):
        m = p.get("symbol", "").split(" / ")[0] + "INR"
        real_cmp = quotes.get("coindcx", {}).get(m)
        p["cmp"] = round(real_cmp, 2) if real_cmp else get_micro_tick(p["cmp"], 0.05)
        p["pnl"] = round(((p["cmp"] - p["entry_price"]) / p["entry_price"]) * p["margin"] * p["lev"], 2)
        p["pct"] = round((p["pnl"] / p["margin"]) * 100, 1)

    # 5. Autonomous Target / SL Check
    pools = {
        "angel_stocks": (2, ANGEL_STOCKS_POOL),
        "angel_options": (2, ANGEL_OPTIONS_POOL),
        "coindcx_spot": (2, COINDCX_SPOT_POOL),
        "coindcx_futures": (2, COINDCX_FUTURES_POOL)
    }

    for cat, pos_list in state["active_positions"].items():
        rem = []
        for p in pos_list:
            target = p.get("target", 0)
            sl = p.get("sl", 0)
            cmp_v = p.get("cmp", 0)
            entry_v = p.get("entry_price", 0)

            hit_target = target > 0 and cmp_v >= target and cmp_v > entry_v
            hit_sl = sl > 0 and cmp_v <= sl and cmp_v < entry_v

            if hit_target or hit_sl:
                broker = p.get("broker", "angel")
                realized = p.get("pnl", 0.0)
                status = "🎯 TARGET HIT" if hit_target else "🛡️ STOP LOSS"

                if broker == "angel":
                    invested = p.get("margin", p.get("invested", 100.0))
                    state["wallets"]["angel_cash"] = round(state["wallets"]["angel_cash"] + invested + realized, 2)
                elif broker == "coindcx":
                    invested = p.get("cost", p.get("margin", 100.0))
                    state["wallets"]["coindcx_cash"] = round(state["wallets"]["coindcx_cash"] + invested + realized, 2)

                state["closed_trades"].append({
                    "symbol": p["symbol"],
                    "broker": broker,
                    "segment": p.get("segment", "AUTO EXIT"),
                    "entry_price": entry_v,
                    "exit_price": cmp_v,
                    "pnl": realized,
                    "status": status,
                    "exit_time": format_ist_time(),
                    "date": today_str
                })
                notifications.append({"msg": f"{status}: {p['symbol']} ({'+' if realized>=0 else ''}₹{realized:,.2f})", "is_win": hit_target})
            else:
                rem.append(p)

        # Auto-replenish to maintain exact slot target
        target_slots, pool = pools.get(cat, (2, []))
        while len(rem) < target_slots:
            cur_syms = [x["symbol"] for x in rem]
            cand = [c for c in pool if c["symbol"] not in cur_syms]
            if cand:
                rem.append(create_position(cat, cand[0], quotes))
            else:
                break

        state["active_positions"][cat] = rem

    save_engine_state(state)
    return notifications
