import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

np.random.seed(42)

COMPANIES = ["AWS", "Azure", "GCP", "Cloudflare", "Vercel", "Fastly", "Akamai"]
SERVICES  = ["Compute", "Storage", "Network", "Database", "CDN", "DNS", "Auth"]
SEVERITIES = ["low", "medium", "high", "critical"]
REGIONS   = ["us-east-1", "us-west-2", "eu-west-1", "ap-south-1", "ap-southeast-1"]
ROOT_CAUSES = [
    "Hardware failure", "Software bug", "DDoS attack", "Config error",
    "Power outage", "Network congestion", "Expired certificate",
    "Memory leak", "Disk full", "Human error"
]

def gen_outages(n=1200):
    rows = []
    start = datetime(2022, 1, 1)
    company_probs = [0.23, 0.20, 0.17, 0.15, 0.11, 0.08, 0.06]
    hour_w = np.ones(24)
    hour_w[2:5]   *= 3.0
    hour_w[14:17] *= 2.0
    hour_w[9:11]  *= 1.5
    hour_w /= hour_w.sum()

    for i in range(n):
        company  = np.random.choice(COMPANIES, p=company_probs)
        gap      = np.random.exponential(28)
        start   += timedelta(hours=gap)
        hour     = np.random.choice(24, p=hour_w)
        ts       = start.replace(hour=hour, minute=np.random.randint(0,60), second=0)
        sev      = np.random.choice(SEVERITIES, p=[0.38,0.32,0.20,0.10])
        base_dur = {"low":12,"medium":55,"high":170,"critical":340}[sev]
        dur      = max(1, round(np.random.exponential(base_dur), 1))
        region   = np.random.choice(REGIONS)
        service  = np.random.choice(SERVICES)
        cause    = np.random.choice(ROOT_CAUSES)
        affected = int(np.random.exponential({"low":500,"medium":5000,"high":50000,"critical":500000}[sev]))
        resolved = np.random.choice([True,False], p=[0.93,0.07])
        rows.append({
            "id":               i+1,
            "company":          company,
            "timestamp":        ts.strftime("%Y-%m-%d %H:%M:%S"),
            "duration_min":     dur,
            "severity":         sev,
            "service":          service,
            "region":           region,
            "root_cause":       cause,
            "users_affected":   affected,
            "resolved":         resolved,
            "year":             ts.year,
            "month":            ts.month,
            "day_of_week":      ts.strftime("%A"),
            "hour":             hour,
        })
    return pd.DataFrame(rows)

def gen_financial(outages_df):
    cost_pm = {"AWS":9200,"Azure":7800,"GCP":7100,"Cloudflare":5200,
               "Vercel":2800,"Fastly":4100,"Akamai":4600}
    rows = []
    for _, r in outages_df.iterrows():
        cpm   = cost_pm.get(r["company"], 5000)
        cost  = round(r["duration_min"] * cpm * (1 + np.random.uniform(-0.1,0.1)), 0)
        rows.append({
            "id":           r["id"],
            "company":      r["company"],
            "timestamp":    r["timestamp"],
            "duration_min": r["duration_min"],
            "severity":     r["severity"],
            "cost_usd":     cost,
            "cost_per_min": cpm,
            "sla_breach":   r["duration_min"] > 60,
            "sla_penalty":  round(cost * 0.15, 0) if r["duration_min"] > 60 else 0,
        })
    return pd.DataFrame(rows)

def gen_predictions(outages_df):
    rows = []
    base = datetime(2024, 6, 1)
    for company in COMPANIES:
        cdf = outages_df[outages_df["company"]==company]
        avg_dur = cdf["duration_min"].mean()
        freq    = len(cdf) / 24  # monthly avg
        for i in range(90):
            dt = base + timedelta(days=i)
            noise = np.random.normal(0, 0.08)
            risk  = round(min(99, max(5, 30 + freq*3 + np.random.normal(0,10))), 1)
            rows.append({
                "company":          company,
                "date":             dt.strftime("%Y-%m-%d"),
                "predicted_outages":max(0, round(freq + noise, 2)),
                "predicted_dur_min":max(0, round(avg_dur + np.random.normal(0,15),1)),
                "risk_score":       risk,
                "confidence":       round(np.random.uniform(0.70, 0.95), 2),
            })
    return pd.DataFrame(rows)

os.makedirs("data/raw", exist_ok=True)
print("Generating outages...")
outages = gen_outages(1200)
outages.to_csv("data/raw/outages.csv", index=False)
print(f"  ✓ outages.csv — {len(outages)} rows")

print("Generating financial impact...")
financial = gen_financial(outages)
financial.to_csv("data/raw/financial.csv", index=False)
print(f"  ✓ financial.csv — {len(financial)} rows")

print("Generating predictions...")
predictions = gen_predictions(outages)
predictions.to_csv("data/raw/predictions.csv", index=False)
print(f"  ✓ predictions.csv — {len(predictions)} rows")

print("\nAll datasets ready in data/raw/")
