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

# ── Inject CSS everywhere ─────────────────────────────────────────────────────
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
    # Re-inject CSS so it works on Streamlit Cloud too
    st.markdown(DARK_THEME_CSS, unsafe_allow_html=True)

    st.markdown("""
    <div style="display:flex; flex-direction:column; align-items:center; justify-content:center;
                min-height:80vh; text-align:center; padding: 2rem;">

        <div style="font-size:4rem; margin-bottom:1rem;">🎓</div>

        <div style="font-family:'Syne',sans-serif; font-size:3.5rem; font-weight:800;
                    background:linear-gradient(135deg,#7b4fff,#00d4ff,#00ff88);
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                    margin-bottom:0.5rem; letter-spacing:-0.03em;">
            Studyverse
        </div>

        <div style="color:rgba(240,238,255,0.6); font-size:1.1rem; margin-bottom:0.3rem;">
            Your AI-powered student intelligence platform
        </div>

        <div style="color:rgba(240,238,255,0.35); font-size:0.9rem; margin-bottom:3rem; font-style:italic;">
            "Study smarter. Procrastinate less. (We know. We know.)"
        </div>

        <div style="display:flex; gap:1rem; flex-wrap:wrap; justify-content:center; margin-bottom:3rem;">
            <span style="background:rgba(123,79,255,0.2); color:#7b4fff; border:1px solid rgba(123,79,255,0.3);
                         padding:0.3rem 0.9rem; border-radius:99px; font-size:0.85rem; font-weight:600;">
                🤖 AI Study Assistant
            </span>
            <span style="background:rgba(0,212,255,0.2); color:#00d4ff; border:1px solid rgba(0,212,255,0.3);
                         padding:0.3rem 0.9rem; border-radius:99px; font-size:0.85rem; font-weight:600;">
                📊 Smart Analytics
            </span>
            <span style="background:rgba(0,255,136,0.2); color:#00ff88; border:1px solid rgba(0,255,136,0.3);
                         padding:0.3rem 0.9rem; border-radius:99px; font-size:0.85rem; font-weight:600;">
                🍅 Pomodoro Timer
            </span>
            <span style="background:rgba(255,77,157,0.2); color:#ff4d9d; border:1px solid rgba(255,77,157,0.3);
                         padding:0.3rem 0.9rem; border-radius:99px; font-size:0.85rem; font-weight:600;">
                🃏 Flashcards
            </span>
            <span style="background:rgba(255,140,66,0.2); color:#ff8c42; border:1px solid rgba(255,140,66,0.3);
                         padding:0.3rem 0.9rem; border-radius:99px; font-size:0.85rem; font-weight:600;">
                🌐 Community Q&A
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="background:rgba(255,255,255,0.04); border:1px solid rgba(123,79,255,0.3);
                    border-radius:16px; padding:2rem; margin-bottom:1rem;">
            <h3 style="text-align:center; margin-bottom:1.5rem; color:#f0eeff;">🚀 Enter Studyverse</h3>
        </div>
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

        st.markdown("""
        <div style="text-align:center; color:rgba(240,238,255,0.35); font-size:0.8rem; margin-top:1rem;">
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
        <div style="padding: 1rem 0 1.5rem 0; border-bottom: 1px solid rgba(255,255,255,0.08);">
            <div style="font-family:'Syne',sans-serif; font-weight:800; font-size:1.5rem;
                        background:linear-gradient(135deg,#7b4fff,#00d4ff);
                        -webkit-background-clip:text; -webkit-text-fill-color:transparent;">
                ⚡ Studyverse
            </div>
            <div style="font-size:0.7rem; color:rgba(240,238,255,0.35); letter-spacing:0.15em;
                        text-transform:uppercase;">
                Student Intelligence Platform
            </div>
        </div>
        """, unsafe_allow_html=True)

        # User card
        stats = get_user_stats(user["id"])
        level_pct = (stats["xp"] % 500) / 500 * 100
        streak = stats.get("streak", 0)

        st.markdown(f"""
        <div style="padding: 1rem 0; border-bottom: 1px solid rgba(255,255,255,0.08);">
            <div style="display:flex; align-items:center; gap:0.7rem; margin-bottom:0.8rem;">
                <div style="width:40px; height:40px; border-radius:50%;
                            background:linear-gradient(135deg,#7b4fff,#00d4ff);
                            display:flex; align-items:center; justify-content:center; font-size:1.2rem;">
                    {user.get('avatar_emoji','🎓')}
                </div>
                <div>
                    <div style="font-weight:700; font-size:0.9rem; color:#f0eeff;">
                        {stats['display_name']}
                    </div>
                    <div style="display:flex; gap:0.4rem; align-items:center; margin-top:2px;">
                        <span style="background:linear-gradient(135deg,#7b4fff,#5b2be0); color:white;
                                     padding:0.15rem 0.5rem; border-radius:99px; font-size:0.72rem; font-weight:700;">
                            Lvl {stats['level']}
                        </span>
                        <span style="color:#ff8c42; font-size:0.8rem;">🔥 {streak}</span>
                    </div>
                </div>
            </div>
            <div style="font-size:0.7rem; color:rgba(240,238,255,0.35); margin-bottom:4px;">
                {stats['xp']} XP · {500 - (stats['xp'] % 500)} to next level
            </div>
            <div style="height:8px; background:rgba(255,255,255,0.06); border-radius:99px; overflow:hidden;">
                <div style="height:100%; width:{level_pct:.1f}%; border-radius:99px;
                            background:linear-gradient(90deg,#7b4fff,#00d4ff);
                            transition:width 0.8s ease;">
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

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
            if st.button(
                f"{emoji}  {label}",
                key=f"nav_{label}",
                use_container_width=True,
                help=hint,
            ):
                st.session_state.page = label
                st.rerun()

        st.markdown("---")

        if st.button("🚪 Switch User", use_container_width=True, key="logout_btn"):
            st.session_state.user = None
            st.session_state.page = "Dashboard"
            for key in list(st.session_state.keys()):
                if key not in ["user", "page"]:
                    del st.session_state[key]
            st.rerun()

        st.markdown(f"""
        <div style="font-size:0.7rem; color:rgba(240,238,255,0.35); text-align:center;
                    margin-top:0.5rem; font-style:italic; line-height:1.3; padding:0.5rem;">
            {random.choice(STUDENT_QUOTES)[:80]}...
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE ROUTER
# ══════════════════════════════════════════════════════════════════════════════
def render_page(user: dict):
    page = st.session_state.page
    routers = {
        "Dashboard":    render_dashboard,
        "AI Assistant": render_ai_assistant,
        "Notes":        render_notes,
        "Tasks":        render_tasks,
        "Flashcards":   render_flashcards,
        "Pomodoro":     render_pomodoro,
        "Quiz":         render_quiz,
        "Analytics":    render_analytics,
        "Community":    render_community,
        "Toolkit":      render_toolkit,
    }
    renderer = routers.get(page, render_dashboard)
    renderer(user)


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
