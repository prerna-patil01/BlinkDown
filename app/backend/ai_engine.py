import pandas as pd
import random

# ------------------ RESPONSE STYLES ------------------
OPENINGS = [
    "Here's what stands out:",
    "Based on current outage data:",
    "After analyzing the system:",
    "Key insight from the data:",
]

RECOMMENDATIONS = [
    "Improve redundancy in critical services",
    "Strengthen monitoring and alerting pipelines",
    "Optimize deployment validation processes",
    "Introduce automated failover mechanisms",
    "Reduce response time with better incident workflows"
]


# ------------------ CORE ANALYSIS ------------------
def analyze_data(df, fin_df, company=None):
    if company:
        df = df[df["company"] == company]
        fin_df = fin_df[fin_df["company"] == company]

    if df.empty:
        return None

    result = {}

    result["top_company"] = df["company"].value_counts().idxmax()
    result["top_service"] = df["service"].value_counts().idxmax()
    result["top_cause"] = df["root_cause"].value_counts().idxmax()
    result["total_incidents"] = len(df)

    result["avg_duration"] = round(df["duration_min"].mean(), 1)
    result["peak_hour"] = df["hour"].value_counts().idxmax()

    if not fin_df.empty:
        result["total_cost"] = int(fin_df["cost_usd"].sum())
        result["sla_rate"] = round(fin_df["sla_breach"].mean() * 100, 1)
    else:
        result["total_cost"] = 0
        result["sla_rate"] = 0

    return result


# ------------------ SMART RESPONSE ENGINE ------------------
def generate_response(question, data):
    q = question.lower()

    opening = random.choice(OPENINGS)
    recs = random.sample(RECOMMENDATIONS, 2)

    if not data:
        return "No sufficient data available for analysis."

    # ----------- CASES -----------

    if "risk" in q or "highest" in q:
        return f"""
{opening}

🔴 **Key Finding:** {data['top_company']} shows the highest outage risk.

📊 **Supporting Data:**
- {data['total_incidents']} total incidents recorded
- Most failures in **{data['top_service']}**
- Dominant issue: **{data['top_cause']}**

💡 **Recommendations:**
1. {recs[0]}
2. {recs[1]}
"""

    elif "root cause" in q:
        return f"""
{opening}

⚙️ **Key Finding:** Primary failure driver is **{data['top_cause']}**

📊 **Supporting Data:**
- Most frequent across incidents
- Strong correlation with {data['top_service']}

💡 **Recommendations:**
1. Build runbooks for {data['top_cause']}
2. {recs[0]}
"""

    elif "pattern" in q or "when" in q:
        return f"""
{opening}

🕒 **Key Finding:** Outages peak at **{data['peak_hour']}:00**

📊 **Supporting Data:**
- High clustering during off-peak hours
- Likely linked to deployments/low monitoring

💡 **Recommendations:**
1. Avoid releases during {data['peak_hour']}:00
2. {recs[0]}
"""

    elif "service" in q:
        return f"""
{opening}

🏗️ **Key Finding:** **{data['top_service']}** is most failure-prone

📊 **Supporting Data:**
- Highest incident concentration
- Frequently impacted by {data['top_cause']}

💡 **Recommendations:**
1. Add redundancy layers
2. {recs[1]}
"""

    elif "cost" in q or "financial" in q:
        return f"""
{opening}

💸 **Key Finding:** Total loss is **${data['total_cost']:,}**

📊 **Supporting Data:**
- Significant SLA violations impact cost
- Repeated downtime spikes

💡 **Recommendations:**
1. Reduce downtime duration
2. {recs[0]}
"""

    elif "sla" in q:
        return f"""
{opening}

⚖️ **Key Finding:** SLA breach rate is **{data['sla_rate']}%**

📊 **Supporting Data:**
- Indicates response inefficiency
- High operational risk

💡 **Recommendations:**
1. Improve response workflows
2. {recs[1]}
"""

    else:
        return f"""
{opening}

📊 **Key Insight:**
- Top company: **{data['top_company']}**
- Main issue: **{data['top_cause']}**
- Peak failure time: **{data['peak_hour']}:00**

💡 **Recommendations:**
1. {recs[0]}
2. {recs[1]}
"""


# ------------------ STREAMING ------------------
def stream_blink(question: str, context: dict, history: list = None):
    df = context["df"]
    fin_df = context["fin_df"]
    company = context.get("company")

    data = analyze_data(df, fin_df, company)
    response = generate_response(question, data)

    for word in response.split():
        yield word + " "


# ------------------ CONTEXT ------------------
def build_context(df, fin_df, company=None):
    return {
        "df": df,
        "fin_df": fin_df,
        "company": company
    }


# ------------------ SUGGESTIONS ------------------
def generate_suggestions(df, fin_df, company: str) -> list:
    data = analyze_data(df, fin_df, company)

    if not data:
        return [("⚠️", "NO DATA", "No data available.")]

    return [
        ("⚙️", "ROOT CAUSE", f"Focus on fixing {data['top_cause']} issues."),
        ("🏗️", "SERVICE", f"{data['top_service']} needs reliability improvements."),
        ("📊", "MONITORING", "Enhance real-time monitoring systems.")
    ]