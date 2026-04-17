import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


# 🎨 Common styling
def _style(fig):
    fig.update_layout(
        template="plotly_dark",
        font=dict(family="Inter, sans-serif")
    )
    return fig


# 📈 OUTAGE TIMELINE
def outage_timeline(df, company=None):
    if company and company != "All":
        df = df[df["company"] == company]

    temp = df.copy()
    temp["date"] = temp["timestamp"].dt.date

    agg = temp.groupby("date").size().reset_index(name="outages")

    fig = px.line(
        agg,
        x="date",
        y="outages",
        markers=True,
        title="Outages Over Time"
    )

    fig.update_traces(line=dict(width=3, color="#6366f1"))
    return _style(fig)


# 🍩 SEVERITY DONUT
def severity_donut(df, company=None):
    if company and company != "All":
        df = df[df["company"] == company]

    agg = df["severity"].value_counts().reset_index()
    agg.columns = ["severity", "count"]

    fig = px.pie(
        agg,
        names="severity",
        values="count",
        hole=0.6,
        color="severity",
        color_discrete_map={
            "low": "#4ade80",
            "medium": "#facc15",
            "high": "#fb923c",
            "critical": "#f87171"
        }
    )

    return _style(fig)


# 🏆 COMPANY COMPARISON
def company_comparison_bar(df):
    agg = df.groupby("company").size().reset_index(name="outages")

    fig = px.bar(
        agg,
        x="company",
        y="outages",
        color="outages",
        color_continuous_scale="Blues"
    )

    return _style(fig)


# 🔥 HEATMAP (hour × day)
def heatmap_hour_day(df, company=None):
    if company and company != "All":
        df = df[df["company"] == company]

    temp = df.copy()
    temp["hour"] = temp["timestamp"].dt.hour
    temp["day"] = temp["timestamp"].dt.day_name()

    pivot = temp.pivot_table(
        index="day",
        columns="hour",
        values="id",
        aggfunc="count"
    ).fillna(0)

    fig = px.imshow(
        pivot,
        aspect="auto",
        color_continuous_scale="Inferno"
    )

    return _style(fig)


# 🏗️ SERVICE BREAKDOWN (🔥 FIXED)
def service_breakdown(df, company=None):
    if company and company != "All":
        df = df[df["company"] == company]

    agg = df["service"].value_counts().reset_index()
    agg.columns = ["service", "count"]

    fig = px.bar(
        agg,
        x="service",
        y="count",
        color="count",
        color_continuous_scale="Teal"
    )

    return _style(fig)


# ⚠️ RISK GAUGE
def risk_gauge(value, company):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={"text": f"{company} Risk Score"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "#6366f1"},
            "steps": [
                {"range": [0, 30], "color": "#4ade80"},
                {"range": [30, 60], "color": "#facc15"},
                {"range": [60, 80], "color": "#fb923c"},
                {"range": [80, 100], "color": "#f87171"},
            ],
        }
    ))

    return fig


# 📊 FORECAST CHART
def forecast_chart(pred_df, company=None):
    if company and company != "All" and "company" in pred_df.columns:
        pred_df = pred_df[pred_df["company"] == company]

    y_col = "predicted_outages" if "predicted_outages" in pred_df.columns else pred_df.columns[1]

    fig = px.line(
        pred_df,
        x="date",
        y=y_col,
        title="Outage Forecast",
        markers=True
    )

    fig.update_traces(line=dict(color="#22c55e", width=3))
    return _style(fig)


# 💸 FINANCIAL BAR CHART
def financial_bar(fin_df, company=None):
    if company and company != "All" and "company" in fin_df.columns:
        fin_df = fin_df[fin_df["company"] == company]

    if "company" in fin_df.columns:
        agg = fin_df.groupby("company")["cost_usd"].sum().reset_index()
        x_col = "company"
    else:
        agg = fin_df.groupby("timestamp")["cost_usd"].sum().reset_index()
        x_col = "timestamp"

    fig = px.bar(
        agg,
        x=x_col,
        y="cost_usd",
        title="Financial Impact",
        color="cost_usd",
        color_continuous_scale="Reds"
    )

    return _style(fig)