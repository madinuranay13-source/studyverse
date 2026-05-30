import streamlit as st
import sys
import os
import random

sys.path.insert(0, os.path.dirname(__file__))

st.set_page_config(
    page_title="Studyverse",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

from database.db import init_db, get_or_create_user, get_user_stats, update_streak
from components.styles import DARK_THEME_CSS, STUDENT_QUOTES
from pages.dashboard import render_dashboard
from pages.ai_assistant import render_ai_assistant
from pages.notes import render_notes
from pages.tasks import render_tasks
from pages.flashcards import render_flashcards
from pages.pomodoro import render_pomodoro
from pages.quiz import render_quiz
from pages.analytics import render_analytics
from pages.community import render_community
from pages.toolkit import render_toolkit

init_db()
st.markdown(DARK_THEME_CSS, unsafe_allow_html=True)

if "user" not in st.session_state:
    st.session_state.user = None
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"


def render_login():
    st.markdown(DARK_THEME_CSS, unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("# 🎓 Studyverse")
        st.markdown("### Your AI-powered student intelligence platform")
        st.caption("Study smarter. Procrastinate less. We know.")
        st.markdown("---")
        st.markdown("**What is inside:**")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.info("🤖 AI Assistant")
            st.info("🃏 Flashcards")
        with c2:
            st.info("📊 Analytics")
            st.info("🍅 Pomodoro")
        with c3:
            st.info("🎯 Quiz Generator")
            st.info("🌐 Community")
        st.markdown("---")
        st.markdown("### 🚀 Enter Studyverse")
        username = st.text_input("Username", placeholder="Pick a username", key="login_username")
        display_name = st.text_input("Display Name", placeholder="What should we call you?", key="login_display")
        if st.button("🎓 Enter Studyverse", use_container_width=True, key="login_btn"):
            uname = username.strip().lower().replace(" ", "_")
            dname = display_name.strip() or uname
            if not uname:
                st.error("Pick a username!")
            elif len(uname) < 3:
                st.error("Username must be at least 3 characters.")
            else:
                user = get_or_create_user(uname, dname)
                update_streak(user["id"])
                st.session_state.user = user
                st.success("Welcome " + dname + "!")
                st.rerun()
        st.caption("No passwords. Just studying.")


def render_sidebar(user: dict):
    with st.sidebar:
        st.markdown("## Studyverse")
        st.caption("Student Intelligence Platform")
        st.markdown("---")
        stats = get_user_stats(user["id"])
        level_pct = int((stats["xp"] % 500) / 500 * 100)
        streak = stats.get("streak", 0)
        st.markdown("**" + stats["display_name"] + "**")
        st.markdown("Level " + str(stats["level"]) + " — Streak " + str(streak) + " days")
        st.progress(level_pct / 100)
        st.caption(str(stats["xp"]) + " XP total")
        st.markdown("---")
        pages = [
            "Dashboard",
            "AI Assistant",
            "Notes",
            "Tasks",
            "Flashcards",
            "Pomodoro",
            "Quiz",
            "Analytics",
            "Community",
            "Toolkit",
        ]
        for label in pages:
            if st.button(label, key="nav_" + label, use_container_width=True):
                st.session_state.page = label
                st.rerun()
        st.markdown("---")
        if st.button("Switch User", use_container_width=True, key="logout_btn"):
            st.session_state.user = None
            st.session_state.page = "Dashboard"
            for key in list(st.session_state.keys()):
                if key not in ["user", "page"]:
                    del st.session_state[key]
            st.rerun()


def render_page(user: dict):
    page = st.session_state.get("page", "Dashboard")

    routers = {
        "Dashboard": render_dashboard,
        "AI Assistant": render_ai_assistant,
        "Notes": render_notes,
        "Tasks": render_tasks,
        "Flashcards": render_flashcards,
        "Pomodoro": render_pomodoro,
        "Quiz": render_quiz,
        "Analytics": render_analytics,
        "Community": render_community,
        "Toolkit": render_toolkit,
    }

    try:
        renderer = routers.get(page, render_dashboard)
        renderer(user)

    except Exception as e:
        import traceback

        st.error(f"Page error: {e}")
        st.code(traceback.format_exc())


def main():
    if st.session_state.user is None:
        render_login()
    else:
        render_sidebar(st.session_state.user)
        render_page(st.session_state.user)


if __name__ == "__main__":
    main()
