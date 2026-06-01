import streamlit as st
from services.ai_service import (
    summarize_content,
    generate_mnemonics,
    generate_study_plan,
    explain_concept,
    solve_problem,
)
from components.styles import SUBJECTS
from datetime import date, timedelta


def render_toolkit(user: dict):
    uid = user["id"]

    st.markdown("""
    <div>
        <span class="sv-hero-title" style="font-size:2rem;">🛠️ AI Study Toolkit</span>
        <div style="color:var(--text-secondary); font-size:0.9rem; margin-top:0.2rem;">
            Every tool a student needs — except a time machine and motivation. We're working on those.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    tool_tab1, tool_tab2, tool_tab3, tool_tab4, tool_tab5 = st.tabs([
        "📋 Summarizer",
        "🧠 Mnemonics",
        "🗓️ Study Plan",
        "💡 Concept Explainer",
        "✏️ Problem Solver",
    ])

    with tool_tab1:
        _render_summarizer()

    with tool_tab2:
        _render_mnemonics()

    with tool_tab3:
        _render_study_plan()

    with tool_tab4:
        _render_concept_explainer()

    with tool_tab5:
        _render_problem_solver()


def _render_summarizer():
    st.markdown("#### 📋 Smart Note Summarizer")
    st.markdown("""
    <div class="sv-quote-box" style="margin-bottom:1rem;">
        Paste anything — textbook pages, lecture notes, Wikipedia articles, your professor's 
        confusing slides — and Sage will distill it to what actually matters. ✨
    </div>
    """, unsafe_allow_html=True)

    sc1, sc2 = st.columns([3, 1])
    with sc1:
        content = st.text_area(
            "Paste your content here",
            height=200,
            placeholder="Paste lecture notes, textbook content, or any study material...",
            key="sum_content_tk",
        )
    with sc2:
        style = st.radio(
            "Summary Style",
            ["Concise Bullets", "Detailed", "ELI5", "Exam Focus"],
            key="sum_style_tk",
        )
        output_format = st.radio("Show as", ["Text", "Markdown"], key="sum_format_tk")

    if st.button("✨ Summarize with AI", key="sum_btn_tk", use_container_width=True):
        if not content.strip():
            st.error("Paste some content first!")
            return
        style_map = {
            "Concise Bullets": "concise",
            "Detailed": "detailed",
            "ELI5": "eli5",
            "Exam Focus": "exam",
        }
        with st.spinner("🤖 Sage is reading... faster than you will, probably."):
            try:
                result = summarize_content(content, style_map[style])
                st.markdown("---")
                st.markdown("#### 📄 Summary")
                st.markdown(f"""
                <div class="sv-card" style="border-color: var(--border-glow); padding: 1.5rem;">
                """, unsafe_allow_html=True)
                st.markdown(result)
                st.markdown("</div>", unsafe_allow_html=True)

                # Word count comparison
                orig_words = len(content.split())
                summ_words = len(result.split())
                reduction = round((1 - summ_words / max(orig_words, 1)) * 100)
                st.success(f"📊 Reduced from ~{orig_words} words to ~{summ_words} words ({reduction}% shorter!)")
            except Exception as e:
                st.error(f"Summarization failed: {e}")


def _render_mnemonics():
    st.markdown("#### 🧠 Memory Tricks Generator")
    st.markdown("""
    <div class="sv-quote-box" style="margin-bottom:1rem;">
        Science says weird and funny mnemonics stick better. So we're basically doing science here. 🔬
    </div>
    """, unsafe_allow_html=True)

    mc1, mc2 = st.columns(2)
    with mc1:
        topic = st.text_input("Topic / Subject Area", placeholder="e.g. The planets in order", key="mnem_topic")
    with mc2:
        items = st.text_input("Items to memorize", placeholder="e.g. Mercury, Venus, Earth, Mars...", key="mnem_items")

    if st.button("🧠 Generate Memory Tricks", key="mnem_btn", use_container_width=True):
        if not topic or not items:
            st.error("Enter both topic and items to memorize!")
            return
        with st.spinner("🤖 Sage is getting weird with it... (for science)"):
            try:
                result = generate_mnemonics(topic, items)
                st.markdown("---")
                st.markdown("#### 🎭 Your Memory Tricks")
                st.markdown(f"""
                <div class="sv-card" style="border-color: var(--border-glow); padding: 1.5rem;">
                """, unsafe_allow_html=True)
                st.markdown(result)
                st.markdown("</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error: {e}")


def _render_study_plan():
    st.markdown("#### 🗓️ Personalized Study Plan Generator")
    st.markdown("""
    <div class="sv-quote-box" style="margin-bottom:1rem;">
        Tell Sage when your exam is, and it'll build you a realistic plan. 
        Actually following it is on you. 😅
    </div>
    """, unsafe_allow_html=True)

    spc1, spc2 = st.columns(2)
    with spc1:
        sp_subject = st.selectbox("Subject", SUBJECTS, key="sp_subject_tk")
        sp_exam_date = st.date_input("Exam Date", value=date.today() + timedelta(weeks=3), key="sp_date_tk")
        sp_level = st.select_slider(
            "Current Knowledge Level",
            options=["Complete Beginner", "Some Basics", "Intermediate", "Advanced"],
            value="Some Basics",
            key="sp_level_tk",
        )
    with spc2:
        sp_topics = st.text_area(
            "Topics to Cover",
            height=120,
            placeholder="List the main topics/chapters you need to study...",
            key="sp_topics_tk",
        )
        sp_hours = st.slider("Available study hours per day", 1, 10, 3, key="sp_hours_tk")

    if st.button("📅 Generate Study Plan", key="sp_btn_tk", use_container_width=True):
        if not sp_topics.strip():
            st.error("List some topics first!")
            return
        with st.spinner("🤖 Sage is planning your path to glory (or at least a passing grade)..."):
            try:
                result = generate_study_plan(
                    sp_subject,
                    str(sp_exam_date),
                    sp_level,
                    sp_topics,
                )
                st.markdown("---")
                st.markdown("#### 📅 Your Study Plan")
                st.markdown(f"""
                <div class="sv-card" style="border-color: var(--border-glow); padding: 1.5rem;">
                """, unsafe_allow_html=True)
                st.markdown(result)
                st.markdown("</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error: {e}")


def _render_concept_explainer():
    st.markdown("#### 💡 Concept Explainer")
    st.markdown("""
    <div class="sv-quote-box" style="margin-bottom:1rem;">
        Choose your complexity level. From "I'm 5 years old" to "I have a PhD and free time." 
        No judgment either way. 🎓
    </div>
    """, unsafe_allow_html=True)

    ec1, ec2 = st.columns([3, 1])
    with ec1:
        concept = st.text_input(
            "Concept to explain",
            placeholder="e.g. Quantum entanglement, Supply and demand, The French Revolution...",
            key="exp_concept_tk",
        )
    with ec2:
        level = st.select_slider(
            "Complexity Level",
            options=["ELI5", "Beginner", "Intermediate", "Advanced", "Expert"],
            value="Intermediate",
            key="exp_level_tk",
        )

    analogy_pref = st.checkbox("Include a fun/unusual analogy 🤪", value=True, key="exp_analogy")

    if st.button("💡 Explain It!", key="exp_btn_tk", use_container_width=True):
        if not concept.strip():
            st.error("Enter a concept to explain!")
            return
        extra = " Include a fun, unusual, or pop-culture analogy." if analogy_pref else ""
        with st.spinner(f"🤖 Sage is thinking at {level} level..."):
            try:
                prompt_concept = concept + extra
                result = explain_concept(prompt_concept, level.lower())
                st.markdown("---")
                st.markdown(f"#### 💡 {concept} — {level} Level")
                st.markdown(f"""
                <div class="sv-card" style="border-color: var(--border-glow); padding: 1.5rem;">
                """, unsafe_allow_html=True)
                st.markdown(result)
                st.markdown("</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error: {e}")


def _render_problem_solver():
    st.markdown("#### ✏️ Homework Problem Solver")
    st.markdown("""
    <div class="sv-quote-box" style="margin-bottom:1rem;">
        Paste your problem, get a step-by-step solution. 
        Sage shows ALL the work — unlike that one classmate who just writes "∴ answer = 42". 😤
    </div>
    """, unsafe_allow_html=True)

    problem = st.text_area(
        "Your Problem",
        height=150,
        placeholder="Paste your homework problem, math equation, essay prompt, coding challenge...",
        key="prob_text_tk",
    )

    ps1, ps2 = st.columns(2)
    with ps1:
        show_concept = st.checkbox("Show underlying concept/theory", value=True, key="prob_concept")
    with ps2:
        show_verify = st.checkbox("Include verification step", value=True, key="prob_verify")

    if st.button("🔍 Solve Step by Step", key="prob_btn_tk", use_container_width=True):
        if not problem.strip():
            st.error("Paste a problem first!")
            return
        with st.spinner("🤖 Sage is solving... (please don't submit this without understanding it first 🙏)"):
            try:
                result = solve_problem(problem)
                st.markdown("---")
                st.markdown("#### 📐 Step-by-Step Solution")
                st.markdown(f"""
                <div class="sv-card" style="border-color: var(--border-glow); padding: 1.5rem;">
                """, unsafe_allow_html=True)
                st.markdown(result)
                st.markdown("</div>", unsafe_allow_html=True)
                st.warning("⚠️ Understand the solution, don't just copy it. Your future exam-self will thank you.")
            except Exception as e:
                st.error(f"Error: {e}")
