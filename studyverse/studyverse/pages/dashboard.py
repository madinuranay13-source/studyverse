import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import random
from datetime import datetime, timedelta
from database.db import get_user_stats, get_performance_data, get_tasks, get_study_sessions
from components.styles import STUDENT_QUOTES, SUBJECT_COLORS, ACHIEVEMENT_DEFINITIONS


def render_dashboard(user: dict):
    uid = user["id"]
    stats = get_user_stats(uid)
    perf = get_performance_data(uid)

    # Random quote at top
    quote = random.choice(STUDENT_QUOTES)

    st.markdown(f"""
    <div class="sv-quote-box" style="margin-bottom:2rem;">
        {quote}
    </div>
    """, unsafe_allow_html=True)

    # Hero section
    level_pct = (stats["xp"] % 500) / 500 * 100
    next_level_xp = 500 - (stats["xp"] % 500)

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"""
        <div style="margin-bottom: 1.5rem;">
            <div class="sv-hero-title">Welcome back,<br>{stats['display_name']} 👋</div>
            <div style="color: var(--text-secondary); margin-top: 0.5rem; font-size: 1rem;">
                Level {stats['level']} Scholar · {stats['xp']} XP total · {next_level_xp} XP to next level
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="sv-xp-bar" style="margin-bottom:1rem;">
            <div class="sv-xp-fill" style="width:{level_pct}%;"></div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        streak = stats.get("streak", 0)
        fire = "🔥" * min(streak, 5) if streak > 0 else "❄️"
        st.markdown(f"""
        <div class="sv-stat-card" style="text-align:center; padding: 1.5rem;">
            <div class="sv-streak-fire">{fire}</div>
            <div style="font-family: var(--font-display); font-size: 2.5rem; font-weight: 800; 
                        background: linear-gradient(135deg, #ff8c42, #ff4d9d);
                        -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                {streak}
            </div>
            <div style="color: var(--text-muted); font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.1em;">
                Day Streak
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Stats row
    c1, c2, c3, c4, c5 = st.columns(5)
    stat_items = [
        ("📝", stats["notes_count"], "Notes"),
        ("✅", stats["tasks_done"], "Tasks Done"),
        ("🃏", stats["flashcard_count"], "Flashcards"),
        ("⏱️", f"{stats['total_study_minutes']//60}h {stats['total_study_minutes']%60}m", "Study Time"),
        ("🎯", f"{stats['quiz_avg']}%", "Quiz Avg"),
    ]
    for col, (emoji, val, label) in zip([c1, c2, c3, c4, c5], stat_items):
        with col:
            st.markdown(f"""
            <div class="sv-stat-card">
                <div style="font-size: 1.5rem; margin-bottom: 0.3rem;">{emoji}</div>
                <div style="font-family: var(--font-display); font-size: 1.6rem; font-weight: 800;
                            background: linear-gradient(135deg, var(--neon-purple), var(--neon-cyan));
                            -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                    {val}
                </div>
                <div style="color: var(--text-muted); font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.08em;">
                    {label}
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Charts row
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("#### 📊 Study Time — Last 14 Days")
        daily = perf["daily_study"]
        if daily:
            # Fill missing dates
            df = pd.DataFrame(daily)
            df["date"] = pd.to_datetime(df["date"])
            all_dates = pd.date_range(end=datetime.now().date(), periods=14)
            full_df = pd.DataFrame({"date": all_dates}).merge(df, on="date", how="left").fillna(0)

            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=full_df["date"],
                y=full_df["minutes"],
                marker=dict(
                    color=full_df["minutes"],
                    colorscale=[[0, "#1a1a2e"], [0.5, "#7b4fff"], [1, "#00d4ff"]],
                    line=dict(width=0),
                ),
                hovertemplate="<b>%{x|%b %d}</b><br>%{y} min<extra></extra>",
            ))
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#f0eeff", family="Space Grotesk"),
                xaxis=dict(showgrid=False, color="#666"),
                yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)", color="#666"),
                margin=dict(l=0, r=0, t=0, b=0),
                height=220,
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.markdown("""
            <div class="sv-loading">
                <div style="font-size: 2rem;">📉</div>
                <div>No study sessions yet. Go study! (or don't, I'm a chart not a cop)</div>
            </div>
            """, unsafe_allow_html=True)

    with col_right:
        st.markdown("#### 🎯 Subject Breakdown")
        subject_data = perf["study_by_subject"]
        if subject_data:
            labels = [d["subject"] or "Unknown" for d in subject_data[:6]]
            values = [d["total_minutes"] for d in subject_data[:6]]
            colors = [SUBJECT_COLORS.get(l, "#7b4fff") for l in labels]

            fig = go.Figure(go.Pie(
                labels=labels,
                values=values,
                hole=0.6,
                marker=dict(colors=colors, line=dict(color="#05050f", width=2)),
                textfont=dict(family="Space Grotesk", size=12),
                hovertemplate="<b>%{label}</b><br>%{value} min<extra></extra>",
            ))
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#f0eeff", family="Space Grotesk"),
                showlegend=True,
                legend=dict(font=dict(color="#f0eeff"), bgcolor="rgba(0,0,0,0)"),
                margin=dict(l=0, r=0, t=0, b=0),
                height=220,
                annotations=[dict(
                    text=f"<b>{sum(values)}</b><br>min",
                    x=0.5, y=0.5,
                    font=dict(size=14, color="#f0eeff"),
                    showarrow=False,
                )],
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.markdown("""
            <div class="sv-loading">
                <div style="font-size: 2rem;">🍩</div>
                <div>Empty like my knowledge before studying.</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Upcoming tasks + achievements
    col_tasks, col_achieve = st.columns([3, 2])

    with col_tasks:
        st.markdown("#### 📋 Upcoming Tasks")
        tasks = get_tasks(uid, status="pending")[:5]
        if tasks:
            priority_colors = {"high": "pink", "medium": "orange", "low": "green"}
            for t in tasks:
                due = t.get("due_date", "")
                days_left = ""
                if due:
                    try:
                        d = datetime.strptime(str(due), "%Y-%m-%d")
                        delta = (d.date() - datetime.now().date()).days
                        if delta < 0:
                            days_left = f'<span style="color:var(--neon-pink)">⚠️ {abs(delta)}d overdue</span>'
                        elif delta == 0:
                            days_left = '<span style="color:var(--neon-orange)">📅 Due today!</span>'
                        else:
                            days_left = f'<span style="color:var(--text-muted)">📅 {delta}d left</span>'
                    except Exception:
                        pass
                pc = priority_colors.get(t.get("priority", "medium"), "orange")
                st.markdown(f"""
                <div class="sv-task-card sv-priority-{t.get('priority','medium')}">
                    <div style="flex:1;">
                        <div style="font-weight:600; font-size:0.9rem;">{t['title']}</div>
                        <div style="color:var(--text-muted); font-size:0.75rem; margin-top:2px;">
                            {t.get('subject','') or ''} {days_left}
                        </div>
                    </div>
                    <span class="sv-badge sv-badge-{pc}">{t.get('priority','medium').upper()}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="sv-quote-box">
                🎉 No pending tasks! Either you're super productive or you haven't added any yet.
                (Both are valid life choices.)
            </div>
            """, unsafe_allow_html=True)

    with col_achieve:
        st.markdown("#### 🏆 Achievements")
        # Show some achievement slots
        earned_keys = ["first_note", "task_crusher"] if stats["notes_count"] > 0 else []
        shown = 0
        for key, ach in list(ACHIEVEMENT_DEFINITIONS.items())[:6]:
            earned = key in earned_keys
            opacity = "1" if earned else "0.3"
            st.markdown(f"""
            <div class="sv-achievement" style="opacity:{opacity}; margin-bottom: 0.5rem;">
                <div style="font-size:1.5rem;">{ach['emoji']}</div>
                <div>
                    <div style="font-weight:600; font-size:0.85rem;">{ach['title']}</div>
                    <div style="color:var(--text-muted); font-size:0.75rem;">{ach['desc']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Quiz performance chart
    quiz_data = perf["quiz_by_subject"]
    if quiz_data:
        st.markdown("---")
        st.markdown("#### 📈 Quiz Performance by Subject")
        df_q = pd.DataFrame(quiz_data)
        fig = go.Figure()
        colors = [SUBJECT_COLORS.get(s, "#7b4fff") for s in df_q["subject"]]
        fig.add_trace(go.Bar(
            x=df_q["subject"],
            y=df_q["avg_score"],
            marker=dict(color=colors, line=dict(width=0)),
            text=[f"{v:.1f}%" for v in df_q["avg_score"]],
            textposition="outside",
            textfont=dict(color="#f0eeff"),
            hovertemplate="<b>%{x}</b><br>Avg Score: %{y:.1f}%<extra></extra>",
        ))
        fig.add_hline(y=70, line_dash="dash", line_color="rgba(255,140,66,0.5)",
                      annotation_text="70% target", annotation_font_color="#ff8c42")
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#f0eeff", family="Space Grotesk"),
            xaxis=dict(showgrid=False, color="#666"),
            yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)", color="#666", range=[0, 110]),
            margin=dict(l=0, r=0, t=20, b=0),
            height=280,
        )
        st.plotly_chart(fig, use_container_width=True)
