"""
╔══════════════════════════════════════════════════════════╗
║           STUDYVERSE — Student Intelligence Platform      ║
║           Built with Streamlit + Claude AI               ║
╚══════════════════════════════════════════════════════════╝
"""

import streamlit as st
import sys
import os

# ── Path setup ───────────────────────────────────────────────────────────────
sys.path.insert(0, os.path.dirname(__file__))

# ── Streamlit page config (MUST be first Streamlit call) ─────────────────────
st.set_page_config(
    page_title="Studyverse",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Now safe to import everything else ───────────────────────────────────────
import random
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

# ── Init DB ───────────────────────────────────────────────────────────────────
init_db()

# ── Inject CSS ────────────────────────────────────────────────────────────────
st.markdown(DARK_THEME_CSS, unsafe_allow_html=True)

# ── Session state defaults ────────────────────────────────────────────────────
if "user" not in st.session_state:
    st.session_state.user = None
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"


# ══════════════════════════════════════════════════════════════════════════════
#  LOGIN / ONBOARDING SCREEN
# ══════════════════════════════════════════════════════════════════════════════
def render_login():
    st.markdown("""
    <div style="display:flex; flex-direction:column; align-items:center; justify-content:center;
                min-height:80vh; text-align:center; padding: 2rem;">

        <div style="font-size:4rem; margin-bottom:1rem; animation: float 3s ease-in-out infinite;">🎓</div>

        <div class="sv-hero-title" style="font-size:3.5rem; margin-bottom:0.5rem;">
            Studyverse
        </div>

        <div style="color:var(--text-secondary); font-size:1.1rem; margin-bottom:0.3rem;">
            Your AI-powered student intelligence platform
        </div>

        <div style="color:var(--text-muted); font-size:0.9rem; margin-bottom:3rem; font-style:italic;">
            "Study smarter. Procrastinate less. (We know. We know.)"
        </div>

        <div style="display:flex; gap:1.5rem; flex-wrap:wrap; justify-content:center; margin-bottom:3rem;">
            <div class="sv-badge sv-badge-purple">🤖 AI Study Assistant</div>
            <div class="sv-badge sv-badge-cyan">📊 Smart Analytics</div>
            <div class="sv-badge sv-badge-green">🍅 Pomodoro Timer</div>
            <div class="sv-badge sv-badge-pink">🃏 Flashcards</div>
            <div class="sv-badge sv-badge-orange">🌐 Community Q&A</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="sv-card" style="padding:2rem; border-color:var(--border-glow);">
            <h3 style="text-align:center; margin-bottom:1.5rem;">🚀 Enter Studyverse</h3>
        """, unsafe_allow_html=True)

        username = st.text_input(
            "Username",
            placeholder="Pick a username (no spaces)",
            key="login_username",
        )
        display_name = st.text_input(
            "Display Name",
            placeholder="What should we call you?",
            key="login_display",
        )

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
                st.success(f"Welcome, {dname}! 🎉")
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
        <div style="text-align:center; color:var(--text-muted); font-size:0.8rem; margin-top:1rem;">
            No passwords, no nonsense. Just studying. 📚
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR NAVIGATION
# ══════════════════════════════════════════════════════════════════════════════
def render_sidebar(user: dict):
    with st.sidebar:
        # Brand
        st.markdown("""
        <div style="padding: 1rem 0 1.5rem 0; border-bottom: 1px solid var(--border-subtle);">
            <div class="sv-sidebar-brand">⚡ Studyverse</div>
            <div class="sv-sidebar-sub">Student Intelligence Platform</div>
        </div>
        """, unsafe_allow_html=True)

        # User card
        stats = get_user_stats(user["id"])
        level_pct = (stats["xp"] % 500) / 500 * 100
        streak = stats.get("streak", 0)

        st.markdown(f"""
        <div style="padding: 1rem 0; border-bottom: 1px solid var(--border-subtle);">
            <div style="display:flex; align-items:center; gap:0.7rem; margin-bottom:0.8rem;">
                <div class="sv-avatar">{user.get('avatar_emoji','🎓')}</div>
                <div>
                    <div style="font-weight:700; font-size:0.9rem;">{stats['display_name']}</div>
                    <div style="display:flex; gap:0.4rem; align-items:center; margin-top:2px;">
                        <span class="sv-level-badge">Lvl {stats['level']}</span>
                        <span style="color:var(--neon-orange); font-size:0.8rem;">🔥 {streak}</span>
                    </div>
                </div>
            </div>
            <div style="font-size:0.7rem; color:var(--text-muted); margin-bottom:4px;">
                {stats['xp']} XP · {500 - (stats['xp'] % 500)} to next level
            </div>
            <div class="sv-xp-bar">
                <div class="sv-xp-fill" style="width:{level_pct:.1f}%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Navigation
        st.markdown("<div style='padding-top:0.5rem;'></div>", unsafe_allow_html=True)

        nav_items = [
            ("🏠", "Dashboard",    "Home & Overview"),
            ("🤖", "AI Assistant", "Chat with Sage"),
            ("📝", "Notes",        "Study Notes"),
            ("✅", "Tasks",        "Homework & Tasks"),
            ("🃏", "Flashcards",   "Memory Cards"),
            ("🍅", "Pomodoro",     "Focus Timer"),
            ("🎯", "Quiz",         "Practice Tests"),
            ("📈", "Analytics",    "Performance Data"),
            ("🌐", "Community",    "Q&A Forum"),
            ("🛠️", "Toolkit",     "AI Study Tools"),
        ]

        current = st.session_state.page
        for emoji, label, hint in nav_items:
            is_active = current == label
            active_style = "background:rgba(123,79,255,0.15); border:1px solid rgba(123,79,255,0.3); color:var(--neon-purple);" if is_active else "background:transparent; border:1px solid transparent; color:var(--text-secondary);"
            if st.button(
                f"{emoji}  {label}",
                key=f"nav_{label}",
                use_container_width=True,
                help=hint,
            ):
                st.session_state.page = label
                st.rerun()

        # Bottom: logout + quote
        st.markdown("""
        <div style="position:fixed; bottom:0; left:0; width:var(--sidebar-width,18rem); 
                    padding:1rem; background:rgba(5,5,15,0.95); 
                    border-top:1px solid var(--border-subtle);">
        """, unsafe_allow_html=True)

        if st.button("🚪 Switch User", use_container_width=True, key="logout_btn"):
            st.session_state.user = None
            st.session_state.page = "Dashboard"
            for key in list(st.session_state.keys()):
                if key not in ["user", "page"]:
                    del st.session_state[key]
            st.rerun()

        st.markdown(f"""
        <div style="font-size:0.7rem; color:var(--text-muted); text-align:center; margin-top:0.5rem; 
                    font-style:italic; line-height:1.3;">
            {random.choice(STUDENT_QUOTES)[:80]}...
        </div>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE ROUTER
# ══════════════════════════════════════════════════════════════════════════════
def render_page(user: dict):
    try:
        page = st.session_state.page

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

        renderer = routers.get(page, render_dashboard)
        renderer(user)

    except Exception as e:
        st.error(f"PAGE ERROR: {e}")
        import traceback
        st.code(traceback.format_exc())
# ══════════════════════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════════════════════
def main():
    if st.session_state.user is None:
        render_login()
    else:
        render_sidebar(st.session_state.user)
        render_page(st.session_state.user)


if __name__ == "__main__":
    main()
