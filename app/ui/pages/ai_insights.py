import streamlit as st
from app.ui.components.cards import section_title, page_header
from app.backend.ai_engine import stream_blink, build_context

COMPANIES = ["All Companies", "AWS", "Azure", "GCP", "Cloudflare", "Vercel", "Fastly", "Akamai"]

QUICK_PROMPTS = [
    "Which company has the highest outage risk right now?",
    "What are the top 3 root causes of critical incidents?",
    "When do most outages happen? Any patterns?",
    "Which service type fails most frequently?",
    "Give me a reliability ranking of all companies.",
    "What should AWS prioritize to reduce downtime?",
    "Estimate total financial impact across all companies.",
    "Which company has the best SLA performance?",
]


def render(df, fin_df, pred_df):
    page_header("🤖 Blink AI Analyst", "Conversational intelligence powered by GPT-4o")

    # ------------------ STATE INIT ------------------
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "pending_prompt" not in st.session_state:
        st.session_state.pending_prompt = None

    # ------------------ LAYOUT ------------------
    left, right = st.columns([3, 1])

    # ------------------ RIGHT PANEL ------------------
    with right:
        section_title("CONTEXT", "🎯")

        company_filter = st.selectbox(
            "Focus on",
            COMPANIES,
            label_visibility="collapsed"
        )

        company = None if company_filter == "All Companies" else company_filter

        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []
            st.session_state.messages = []
            st.session_state.pending_prompt = None
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        section_title("QUICK PROMPTS", "⚡")

        for i, qp in enumerate(QUICK_PROMPTS):
            if st.button(qp, key=f"qp_{i}", use_container_width=True):
                st.session_state.pending_prompt = qp

    # ------------------ LEFT PANEL ------------------
    with left:
        section_title("CONVERSATION", "💬")

        if not st.session_state.messages:
            st.markdown("""
<div class="chat-bubble-ai">
  <b>👋 Hi, I'm Blink!</b><br><br>
  I'm your AI outage analyst. Ask me anything about the service reliability data —
  risk scores, patterns, cost impact, root causes, or recommendations.<br><br>
  Try: <i>"Which company is most at risk right now?"</i>
</div>
""", unsafe_allow_html=True)

        # Show chat history
        for msg in st.session_state.messages:
            role_class = "chat-bubble-user" if msg["role"] == "user" else "chat-bubble-ai"
            st.markdown(
                f'<div class="{role_class}">{msg["content"]}</div>',
                unsafe_allow_html=True
            )

        # ------------------ INPUT ------------------
        pending = st.session_state.pending_prompt
        question = st.chat_input("Ask Blink anything about outage intelligence...")

        if pending:
            question = pending
            st.session_state.pending_prompt = None

        # ------------------ HANDLE QUESTION ------------------
        if question:
            st.session_state.messages.append({"role": "user", "content": question})

            context = build_context(df, fin_df, company)

            st.markdown(
                f'<div class="chat-bubble-user">{question}</div>',
                unsafe_allow_html=True
            )

            with st.spinner("Blink is analyzing..."):
                response = ""
                placeholder = st.empty()

                for chunk in stream_blink(
                    question,
                    context,
                    st.session_state.chat_history
                ):
                    response += chunk
                    placeholder.markdown(
                        f'<div class="chat-bubble-ai">{response}▌</div>',
                        unsafe_allow_html=True
                    )

                placeholder.markdown(
                    f'<div class="chat-bubble-ai">{response}</div>',
                    unsafe_allow_html=True
                )
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.session_state.chat_history.append({"role": "user", "content": question})
            st.session_state.chat_history.append({"role": "assistant", "content": response})

            st.rerun()