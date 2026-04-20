import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from ui.components.cards import section_title, page_header, metric_card
from ui.components.charts import financial_bar
from ui.theme import PLOTLY_THEME, COLORS

COMPANIES = ["AWS", "Azure", "GCP", "Cloudflare", "Vercel", "Fastly", "Akamai"]

def render(df, fin_df, pred_df):
    page_header("💸 Financial Intelligence", "Cost impact analysis and SLA breach tracking")

    total = fin_df["cost_usd"].sum()

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        metric_card("Total Est. Loss", f"${total/1e6:.1f}M", icon="💸", color="#ef4444")
    with m2:
        metric_card("Avg Cost/Incident", f"${fin_df['cost_usd'].mean():,.0f}", icon="📊", color="#f59e0b")
    with m3:
        metric_card("SLA Breaches", f"{fin_df['sla_breach'].sum():,}", icon="📋", color="#8b5cf6")
    with m4:
        metric_card("Total SLA Penalty", f"${fin_df['sla_penalty'].sum()/1e6:.2f}M", icon="⚖️", color="#ef4444")

    st.markdown("<br>", unsafe_allow_html=True)

    section_title("FINANCIAL IMPACT BY COMPANY", "💰")
    st.plotly_chart(financial_bar(fin_df), use_container_width=True, config={"displayModeBar": False})

    left, right = st.columns(2)

    # ---------------- LEFT ----------------
    with left:
        section_title("MONTHLY COST TREND", "📈")

        fin_df["month"] = pd.to_datetime(fin_df["timestamp"]).dt.to_period("M").astype(str)
        monthly = fin_df.groupby("month")["cost_usd"].sum().reset_index()

        fig = go.Figure(go.Scatter(
            x=monthly["month"],
            y=monthly["cost_usd"],
            mode="lines+markers",
            line=dict(color=COLORS["indigo"], width=2.5),
            fill="tozeroy",
            fillcolor="rgba(99,102,241,0.08)",
            marker=dict(size=6, color=COLORS["purple"]),
            hovertemplate="<b>%{x}</b><br>Cost: $%{y:,.0f}<extra></extra>"
        ))

        layout = {**PLOTLY_THEME}
        layout["xaxis"] = {**layout.get("xaxis", {}), "title": "Month"}
        layout["yaxis"] = {**layout.get("yaxis", {}), "title": "Cost (USD)"}

        fig.update_layout(**layout)

        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # ---------------- RIGHT ----------------
    with right:
        section_title("SLA BREACH RATE BY COMPANY", "⚖️")

        sla = fin_df.groupby("company").agg(
            total=("sla_breach", "count"),
            breaches=("sla_breach", "sum")
        ).reset_index()

        sla["rate"] = (sla["breaches"] / sla["total"] * 100).round(1)
        sla = sla.sort_values("rate", ascending=False)

        fig = go.Figure(go.Bar(
            x=sla["company"],
            y=sla["rate"],
            marker=dict(
                color=sla["rate"],
                colorscale=[[0, COLORS["low"]], [0.5, COLORS["medium"]], [1, COLORS["critical"]]],
                line=dict(width=0)
            ),
            text=[f"{v}%" for v in sla["rate"]],
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>SLA Breach Rate: %{y}%<extra></extra>"
        ))

        # ✅ FIXED PROPERLY (NO DUPLICATE YAXIS)
        layout = {**PLOTLY_THEME}
        layout["yaxis"] = {**layout.get("yaxis", {}), "range": [0, 55]}

        fig.update_layout(**layout)
        fig.update_layout(showlegend=False)

        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # ---------------- TABLE ----------------
    section_title("FINANCIAL DETAIL TABLE", "📋")

    show = fin_df.groupby("company").agg(
        total_cost=("cost_usd", "sum"),
        avg_cost=("cost_usd", "mean"),
        sla_breaches=("sla_breach", "sum"),
        sla_penalties=("sla_penalty", "sum")
    ).reset_index()

    show.columns = ["Company", "Total Cost", "Avg/Incident", "SLA Breaches", "SLA Penalties"]

    show["Total Cost"] = show["Total Cost"].apply(lambda x: f"${x:,.0f}")
    show["Avg/Incident"] = show["Avg/Incident"].apply(lambda x: f"${x:,.0f}")
    show["SLA Penalties"] = show["SLA Penalties"].apply(lambda x: f"${x:,.0f}")

    st.dataframe(show.set_index("Company"), use_container_width=True)