import streamlit as st

from app.ui.theme import inject_css
from app.backend.data_engine import load_outages, load_financial, load_predictions
from app.ui.pages import overview, company, predictions, compare, incidents, financial, ai_insights
st.set_page_config(
    page_title="BlinkDown",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_css()

# ── Sidebar ───────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
<div style="padding:20px 8px 16px;">
  <div style="font-size:22px;font-weight:800;background:linear-gradient(135deg,#6366f1,#8b5cf6,#06b6d4);
              -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">
    ⚡ BlinkDown
  </div>
  <div style="font-size:11px;color:#475569;letter-spacing:0.08em;margin-top:2px;">
    AI OUTAGE INTELLIGENCE
  </div>
</div>""", unsafe_allow_html=True)
    st.divider()

    NAV = [
        ("overview",    "🏠", "Overview"),
        ("company",     "🏢", "Company View"),
        ("predictions", "🔮", "Predictions"),
        ("compare",     "⚖️",  "Compare"),
        ("incidents",   "📋", "Incidents"),
        ("financial",   "💸", "Financial"),
        ("ai_insights", "🤖", "Blink AI"),
    ]

    if "page" not in st.session_state:
        st.session_state.page = "overview"

    for key, icon, label in NAV:
        active = "active" if st.session_state.page == key else ""
        if st.button(f"{icon}  {label}", key=f"nav_{key}",
                     use_container_width=True,
                     type="primary" if active else "secondary"):
            st.session_state.page = key
            st.rerun()

    st.divider()
    st.markdown("""
<div style="font-size:10px;color:#334155;text-align:center;line-height:1.8;">
  v1.0.0 · GPT-4o powered<br>
  Built for SRE & DevOps teams
</div>""", unsafe_allow_html=True)

# ── Load data ─────────────────────────────────────────────────────
df      = load_outages()
fin_df  = load_financial()
pred_df = load_predictions()

# ── Route ────────────────────────────────────────────────────────
page = st.session_state.page
if   page == "overview":    overview.render(df, fin_df, pred_df)
elif page == "company":     company.render(df, fin_df, pred_df)
elif page == "predictions": predictions.render(df, fin_df, pred_df)
elif page == "compare":     compare.render(df, fin_df, pred_df)
elif page == "incidents":   incidents.render(df, fin_df, pred_df)
elif page == "financial":   financial.render(df, fin_df, pred_df)
elif page == "ai_insights": ai_insights.render(df, fin_df, pred_df)
