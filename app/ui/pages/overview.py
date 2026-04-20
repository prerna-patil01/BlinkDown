import streamlit as st
import pandas as pd
from ui.components.cards import metric_card, section_title, page_header, status_indicator, glass_card
from ui.components.charts import outage_timeline, severity_donut, company_comparison_bar, heatmap_hour_day
from backend.data_engine import get_dashboard_kpis, get_current_status

def render(df, fin_df, pred_df):
    page_header("⚡ BlinkDown Overview", "Real-time outage intelligence across all monitored services")
    kpis = get_dashboard_kpis(df, fin_df)
    status_map = get_current_status(df)

    c1,c2,c3,c4,c5,c6 = st.columns(6)
    with c1: metric_card("Total Outages",   f"{kpis['total_outages']:,}",    icon="📡", color="#6366f1")
    with c2: metric_card("Est. Loss",       f"${kpis['total_cost']/1e6:.1f}M", icon="💸", color="#ef4444")
    with c3: metric_card("Avg Duration",    f"{kpis['avg_duration']}m",      icon="⏱️", color="#f59e0b")
    with c4: metric_card("Critical %",      f"{kpis['critical_pct']}%",      icon="🚨", color="#ef4444")
    with c5: metric_card("SLA Breaches",    f"{kpis['sla_breaches']:,}",     icon="📋", color="#8b5cf6")
    with c6: metric_card("Companies",       f"{kpis['companies_monitored']}", icon="🏢", color="#06b6d4")

    st.markdown("<br>", unsafe_allow_html=True)
    left, right = st.columns([2,1])
    with left:
        section_title("OUTAGE FREQUENCY TIMELINE", "📈")
        st.plotly_chart(outage_timeline(df), use_container_width=True, config={"displayModeBar":False})
        section_title("OUTAGE HEATMAP — HOUR × DAY", "🔥")
        st.plotly_chart(heatmap_hour_day(df), use_container_width=True, config={"displayModeBar":False})
    with right:
        section_title("LIVE SERVICE STATUS", "🟢")
        for company, (status, color) in status_map.items():
            status_indicator(company, status, color)
        st.markdown("<br>", unsafe_allow_html=True)
        section_title("SEVERITY DISTRIBUTION", "🎯")
        st.plotly_chart(severity_donut(df), use_container_width=True, config={"displayModeBar":False})

    st.markdown("<br>", unsafe_allow_html=True)
    section_title("COMPANY COMPARISON", "🏆")
    st.plotly_chart(company_comparison_bar(df), use_container_width=True, config={"displayModeBar":False})
