import streamlit as st
import time

# -------------------------------------------------------------
# 1. APPLICATION SETUP & PAGE CONFIG
# -------------------------------------------------------------
st.set_page_config(
    page_title="Fintech Pro",
    page_icon="assets/logo.png",
    layout="centered",
    initial_sidebar_state="collapsed"
)

from config.settings import (
    ANGEL_INITIAL_CAPITAL,
    COINDCX_INITIAL_CAPITAL,
    TOTAL_INITIAL_CAPITAL
)
from engine.ledger import (
    load_engine_state,
    reset_engine_state,
    square_off_position,
    clear_trade_history,
    open_new_position,
    update_live_ticks_and_triggers
)
from ui.theme import get_custom_css
from ui.components import (
    render_html,
    render_header,
    render_portfolio_hero,
    render_sub_tabs,
    render_position_card,
    render_history_card,
    render_bottom_nav
)

# -------------------------------------------------------------
# 2. QUERY PARAMS & THEME EXTRACTION
# -------------------------------------------------------------
# 2. QUERY PARAMS & THEME EXTRACTION (WITH SESSION PERSISTENCE)
# -------------------------------------------------------------
if "app_theme" not in st.session_state:
    st.session_state["app_theme"] = "dark"

active_tab = "home"
sub_tab = ""
req_action = None
req_cid = None
req_cat = None

try:
    if hasattr(st, "query_params"):
        q_tab = st.query_params.get("tab", "home")
        active_tab = q_tab[0] if isinstance(q_tab, list) else str(q_tab)

        q_sub = st.query_params.get("sub", "")
        sub_tab = q_sub[0] if isinstance(q_sub, list) else str(q_sub)

        q_theme = st.query_params.get("theme", None)
        if q_theme is not None:
            t_str = (q_theme[0] if isinstance(q_theme, list) else str(q_theme)).strip().lower()
            if t_str in ["light", "dark"]:
                st.session_state["app_theme"] = t_str

        q_act = st.query_params.get("action", None)
        req_action = q_act[0] if isinstance(q_act, list) else q_act

        q_cid = st.query_params.get("cid", None)
        req_cid = q_cid[0] if isinstance(q_cid, list) else q_cid

        q_cat = st.query_params.get("cat", None)
        req_cat = q_cat[0] if isinstance(q_cat, list) else q_cat
    else:
        params = st.experimental_get_query_params()
        if "tab" in params and params["tab"]: active_tab = str(params["tab"][0])
        if "sub" in params and params["sub"]: sub_tab = str(params["sub"][0])
        if "theme" in params and params["theme"]:
            t_str = str(params["theme"][0]).strip().lower()
            if t_str in ["light", "dark"]:
                st.session_state["app_theme"] = t_str
        if "action" in params and params["action"]: req_action = str(params["action"][0])
        if "cid" in params and params["cid"]: req_cid = str(params["cid"][0])
        if "cat" in params and params["cat"]: req_cat = str(params["cat"][0])
except Exception:
    pass

current_theme = st.session_state.get("app_theme", "dark")
is_dark = current_theme != "light"
st.markdown(get_custom_css(is_dark), unsafe_allow_html=True)

# -------------------------------------------------------------
# 3. ENGINE STATE & ACTION DISPATCHER
# -------------------------------------------------------------
state = load_engine_state()

# Handle query actions
if req_action == "close" and req_cid:
    if square_off_position(state, req_cid):
        st.toast("⚡ Position Squared Off & Closed!", icon="✅")
    if hasattr(st, "query_params"):
        st.query_params.clear()
        st.query_params["tab"] = active_tab
        if sub_tab: st.query_params["sub"] = sub_tab
        st.query_params["theme"] = current_theme
    st.rerun()

elif req_action == "open_trade" and req_cat:
    if open_new_position(state, req_cat):
        st.toast("🚀 New Position Opened Successfully!", icon="📈")
    else:
        st.toast("⚠️ Insufficient Wallet Cash or All Pool Slots Active!", icon="⚠️")
    if hasattr(st, "query_params"):
        st.query_params.clear()
        st.query_params["tab"] = active_tab
        if sub_tab: st.query_params["sub"] = sub_tab
        st.query_params["theme"] = current_theme
    st.rerun()

elif req_action == "clear_history":
    clear_trade_history(state)
    st.toast("🧹 Trade Audit Ledger Cleared!", icon="🗑️")
    if hasattr(st, "query_params"):
        st.query_params.clear()
        st.query_params["tab"] = "history"
        st.query_params["theme"] = current_theme
    st.rerun()

elif req_action == "reset_paper":
    state = reset_engine_state()
    st.toast("🔄 Paper Accounts Reset to Fresh ₹2,000 Grant!", icon="✨")
    if hasattr(st, "query_params"):
        st.query_params.clear()
        st.query_params["tab"] = active_tab
        if sub_tab: st.query_params["sub"] = sub_tab
        st.query_params["theme"] = current_theme
    st.rerun()

# Real-time tick update and autonomous Target/SL trigger check
notifications = update_live_ticks_and_triggers(state)
for n in notifications:
    st.toast(n["msg"], icon="🎯" if n["is_win"] else "🛡️")

# -------------------------------------------------------------
# 4. PORTFOLIO TOTALS & METRICS CALCULATION
# -------------------------------------------------------------
# Angel One Totals
angel_stocks = state["active_positions"].get("angel_stocks", [])
angel_options = state["active_positions"].get("angel_options", [])
angel_invested = round(sum(p.get("margin", 0.0) for p in angel_stocks) + sum(p.get("invested", 0.0) for p in angel_options), 2)
angel_active_pnl = round(sum(p.get("pnl", 0.0) for p in angel_stocks + angel_options), 2)
angel_closed_pnl = round(sum(t.get("pnl", 0.0) for t in state.get("closed_trades", []) if t.get("broker") == "angel"), 2)
angel_wallet = round(state["wallets"].get("angel_cash", 0.0), 2)
angel_total_portfolio = round(angel_wallet + angel_invested + angel_active_pnl, 2)
angel_net_pnl = round(angel_total_portfolio - ANGEL_INITIAL_CAPITAL, 2)
angel_pct = round((angel_net_pnl / ANGEL_INITIAL_CAPITAL) * 100, 2)

# CoinDCX Totals
coindcx_spot = state["active_positions"].get("coindcx_spot", [])
coindcx_futures = state["active_positions"].get("coindcx_futures", [])
coindcx_invested = round(sum(p.get("cost", 0.0) for p in coindcx_spot) + sum(p.get("margin", 0.0) for p in coindcx_futures), 2)
coindcx_active_pnl = round(sum(p.get("pnl", 0.0) for p in coindcx_spot + coindcx_futures), 2)
coindcx_closed_pnl = round(sum(t.get("pnl", 0.0) for t in state.get("closed_trades", []) if t.get("broker") == "coindcx"), 2)
coindcx_wallet = round(state["wallets"].get("coindcx_cash", 0.0), 2)
coindcx_total_portfolio = round(coindcx_wallet + coindcx_invested + coindcx_active_pnl, 2)
coindcx_net_pnl = round(coindcx_total_portfolio - COINDCX_INITIAL_CAPITAL, 2)
coindcx_pct = round((coindcx_net_pnl / COINDCX_INITIAL_CAPITAL) * 100, 2)

# Overall Combined Portfolio Totals
total_portfolio = round(angel_total_portfolio + coindcx_total_portfolio, 2)
total_available = round(angel_wallet + coindcx_wallet, 2)
total_invested = round(angel_invested + coindcx_invested, 2)
total_net_pnl = round(total_portfolio - TOTAL_INITIAL_CAPITAL, 2)
total_pct = round((total_net_pnl / TOTAL_INITIAL_CAPITAL) * 100, 2)

# -------------------------------------------------------------
# 5. TAB 1: ⚡ HOME OVERVIEW
# -------------------------------------------------------------
if active_tab == "home":
    render_header("Fintech Pro", is_dark, "home")

    # Master Portfolio Hero
    render_portfolio_hero(
        title="Total Net Portfolio (₹4,000 Grant)",
        balance=total_portfolio,
        pnl=total_net_pnl,
        pct_gain=total_pct,
        available=total_available,
        invested=total_invested,
        is_dark=is_dark
    )

    # Broker Distribution Cards
    theme_arg = f"&theme={'dark' if is_dark else 'light'}"
    render_html(f"""
    <div style="font-size:12.5px; font-weight:700; color:{'#94a3b8' if is_dark else '#64748b'}; margin:16px 0 10px 0; text-transform:uppercase; letter-spacing:0.5px;">
        🏛️ Active Broker Accounts
    </div>
    
    <!-- Angel One Card -->
    <div class="trade-card" style="margin-bottom:12px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <div style="display:flex; align-items:center; gap:8px;">
                <span style="font-size:20px;">📈</span>
                <div>
                    <div style="font-size:15px; font-weight:800; color:{'#ffffff' if is_dark else '#0f172a'};">Angel One Demat</div>
                    <div style="font-size:11px; color:#94a3b8;">NSE Stocks & F&O Options</div>
                </div>
            </div>
            <span class="segment-tag" style="background:rgba(16,185,129,0.15); color:#10b981;">● ACTIVE</span>
        </div>
        <div class="metrics-grid">
            <div class="metric-col">
                <span class="metric-label">TOTAL VAL</span>
                <span class="metric-val">₹{angel_total_portfolio:,.2f}</span>
            </div>
            <div class="metric-col">
                <span class="metric-label">CASH</span>
                <span class="metric-val">₹{angel_wallet:,.2f}</span>
            </div>
            <div class="metric-col" style="text-align:right;">
                <span class="metric-label">P/L</span>
                <span class="metric-val" style="color:{'#10b981' if angel_net_pnl>=0 else '#ef4444'};">{'+' if angel_net_pnl>=0 else ''}₹{angel_net_pnl:,.2f}</span>
            </div>
        </div>
        <a href="?tab=angel{theme_arg}" target="_self" class="btn-action-primary" style="display:block; width:100%; text-align:center;">
            Open Angel One →
        </a>
    </div>

    <!-- CoinDCX Card -->
    <div class="trade-card">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <div style="display:flex; align-items:center; gap:8px;">
                <span style="font-size:20px;">🇮🇳</span>
                <div>
                    <div style="font-size:15px; font-weight:800; color:{'#ffffff' if is_dark else '#0f172a'};">CoinDCX India</div>
                    <div style="font-size:11px; color:#94a3b8;">24/7 Spot & 10x Futures</div>
                </div>
            </div>
            <span class="segment-tag" style="background:rgba(56,189,248,0.15); color:#38bdf8;">● ACTIVE</span>
        </div>
        <div class="metrics-grid">
            <div class="metric-col">
                <span class="metric-label">TOTAL VAL</span>
                <span class="metric-val">₹{coindcx_total_portfolio:,.2f}</span>
            </div>
            <div class="metric-col">
                <span class="metric-label">CASH</span>
                <span class="metric-val">₹{coindcx_wallet:,.2f}</span>
            </div>
            <div class="metric-col" style="text-align:right;">
                <span class="metric-label">P/L</span>
                <span class="metric-val" style="color:{'#10b981' if coindcx_net_pnl>=0 else '#ef4444'};">{'+' if coindcx_net_pnl>=0 else ''}₹{coindcx_net_pnl:,.2f}</span>
            </div>
        </div>
        <a href="?tab=coindcx{theme_arg}" target="_self" class="btn-action-primary" style="display:block; width:100%; text-align:center;">
            Open CoinDCX →
        </a>
    </div>
    """)

# -------------------------------------------------------------
# 6. TAB 2: 🇮🇳 COINDCX
# -------------------------------------------------------------
elif active_tab == "coindcx":
    cur_sub = sub_tab if sub_tab in ["spot", "futures"] else "spot"
    render_header("CoinDCX", is_dark, "coindcx", cur_sub)

    render_portfolio_hero(
        title="CoinDCX Portfolio (₹2,000 Grant)",
        balance=coindcx_total_portfolio,
        pnl=coindcx_net_pnl,
        pct_gain=coindcx_pct,
        available=coindcx_wallet,
        invested=coindcx_invested,
        is_dark=is_dark
    )

    render_sub_tabs(
        current_tab="coindcx",
        current_sub=cur_sub,
        options=[("spot", f"💎 Spot Holdings ({len(coindcx_spot)})"), ("futures", f"⚡ 10X Futures ({len(coindcx_futures)})")],
        is_dark=is_dark
    )

    category_key = "coindcx_spot" if cur_sub == "spot" else "coindcx_futures"
    positions = state["active_positions"].get(category_key, [])
    theme_arg = f"&theme={'dark' if is_dark else 'light'}"

    if positions:
        for pos in positions:
            render_position_card(pos, is_dark, "coindcx", cur_sub)
        if len(positions) < 2:
            open_url = f"?tab=coindcx&sub={cur_sub}&action=open_trade&cat={category_key}{theme_arg}"
            render_html(f"""
            <div style="margin-top:12px;">
                <a href="{open_url}" target="_self" class="btn-action-secondary" style="display:block; width:100%; text-align:center; padding:10px;">
                    + 🚀 Open Next CoinDCX Trade ({len(positions)}/2 Active)
                </a>
            </div>
            """)
    else:
        open_url = f"?tab=coindcx&sub={cur_sub}&action=open_trade&cat={category_key}{theme_arg}"
        render_html(f"""
        <div style="background:{'#0f172a' if is_dark else '#ffffff'}; border:1px dashed {'#334155' if is_dark else '#cbd5e1'}; border-radius:18px; padding:24px 16px; text-align:center; margin:14px 0;">
            <div style="font-size:26px; margin-bottom:6px;">💼</div>
            <div style="font-size:14px; font-weight:700; color:{'#f8fafc' if is_dark else '#0f172a'};">No Active Trades in this Segment</div>
            <div style="font-size:11.5px; color:#94a3b8; margin-top:4px; line-height:1.4;">
                All positions in this category are closed and cash is safely in your wallet.
            </div>
            <div style="margin-top:14px;">
                <a href="{open_url}" target="_self" class="btn-action-primary" style="display:inline-block; padding:8px 18px;">
                    + 🚀 Open Fresh Position
                </a>
            </div>
        </div>
        """)

# -------------------------------------------------------------
# 7. TAB 3: 📈 ANGEL ONE
# -------------------------------------------------------------
elif active_tab == "angel":
    cur_sub = sub_tab if sub_tab in ["stocks", "options"] else "stocks"
    render_header("Angel One", is_dark, "angel", cur_sub)

    render_portfolio_hero(
        title="Angel One Demat (₹2,000 Grant)",
        balance=angel_total_portfolio,
        pnl=angel_net_pnl,
        pct_gain=angel_pct,
        available=angel_wallet,
        invested=angel_invested,
        is_dark=is_dark
    )

    render_sub_tabs(
        current_tab="angel",
        current_sub=cur_sub,
        options=[("stocks", f"🏢 NSE Stocks ({len(angel_stocks)})"), ("options", f"🚀 Zero to Hero ({len(angel_options)})")],
        is_dark=is_dark
    )

    category_key = "angel_stocks" if cur_sub == "stocks" else "angel_options"
    positions = state["active_positions"].get(category_key, [])
    theme_arg = f"&theme={'dark' if is_dark else 'light'}"

    if positions:
        for pos in positions:
            render_position_card(pos, is_dark, "angel", cur_sub)
        if len(positions) < 2:
            open_url = f"?tab=angel&sub={cur_sub}&action=open_trade&cat={category_key}{theme_arg}"
            render_html(f"""
            <div style="margin-top:12px;">
                <a href="{open_url}" target="_self" class="btn-action-secondary" style="display:block; width:100%; text-align:center; padding:10px;">
                    + 🚀 Open Next Angel One Trade ({len(positions)}/2 Active)
                </a>
            </div>
            """)
    else:
        open_url = f"?tab=angel&sub={cur_sub}&action=open_trade&cat={category_key}{theme_arg}"
        render_html(f"""
        <div style="background:{'#0f172a' if is_dark else '#ffffff'}; border:1px dashed {'#334155' if is_dark else '#cbd5e1'}; border-radius:18px; padding:24px 16px; text-align:center; margin:14px 0;">
            <div style="font-size:26px; margin-bottom:6px;">💼</div>
            <div style="font-size:14px; font-weight:700; color:{'#f8fafc' if is_dark else '#0f172a'};">No Active Trades in this Segment</div>
            <div style="font-size:11.5px; color:#94a3b8; margin-top:4px; line-height:1.4;">
                All positions in this category are closed and cash is safely in your wallet.
            </div>
            <div style="margin-top:14px;">
                <a href="{open_url}" target="_self" class="btn-action-primary" style="display:inline-block; padding:8px 18px;">
                    + 🚀 Open Fresh Position
                </a>
            </div>
        </div>
        """)

# -------------------------------------------------------------
# 8. TAB 4: 📜 TRADE HISTORY & AUDIT LEDGER
# -------------------------------------------------------------
elif active_tab == "history":
    cur_sub = sub_tab if sub_tab in ["all", "angel", "coindcx"] else "all"
    render_header("Trade History", is_dark, "history", cur_sub)

    closed_all = state.get("closed_trades", [])
    if cur_sub == "angel":
        filtered_trades = [t for t in closed_all if t.get("broker") == "angel"]
    elif cur_sub == "coindcx":
        filtered_trades = [t for t in closed_all if t.get("broker") == "coindcx"]
    else:
        filtered_trades = closed_all

    tot_realized = round(sum(t.get("pnl", 0.0) for t in filtered_trades), 2)
    tot_count = len(filtered_trades)
    wins = len([t for t in filtered_trades if t.get("pnl", 0.0) >= 0])
    win_rate = round((wins / tot_count * 100), 1) if tot_count > 0 else 0.0

    # History Master Card
    is_p = tot_realized >= 0
    p_sign = "+" if is_p else ""
    theme_arg = f"&theme={'dark' if is_dark else 'light'}"

    render_html(f"""
    <div class="hero-card" style="padding:16px 18px;">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <span class="hero-label">Cumulative Realized Profit</span>
            <span style="background:rgba(16,185,129,0.14); color:#10b981; font-weight:700; font-size:10px; padding:2px 8px; border-radius:10px;">
                ● Win Rate: {win_rate:.1f}%
            </span>
        </div>
        <div class="hero-balance" style="margin-top:4px;">
            {p_sign}₹{tot_realized:,.2f}
            <span class="{'badge-gain' if is_p else 'badge-loss'}">{wins}/{tot_count} Won</span>
        </div>
    </div>
    """)

    render_sub_tabs(
        current_tab="history",
        current_sub=cur_sub,
        options=[
            ("all", f"🌐 All ({len(closed_all)})"),
            ("angel", f"📈 Angel ({len([t for t in closed_all if t.get('broker') == 'angel'])})"),
            ("coindcx", f"🇮🇳 CoinDCX ({len([t for t in closed_all if t.get('broker') == 'coindcx'])})")
        ],
        is_dark=is_dark
    )

    if filtered_trades:
        for t in reversed(filtered_trades):
            render_history_card(t, is_dark)
    else:
        render_html(f"""
        <div style="background:{'#0f172a' if is_dark else '#ffffff'}; border:1px dashed {'#334155' if is_dark else '#cbd5e1'}; border-radius:18px; padding:24px 16px; text-align:center; margin:16px 0;">
            <div style="font-size:26px; margin-bottom:6px;">⚡</div>
            <div style="font-size:14px; font-weight:700; color:{'#f8fafc' if is_dark else '#0f172a'};">No Settled Trades Yet</div>
            <div style="font-size:11.5px; color:#94a3b8; margin-top:4px; line-height:1.4;">
                Active trades are currently running live in Angel One and CoinDCX.<br>
                When a trade hits Target or Stop Loss, it will automatically archive here!
            </div>
            <div style="margin-top:14px; display:flex; gap:8px; justify-content:center;">
                <a href="?tab=angel{theme_arg}" target="_self" class="btn-action-primary" style="font-size:11px; padding:6px 14px;">
                    📈 Angel Active
                </a>
                <a href="?tab=coindcx{theme_arg}" target="_self" class="btn-action-primary" style="font-size:11px; padding:6px 14px;">
                    🇮🇳 CoinDCX Active
                </a>
            </div>
        </div>
        """)

    # Action Toolbar
    render_html(f"""
    <div style="display:flex; gap:10px; margin-top:14px;">
        <a href="?tab=history&action=clear_history{theme_arg}" target="_self" class="btn-action-secondary" style="flex:1;">
            🧹 Clear History
        </a>
        <a href="?tab=history&action=reset_paper{theme_arg}" target="_self" class="btn-action-primary" style="flex:1;">
            🔄 Reset Paper (₹4,000)
        </a>
    </div>
    """)

# -------------------------------------------------------------
# 9. BOTTOM NATIVE APP DOCK
# -------------------------------------------------------------
render_bottom_nav(active_tab, is_dark)
