import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from app.ui.components.cards import section_title, page_header, metric_card
from app.ui.components.charts import severity_donut
from app.backend.data_engine import compute_risk, get_company_stats
from app.ui.theme import PLOTLY_THEME, COLORS

COMPANIES = ["AWS", "Azure", "GCP", "Cloudflare", "Vercel", "Fastly", "Akamai"]


def render(df, fin_df, pred_df):
    page_header("⚖️ Company Comparison", "Side-by-side reliability benchmarking")

    sel = st.multiselect(
        "Select companies to compare",
        COMPANIES,
        default=["AWS", "Azure", "GCP"],
        label_visibility="collapsed"
    )

    if len(sel) < 2:
        st.warning("Select at least 2 companies to compare.")
        return

    # Build comparison dataframe
    rows = []
    for c in sel:
        s = get_company_stats(df, fin_df, c)
        r = compute_risk(df, c)

        rows.append({
            "Company": c,
            "Outages": s["total_outages"],
            "Avg Duration": s["avg_duration"],
            "Downtime (h)": s["total_downtime"],
            "Critical": s["critical_count"],
            "Cost ($M)": round(s["total_cost"] / 1e6, 2),
            "SLA Breaches": s["sla_breaches"],
            "Risk %": r["risk_pct"],
            "Risk Label": r["label"]
        })

    cmp_df = pd.DataFrame(rows)

    # Summary cards
    cols = st.columns(len(sel))
    for i, c in enumerate(sel):
        row = cmp_df[cmp_df["Company"] == c].iloc[0]

        with cols[i]:
            metric_card(
                c,
                f"{row['Risk %']}% risk",
                delta=row["Risk Label"],
                delta_good=row["Risk Label"] in ["Low", "Medium"],
                icon="🏢",
                color={
                    "Low": "#4ade80",
                    "Medium": "#facc15",
                    "High": "#fb923c",
                    "Critical": "#f87171"
                }.get(row["Risk Label"], "#6366f1")
            )

    st.markdown("<br>", unsafe_allow_html=True)

    t1, t2 = st.columns(2)

    # ------------------ TOTAL OUTAGES ------------------
    with t1:
        section_title("TOTAL OUTAGES", "📊")

        fig = go.Figure(go.Bar(
            x=cmp_df["Company"],
            y=cmp_df["Outages"],
            marker=dict(color=COLORS["indigo"], line=dict(width=0)),
            text=cmp_df["Outages"],
            textposition="outside"
        ))

        fig.update_layout(**PLOTLY_THEME)
        fig.update_yaxes(range=[0, 110])

        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # ------------------ FINANCIAL LOSS ------------------
    with t2:
        section_title("ESTIMATED FINANCIAL LOSS", "💸")

        fig = go.Figure(go.Bar(
            x=cmp_df["Company"],
            y=cmp_df["Cost ($M)"],
            marker=dict(
                color=cmp_df["Cost ($M)"],
                colorscale=[[0, COLORS["cyan"]], [1, COLORS["critical"]]],
                line=dict(width=0)
            ),
            text=[f"${v:.1f}M" for v in cmp_df["Cost ($M)"]],
            textposition="outside"
        ))

        fig.update_layout(**PLOTLY_THEME, showlegend=False)

        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    t3, t4 = st.columns(2)

    # ------------------ RISK SCORE ------------------
    with t3:
        section_title("RISK SCORE COMPARISON", "⚠️")

        colors = [
            {
                "Low": "#4ade80",
                "Medium": "#facc15",
                "High": "#fb923c",
                "Critical": "#f87171"
            }.get(label, "#6366f1")
            for label in cmp_df["Risk Label"]
        ]

        fig = go.Figure(go.Bar(
            x=cmp_df["Company"],
            y=cmp_df["Risk %"],
            marker=dict(color=colors, line=dict(width=0)),
            text=[f"{v}%" for v in cmp_df["Risk %"]],
            textposition="outside"
        ))

        fig.update_layout(**PLOTLY_THEME)
        fig.update_yaxes(range=[0, 110])

        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # ------------------ AVG DURATION ------------------
    with t4:
        section_title("AVG INCIDENT DURATION (MIN)", "⏱️")

        fig = go.Figure(go.Bar(
            x=cmp_df["Company"],
            y=cmp_df["Avg Duration"],
            marker=dict(color=COLORS["purple"], line=dict(width=0)),
            text=[f"{v}m" for v in cmp_df["Avg Duration"]],
            textposition="outside"
        ))

        fig.update_layout(**PLOTLY_THEME, showlegend=False)

        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # ------------------ TABLE ------------------
    st.markdown("<br>", unsafe_allow_html=True)
    section_title("FULL COMPARISON TABLE", "📋")

    show = cmp_df.drop(columns=["Risk Label"]).set_index("Company")
    st.dataframe(show, use_container_width=True)

    # ------------------ RADAR ------------------
    section_title("RELIABILITY RADAR", "🕸️")

    categories = ["Outages", "Avg Duration", "Critical", "Cost ($M)", "Risk %", "SLA Breaches"]

    fig = go.Figure()

    for c in sel:
        row = cmp_df[cmp_df["Company"] == c].iloc[0]
        values = [row[k] for k in categories]

        max_vals = cmp_df[categories].max()
        normalized = [
            (v / m) * 100 if m > 0 else 0
            for v, m in zip(values, max_vals)
        ]

        fig.add_trace(go.Scatterpolar(
            r=normalized + [normalized[0]],
            theta=categories + [categories[0]],
            fill="toself",
            name=c,
            line=dict(width=2),
            opacity=0.75
        ))

    fig.update_layout(
        **PLOTLY_THEME,
        polar=dict(
            bgcolor="rgba(8,12,28,0.80)",
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor="rgba(99,102,241,0.15)",
                tickfont=dict(size=9, color="#64748b")
            ),
            angularaxis=dict(
                gridcolor="rgba(99,102,241,0.15)",
                tickfont=dict(size=11, color="#94a3b8")
            )
        ),
        showlegend=True,
        height=450
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})