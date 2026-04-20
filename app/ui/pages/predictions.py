import streamlit as st
import pandas as pd
from ui.components.cards import metric_card, section_title, page_header, risk_badge
from ui.components.charts import forecast_chart, risk_gauge
from backend.data_engine import compute_risk

COMPANIES = ["AWS", "Azure", "GCP", "Cloudflare", "Vercel", "Fastly", "Akamai"]


def render(df, fin_df, pred_df):
    page_header("Predictive Intelligence", "ML-powered outage forecasting and risk scoring")

    col_sel, col_hz, _ = st.columns([1, 1, 2])

    with col_sel:
        company = st.selectbox("Company", COMPANIES, label_visibility="collapsed")

    with col_hz:
        horizon = st.slider("Forecast days", 14, 90, 30, label_visibility="collapsed")

    risk = compute_risk(df, company)
    cpred = pred_df[(pred_df["company"] == company)].head(horizon).copy()

    # ------------------ METRICS ------------------
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card("Risk Score", f"{risk['risk_pct']}%", icon="⚠️", color=risk["color"])

    with c2:
        metric_card("Risk Level", risk["label"], icon="🎯", color=risk["color"])

    with c3:
        metric_card("Forecast Days", str(horizon), icon="📅", color="#6366f1")

    with c4:
        avg_pred = cpred["predicted_dur_min"].mean() if not cpred.empty else 0
        metric_card("Predicted Avg Downtime", f"{avg_pred:.0f}m", icon="⏱️", color="#f59e0b")

    st.markdown("<br>", unsafe_allow_html=True)

    left, right = st.columns([3, 1])

    # ------------------ LEFT SIDE ------------------
    with left:
        section_title("DOWNTIME FORECAST CURVE", "📈")

        if not cpred.empty:
            st.plotly_chart(
                forecast_chart(cpred, company),
                use_container_width=True,
                config={"displayModeBar": False}
            )
        else:
            st.info("No prediction data available for this selection.")

        # -------- RISK LANDSCAPE --------
        section_title("RISK LANDSCAPE — ALL COMPANIES", "🌐")

        import plotly.graph_objects as go
        from ui.theme import PLOTLY_THEME, COLORS

        risks = [(c, compute_risk(df, c)) for c in COMPANIES]
        risks.sort(key=lambda x: x[1]["risk_pct"], reverse=True)

        fig = go.Figure(go.Bar(
            x=[r[0] for r in risks],
            y=[r[1]["risk_pct"] for r in risks],
            marker=dict(
                color=[r[1]["color"] for r in risks],
                line=dict(width=0)
            ),
            text=[f"{r[1]['risk_pct']}%" for r in risks],
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>Risk: %{y}%<extra></extra>"
        ))

        fig.update_layout(**PLOTLY_THEME)
        fig.update_yaxes(range=[0, 110])

        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # ------------------ RIGHT SIDE ------------------
    with right:
        section_title("RISK GAUGE", "🎯")

        st.plotly_chart(
            risk_gauge(risk["risk_pct"], company),
            use_container_width=True,
            config={"displayModeBar": False}
        )

        badge = risk_badge(risk["label"])
        st.markdown(
            f'<div style="text-align:center;margin:8px 0 16px">{badge}</div>',
            unsafe_allow_html=True
        )

        section_title("PREDICTION TABLE", "📋")

        if not cpred.empty:
            show = cpred[[
                "date",
                "predicted_outages",
                "predicted_dur_min",
                "risk_score",
                "confidence"
            ]].copy()

            show["date"] = show["date"].dt.strftime("%m/%d")
            show["confidence"] = (show["confidence"] * 100).round(0).astype(int).astype(str) + "%"

            show.columns = ["Date", "Outages", "Dur(m)", "Risk%", "Conf"]

            st.dataframe(show.head(14), hide_index=True, use_container_width=True)