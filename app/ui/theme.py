import streamlit as st

def inject_css():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── BASE ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; }

html, body, [class*="css"], .stApp {
    font-family: 'Space Grotesk', sans-serif;
    background: #020408;
    color: #e2e8f0;
}

.stApp {
    background:
        radial-gradient(ellipse 80% 50% at 20% 10%, rgba(99,102,241,0.18) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 80%, rgba(139,92,246,0.14) 0%, transparent 55%),
        radial-gradient(ellipse 50% 60% at 60% 30%, rgba(6,182,212,0.08) 0%, transparent 50%),
        linear-gradient(160deg, #020408 0%, #050b14 40%, #060a18 100%);
    min-height: 100vh;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background:
        linear-gradient(180deg, rgba(99,102,241,0.06) 0%, transparent 40%),
        rgba(4, 6, 16, 0.95) !important;
    border-right: 1px solid rgba(99,102,241,0.20) !important;
    backdrop-filter: blur(20px);
}
[data-testid="stSidebar"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #6366f1, #8b5cf6, #06b6d4, #6366f1);
    background-size: 200%;
    animation: shimmer 3s linear infinite;
}
@keyframes shimmer { 0%{background-position:0%} 100%{background-position:200%} }

/* ── GLASS CARDS ── */
.glass-card {
    background: linear-gradient(135deg,
        rgba(255,255,255,0.06) 0%,
        rgba(255,255,255,0.02) 100%);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 16px;
    padding: 24px;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    box-shadow:
        0 8px 32px rgba(0,0,0,0.40),
        0 2px 8px rgba(0,0,0,0.30),
        inset 0 1px 0 rgba(255,255,255,0.08);
    transition: transform 0.2s, box-shadow 0.2s;
    position: relative;
    overflow: hidden;
}
.glass-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.15), transparent);
}
.glass-card:hover {
    transform: translateY(-2px);
    box-shadow:
        0 16px 48px rgba(0,0,0,0.50),
        0 4px 16px rgba(99,102,241,0.15),
        inset 0 1px 0 rgba(255,255,255,0.10);
}

/* ── 3D METRIC CARDS ── */
.metric-card {
    background: linear-gradient(145deg,
        rgba(15,20,40,0.90) 0%,
        rgba(8,12,28,0.95) 100%);
    border: 1px solid rgba(99,102,241,0.25);
    border-radius: 16px;
    padding: 20px 22px;
    position: relative;
    overflow: hidden;
    box-shadow:
        0 20px 40px rgba(0,0,0,0.50),
        0 4px 12px rgba(0,0,0,0.30),
        inset 0 1px 0 rgba(255,255,255,0.07),
        inset 0 -1px 0 rgba(0,0,0,0.30);
    transform: perspective(800px) rotateX(0deg);
    transition: all 0.3s cubic-bezier(0.34,1.56,0.64,1);
}
.metric-card::after {
    content: '';
    position: absolute;
    top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: radial-gradient(circle at 30% 30%,
        rgba(255,255,255,0.04) 0%, transparent 60%);
    pointer-events: none;
}
.metric-card:hover {
    transform: perspective(800px) rotateX(-3deg) translateY(-4px) scale(1.01);
    border-color: rgba(99,102,241,0.50);
    box-shadow:
        0 30px 60px rgba(0,0,0,0.60),
        0 8px 20px rgba(99,102,241,0.20),
        inset 0 1px 0 rgba(255,255,255,0.10);
}

.metric-value {
    font-size: 32px;
    font-weight: 700;
    line-height: 1.1;
    background: linear-gradient(135deg, #e2e8f0 0%, #94a3b8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.metric-label {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #64748b;
    margin-top: 4px;
}
.metric-delta {
    font-size: 12px;
    font-weight: 600;
    margin-top: 8px;
}
.metric-icon {
    position: absolute;
    top: 16px; right: 16px;
    font-size: 28px;
    opacity: 0.25;
}

/* ── RISK BADGE ── */
.risk-low      { background:rgba(34,197,94,0.15);  color:#4ade80; border:1px solid rgba(34,197,94,0.30); }
.risk-medium   { background:rgba(234,179,8,0.15);   color:#facc15; border:1px solid rgba(234,179,8,0.30); }
.risk-high     { background:rgba(249,115,22,0.15);  color:#fb923c; border:1px solid rgba(249,115,22,0.30); }
.risk-critical { background:rgba(239,68,68,0.15);   color:#f87171; border:1px solid rgba(239,68,68,0.30); }

.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}

/* ── SECTION TITLE ── */
.section-title {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #6366f1;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.section-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, rgba(99,102,241,0.4), transparent);
}

/* ── PAGE TITLE ── */
.page-title {
    font-size: 28px;
    font-weight: 700;
    background: linear-gradient(135deg, #e2e8f0 0%, #94a3b8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 4px;
}
.page-subtitle {
    font-size: 13px;
    color: #475569;
    margin-bottom: 24px;
}

/* ── TABLE ── */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid rgba(99,102,241,0.15) !important;
}

/* ── SELECTBOX / INPUT ── */
[data-testid="stSelectbox"] > div > div,
[data-testid="stMultiSelect"] > div > div {
    background: rgba(10,14,30,0.80) !important;
    border: 1px solid rgba(99,102,241,0.25) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    backdrop-filter: blur(10px);
}

/* ── BUTTONS ── */
.stButton > button {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
    color: white;
    border: none;
    border-radius: 10px;
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 600;
    font-size: 13px;
    padding: 10px 24px;
    box-shadow: 0 4px 16px rgba(99,102,241,0.35),
                inset 0 1px 0 rgba(255,255,255,0.15);
    transition: all 0.2s;
}
.stButton > button:hover {
    box-shadow: 0 8px 28px rgba(99,102,241,0.50),
                inset 0 1px 0 rgba(255,255,255,0.20);
    transform: translateY(-1px);
}

/* ── TABS ── */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: rgba(10,14,30,0.60);
    border-radius: 12px;
    padding: 4px;
    border: 1px solid rgba(99,102,241,0.15);
    gap: 4px;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    border-radius: 8px;
    font-weight: 600;
    font-size: 13px;
    color: #64748b !important;
    transition: all 0.2s;
}
[data-testid="stTabs"] [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(99,102,241,0.25), rgba(139,92,246,0.25)) !important;
    color: #a5b4fc !important;
    box-shadow: 0 2px 8px rgba(99,102,241,0.20);
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: rgba(10,14,30,0.50); }
::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #6366f1, #8b5cf6);
    border-radius: 3px;
}

/* ── PLOTLY CHARTS ── */
.js-plotly-plot .plotly { border-radius: 12px; }

/* ── STATUS DOT ── */
.status-dot {
    display: inline-block;
    width: 8px; height: 8px;
    border-radius: 50%;
    margin-right: 6px;
    animation: pulse-dot 2s infinite;
}
@keyframes pulse-dot {
    0%,100% { opacity: 1; }
    50% { opacity: 0.4; }
}

/* ── CHAT ── */
.chat-bubble-user {
    background: linear-gradient(135deg, rgba(99,102,241,0.20), rgba(139,92,246,0.15));
    border: 1px solid rgba(99,102,241,0.25);
    border-radius: 16px 16px 4px 16px;
    padding: 12px 16px;
    margin: 8px 0;
    font-size: 14px;
    max-width: 80%;
    margin-left: auto;
}
.chat-bubble-ai {
    background: linear-gradient(135deg, rgba(6,182,212,0.10), rgba(59,130,246,0.08));
    border: 1px solid rgba(6,182,212,0.20);
    border-radius: 16px 16px 16px 4px;
    padding: 12px 16px;
    margin: 8px 0;
    font-size: 14px;
    max-width: 85%;
    line-height: 1.6;
}

/* ── SIDEBAR NAV ── */
.nav-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 14px;
    border-radius: 10px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 500;
    color: #64748b;
    transition: all 0.2s;
    margin: 2px 0;
}
.nav-item:hover {
    background: rgba(99,102,241,0.12);
    color: #a5b4fc;
}
.nav-item.active {
    background: linear-gradient(135deg, rgba(99,102,241,0.20), rgba(139,92,246,0.15));
    color: #a5b4fc;
    border: 1px solid rgba(99,102,241,0.25);
    box-shadow: 0 4px 12px rgba(99,102,241,0.15);
}

/* ── DIVIDER ── */
hr { border-color: rgba(99,102,241,0.15) !important; }

/* ── HIDE STREAMLIT DEFAULT ── */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }
</style>
""", unsafe_allow_html=True)


PLOTLY_THEME = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(8,12,28,0.60)",
    font=dict(family="Space Grotesk", color="#94a3b8", size=12),
    colorway=["#6366f1","#8b5cf6","#06b6d4","#10b981","#f59e0b","#ef4444","#ec4899"],
    margin=dict(l=16, r=16, t=36, b=16),
    xaxis=dict(
        gridcolor="rgba(99,102,241,0.08)",
        zerolinecolor="rgba(99,102,241,0.15)",
        tickfont=dict(size=11),
    ),
    yaxis=dict(
        gridcolor="rgba(99,102,241,0.08)",
        zerolinecolor="rgba(99,102,241,0.15)",
        tickfont=dict(size=11),
    ),
)

COLORS = {
    "indigo":   "#6366f1",
    "purple":   "#8b5cf6",
    "cyan":     "#06b6d4",
    "emerald":  "#10b981",
    "amber":    "#f59e0b",
    "red":      "#ef4444",
    "pink":     "#ec4899",
    "low":      "#4ade80",
    "medium":   "#facc15",
    "high":     "#fb923c",
    "critical": "#f87171",
}
