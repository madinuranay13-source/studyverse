import streamlit as st
import json
from database.db import save_quiz_result
from components.styles import SUBJECTS
from services.ai_service import generate_quiz


def render_quiz(user: dict):
    uid = user["id"]

    st.markdown("""
    <div>
        <span class="sv-hero-title" style="font-size:2rem;">🎯 AI Quiz Generator</span>
        <div style="color:var(--text-secondary); font-size:0.9rem; margin-top:0.2rem;">
            Sage generates personalized quizzes. Like a teacher, but less terrifying.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    # Quiz setup vs active quiz
    if "quiz_active" not in st.session_state:
        st.session_state.quiz_active = False
    if "quiz_questions" not in st.session_state:
        st.session_state.quiz_questions = []
    if "quiz_answers" not in st.session_state:
        st.session_state.quiz_answers = {}
    if "quiz_submitted" not in st.session_state:
        st.session_state.quiz_submitted = False
    if "quiz_subject" not in st.session_state:
        st.session_state.quiz_subject = ""

    if not st.session_state.quiz_active:
        _render_quiz_setup(uid)
    elif st.session_state.quiz_submitted:
        _render_quiz_results(uid)
    else:
        _render_quiz_active(uid)


def _render_quiz_setup(uid: int):
    st.markdown("#### ⚙️ Configure Your Quiz")

    col1, col2 = st.columns(2)
    with col1:
        q_subject = st.selectbox("Subject", SUBJECTS, key="qs_subject")
        q_topic = st.text_input("Topic / Chapter", placeholder="e.g. Newton's Laws of Motion", key="qs_topic")
        q_num = st.slider("Number of Questions", 3, 15, 5, key="qs_num")

    with col2:
        q_diff = st.select_slider(
            "Difficulty",
            options=["Easy 😌", "Medium 🤔", "Hard 😤", "Expert 🤯"],
            value="Medium 🤔",
            key="qs_diff",
        )
        q_style = st.radio(
            "Question Style",
            ["Mixed", "Conceptual", "Problem-solving", "Definition-based"],
            key="qs_style",
        )

    st.markdown("""
    <div class="sv-quote-box" style="margin: 1rem 0;">
        💡 The more specific your topic, the better the quiz. 
        "Biology" → meh. "Cell division — mitosis vs meiosis" → 🔥
    </div>
    """, unsafe_allow_html=True)

    if st.button("⚡ Generate Quiz with AI", key="gen_quiz_main"):
        if not q_topic:
            st.error("Enter a topic to generate questions!")
            return

        with st.spinner("🤖 Sage is crafting your quiz... (don't peek at the answers)"):
            try:
                diff_clean = q_diff.split(" ")[0]
                questions = generate_quiz(q_subject, q_topic, diff_clean, q_num)
                if questions:
                    st.session_state.quiz_questions = questions
                    st.session_state.quiz_answers = {}
                    st.session_state.quiz_submitted = False
                    st.session_state.quiz_active = True
                    st.session_state.quiz_subject = q_subject
                    st.session_state.quiz_topic = q_topic
                    st.rerun()
                else:
                    st.error("Couldn't generate quiz. Try a different topic or check your API key.")
            except Exception as e:
                st.error(f"Quiz generation failed: {e}")

    # Past quiz results
    from database.db import get_quiz_results
    past = get_quiz_results(uid)
    if past:
        st.markdown("---")
        st.markdown("#### 📊 Past Quiz Results")
        for r in past[:5]:
            score_color = "#00ff88" if r["score_percent"] >= 80 else "#ff8c42" if r["score_percent"] >= 60 else "#ff4d9d"
            st.markdown(f"""
            <div class="sv-card" style="display:flex; justify-content:space-between; align-items:center; 
                         padding:0.8rem 1.2rem; margin-bottom:0.4rem;">
                <div>
                    <span style="font-weight:600;">{r['subject']}</span>
                    <span style="color:var(--text-muted); margin-left:0.5rem; font-size:0.8rem;">
                        {r['correct_answers']}/{r['total_questions']} correct
                    </span>
                </div>
                <div style="font-family:var(--font-display); font-size:1.3rem; font-weight:800; color:{score_color};">
                    {r['score_percent']:.0f}%
                </div>
            </div>
            """, unsafe_allow_html=True)


def _render_quiz_active(uid: int):
    questions = st.session_state.quiz_questions
    answers = st.session_state.quiz_answers

    topic = st.session_state.get("quiz_topic", "")
    subject = st.session_state.get("quiz_subject", "")

    # Header
    answered = len(answers)
    total = len(questions)
    st.progress(answered / total)
    st.caption(f"Progress: {answered}/{total} questions answered • {subject} — {topic}")

    col_quiz, col_nav = st.columns([3, 1])

    with col_nav:
        st.markdown("#### 📋 Questions")
        for i, q in enumerate(questions):
            answered_i = i in answers
            color = "var(--neon-green)" if answered_i else "var(--text-muted)"
            st.markdown(f"""
            <div style="padding:0.3rem 0.5rem; border-radius:6px; margin-bottom:0.2rem;
                        background:{'rgba(0,255,136,0.1)' if answered_i else 'transparent'};
                        color:{color}; font-size:0.85rem;">
                {'✅' if answered_i else '○'} Q{i+1}
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        if st.button("🏁 Submit Quiz", use_container_width=True, key="submit_quiz"):
            if len(answers) < len(questions):
                st.warning(f"Answer all questions first! ({len(questions) - len(answers)} remaining)")
            else:
                st.session_state.quiz_submitted = True
                st.rerun()

        if st.button("❌ Cancel Quiz", use_container_width=True, key="cancel_quiz"):
            st.session_state.quiz_active = False
            st.rerun()

    with col_quiz:
        for i, q in enumerate(questions):
            st.markdown(f"""
            <div class="sv-card" style="margin-bottom:1.5rem; padding:1.5rem;">
                <div style="color:var(--text-muted); font-size:0.75rem; text-transform:uppercase; 
                            letter-spacing:0.1em; margin-bottom:0.5rem;">Question {i+1}</div>
                <div style="font-size:1rem; font-weight:600; margin-bottom:1.2rem; line-height:1.5;">
                    {q['question']}
                </div>
            """, unsafe_allow_html=True)

            options = q.get("options", [])
            selected = answers.get(i)

            for j, opt in enumerate(options):
                opt_key = f"q{i}_opt{j}"
                is_selected = selected == j
                btn_style = "background:rgba(123,79,255,0.2); border-color:var(--neon-purple);" if is_selected else ""

                if st.button(
                    f"{'◉' if is_selected else '○'} {opt}",
                    key=opt_key,
                    use_container_width=True,
                ):
                    st.session_state.quiz_answers[i] = j
                    st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)


def _render_quiz_results(uid: int):
    questions = st.session_state.quiz_questions
    answers = st.session_state.quiz_answers
    subject = st.session_state.get("quiz_subject", "")

    # Calculate score
    correct = sum(1 for i, q in enumerate(questions) if answers.get(i) == q.get("correct", -1))
    total = len(questions)
    score_pct = (correct / total) * 100 if total > 0 else 0

    # Save result
    if "quiz_saved" not in st.session_state:
        save_quiz_result(uid, subject, total, correct)
        st.session_state.quiz_saved = True

    # Score display
    score_color = "#00ff88" if score_pct >= 80 else "#ff8c42" if score_pct >= 60 else "#ff4d9d"
    grade_emoji = "🏆" if score_pct >= 90 else "⭐" if score_pct >= 80 else "✅" if score_pct >= 60 else "😅"
    grade_msg = (
        "PERFECT! You absolute legend! 🎉"
        if score_pct == 100
        else "Excellent work! Sage is proud! 🔥"
        if score_pct >= 90
        else "Great job! A few more reviews and you'll ace it! 💪"
        if score_pct >= 70
        else "Good effort! Review the ones you missed and retry! 📚"
        if score_pct >= 50
        else "Room for improvement! Don't worry — even Einstein failed sometimes. (Probably.) 😅"
    )

    st.markdown(f"""
    <div class="sv-card-glow" style="text-align:center; padding:2.5rem; margin-bottom:2rem;">
        <div style="font-size:3rem; margin-bottom:0.5rem;">{grade_emoji}</div>
        <div style="font-family:var(--font-display); font-size:4rem; font-weight:800; color:{score_color};">
            {score_pct:.0f}%
        </div>
        <div style="font-size:1.2rem; color:var(--text-secondary); margin-top:0.3rem;">
            {correct} out of {total} correct
        </div>
        <div style="color:var(--text-muted); margin-top:1rem; font-style:italic;">
            {grade_msg}
        </div>
    </div>
    """, unsafe_allow_html=True)

    if score_pct >= 80:
        st.balloons()

    # Detailed breakdown
    st.markdown("#### 📋 Answer Breakdown")
    for i, q in enumerate(questions):
        user_ans = answers.get(i, -1)
        correct_idx = q.get("correct", 0)
        is_correct = user_ans == correct_idx
        options = q.get("options", [])

        icon = "✅" if is_correct else "❌"
        bg = "rgba(0,255,136,0.05)" if is_correct else "rgba(255,77,157,0.05)"
        border = "var(--neon-green)" if is_correct else "var(--neon-pink)"

        st.markdown(f"""
        <div style="background:{bg}; border:1px solid {border}; border-radius:12px; 
                    padding:1.2rem; margin-bottom:0.8rem;">
            <div style="font-weight:600; margin-bottom:0.8rem;">{icon} Q{i+1}: {q['question']}</div>
            <div style="color:var(--text-muted); font-size:0.85rem; margin-bottom:0.3rem;">
                Your answer: <span style="color:{'var(--neon-green)' if is_correct else 'var(--neon-pink)'}; font-weight:600;">
                    {options[user_ans] if 0 <= user_ans < len(options) else 'Not answered'}
                </span>
            </div>
            {f'<div style="color:var(--text-muted); font-size:0.85rem; margin-bottom:0.3rem;">Correct: <span style="color:var(--neon-green); font-weight:600;">{options[correct_idx] if 0 <= correct_idx < len(options) else "?"}</span></div>' if not is_correct else ''}
            <div style="color:var(--text-secondary); font-size:0.85rem; margin-top:0.5rem; 
                        padding:0.5rem; background:rgba(0,0,0,0.2); border-radius:8px;">
                💡 {q.get('explanation', 'No explanation available.')}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Retry / new quiz
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Retry Quiz", use_container_width=True):
            st.session_state.quiz_answers = {}
            st.session_state.quiz_submitted = False
            st.session_state.quiz_saved = False
            st.rerun()
    with col2:
        if st.button("🆕 New Quiz", use_container_width=True):
            st.session_state.quiz_active = False
            st.session_state.quiz_questions = []
            st.session_state.quiz_answers = {}
            st.session_state.quiz_submitted = False
            if "quiz_saved" in st.session_state:
                del st.session_state.quiz_saved
            st.rerun()
