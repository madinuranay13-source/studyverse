import streamlit as st
from datetime import datetime
from database.db import save_note, get_notes, delete_note, pin_note
from components.styles import SUBJECTS, SUBJECT_COLORS
from services.ai_service import summarize_content


def render_notes(user: dict):
    uid = user["id"]

    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("""
        <div>
            <span class="sv-hero-title" style="font-size:2rem;">📝 Study Notes</span>
            <div style="color:var(--text-secondary); font-size:0.9rem; margin-top:0.2rem;">
                Your second brain. More organized than your actual brain.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Filter bar
    st.markdown("---")
    fc1, fc2, fc3 = st.columns([2, 2, 1])
    with fc1:
        filter_subject = st.selectbox("Filter by Subject", ["All"] + SUBJECTS, key="notes_filter_subject")
    with fc2:
        search = st.text_input("🔍 Search notes", placeholder="Search by title or content...", key="notes_search")
    with fc3:
        st.markdown("<br>", unsafe_allow_html=True)
        show_form = st.button("➕ New Note", use_container_width=True)

    # New note form
    if show_form or st.session_state.get("show_note_form"):
        st.session_state.show_note_form = True
        with st.container():
            st.markdown("""
            <div class="sv-card-glow" style="margin: 1rem 0; padding: 1.5rem; 
                         background: rgba(123,79,255,0.05); border-radius: 16px;
                         border: 1px solid rgba(123,79,255,0.3);">
            """, unsafe_allow_html=True)
            st.markdown("#### ✍️ New Note")
            nc1, nc2 = st.columns(2)
            with nc1:
                n_title = st.text_input("Title*", placeholder="Give your note a great title...", key="new_note_title")
                n_subject = st.selectbox("Subject", SUBJECTS, key="new_note_subject")
            with nc2:
                n_tags = st.text_input("Tags", placeholder="comma, separated, tags", key="new_note_tags")

            n_content = st.text_area(
                "Content",
                placeholder="Write your notes here... Markdown is supported! **bold**, *italic*, `code`, etc.",
                height=200,
                key="new_note_content",
            )

            btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 3])
            with btn_col1:
                if st.button("💾 Save Note", key="save_note_btn"):
                    if n_title and n_content:
                        save_note(uid, n_title, n_content, n_subject, n_tags)
                        st.session_state.show_note_form = False
                        st.success("✅ Note saved! +10 XP")
                        st.rerun()
                    else:
                        st.error("Title and content are required!")

            with btn_col2:
                if st.button("✨ AI Summarize", key="ai_sum_note"):
                    if n_content:
                        with st.spinner("Sage is reading your notes... 🤖"):
                            try:
                                summary = summarize_content(n_content, "concise")
                                st.info(f"**Summary:**\n{summary}")
                            except Exception as e:
                                st.error(f"AI error: {e}")
                    else:
                        st.warning("Write some content first!")

            with btn_col3:
                if st.button("❌ Cancel", key="cancel_note"):
                    st.session_state.show_note_form = False
                    st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)

    # Load and display notes
    subject_filter = None if filter_subject == "All" else filter_subject
    notes = get_notes(uid, subject=subject_filter)

    # Search filter
    if search:
        notes = [n for n in notes if search.lower() in n["title"].lower() or search.lower() in (n["content"] or "").lower()]

    if not notes:
        st.markdown("""
        <div class="sv-loading" style="padding: 4rem; text-align:center;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">📭</div>
            <div style="font-size: 1.1rem; color: var(--text-secondary);">No notes found.</div>
            <div style="color: var(--text-muted); margin-top: 0.5rem;">
                Create your first note above! Your future self will thank you.<br>
                (Unlike your past self who said "I'll remember it.")
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    # Notes count
    st.markdown(f"""
    <div style="color: var(--text-muted); font-size: 0.85rem; margin: 1rem 0;">
        📚 {len(notes)} note{'s' if len(notes) != 1 else ''} found
    </div>
    """, unsafe_allow_html=True)

    # Display notes in a 2-column grid
    for i in range(0, len(notes), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            if i + j < len(notes):
                note = notes[i + j]
                _render_note_card(note, col, uid)


def _render_note_card(note: dict, col, uid: int):
    with col:
        subject_color = SUBJECT_COLORS.get(note.get("subject", ""), "#7b4fff")
        pinned_class = "sv-pinned" if note.get("is_pinned") else ""
        pin_emoji = "📌" if note.get("is_pinned") else ""

        # Truncate content for preview
        preview = (note.get("content") or "")[:200]
        if len(note.get("content") or "") > 200:
            preview += "..."

        tags = note.get("tags") or ""
        tag_html = ""
        if tags:
            for tag in tags.split(",")[:3]:
                tag = tag.strip()
                if tag:
                    tag_html += f'<span class="sv-badge sv-badge-purple" style="margin-right:4px; font-size:0.7rem;">{tag}</span>'

        created = ""
        if note.get("created_at"):
            try:
                dt = datetime.strptime(str(note["created_at"])[:10], "%Y-%m-%d")
                created = dt.strftime("%b %d, %Y")
            except Exception:
                pass

        st.markdown(f"""
        <div class="sv-note-card {pinned_class}">
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.5rem;">
                <div>
                    <span style="font-size:0.75rem; color:{subject_color}; font-weight:600; text-transform:uppercase; letter-spacing:0.08em;">
                        {note.get('subject','') or 'General'}
                    </span>
                    {f'<span style="color:var(--neon-orange); margin-left:0.5rem;">{pin_emoji}</span>' if pin_emoji else ''}
                </div>
                <span style="color:var(--text-muted); font-size:0.75rem;">{created}</span>
            </div>
            <h4 style="margin:0 0 0.5rem 0; font-size:1rem; font-weight:700;">{note['title']}</h4>
            <p style="color:var(--text-secondary); font-size:0.85rem; line-height:1.5; margin-bottom:0.8rem;">{preview}</p>
            <div>{tag_html}</div>
        </div>
        """, unsafe_allow_html=True)

        # Action buttons
        bc1, bc2, bc3 = st.columns(3)
        with bc1:
            if st.button("👁️ View", key=f"view_note_{note['id']}", use_container_width=True):
                st.session_state[f"expand_note_{note['id']}"] = True

        with bc2:
            pin_label = "📌 Unpin" if note.get("is_pinned") else "📌 Pin"
            if st.button(pin_label, key=f"pin_note_{note['id']}", use_container_width=True):
                pin_note(note["id"], not note.get("is_pinned"))
                st.rerun()

        with bc3:
            if st.button("🗑️ Delete", key=f"del_note_{note['id']}", use_container_width=True):
                delete_note(note["id"])
                st.success("Note deleted!")
                st.rerun()

        # Expandable full view
        if st.session_state.get(f"expand_note_{note['id']}"):
            with st.expander("📖 Full Note", expanded=True):
                st.markdown(f"# {note['title']}")
                st.markdown(f"**Subject:** {note.get('subject','General')} | **Created:** {created}")
                st.markdown("---")
                st.markdown(note.get("content", ""))
                if st.button("❌ Close", key=f"close_note_{note['id']}"):
                    st.session_state[f"expand_note_{note['id']}"] = False
                    st.rerun()
