import streamlit as st
import uuid
from services.ai_service import stream_ai_response, SYSTEM_PROMPT
from database.db import save_chat_message, get_chat_history


SAGE_STARTERS = [
    "🧮 Solve a math problem step-by-step",
    "💡 Explain a concept (any level)",
    "📝 Summarize my notes",
    "🎯 Generate a practice quiz",
    "🧠 Create memory tricks for...",
    "📚 Help me make a study plan",
    "🔍 Break down a complex topic",
    "✅ Check if my answer is correct",
]


def render_ai_assistant(user: dict):
    uid = user["id"]

    # Session ID for conversation continuity
    if "chat_session_id" not in st.session_state:
        st.session_state.chat_session_id = str(uuid.uuid4())[:8]

    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Load from DB
        history = get_chat_history(uid, st.session_state.chat_session_id)
        st.session_state.messages = history

    # Header
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        st.markdown("""
        <div>
            <span class="sv-hero-title" style="font-size:2rem;">🤖 Sage AI</span>
            <div style="color:var(--text-secondary); font-size:0.9rem; margin-top:0.2rem;">
                Your personal study companion. Smarter than your textbook, funnier than your professor.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style="text-align:right; padding-top:0.5rem;">
            <span class="sv-badge sv-badge-green">🟢 Online</span>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        if st.button("🗑️ Clear Chat", type="secondary"):
            st.session_state.messages = []
            st.session_state.chat_session_id = str(uuid.uuid4())[:8]
            st.rerun()

    st.markdown("---")

    # Quick starters (only show if no messages)
    if not st.session_state.messages:
        st.markdown("#### ✨ What can Sage help you with?")
        cols = st.columns(4)
        for i, starter in enumerate(SAGE_STARTERS):
            with cols[i % 4]:
                if st.button(starter, key=f"starter_{i}", use_container_width=True):
                    # Strip emoji for cleaner input
                    clean = " ".join(starter.split()[1:])
                    st.session_state.pending_message = clean
                    st.rerun()

        st.markdown("""
        <div class="sv-quote-box" style="margin-top: 1rem; text-align: center;">
            <strong>Pro tip:</strong> The more specific your question, the better Sage's answer.
            "Explain photosynthesis" → good. 
            "Explain photosynthesis like I'm 5 and I forgot to study" → legendary. 🏆
        </div>
        """, unsafe_allow_html=True)

    # Display chat history
    for msg in st.session_state.messages:
        role = msg["role"]
        content = msg["content"]
        with st.chat_message(role, avatar="🤖" if role == "assistant" else user.get("avatar_emoji", "🎓")):
            st.markdown(content)

    # Handle pending message from quick starters
    if "pending_message" in st.session_state:
        prompt = st.session_state.pop("pending_message")
        _send_message(prompt, uid)

    # Chat input
    if prompt := st.chat_input("Ask Sage anything... homework, concepts, quizzes, study plans 🚀"):
        _send_message(prompt, uid)

    # Side panel with tools
    with st.sidebar:
        st.markdown("---")
        st.markdown("#### 🛠️ Sage Tools")

        with st.expander("📊 Generate Quiz", expanded=False):
            q_subject = st.selectbox("Subject", ["Mathematics", "Physics", "Chemistry", "Biology", "History", "English", "Other"], key="quiz_subject_ai")
            q_topic = st.text_input("Topic", placeholder="e.g. Quadratic equations", key="quiz_topic_ai")
            q_diff = st.select_slider("Difficulty", ["Easy", "Medium", "Hard", "Expert"], value="Medium", key="quiz_diff_ai")
            if st.button("⚡ Generate Quiz", use_container_width=True, key="gen_quiz_btn"):
                if q_topic:
                    st.session_state.pending_message = f"Generate a {q_diff} quiz with 5 multiple-choice questions about {q_topic} in {q_subject}. Format each question clearly with A/B/C/D options and show the answer and explanation at the end."
                    st.rerun()

        with st.expander("🃏 Make Flashcards", expanded=False):
            fc_content = st.text_area("Paste your notes or topic", height=100, key="fc_content_ai")
            fc_num = st.slider("Number of cards", 5, 15, 8, key="fc_num_ai")
            if st.button("🃏 Create Flashcards", use_container_width=True, key="gen_fc_btn"):
                if fc_content:
                    st.session_state.pending_message = f"Create {fc_num} flashcards from this content (format as Q: / A: pairs):\n\n{fc_content}"
                    st.rerun()

        with st.expander("📝 Summarize Notes", expanded=False):
            sum_content = st.text_area("Paste content to summarize", height=100, key="sum_content_ai")
            sum_style = st.radio("Style", ["Concise bullets", "Detailed", "ELI5", "Exam focus"], key="sum_style_ai")
            if st.button("✨ Summarize", use_container_width=True, key="sum_btn"):
                if sum_content:
                    style_map = {"Concise bullets": "concise bullet points", "Detailed": "detailed sections", "ELI5": "simple terms a child could understand", "Exam focus": "exam-focused key points"}
                    st.session_state.pending_message = f"Summarize this in {style_map.get(sum_style, 'concise bullet points')}:\n\n{sum_content}"
                    st.rerun()

        with st.expander("🧠 Explain Concept", expanded=False):
            exp_concept = st.text_input("Concept to explain", key="exp_concept_ai")
            exp_level = st.select_slider("Complexity", ["ELI5", "Beginner", "Intermediate", "Advanced", "Expert"], value="Intermediate", key="exp_level_ai")
            if st.button("💡 Explain It", use_container_width=True, key="exp_btn"):
                if exp_concept:
                    st.session_state.pending_message = f"Explain '{exp_concept}' at {exp_level} level with examples and analogies."
                    st.rerun()


def _send_message(prompt: str, uid: int):
    """Send user message and stream AI response."""
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    save_chat_message(uid, "user", prompt, st.session_state.chat_session_id)

    with st.chat_message("user", avatar="🎓"):
        st.markdown(prompt)

    # Stream assistant response
    with st.chat_message("assistant", avatar="🤖"):
        response_placeholder = st.empty()
        full_response = ""

        # Build message history for API (last 20 messages)
        api_messages = [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages[-20:]
        ]

        try:
            for chunk in stream_ai_response(api_messages, SYSTEM_PROMPT):
                full_response += chunk
                response_placeholder.markdown(full_response + "▊")
            response_placeholder.markdown(full_response)
        except Exception as e:
            full_response = f"⚠️ Sage is having a moment... ({str(e)})\n\nMake sure your ANTHROPIC_API_KEY is set!"
            response_placeholder.error(full_response)

    # Save assistant response
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    save_chat_message(uid, "assistant", full_response, st.session_state.chat_session_id)
