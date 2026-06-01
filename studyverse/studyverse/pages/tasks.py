import streamlit as st
from datetime import datetime, date, timedelta
from database.db import save_task, get_tasks, update_task_status
from components.styles import SUBJECTS
from services.ai_service import summarize_content


def render_tasks(user: dict):
    uid = user["id"]

    st.markdown("""
    <div>
        <span class="sv-hero-title" style="font-size:2rem;">✅ Tasks & Homework</span>
        <div style="color:var(--text-secondary); font-size:0.9rem; margin-top:0.2rem;">
            The only to-do list that silently judges your deadline management.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    # Stats bar
    all_tasks = get_tasks(uid)
    pending = [t for t in all_tasks if t["status"] == "pending"]
    in_progress = [t for t in all_tasks if t["status"] == "in_progress"]
    done = [t for t in all_tasks if t["status"] == "done"]

    sc1, sc2, sc3, sc4 = st.columns(4)
    for col, (label, val, color) in zip(
        [sc1, sc2, sc3, sc4],
        [
            ("Total", len(all_tasks), "#7b4fff"),
            ("Pending", len(pending), "#ff8c42"),
            ("In Progress", len(in_progress), "#00d4ff"),
            ("Done ✓", len(done), "#00ff88"),
        ],
    ):
        with col:
            st.markdown(f"""
            <div class="sv-stat-card">
                <div style="font-family:var(--font-display); font-size:2rem; font-weight:800; color:{color};">{val}</div>
                <div style="color:var(--text-muted); font-size:0.75rem; text-transform:uppercase; letter-spacing:0.08em;">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Add task form
    with st.expander("➕ Add New Task / Homework", expanded=False):
        tc1, tc2 = st.columns(2)
        with tc1:
            t_title = st.text_input("Task Title*", placeholder="e.g. Chapter 5 Exercises", key="task_title")
            t_subject = st.selectbox("Subject", SUBJECTS, key="task_subject")
            t_priority = st.select_slider("Priority", ["low", "medium", "high"], value="medium", key="task_priority")
        with tc2:
            t_due = st.date_input("Due Date", value=date.today() + timedelta(days=3), key="task_due")
            t_desc = st.text_area("Description / Assignment details", height=100, key="task_desc")

        btn1, btn2 = st.columns(2)
        with btn1:
            if st.button("💾 Save Task", key="save_task_btn"):
                if t_title:
                    ai_sum = ""
                    if t_desc:
                        try:
                            ai_sum = summarize_content(t_desc, "exam")
                        except Exception:
                            pass
                    save_task(uid, t_title, t_desc, t_subject, t_priority, str(t_due), ai_sum)
                    st.success("✅ Task saved! +5 XP")
                    st.rerun()
                else:
                    st.error("Title is required!")
        with btn2:
            if st.button("🤖 AI Analyze Task", key="ai_task_btn"):
                if t_desc:
                    with st.spinner("Sage is analyzing your assignment... 🤖"):
                        try:
                            result = summarize_content(t_desc, "exam")
                            st.info(f"**AI Analysis:**\n{result}")
                        except Exception as e:
                            st.error(f"API Error: {e}")
                else:
                    st.warning("Add a description to analyze!")

    # Tabs for status
    tab_pending, tab_progress, tab_done = st.tabs(["📋 Pending", "⏳ In Progress", "✅ Done"])

    with tab_pending:
        _render_task_list(pending, "pending", uid)

    with tab_progress:
        _render_task_list(in_progress, "in_progress", uid)

    with tab_done:
        _render_task_list(done, "done", uid)


def _render_task_list(tasks: list, status: str, uid: int):
    if not tasks:
        msgs = {
            "pending": "🎉 No pending tasks! Are you a wizard?",
            "in_progress": "🤷 Nothing in progress. Start something!",
            "done": "😅 Nothing completed yet. No pressure... (there's pressure).",
        }
        st.markdown(f"""
        <div class="sv-loading" style="padding:2rem;">
            {msgs.get(status, 'No tasks here.')}
        </div>
        """, unsafe_allow_html=True)
        return

    priority_colors = {"high": "var(--neon-pink)", "medium": "var(--neon-orange)", "low": "var(--neon-green)"}

    for task in tasks:
        due_str = ""
        overdue = False
        if task.get("due_date"):
            try:
                due_dt = datetime.strptime(str(task["due_date"]), "%Y-%m-%d").date()
                delta = (due_dt - date.today()).days
                if delta < 0:
                    due_str = f"⚠️ {abs(delta)}d overdue"
                    overdue = True
                elif delta == 0:
                    due_str = "📅 Due TODAY"
                elif delta == 1:
                    due_str = "📅 Due tomorrow"
                else:
                    due_str = f"📅 {due_dt.strftime('%b %d')}"
            except Exception:
                due_str = str(task["due_date"])

        border_color = "var(--neon-pink)" if overdue else priority_colors.get(task.get("priority", "medium"), "var(--border-subtle)")

        col_info, col_actions = st.columns([3, 1])
        with col_info:
            st.markdown(f"""
            <div class="sv-task-card" style="border-left: 3px solid {border_color}; margin-bottom:0.3rem;">
                <div style="flex:1;">
                    <div style="font-weight:700; font-size:0.95rem; 
                                {'text-decoration:line-through; opacity:0.6;' if status == 'done' else ''}">
                        {task['title']}
                    </div>
                    <div style="color:var(--text-muted); font-size:0.8rem; margin-top:3px; display:flex; gap:1rem;">
                        <span>📚 {task.get('subject','') or 'General'}</span>
                        <span>{'⚠️ ' if overdue else ''}{due_str}</span>
                        <span class="sv-badge sv-badge-{'pink' if task.get('priority')=='high' else 'orange' if task.get('priority')=='medium' else 'green'}" style="font-size:0.7rem;">
                            {(task.get('priority') or 'medium').upper()}
                        </span>
                    </div>
                    {f'<div style="color:var(--text-muted); font-size:0.8rem; margin-top:4px;">{task["description"][:100]}{"..." if len(task.get("description","") or "") > 100 else ""}</div>' if task.get('description') else ''}
                    {f'<div style="color:var(--neon-cyan); font-size:0.78rem; margin-top:4px;">🤖 {task["ai_summary"][:100]}...</div>' if task.get('ai_summary') else ''}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_actions:
            if status == "pending":
                if st.button("▶️ Start", key=f"start_{task['id']}", use_container_width=True):
                    update_task_status(task["id"], "in_progress")
                    st.rerun()
            elif status == "in_progress":
                if st.button("✅ Done!", key=f"done_{task['id']}", use_container_width=True):
                    update_task_status(task["id"], "done")
                    st.success("🎉 Task completed! +XP")
                    st.rerun()
            elif status == "done":
                if st.button("↩️ Reopen", key=f"reopen_{task['id']}", use_container_width=True):
                    update_task_status(task["id"], "pending")
                    st.rerun()

        # Show AI summary in expander
        if task.get("ai_summary") and task.get("description"):
            with st.expander(f"🤖 AI Analysis — {task['title'][:40]}"):
                st.markdown("**Original Description:**")
                st.markdown(task["description"])
                st.markdown("---")
                st.markdown("**AI Summary:**")
                st.markdown(task["ai_summary"])
