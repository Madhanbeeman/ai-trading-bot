import streamlit as st
from config.settings import format_ist_clock

def render_html(html_str: str):
    """Safely renders HTML without Markdown indented-code-block interference."""
    clean = "\n".join(line.strip() for line in html_str.splitlines() if line.strip() and not line.strip().startswith("<!--"))
    st.markdown(clean, unsafe_allow_html=True)

def render_header(title: str, is_dark: bool, current_tab: str, sub_tab: str = ""):
    """Renders sleek top user bar with live clock and theme toggle."""
    clock_str = format_ist_clock()
    toggle_theme = "light" if is_dark else "dark"
    theme_icon = "☀️" if is_dark else "🌙"
    sub_param = f"&sub={sub_tab}" if sub_tab else ""

    render_html(f"""
    <div class="top-bar">
        <div class="brand-title">
            <span style="font-size:18px;">⚡</span> {title}
        </div>
        <div style="display:flex; align-items:center; gap:8px;">
            <div class="live-pulse-badge">
                <span class="radar-dot"></span> IST {clock_str}
            </div>
            <a href="?tab={current_tab}{sub_param}&theme={toggle_theme}" target="_self" class="theme-toggle-btn" title="Toggle Theme">
                {theme_icon}
            </a>
        </div>
    </div>
    """)

def render_portfolio_hero(title: str, balance: float, pnl: float, pct_gain: float, available: float, invested: float, is_dark: bool):
    """Renders the master balance hero card."""
    is_profit = pnl >= 0
    pnl_sign = "+" if is_profit else ""
    badge_cls = "badge-gain" if is_profit else "badge-loss"

    render_html(f"""
    <div class="hero-card">
        <div class="hero-label">{title}</div>
        <div class="hero-balance">
            ₹{balance:,.2f}
            <span class="{badge_cls}">{pnl_sign}₹{pnl:,.2f} ({pnl_sign}{pct_gain:.2f}%)</span>
        </div>
        <div class="vault-grid">
            <div class="vault-item">
                <div class="vault-sub-label">💵 Available Cash</div>
                <div class="vault-sub-val">₹{available:,.2f}</div>
            </div>
            <div class="vault-item">
                <div class="vault-sub-label">📊 Invested / Margin</div>
                <div class="vault-sub-val">₹{invested:,.2f}</div>
            </div>
        </div>
    </div>
    """)

def render_sub_tabs(current_tab: str, current_sub: str, options: list, is_dark: bool):
    """Renders modern segmented pill selector."""
    theme_arg = f"&theme={'dark' if is_dark else 'light'}"
    html = '<div class="tab-bar">'
    for val, label in options:
        active_cls = "tab-pill-active" if current_sub == val else "tab-pill-inactive"
        html += f'<a href="?tab={current_tab}&sub={val}{theme_arg}" target="_self" class="tab-pill {active_cls}">{label}</a>'
    html += '</div>'
    render_html(html)

def render_position_card(pos: dict, is_dark: bool, current_tab: str, current_sub: str = ""):
    """Renders high-finish active trade card with live CMP and square off action button."""
    pnl = round(pos.get("pnl", 0.0), 2)
    pct = round(pos.get("pct", 0.0), 2)

    # Bulletproof PnL formatting - NEVER print +₹-0.00
    if abs(pnl) < 0.005:
        pnl = 0.0
        pct = 0.0
        pnl_text = "₹0.00 (0.00%)"
        pnl_color = "#94a3b8"
    elif pnl > 0:
        pnl_text = f"+₹{pnl:,.2f} (+{pct:.2f}%)"
        pnl_color = "#10b981"
    else:
        pnl_text = f"-₹{abs(pnl):,.2f} ({pct:.2f}%)"
        pnl_color = "#ef4444"

    sub_arg = f"&sub={current_sub}" if current_sub else ""
    theme_arg = f"&theme={'dark' if is_dark else 'light'}"
    close_url = f"?tab={current_tab}{sub_arg}&action=close&cid={pos['id']}{theme_arg}"

    badge_html = ""
    if "badge" in pos:
        badge_html = f"""<span class="segment-tag" style="background:{pos.get('badge_bg', 'rgba(16,185,129,0.15)')}; color:{pos.get('badge_color', '#10b981')};">{pos['badge']}</span>"""
    else:
        badge_html = f"""<span class="segment-tag" style="background:rgba(56,189,248,0.15); color:#38bdf8;">{pos.get('segment', 'MARKET')}</span>"""

    render_html(f"""
    <div class="trade-card">
        <div class="trade-header">
            <div>
                <div class="symbol-title">{pos['symbol']}</div>
                <div style="font-size:11px; color:#94a3b8; font-weight:500; margin-top:1px;">{pos.get('name', '')} • {pos.get('date', 'Today')}</div>
            </div>
            {badge_html}
        </div>
        <div class="metrics-grid">
            <div class="metric-col">
                <span class="metric-label">ENTRY PRICE</span>
                <span class="metric-val">₹{pos['entry_price']:,.2f}</span>
            </div>
            <div class="metric-col">
                <span class="metric-label">CURRENT CMP</span>
                <span class="metric-val" style="color:#38bdf8;">₹{pos['cmp']:,.2f}</span>
            </div>
            <div class="metric-col" style="text-align:right;">
                <span class="metric-label">LIVE P/L</span>
                <span class="metric-val" style="color:{pnl_color}; font-size:12px;">{pnl_text}</span>
            </div>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center; font-size:11px; color:#94a3b8; margin-bottom:12px;">
            <span>🎯 Target: <b style="color:#10b981;">₹{pos.get('target', 0):,.2f}</b></span>
            <span>🛡️ Stop Loss: <b style="color:#ef4444;">₹{pos.get('sl', 0):,.2f}</b></span>
        </div>
        <a href="{close_url}" target="_self" class="btn-square-off">
            ⚡ Square Off Position
        </a>
    </div>
    """)

def render_history_card(trade: dict, is_dark: bool):
    """Renders settled trade audit ledger entry."""
    pnl = round(trade.get("pnl", 0.0), 2)
    if abs(pnl) < 0.005:
        pnl_text = "₹0.00"
        pnl_color = "#94a3b8"
    elif pnl > 0:
        pnl_text = f"+₹{pnl:,.2f}"
        pnl_color = "#10b981"
    else:
        pnl_text = f"-₹{abs(pnl):,.2f}"
        pnl_color = "#ef4444"

    broker_title = "ANGEL ONE" if trade.get("broker") == "angel" else "COINDCX"
    broker_bg = "rgba(168,85,247,0.15)" if trade.get("broker") == "angel" else "rgba(14,165,233,0.15)"
    broker_color = "#c084fc" if trade.get("broker") == "angel" else "#38bdf8"

    render_html(f"""
    <div class="trade-card" style="margin-bottom:10px; padding:14px;">
        <div class="trade-header" style="margin-bottom:8px;">
            <div style="display:flex; align-items:center; gap:8px;">
                <span class="segment-tag" style="background:{broker_bg}; color:{broker_color};">{broker_title}</span>
                <span class="symbol-title" style="font-size:14px;">{trade['symbol']}</span>
            </div>
            <span style="font-size:10.5px; color:#94a3b8;">📅 {trade.get('exit_time', '')}</span>
        </div>
        <div class="metrics-grid" style="margin-bottom:8px;">
            <div class="metric-col">
                <span class="metric-label">ENTRY</span>
                <span class="metric-val">₹{trade.get('entry_price', 0):,.2f}</span>
            </div>
            <div class="metric-col">
                <span class="metric-label">EXIT</span>
                <span class="metric-val" style="color:#10b981;">₹{trade.get('exit_price', 0):,.2f}</span>
            </div>
            <div class="metric-col" style="text-align:right;">
                <span class="metric-label">NET P/L</span>
                <span class="metric-val" style="color:{pnl_color};">{pnl_text}</span>
            </div>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center; font-size:10.5px;">
            <span style="color:#94a3b8;">Segment: {trade.get('segment', 'MARKET')}</span>
            <span style="font-weight:700; color:{pnl_color};">{trade.get('status', 'TARGET HIT')}</span>
        </div>
    </div>
    """)

def render_bottom_nav(active_tab: str, is_dark: bool):
    """Renders the native mobile bottom navigation dock with icons."""
    theme_arg = f"&theme={'dark' if is_dark else 'light'}"
    tabs = [
        ("home", "⚡", "Home"),
        ("coindcx", "🇮🇳", "CoinDCX"),
        ("angel", "📈", "Angel One"),
        ("history", "📜", "History")
    ]

    html_parts = ['<div class="bottom-dock">']
    for tid, icon, label in tabs:
        is_active = active_tab == tid
        cls = "dock-active" if is_active else "dock-inactive"
        html_parts.append(f'<a href="?tab={tid}{theme_arg}" target="_self" class="dock-tab {cls}"><span class="dock-icon">{icon}</span><span class="dock-label">{label}</span></a>')
    html_parts.append('</div>')
    
    render_html("".join(html_parts))
