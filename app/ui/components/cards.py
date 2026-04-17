import streamlit as st

def metric_card(label, value, delta=None, delta_good=True, icon="", color="#6366f1"):
    delta_color = "#4ade80" if delta_good else "#f87171"
    delta_html  = f'<div class="metric-delta" style="color:{delta_color}">{delta}</div>' if delta else ""
    bar_color   = color
    st.markdown(f"""
<div class="metric-card">
  <span class="metric-icon">{icon}</span>
  <div class="metric-label">{label}</div>
  <div class="metric-value" style="background:linear-gradient(135deg,#e2e8f0,#94a3b8);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text">{value}</div>
  {delta_html}
  <div style="position:absolute;bottom:0;left:0;right:0;height:3px;
              background:linear-gradient(90deg,{bar_color},{bar_color}88,transparent);
              border-radius:0 0 16px 16px;"></div>
</div>""", unsafe_allow_html=True)

def glass_card(content_html, glow_color="rgba(99,102,241,0.15)"):
    st.markdown(f"""
<div class="glass-card" style="box-shadow:0 8px 32px rgba(0,0,0,0.4),0 0 40px {glow_color},
     inset 0 1px 0 rgba(255,255,255,0.08);">
  {content_html}
</div>""", unsafe_allow_html=True)

def risk_badge(label):
    level = label.lower()
    c = {"low":"#4ade80","medium":"#facc15","high":"#fb923c","critical":"#f87171"}.get(level,"#94a3b8")
    bg= {"low":"rgba(34,197,94,0.12)","medium":"rgba(234,179,8,0.12)",
         "high":"rgba(249,115,22,0.12)","critical":"rgba(239,68,68,0.12)"}.get(level,"rgba(148,163,184,0.12)")
    bc= {"low":"rgba(34,197,94,0.30)","medium":"rgba(234,179,8,0.30)",
         "high":"rgba(249,115,22,0.30)","critical":"rgba(239,68,68,0.30)"}.get(level,"rgba(148,163,184,0.30)")
    return f'<span class="badge" style="color:{c};background:{bg};border:1px solid {bc}">{label.upper()}</span>'

def section_title(text, icon=""):
    st.markdown(f'<div class="section-title">{icon} {text}</div>', unsafe_allow_html=True)

def page_header(title, subtitle=""):
    st.markdown(f"""
<div style="margin-bottom:28px;">
  <div class="page-title">{title}</div>
  <div class="page-subtitle">{subtitle}</div>
</div>""", unsafe_allow_html=True)

def status_indicator(company, status, color):
    dot_colors = {"operational":"#4ade80","minor issues":"#facc15",
                  "degraded":"#fb923c","critical outage":"#f87171"}
    dc = dot_colors.get(status, "#94a3b8")
    st.markdown(f"""
<div style="display:flex;align-items:center;justify-content:space-between;
            padding:10px 14px;border-radius:10px;
            background:rgba(10,14,30,0.60);
            border:1px solid rgba(99,102,241,0.12);margin:4px 0;">
  <span style="font-weight:600;font-size:13px;color:#e2e8f0">{company}</span>
  <span>
    <span class="status-dot" style="background:{dc}"></span>
    <span style="font-size:12px;color:{dc};font-weight:600">{status.upper()}</span>
  </span>
</div>""", unsafe_allow_html=True)
