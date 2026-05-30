"""
╔══════════════════════════════════════════════════════════╗
║           STUDYVERSE — Student Intelligence Platform      ║
║           Built with Streamlit + Claude AI               ║
╚══════════════════════════════════════════════════════════╝
"""

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

    # ── Hero section using native Streamlit ──
    st.markdown("<br><br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:

        st.markdown("# 🎓 Studyverse")
        st.markdown("### Your AI-powered student intelligence platform")
        st.caption('"Study smarter. Procrastinate less. (We know. We know.)"')

        st.markdown("---")

        st.markdown("**What's inside:**")
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

        username = st.text_input(
            "Username",
            placeholder="Pick a username (no spaces)",
            key="login_username",
        )
        display_name = st.text_input(
            "Display Name",
            placeholder="W
