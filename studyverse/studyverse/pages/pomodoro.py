import streamlit as st
import time
from datetime import datetime
from database.db import log_study_session
from components.styles import SUBJECTS


POMODORO_QUOTES = [
    "🍅 Time to focus! Your Netflix will still be there. Probably.",
    "🔥 25 minutes. You can do ANYTHING for 25 minutes. Maybe.",
    "💪 Channel your inner scholar. Or at least pretend.",
    "☕ Coffee's hot, brain's... warming up. Let's go.",
    "🎯 Focus mode: ON. Everything else: DENIED.",
    "🧠 Fun fact: You can't scroll TikTok and study at the same time. Trust me.",
]

def render_pomodoro(user: dict):
    uid = user["id"]

    st.markdown("""
    <div>
        <span class="sv-hero-title" style="font-size:2rem;">🍅 Pomodoro & Focus</span>
        <div style="color:var(--text-secondary); font-size:0.9rem; margin-top:0.2rem;">
            25 minutes of focus, 5 minutes of wondering why you chose this degree.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    # Initialize session state
    if "pomo_mode" not in st.session_state:
        st.session_state.pomo_mode = "focus"  # focus, short_break, long_break
    if "pomo_running" not in st.session_state:
        st.session_state.pomo_running = False
    if "pomo_start_time" not in st.session_state:
        st.session_state.pomo_start_time = None
    if "pomo_duration" not in st.session_state:
        st.session_state.pomo_duration = 25 * 60
    if "pomo_sessions_today" not in st.session_state:
        st.session_state.pomo_sessions_today = 0
    if "pomo_subject" not in st.session_state:
        st.session_state.pomo_subject = SUBJECTS[0]
    if "pomo_elapsed" not in st.session_state:
        st.session_state.pomo_elapsed = 0

    col_timer, col_settings = st.columns([2, 1])

    with col_settings:
        st.markdown("#### ⚙️ Settings")
        pomo_subject = st.selectbox("Subject", SUBJECTS, key="pomo_subject_select")
        st.session_state.pomo_subject = pomo_subject

        st.markdown("**Duration (minutes)**")
        sc1, sc2, sc3 = st.columns(3)
        with sc1:
            if st.button("25m\nFocus", key="pomo_25", use_container_width=True):
                st.session_state.pomo_duration = 25 * 60
                st.session_state.pomo_mode = "focus"
                st.session_state.pomo_running = False
                st.session_state.pomo_elapsed = 0
                st.rerun()
        with sc2:
            if st.button("5m\nBreak", key="pomo_5", use_container_width=True):
                st.session_state.pomo_duration = 5 * 60
                st.session_state.pomo_mode = "short_break"
                st.session_state.pomo_running = False
                st.session_state.pomo_elapsed = 0
                st.rerun()
        with sc3:
            if st.button("15m\nLong", key="pomo_15", use_container_width=True):
                st.session_state.pomo_duration = 15 * 60
                st.session_state.pomo_mode = "long_break"
                st.session_state.pomo_running = False
                st.session_state.pomo_elapsed = 0
                st.rerun()

        custom_min = st.number_input("Custom (minutes)", min_value=1, max_value=120, value=25, key="pomo_custom")
        if st.button("Set Custom", use_container_width=True, key="pomo_custom_set"):
            st.session_state.pomo_duration = custom_min * 60
            st.session_state.pomo_running = False
            st.session_state.pomo_elapsed = 0
            st.rerun()

        st.markdown("---")
        st.markdown("#### 📊 Today's Progress")
        sessions = st.session_state.pomo_sessions_today
        st.markdown(f"""
        <div style="text-align:center; padding:1rem;">
            <div style="font-size:2.5rem;">{'🍅' * min(sessions, 8)}</div>
            <div style="font-family:var(--font-display); font-size:2rem; font-weight:800; 
                        color:var(--neon-orange);">{sessions}</div>
            <div style="color:var(--text-muted); font-size:0.8rem;">Pomodoros completed</div>
            <div style="color:var(--text-secondary); font-size:0.85rem; margin-top:0.3rem;">
                = {sessions * 25} minutes of focus time
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_timer:
        # Compute time remaining
        elapsed = st.session_state.pomo_elapsed
        if st.session_state.pomo_running and st.session_state.pomo_start_time:
            current_elapsed = (datetime.now() - st.session_state.pomo_start_time).seconds
            elapsed = st.session_state.pomo_elapsed + current_elapsed

        remaining = max(0, st.session_state.pomo_duration - elapsed)
        minutes = remaining // 60
        seconds = remaining % 60

        # Timer completed
        if remaining == 0 and st.session_state.pomo_running:
            st.session_state.pomo_running = False
            if st.session_state.pomo_mode == "focus":
                st.session_state.pomo_sessions_today += 1
                duration_min = st.session_state.pomo_duration // 60
                log_study_session(uid, st.session_state.pomo_subject, duration_min, "pomodoro")
            st.session_state.pomo_elapsed = 0
            st.session_state.pomo_start_time = None
            st.balloons()

        # Mode indicator
        mode_config = {
            "focus":       ("🎯 Focus Time",   "var(--neon-purple)", "var(--neon-cyan)"),
            "short_break": ("☕ Short Break",   "var(--neon-green)",  "var(--neon-orange)"),
            "long_break":  ("🌿 Long Break",    "var(--neon-cyan)",   "var(--neon-green)"),
        }
        mode_label, c1, c2 = mode_config.get(st.session_state.pomo_mode, mode_config["focus"])

        # Progress circle (CSS-based)
        pct = (1 - remaining / st.session_state.pomo_duration) * 100 if st.session_state.pomo_duration > 0 else 0
        deg = pct * 3.6

        st.markdown(f"""
        <div style="text-align:center; padding: 2rem 0;">
            <div style="margin-bottom:1rem;">
                <span class="sv-badge sv-badge-purple">{mode_label}</span>
            </div>
            <div style="position:relative; width:220px; height:220px; margin:0 auto 2rem;">
                <svg width="220" height="220" style="transform:rotate(-90deg)">
                    <circle cx="110" cy="110" r="95" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="12"/>
                    <circle cx="110" cy="110" r="95" fill="none" 
                            stroke="url(#gradient)" stroke-width="12"
                            stroke-dasharray="{pct * 5.97:.1f} 597"
                            stroke-linecap="round"/>
                    <defs>
                        <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="0%">
                            <stop offset="0%" stop-color="{c1}"/>
                            <stop offset="100%" stop-color="{c2}"/>
                        </linearGradient>
                    </defs>
                </svg>
                <div style="position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); text-align:center;">
                    <div style="font-family:var(--font-display); font-size:3rem; font-weight:800; 
                                background:linear-gradient(135deg,{c1},{c2});
                                -webkit-background-clip:text; -webkit-text-fill-color:transparent;">
                        {minutes:02d}:{seconds:02d}
                    </div>
                    <div style="color:var(--text-muted); font-size:0.75rem; margin-top:0.2rem;">
                        {st.session_state.pomo_subject}
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Control buttons
        btn1, btn2, btn3 = st.columns(3)
        with btn1:
            if not st.session_state.pomo_running:
                if st.button("▶️ Start", key="pomo_start", use_container_width=True):
                    st.session_state.pomo_running = True
                    st.session_state.pomo_start_time = datetime.now()
                    st.rerun()
            else:
                if st.button("⏸️ Pause", key="pomo_pause", use_container_width=True):
                    elapsed_now = (datetime.now() - st.session_state.pomo_start_time).seconds
                    st.session_state.pomo_elapsed += elapsed_now
                    st.session_state.pomo_running = False
                    st.session_state.pomo_start_time = None
                    st.rerun()

        with btn2:
            if st.button("⏹️ Reset", key="pomo_reset", use_container_width=True):
                st.session_state.pomo_running = False
                st.session_state.pomo_elapsed = 0
                st.session_state.pomo_start_time = None
                st.rerun()

        with btn3:
            if st.button("📝 Log Session", key="pomo_log", use_container_width=True):
                mins_studied = elapsed // 60
                if mins_studied > 0:
                    log_study_session(uid, st.session_state.pomo_subject, mins_studied, "manual")
                    st.success(f"✅ Logged {mins_studied} minutes! +{mins_studied//5} XP")
                else:
                    st.warning("Study at least 1 minute first!")

        # Auto-refresh when running
        if st.session_state.pomo_running:
            import random
            quote = random.choice(POMODORO_QUOTES)
            st.markdown(f"""
            <div class="sv-meme-strip" style="margin-top:1rem; border-radius:8px;">
                {quote}
            </div>
            """, unsafe_allow_html=True)
            time.sleep(1)
            st.rerun()

    # Study tips section
    st.markdown("---")
    st.markdown("#### 💡 The Pomodoro Technique")
    tip1, tip2, tip3, tip4 = st.columns(4)
    tips = [
        ("🎯", "Focus", "Work on one task for 25 minutes without interruption"),
        ("☕", "Break", "Take a 5-minute break. Stretch, hydrate, stare into the void"),
        ("🔁", "Repeat", "After 4 pomodoros, take a longer 15-30 min break"),
        ("📊", "Track", "Every session is logged to your analytics automatically"),
    ]
    for col, (emoji, title, desc) in zip([tip1, tip2, tip3, tip4], tips):
        with col:
            st.markdown(f"""
            <div class="sv-card" style="text-align:center; padding:1rem;">
                <div style="font-size:1.8rem; margin-bottom:0.5rem;">{emoji}</div>
                <div style="font-weight:700; margin-bottom:0.3rem;">{title}</div>
                <div style="color:var(--text-muted); font-size:0.8rem; line-height:1.4;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
