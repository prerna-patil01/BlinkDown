import streamlit as st
import pandas as pd
from app.ui.components.cards import metric_card, section_title, page_header, risk_badge, glass_card
from app.ui.components.charts import (outage_timeline, severity_donut, heatmap_hour_day,
                                       service_breakdown, risk_gauge)
from app.backend.data_engine import compute_risk, get_company_stats
from app.backend.ai_engine import generate_suggestions

COMPANIES = ["AWS", "Azure", "GCP", "Cloudflare", "Vercel", "Fastly", "Akamai"]

def render(df, fin_df, pred_df):
    page_header("🏢 Company Deep Dive", "Select a company to explore full outage intelligence")
    col_sel, _ = st.columns([1,3])
    with col_sel:
        company = st.selectbox("Select Company", COMPANIES, label_visibility="collapsed")

    risk  = compute_risk(df, company)
    stats = get_company_stats(df, fin_df, company)
    cdf   = df[df["company"]==company]

    # Metrics
    c1,c2,c3,c4,c5 = st.columns(5)
    with c1: metric_card("Total Outages",  f"{stats['total_outages']:,}",      icon="📡", color="#6366f1")
    with c2: metric_card("Avg Duration",   f"{stats['avg_duration']}m",         icon="⏱️", color="#f59e0b")
    with c3: metric_card("Total Downtime", f"{stats['total_downtime']}h",       icon="📉", color="#8b5cf6")
    with c4: metric_card("Est. Loss",      f"${stats['total_cost']/1e6:.1f}M",  icon="💸", color="#ef4444")
    with c5: metric_card("Users Affected", f"{stats['users_affected']/1e6:.1f}M",icon="👥", color="#06b6d4")

    st.markdown("<br>", unsafe_allow_html=True)
    left, right = st.columns([3,1])
    with left:
        section_title("OUTAGE TIMELINE", "📈")
        st.plotly_chart(outage_timeline(df, company), use_container_width=True, config={"displayModeBar":False})
        t1, t2 = st.columns(2)
        with t1:
            section_title("SEVERITY BREAKDOWN", "🎯")
            st.plotly_chart(severity_donut(df, company), use_container_width=True, config={"displayModeBar":False})
        with t2:
            section_title("SERVICE BREAKDOWN", "🏗️")
            st.plotly_chart(service_breakdown(df, company), use_container_width=True, config={"displayModeBar":False})
        section_title("FAILURE HEATMAP", "🔥")
        st.plotly_chart(heatmap_hour_day(df, company), use_container_width=True, config={"displayModeBar":False})
    with right:
        section_title("RISK SCORE", "⚠️")
        st.plotly_chart(risk_gauge(risk["risk_pct"], company), use_container_width=True,
                        config={"displayModeBar":False})
        badge = risk_badge(risk["label"])
        st.markdown(f'<div style="text-align:center;margin-bottom:16px">{badge}</div>', unsafe_allow_html=True)
        section_title("AI RECOMMENDATIONS", "🤖")
        tips = generate_suggestions(df, fin_df, company)
        for icon, title, text in tips:
            st.markdown(f"""
<div style="background:rgba(10,14,30,0.70);border:1px solid rgba(99,102,241,0.18);
            border-radius:10px;padding:12px;margin:6px 0;">
  <div style="font-size:11px;font-weight:700;letter-spacing:0.08em;
              color:#6366f1;margin-bottom:4px">{icon} {title}</div>
  <div style="font-size:12px;color:#94a3b8;line-height:1.5">{text}</div>
</div>""", unsafe_allow_html=True)

        # Recent incidents table
        st.markdown("<br>", unsafe_allow_html=True)
        section_title("RECENT INCIDENTS", "📋")
        recent = cdf.sort_values("timestamp", ascending=False).head(8)[
            ["timestamp","severity","service","duration_min","root_cause"]].copy()
        recent["timestamp"] = recent["timestamp"].dt.strftime("%m/%d %H:%M")
        recent.columns = ["Time","Severity","Service","Duration(m)","Root Cause"]
        st.dataframe(recent, hide_index=True, use_container_width=True,
                     column_config={"Severity": st.column_config.TextColumn("Severity")})
