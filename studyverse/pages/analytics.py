import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
from database.db import get_performance_data, get_quiz_results, get_study_sessions, get_user_stats
from components.styles import SUBJECT_COLORS
from services.ai_service import analyze_weaknesses


def render_analytics(user: dict):
    uid = user["id"]

    st.markdown("""
    <div>
        <span class="sv-hero-title" style="font-size:2rem;">📈 Intelligence Analytics</span>
        <div style="color:var(--text-secondary); font-size:0.9rem; margin-top:0.2rem;">
            Data-driven insights about your study habits. The numbers don't lie (but they do judge).
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    stats = get_user_stats(uid)
    perf = get_performance_data(uid)
    quiz_results = get_quiz_results(uid)
    sessions = get_study_sessions(uid, days=30)

    # Summary KPIs
    total_hours = stats["total_study_minutes"] / 60
    completion_rate = (stats["tasks_done"] / max(stats["tasks_total"], 1)) * 100

    k1, k2, k3, k4 = st.columns(4)
    kpis = [
        ("⏱️", f"{total_hours:.1f}h", "Total Study Time", "#7b4fff"),
        ("🎯", f"{stats['quiz_avg']:.1f}%", "Quiz Average", "#00d4ff"),
        ("✅", f"{completion_rate:.0f}%", "Task Completion", "#00ff88"),
        ("🔥", str(stats.get("streak", 0)), "Current Streak", "#ff8c42"),
    ]
    for col, (emoji, val, label, color) in zip([k1, k2, k3, k4], kpis):
        with col:
            st.markdown(f"""
            <div class="sv-stat-card">
                <div style="font-size:1.5rem;">{emoji}</div>
                <div style="font-family:var(--font-display); font-size:2rem; font-weight:800; color:{color};">
                    {val}
                </div>
                <div style="color:var(--text-muted); font-size:0.75rem; text-transform:uppercase; letter-spacing:0.08em;">
                    {label}
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Row 1: Study time heatmap + subject radar
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📅 Daily Study — Last 30 Days")
        if sessions:
            # Build daily totals
            date_mins = {}
            for s in sessions:
                try:
                    d = str(s["started_at"])[:10]
                    date_mins[d] = date_mins.get(d, 0) + (s["duration_minutes"] or 0)
                except Exception:
                    pass

            days_30 = [(datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(29, -1, -1)]
            vals = [date_mins.get(d, 0) for d in days_30]
            labels = [(datetime.now() - timedelta(days=i)).strftime("%b %d") for i in range(29, -1, -1)]

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=labels, y=vals,
                fill="tozeroy",
                mode="lines+markers",
                line=dict(color="#7b4fff", width=2),
                marker=dict(size=4, color="#00d4ff"),
                fillcolor="rgba(123,79,255,0.1)",
                hovertemplate="<b>%{x}</b><br>%{y} min<extra></extra>",
            ))
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#f0eeff", family="Space Grotesk"),
                xaxis=dict(showgrid=False, color="#555", tickangle=-45, nticks=8),
                yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)", color="#555"),
                margin=dict(l=0, r=0, t=10, b=40),
                height=250,
                showlegend=False,
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            _empty_chart("📅 Start studying to see your calendar!")

    with col2:
        st.markdown("#### 🕸️ Subject Performance Radar")
        subject_data = perf["study_by_subject"]
        quiz_data = {r["subject"]: r["avg_score"] for r in perf["quiz_by_subject"]}

        if subject_data:
            subjects = [d["subject"] for d in subject_data[:6]]
            study_vals = [min(d["total_minutes"] / 10, 100) for d in subject_data[:6]]  # normalize
            quiz_vals = [quiz_data.get(s, 0) for s in subjects]

            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=study_vals, theta=subjects,
                fill="toself", name="Study Time",
                line_color="#7b4fff",
                fillcolor="rgba(123,79,255,0.15)",
            ))
            fig.add_trace(go.Scatterpolar(
                r=quiz_vals, theta=subjects,
                fill="toself", name="Quiz Score",
                line_color="#00d4ff",
                fillcolor="rgba(0,212,255,0.15)",
            ))
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 100], color="#555", gridcolor="rgba(255,255,255,0.05)"),
                    angularaxis=dict(color="#f0eeff"),
                    bgcolor="rgba(0,0,0,0)",
                ),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#f0eeff", family="Space Grotesk"),
                legend=dict(font=dict(color="#f0eeff"), bgcolor="rgba(0,0,0,0)"),
                margin=dict(l=0, r=0, t=10, b=0),
                height=280,
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            _empty_chart("🕸️ No subject data yet.")

    # Row 2: Quiz trend + task breakdown
    col3, col4 = st.columns(2)

    with col3:
        st.markdown("#### 📈 Quiz Score Trend")
        if quiz_results:
            df = pd.DataFrame(quiz_results[-15:])
            df["taken_at"] = pd.to_datetime(df["taken_at"])
            df["label"] = df.apply(lambda r: f"{r['subject'][:10]} ({r['taken_at'].strftime('%m/%d')})", axis=1)

            fig = go.Figure()
            colors = [SUBJECT_COLORS.get(r, "#7b4fff") for r in df["subject"]]
            fig.add_trace(go.Scatter(
                x=df["label"], y=df["score_percent"],
                mode="lines+markers+text",
                line=dict(color="#7b4fff", width=2, dash="dot"),
                marker=dict(size=10, color=colors, line=dict(width=2, color="#ffffff")),
                text=[f"{v:.0f}%" for v in df["score_percent"]],
                textposition="top center",
                textfont=dict(color="#f0eeff", size=10),
                hovertemplate="<b>%{x}</b><br>Score: %{y:.1f}%<extra></extra>",
            ))
            fig.add_hline(y=70, line_dash="dash", line_color="rgba(255,140,66,0.4)")
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#f0eeff", family="Space Grotesk"),
                xaxis=dict(showgrid=False, color="#555", tickangle=-30),
                yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)", color="#555", range=[0, 110]),
                margin=dict(l=0, r=0, t=10, b=40),
                height=250,
                showlegend=False,
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            _empty_chart("📈 Take some quizzes to see your trend!")

    with col4:
        st.markdown("#### ✅ Task Completion")
        task_status = perf["task_status"]
        if task_status:
            labels = list(task_status.keys())
            values = list(task_status.values())
            colors_map = {"pending": "#ff8c42", "in_progress": "#00d4ff", "done": "#00ff88"}
            pie_colors = [colors_map.get(l, "#7b4fff") for l in labels]
            labels_display = [l.replace("_", " ").title() for l in labels]

            fig = go.Figure(go.Pie(
                labels=labels_display, values=values, hole=0.55,
                marker=dict(colors=pie_colors, line=dict(color="#05050f", width=2)),
                textfont=dict(family="Space Grotesk"),
                hovertemplate="<b>%{label}</b><br>%{value} tasks<extra></extra>",
            ))
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#f0eeff", family="Space Grotesk"),
                legend=dict(font=dict(color="#f0eeff"), bgcolor="rgba(0,0,0,0)"),
                margin=dict(l=0, r=0, t=10, b=0),
                height=250,
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            _empty_chart("✅ Add tasks to see completion stats!")

    # AI Insights
    st.markdown("---")
    st.markdown("#### 🤖 AI Performance Analysis")

    col_insight, col_btn = st.columns([4, 1])
    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        run_analysis = st.button("🔍 Analyze Me", use_container_width=True)

    with col_insight:
        if run_analysis or st.session_state.get("ai_analysis_done"):
            if run_analysis:
                with st.spinner("🤖 Sage is studying your study habits... deeply ironic."):
                    try:
                        analysis = analyze_weaknesses(quiz_results, sessions)
                        st.session_state.ai_analysis_result = analysis
                        st.session_state.ai_analysis_done = True
                    except Exception as e:
                        st.error(f"Analysis failed: {e}")
                        return

            if "ai_analysis_result" in st.session_state:
                st.markdown(f"""
                <div class="sv-card" style="padding: 1.5rem; border-color: var(--border-glow);">
                    {st.session_state.ai_analysis_result}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="sv-quote-box">
                Click "Analyze Me" to get Sage's honest take on your performance.
                Warning: Sage will be constructive, encouraging, and slightly snarky. 🤖
            </div>
            """, unsafe_allow_html=True)

    # Study session log
    st.markdown("---")
    st.markdown("#### 📋 Recent Study Sessions")
    if sessions:
        df_sessions = pd.DataFrame(sessions[:10])
        df_sessions = df_sessions[["subject", "duration_minutes", "session_type", "started_at"]].copy()
        df_sessions.columns = ["Subject", "Duration (min)", "Type", "Started At"]
        df_sessions["Started At"] = pd.to_datetime(df_sessions["Started At"]).dt.strftime("%b %d, %H:%M")
        st.dataframe(df_sessions, use_container_width=True, hide_index=True)
    else:
        st.info("No study sessions recorded yet. Start a Pomodoro session to log your study time!")


def _empty_chart(msg: str):
    st.markdown(f"""
    <div class="sv-loading" style="height:200px; display:flex; align-items:center; 
         justify-content:center; text-align:center; color:var(--text-muted);">
        {msg}
    </div>
    """, unsafe_allow_html=True)
