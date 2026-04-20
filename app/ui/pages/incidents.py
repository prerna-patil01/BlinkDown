import streamlit as st
import pandas as pd
from ui.components.cards import section_title, page_header, metric_card
from ui.components.charts import service_breakdown
from ui.theme import PLOTLY_THEME, COLORS
import plotly.graph_objects as go

TABLE_HEIGHT = 420
CHART_HEIGHT = 250

SEVERITIES = ["All", "critical", "high", "medium", "low"]

# -------------------- PREPROCESS --------------------
@st.cache_data
def preprocess(df):
    df = df.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df

# -------------------- MAIN --------------------
def render(df, fin_df, pred_df):

    df = preprocess(df)
    companies = ["All"] + sorted(df["company"].dropna().unique().tolist())

    page_header("📋 Incident Explorer", "Browse, filter, and analyze all recorded incidents")

    # -------------------- FILTERS --------------------
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        company = st.selectbox("Select Company", companies)

    with c2:
        severity = st.selectbox("Select Severity", SEVERITIES)

    with c3:
        start = st.date_input("From", df["timestamp"].min().date())

    with c4:
        end = st.date_input("To", df["timestamp"].max().date())

    # -------------------- FILTER LOGIC --------------------
    query = (df["timestamp"].dt.date >= start) & (df["timestamp"].dt.date <= end)

    if company != "All":
        query &= (df["company"] == company)

    if severity != "All":
        query &= (df["severity"] == severity)

    filtered = df[query]

    # -------------------- METRICS --------------------
    m1, m2, m3, m4 = st.columns(4)

    total_incidents = len(filtered)
    avg_duration = filtered["duration_min"].mean() if not filtered.empty else 0
    total_downtime = filtered["duration_min"].sum() if not filtered.empty else 0
    users_affected = filtered["users_affected"].sum() if not filtered.empty else 0

    with m1:
        metric_card("Filtered Incidents", f"{total_incidents:,}", icon="📡", color="#6366f1")

    with m2:
        metric_card("Avg Duration", f"{avg_duration:.1f}m", icon="⏱️", color="#f59e0b")

    with m3:
        metric_card("Total Downtime", f"{total_downtime/60:.1f}h", icon="📉", color="#8b5cf6")

    with m4:
        metric_card("Users Affected", f"{users_affected/1e6:.1f}M", icon="👥", color="#06b6d4")

    st.markdown("<br>", unsafe_allow_html=True)

    if filtered.empty:
        st.warning("No incidents match the selected filters.")
        return

    # -------------------- LAYOUT --------------------
    left, right = st.columns([2, 1])

    # -------------------- TABLE --------------------
    with left:
        section_title("INCIDENT LOG", "📋")

        show = filtered.sort_values("timestamp", ascending=False).copy()
        show["timestamp"] = show["timestamp"].dt.strftime("%Y-%m-%d %H:%M")

        show = show[[
            "timestamp", "company", "severity", "service",
            "duration_min", "region", "root_cause",
            "users_affected", "resolved"
        ]].rename(columns={
            "timestamp": "Time",
            "company": "Company",
            "severity": "Severity",
            "service": "Service",
            "duration_min": "Duration(m)",
            "region": "Region",
            "root_cause": "Root Cause",
            "users_affected": "Users",
            "resolved": "Resolved"
        })

        st.dataframe(show, hide_index=True, use_container_width=True, height=TABLE_HEIGHT)

    # -------------------- RIGHT PANEL --------------------
    with right:
        section_title("SERVICE IMPACT", "🏗️")

        # 🔥 FIXED HERE
        st.plotly_chart(
            service_breakdown(filtered, company),  # pass company
            use_container_width=True,
            config={"displayModeBar": False}
        )

        section_title("ROOT CAUSE ANALYSIS", "🔍")

        rc = (
            filtered["root_cause"]
            .value_counts()
            .head(6)
            .reset_index()
        )
        rc.columns = ["cause", "count"]

        fig = go.Figure(go.Bar(
            y=rc["cause"],
            x=rc["count"],
            orientation="h",
            marker=dict(
                color=rc["count"],
                colorscale=[[0, COLORS["cyan"]], [1, COLORS["indigo"]]],
                line=dict(width=0)
            ),
            hovertemplate="<b>%{y}</b><br>%{x} incidents<extra></extra>"
        ))

        layout = {**PLOTLY_THEME}
        layout["margin"] = dict(l=8, r=8, t=30, b=8)

        fig.update_layout(
            **layout,
            showlegend=False,
            height=CHART_HEIGHT
        )

        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})