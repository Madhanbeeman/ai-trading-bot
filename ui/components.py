import streamlit as st
from config.settings import format_ist_clock
from .logo import FOX_LOGO_URI

def render_html(html_str: str):
    """Safely renders HTML without Markdown indented-code-block interference."""
    clean = "\n".join(line.strip() for line in html_str.splitlines() if line.strip() and not line.strip().startswith("<!--"))
    st.markdown(clean, unsafe_allow_html=True)

def generate_sparkline_svg(is_profit: bool, pos_id: str) -> str:
    """Generates an ultra-lightweight, responsive inline SVG trend chart for each trade card."""
    stroke_color = "#10b981" if is_profit else "#ef4444"
    grad_id = f"spark_{pos_id}"

    if is_profit:
        # Upward trajectory with realistic micro-swings
        points = "0,34 35,31 70,33 110,25 150,27 195,19 240,22 285,14 330,16 375,8 415,4"
        area = "0,34 35,31 70,33 110,25 150,27 195,19 240,22 285,14 330,16 375,8 415,4 415,40 0,40"
        color_start = "rgba(16, 185, 129, 0.32)"
        color_end = "rgba(16, 185, 129, 0.0)"
        dot_y = 4
    else:
        # Downward trajectory with realistic micro-swings
        points = "0,6 35,10 70,8 110,16 150,14 195,22 240,20 285,28 330,26 375,34 415,38"
        area = "0,6 35,10 70,8 110,16 150,14 195,22 240,20 285,28 330,26 375,34 415,38 415,40 0,40"
        color_start = "rgba(239, 68, 68, 0.32)"
        color_end = "rgba(239, 68, 68, 0.0)"
        dot_y = 38

    return f"""
    <svg viewBox="0 0 420 40" preserveAspectRatio="none" style="width:100%; height:34px; display:block; margin:6px 0 8px 0; border-radius:6px; overflow:hidden;">
        <defs>
            <linearGradient id="{grad_id}" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="{color_start}" />
                <stop offset="100%" stop-color="{color_end}" />
            </linearGradient>
        </defs>
        <polygon points="{area}" fill="url(#{grad_id})" />
        <polyline fill="none" stroke="{stroke_color}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" points="{points}" />
        <circle cx="415" cy="{dot_y}" r="3" fill="{stroke_color}" />
    </svg>
    """

def render_header(title: str, is_dark: bool, current_tab: str, sub_tab: str = ""):
    """Renders sleek top user bar with live clock and Sun ☀️ / Moon 🌙 switch toggle."""
    clock_str = format_ist_clock()
    sub_param = f"&sub={sub_tab}" if sub_tab else ""
    target_sun = f"?tab={current_tab}{sub_param}&theme=light"
    target_moon = f"?tab={current_tab}{sub_param}&theme=dark"

    sun_cls = "theme-btn-active-sun" if not is_dark else "theme-btn-inactive"
    moon_cls = "theme-btn-active-moon" if is_dark else "theme-btn-inactive"

    render_html(f"""
    <div class="top-bar">
        <div class="brand-title">
            <img src="{FOX_LOGO_URI}" style="width:28px; height:28px; border-radius:8px; object-fit:contain; box-shadow:0 2px 8px rgba(0,0,0,0.25); vertical-align:middle;" />
            <span>{title}</span>
        </div>
        <div style="display:flex; align-items:center; gap:8px;">
            <div class="live-pulse-badge">
                <span class="radar-dot"></span> IST {clock_str}
            </div>
            <div class="theme-switch-bar">
                <a href="{target_sun}" target="_self" class="theme-btn {sun_cls}" title="Light Theme" onclick="try {{ window.location.search = '?tab={current_tab}{sub_param}&theme=light'; }} catch(e) {{ window.location.href = '{target_sun}'; }} return false;">
                    ☀️
                </a>
                <a href="{target_moon}" target="_self" class="theme-btn {moon_cls}" title="Dark Theme" onclick="try {{ window.location.search = '?tab={current_tab}{sub_param}&theme=dark'; }} catch(e) {{ window.location.href = '{target_moon}'; }} return false;">
                    🌙
                </a>
            </div>
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
    """Renders high-finish active trade card showing YOUR actual invested money, current value, live P/L, and inline sparkline chart."""
    pnl = round(pos.get("pnl", 0.0), 2)
    pct = round(pos.get("pct", 0.0), 2)

    # Bulletproof PnL formatting - NEVER print +₹-0.00
    if abs(pnl) < 0.005:
        pnl = 0.0
        pct = 0.0
        pnl_text = "₹0.00 (0.00%)"
        pnl_color = "#94a3b8"
        is_profit = True
    elif pnl > 0:
        pnl_text = f"+₹{pnl:,.2f} (+{pct:.2f}%)"
        pnl_color = "#10b981"
        is_profit = True
    else:
        pnl_text = f"-₹{abs(pnl):,.2f} ({pct:.2f}%)"
        pnl_color = "#ef4444"
        is_profit = False

    # YOUR actual entry money vs current value
    invested_amt = pos.get("cost", pos.get("margin", pos.get("invested", 100.0)))
    current_val = round(max(0.0, invested_amt + pnl), 2)

    sub_arg = f"&sub={current_sub}" if current_sub else ""
    theme_arg = f"&theme={'dark' if is_dark else 'light'}"
    close_url = f"?tab={current_tab}{sub_arg}&action=close&cid={pos['id']}{theme_arg}"

    badge_html = ""
    if "badge" in pos:
        badge_html = f"""<span class="segment-tag" style="background:{pos.get('badge_bg', 'rgba(16,185,129,0.15)')}; color:{pos.get('badge_color', '#10b981')};">{pos['badge']}</span>"""
    else:
        badge_html = f"""<span class="segment-tag" style="background:rgba(56,189,248,0.15); color:#38bdf8;">{pos.get('segment', 'MARKET')}</span>"""

    # Inline micro sparkline chart
    sparkline_html = generate_sparkline_svg(is_profit, pos['id'])

    render_html(f"""
    <div class="trade-card">
        <div class="trade-header">
            <div>
                <div class="symbol-title">{pos['symbol']}</div>
                <div style="font-size:11px; color:#94a3b8; font-weight:500; margin-top:1px;">{pos.get('name', '')} • {pos.get('date', 'Today')}</div>
            </div>
            {badge_html}
        </div>
        
        <!-- Primary Row: YOUR Invested Money & Current Value -->
        <div class="metrics-grid">
            <div class="metric-col">
                <span class="metric-label">MY INVESTED</span>
                <span class="metric-val">₹{invested_amt:,.2f}</span>
            </div>
            <div class="metric-col">
                <span class="metric-label">CURRENT VALUE</span>
                <span class="metric-val" style="color:{'#ffffff' if is_dark else '#0f172a'};">₹{current_val:,.2f}</span>
            </div>
            <div class="metric-col" style="text-align:right;">
                <span class="metric-label">LIVE P/L</span>
                <span class="metric-val" style="color:{pnl_color}; font-size:12px;">{pnl_text}</span>
            </div>
        </div>

        <!-- Inline Mini Trading Chart -->
        {sparkline_html}

        <!-- Secondary Row: Market Price & Targets -->
        <div style="background:{'rgba(255,255,255,0.03)' if is_dark else 'rgba(0,0,0,0.03)'}; border-radius:10px; padding:6px 10px; display:flex; justify-content:space-between; align-items:center; font-size:10.5px; color:#94a3b8; margin-bottom:12px; font-family:'JetBrains Mono', monospace;">
            <span>Asset CMP: <b style="color:#38bdf8;">₹{pos['cmp']:,.2f}</b></span>
            <span>🎯 Tgt: <b style="color:#10b981;">₹{pos.get('target', 0):,.2f}</b></span>
            <span>🛡️ SL: <b style="color:#ef4444;">₹{pos.get('sl', 0):,.2f}</b></span>
        </div>

        <!-- Exit Action -->
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
    fox_icon_html = f'<img src="{FOX_LOGO_URI}" style="width:20px; height:20px; object-fit:contain; border-radius:4px; vertical-align:middle; display:inline-block;" />'
    tabs = [
        ("home", fox_icon_html, "Home"),
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
