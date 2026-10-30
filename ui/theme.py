def get_custom_css(is_dark: bool = True) -> str:
    """Returns ultra-sleek, premium native FinTech CSS with zero ugly hyperlinks."""
    
    # Color palette
    if is_dark:
        bg_main = "#080c14"
        bg_card = "#0f172a"
        bg_subcard = "#162032"
        border_color = "rgba(255, 255, 255, 0.08)"
        border_glow = "rgba(16, 185, 129, 0.2)"
        text_primary = "#f8fafc"
        text_secondary = "#94a3b8"
        text_muted = "#64748b"
        accent_lime = "#ccff00"
        accent_emerald = "#10b981"
        nav_bg = "rgba(15, 23, 42, 0.94)"
        nav_border = "rgba(255, 255, 255, 0.1)"
    else:
        bg_main = "#f1f5f9"
        bg_card = "#ffffff"
        bg_subcard = "#f8fafc"
        border_color = "#e2e8f0"
        border_glow = "rgba(16, 185, 129, 0.25)"
        text_primary = "#0f172a"
        text_secondary = "#475569"
        text_muted = "#94a3b8"
        accent_lime = "#047857"
        accent_emerald = "#059669"
        nav_bg = "rgba(255, 255, 255, 0.96)"
        nav_border = "#e2e8f0"

    return f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600;700&display=swap');

    /* Global Streamlit Resets */
    html, body, [data-testid="stAppViewContainer"] {{
        background: {bg_main} !important;
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: {text_primary} !important;
        -webkit-font-smoothing: antialiased;
        overflow-x: hidden !important;
    }}

    header[data-testid="stHeader"] {{
        background: transparent !important;
        height: 0px !important;
    }}

    .block-container {{
        max-width: 480px !important;
        padding: 12px 14px 100px 14px !important;
        margin: 0 auto !important;
    }}

    /* Remove Streamlit default ugly decoration */
    #MainMenu, footer, [data-testid="stToolbar"] {{
        display: none !important;
    }}

    /* Typography Defaults */
    h1, h2, h3, h4, p, span, div {{
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }}

    /* Premium Top Header */
    .top-bar {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 6px 0 14px 0;
        border-bottom: 1px solid {border_color};
        margin-bottom: 14px;
    }}

    .brand-title {{
        font-size: 16px;
        font-weight: 800;
        letter-spacing: -0.3px;
        color: {text_primary};
        display: flex;
        align-items: center;
        gap: 8px;
    }}

    .live-pulse-badge {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(16, 185, 129, 0.12);
        border: 1px solid rgba(16, 185, 129, 0.3);
        color: {accent_emerald};
        font-size: 10px;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 20px;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: 0.3px;
    }}

    .radar-dot {{
        width: 6px;
        height: 6px;
        background: {accent_emerald};
        border-radius: 50%;
        box-shadow: 0 0 8px {accent_emerald};
    }}

    /* Premium Hero Portfolio Card */
    .hero-card {{
        background: {bg_card};
        border: 1px solid {border_color};
        border-radius: 22px;
        padding: 20px 18px;
        margin-bottom: 16px;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.18);
        position: relative;
        overflow: hidden;
    }}

    .hero-label {{
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        color: {text_muted};
        margin-bottom: 4px;
    }}

    .hero-balance {{
        font-size: 30px;
        font-weight: 800;
        letter-spacing: -0.8px;
        color: {text_primary};
        font-family: 'JetBrains Mono', monospace;
        display: flex;
        align-items: baseline;
        gap: 10px;
        line-height: 1.1;
    }}

    .badge-gain {{
        font-size: 12px;
        font-weight: 700;
        padding: 3px 8px;
        border-radius: 12px;
        background: rgba(16, 185, 129, 0.14);
        color: #10b981;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }}

    .badge-loss {{
        font-size: 12px;
        font-weight: 700;
        padding: 3px 8px;
        border-radius: 12px;
        background: rgba(239, 68, 68, 0.14);
        color: #ef4444;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }}

    /* 2-Column Vault Grid */
    .vault-grid {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;
        margin-top: 16px;
        padding-top: 14px;
        border-top: 1px solid {border_color};
    }}

    .vault-item {{
        background: {bg_subcard};
        border: 1px solid {border_color};
        border-radius: 14px;
        padding: 10px 12px;
    }}

    .vault-sub-label {{
        font-size: 10px;
        font-weight: 600;
        color: {text_muted};
        margin-bottom: 2px;
        letter-spacing: 0.2px;
    }}

    .vault-sub-val {{
        font-size: 15px;
        font-weight: 700;
        color: {text_primary};
        font-family: 'JetBrains Mono', monospace;
    }}

    /* Interactive Sub-tab Pills (No links, looks like native iOS segmented control) */
    .tab-bar {{
        display: flex;
        background: {bg_subcard};
        border: 1px solid {border_color};
        border-radius: 16px;
        padding: 4px;
        gap: 4px;
        margin-bottom: 16px;
    }}

    .tab-pill {{
        flex: 1;
        text-align: center;
        padding: 8px 10px;
        border-radius: 12px;
        font-size: 11.5px;
        font-weight: 700;
        text-decoration: none !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        display: inline-block;
    }}

    .tab-pill-active {{
        background: #10b981 !important;
        color: #ffffff !important;
        box-shadow: 0 4px 14px rgba(16, 185, 129, 0.35);
    }}

    .tab-pill-inactive {{
        background: transparent !important;
        color: {text_secondary} !important;
    }}

    .tab-pill-inactive:hover {{
        color: {text_primary} !important;
    }}

    /* Trade Position Card */
    .trade-card {{
        background: {bg_card};
        border: 1px solid {border_color};
        border-radius: 18px;
        padding: 16px;
        margin-bottom: 12px;
        box-shadow: 0 4px 18px rgba(0, 0, 0, 0.08);
        transition: transform 0.15s ease, border-color 0.15s ease;
    }}

    .trade-card:hover {{
        border-color: {border_glow};
        transform: translateY(-1.5px);
    }}

    .trade-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
    }}

    .symbol-title {{
        font-size: 15px;
        font-weight: 800;
        color: {text_primary};
        letter-spacing: -0.2px;
    }}

    .segment-tag {{
        font-size: 9.5px;
        font-weight: 700;
        padding: 2px 7px;
        border-radius: 6px;
        letter-spacing: 0.3px;
    }}

    .metrics-grid {{
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        gap: 8px;
        background: {bg_subcard};
        border-radius: 12px;
        padding: 10px;
        margin-bottom: 12px;
    }}

    .metric-col {{
        display: flex;
        flex-direction: column;
    }}

    .metric-label {{
        font-size: 9.5px;
        font-weight: 600;
        color: {text_muted};
        letter-spacing: 0.3px;
        margin-bottom: 2px;
    }}

    .metric-val {{
        font-size: 13.5px;
        font-weight: 700;
        color: {text_primary};
        font-family: 'JetBrains Mono', monospace;
    }}

    /* Action Buttons (Square off, clear, reset) - Crisp App Look */
    .btn-square-off {{
        display: block;
        width: 100%;
        text-align: center;
        background: rgba(239, 68, 68, 0.12);
        color: #ef4444 !important;
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-radius: 11px;
        padding: 8px 12px;
        font-size: 11.5px;
        font-weight: 700;
        text-decoration: none !important;
        transition: all 0.15s ease;
    }}

    .btn-square-off:hover {{
        background: #ef4444 !important;
        color: #ffffff !important;
        box-shadow: 0 4px 12px rgba(239, 68, 68, 0.35);
    }}

    .btn-action-primary {{
        display: inline-block;
        text-align: center;
        background: #10b981;
        color: #ffffff !important;
        border-radius: 12px;
        padding: 9px 16px;
        font-size: 12px;
        font-weight: 700;
        text-decoration: none !important;
        box-shadow: 0 4px 14px rgba(16, 185, 129, 0.3);
        transition: all 0.15s ease;
    }}

    .btn-action-primary:hover {{
        transform: translateY(-1px);
        box-shadow: 0 6px 18px rgba(16, 185, 129, 0.45);
    }}

    .btn-action-secondary {{
        display: inline-block;
        text-align: center;
        background: {bg_subcard};
        color: {text_secondary} !important;
        border: 1px solid {border_color};
        border-radius: 12px;
        padding: 9px 16px;
        font-size: 12px;
        font-weight: 700;
        text-decoration: none !important;
        transition: all 0.15s ease;
    }}

    .btn-action-secondary:hover {{
        color: {text_primary} !important;
        border-color: {text_secondary};
    }}

    /* Bottom Navigation Dock (Native iOS/Android App Style) */
    .bottom-dock {{
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        max-width: 480px;
        margin: 0 auto;
        background: {nav_bg};
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-top: 1px solid {nav_border};
        display: flex;
        justify-content: space-around;
        padding: 8px 10px 14px 10px;
        z-index: 9999;
    }}

    .dock-tab {{
        flex: 1;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 3px;
        text-decoration: none !important;
        transition: transform 0.15s ease;
        padding: 4px;
        border-radius: 10px;
    }}

    .dock-tab:hover {{
        transform: scale(1.05);
    }}

    .dock-icon {{
        font-size: 19px;
        line-height: 1;
    }}

    .dock-label {{
        font-size: 10.5px;
        font-weight: 700;
        letter-spacing: -0.1px;
    }}

    .dock-active .dock-label {{
        color: #10b981 !important;
    }}

    .dock-inactive .dock-label {{
        color: {text_muted} !important;
    }}

    /* Theme Switch Button */
    .theme-toggle-btn {{
        background: {bg_subcard};
        border: 1px solid {border_color};
        color: {text_primary};
        border-radius: 10px;
        padding: 4px 8px;
        font-size: 13px;
        text-decoration: none !important;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        transition: all 0.15s ease;
    }}
    </style>
    """
