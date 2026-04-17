import pandas as pd
import numpy as np
import streamlit as st
from pathlib import Path

DATA_DIR = Path("data/raw")

@st.cache_data(ttl=600)
def load_outages():
    df = pd.read_csv(DATA_DIR / "outages.csv")
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["severity_num"] = df["severity"].map({"low":1,"medium":2,"high":3,"critical":4})
    return df

@st.cache_data(ttl=600)
def load_financial():
    df = pd.read_csv(DATA_DIR / "financial.csv")
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df

@st.cache_data(ttl=600)
def load_predictions():
    df = pd.read_csv(DATA_DIR / "predictions.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df

def compute_risk(df, company):
    cdf = df[df["company"]==company].copy()
    if cdf.empty:
        return {"risk_pct":0,"label":"Unknown","color":"#64748b"}
    recent = cdf[cdf["timestamp"] >= cdf["timestamp"].max() - pd.Timedelta(days=7)]
    freq      = len(recent)
    avg_dur   = recent["duration_min"].mean() if not recent.empty else 0
    max_sev   = recent["severity_num"].max() if not recent.empty else 0
    crit_cnt  = (recent["severity"]=="critical").sum()
    score = min(100, round(
        min(freq/12,1)*35 + min(avg_dur/300,1)*30 +
        min(max_sev/4,1)*20 + min(crit_cnt/3,1)*15, 1))
    label = ("Low" if score<30 else "Medium" if score<60 else
             "High" if score<80 else "Critical")
    color = {"Low":"#4ade80","Medium":"#facc15","High":"#fb923c","Critical":"#f87171"}[label]
    return {"risk_pct":score,"label":label,"color":color}

def get_company_stats(df, fin_df, company):
    cdf  = df[df["company"]==company]
    fdf  = fin_df[fin_df["company"]==company]
    return {
        "total_outages":    len(cdf),
        "avg_duration":     round(cdf["duration_min"].mean(), 1),
        "total_downtime":   round(cdf["duration_min"].sum() / 60, 1),
        "critical_count":   int((cdf["severity"]=="critical").sum()),
        "total_cost":       round(fdf["cost_usd"].sum(), 0),
        "sla_breaches":     int(fdf["sla_breach"].sum()),
        "top_service":      cdf["service"].value_counts().index[0] if not cdf.empty else "N/A",
        "top_cause":        cdf["root_cause"].value_counts().index[0] if not cdf.empty else "N/A",
        "users_affected":   int(cdf["users_affected"].sum()),
    }

def get_dashboard_kpis(df, fin_df):
    return {
        "total_outages":  len(df),
        "total_cost":     round(fin_df["cost_usd"].sum(), 0),
        "avg_duration":   round(df["duration_min"].mean(), 1),
        "critical_pct":   round((df["severity"]=="critical").mean()*100, 1),
        "sla_breaches":   int(fin_df["sla_breach"].sum()),
        "companies_monitored": df["company"].nunique(),
    }

def get_current_status(df):
    cutoff = df["timestamp"].max() - pd.Timedelta(hours=48)
    recent = df[df["timestamp"] >= cutoff]
    status_map = {}
    for c in df["company"].unique():
        cdf = recent[recent["company"]==c]
        if cdf.empty:
            status_map[c] = ("operational", "#4ade80")
        elif (cdf["severity"]=="critical").any():
            status_map[c] = ("critical outage", "#f87171")
        elif (cdf["severity"]=="high").any():
            status_map[c] = ("degraded", "#fb923c")
        else:
            status_map[c] = ("minor issues", "#facc15")
    return status_map
