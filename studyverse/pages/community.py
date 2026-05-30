import streamlit as st
from database.db import create_post, get_posts, upvote_post, add_reply, get_replies
from components.styles import SUBJECTS


def render_community(user: dict):
    uid = user["id"]

    st.markdown("""
    <div>
        <span class="sv-hero-title" style="font-size:2rem;">🌐 Community</span>
        <div style="color:var(--text-secondary); font-size:0.9rem; margin-top:0.2rem;">
            Ask, answer, debate. Like Stack Overflow but with more caffeine and less gatekeeping.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    tab_feed, tab_ask, tab_mypost = st.tabs(["📰 Feed", "❓ Ask a Question", "📌 My Posts"])

    with tab_feed:
        _render_feed(uid, user)

    with tab_ask:
        _render_ask(uid)

    with tab_mypost:
        _render_my_posts(uid, user)


def _render_feed(uid: int, user: dict):
    fc1, fc2 = st.columns(2)
    with fc1:
        filter_subject = st.selectbox("Subject", ["All"] + SUBJECTS, key="comm_filter_sub")
    with fc2:
        filter_type = st.selectbox("Type", ["All", "question", "discussion", "resource"], key="comm_filter_type")

    subject_arg = None if filter_subject == "All" else filter_subject
    type_arg = None if filter_type == "All" else filter_type

    posts = get_posts(subject=subject_arg, post_type=type_arg)

    if not posts:
        st.markdown("""
        <div class="sv-loading" style="padding:3rem; text-align:center;">
            <div style="font-size:3rem;">🦗</div>
            <div style="color:var(--text-secondary);">Crickets. No posts yet — be the first!</div>
        </div>
        """, unsafe_allow_html=True)
        return

    for post in posts:
        _render_post_card(post, uid, user)


def _render_post_card(post: dict, uid: int, user: dict):
    post_id = post["id"]
    expand_key = f"expand_post_{post_id}"
    type_colors = {"question": "purple", "discussion": "cyan", "resource": "green"}
    tc = type_colors.get(post.get("post_type", "question"), "purple")

    st.markdown(f"""
    <div class="sv-community-post">
        <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.5rem;">
            <div style="display:flex; align-items:center; gap:0.6rem;">
                <div class="sv-avatar">{post.get('avatar_emoji','🎓')}</div>
                <div>
                    <div style="font-weight:600; font-size:0.9rem;">{post.get('display_name','Anonymous')}</div>
                    <div style="color:var(--text-muted); font-size:0.75rem;">Level {post.get('level',1)} Scholar</div>
                </div>
            </div>
            <div style="display:flex; gap:0.5rem; align-items:center;">
                <span class="sv-badge sv-badge-{tc}">{post.get('post_type','question').title()}</span>
                <span class="sv-badge sv-badge-purple">📚 {post.get('subject','General')}</span>
            </div>
        </div>
        <div style="font-weight:700; font-size:1rem; margin-bottom:0.4rem;">{post['title']}</div>
        <div style="color:var(--text-secondary); font-size:0.85rem; line-height:1.5;">
            {(post.get('content') or '')[:200]}{'...' if len(post.get('content','') or '') > 200 else ''}
        </div>
        <div style="display:flex; gap:1.5rem; margin-top:0.8rem; color:var(--text-muted); font-size:0.8rem;">
            <span>👍 {post.get('upvotes',0)} upvotes</span>
            <span>💬 {post.get('reply_count',0)} replies</span>
            {'<span style="color:var(--neon-green);">✅ Answered</span>' if post.get('is_answered') else ''}
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_upvote, col_reply, col_expand = st.columns([1, 1, 2])
    with col_upvote:
        if st.button(f"👍 Upvote", key=f"upvote_{post_id}", use_container_width=True):
            upvote_post(post_id)
            st.rerun()
    with col_reply:
        if st.button(f"💬 Reply", key=f"toggle_reply_{post_id}", use_container_width=True):
            st.session_state[expand_key] = not st.session_state.get(expand_key, False)
            st.rerun()
    with col_expand:
        if st.button(f"👁️ View Thread ({post.get('reply_count',0)} replies)", key=f"view_{post_id}", use_container_width=True):
            st.session_state[f"view_thread_{post_id}"] = not st.session_state.get(f"view_thread_{post_id}", False)
            st.rerun()

    # Reply form
    if st.session_state.get(expand_key):
        reply_text = st.text_area("Your reply", key=f"reply_text_{post_id}", height=80, placeholder="Share your knowledge (or at least your best guess) 🤓")
        if st.button("📤 Post Reply", key=f"post_reply_{post_id}"):
            if reply_text.strip():
                add_reply(post_id, uid, reply_text.strip())
                st.session_state[expand_key] = False
                st.success("✅ Reply posted! +10 XP")
                st.rerun()
            else:
                st.warning("Write something first!")

    # Thread view
    if st.session_state.get(f"view_thread_{post_id}"):
        replies = get_replies(post_id)
        if replies:
            for r in replies:
                accepted = "✅ " if r.get("is_accepted") else ""
                st.markdown(f"""
                <div class="sv-reply">
                    <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:0.4rem;">
                        <span style="font-size:1.1rem;">{r.get('avatar_emoji','🎓')}</span>
                        <span style="font-weight:600; font-size:0.85rem;">{accepted}{r.get('display_name','Anonymous')}</span>
                        <span style="color:var(--text-muted); font-size:0.75rem;">Lvl {r.get('level',1)}</span>
                        <span style="color:var(--text-muted); font-size:0.75rem; margin-left:auto;">👍 {r.get('upvotes',0)}</span>
                    </div>
                    <div style="color:var(--text-secondary); font-size:0.875rem; line-height:1.5;">{r.get('content','')}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.caption("No replies yet. Be the first brave soul.")

    st.markdown("<div style='margin-bottom:0.3rem;'></div>", unsafe_allow_html=True)


def _render_ask(uid: int):
    st.markdown("#### ❓ Ask the Community")
    st.markdown("""
    <div class="sv-quote-box" style="margin-bottom:1rem;">
        There are no dumb questions. Only questions that could've been googled. But honestly, ask anyway — we're all in this together. 🤝
    </div>
    """, unsafe_allow_html=True)

    ac1, ac2 = st.columns(2)
    with ac1:
        p_title = st.text_input("Question Title*", placeholder="e.g. How do I integrate sin²(x)?", key="post_title")
        p_subject = st.selectbox("Subject", SUBJECTS, key="post_subject")
    with ac2:
        p_type = st.selectbox("Post Type", ["question", "discussion", "resource"], key="post_type")

    p_content = st.text_area(
        "Details",
        height=150,
        placeholder="Explain your question in detail. Include what you've tried, what's confusing you, and any relevant context.",
        key="post_content",
    )

    if st.button("🚀 Post to Community", key="submit_post"):
        if p_title and p_content:
            create_post(uid, p_title, p_content, p_subject, p_type)
            st.success("✅ Posted! +15 XP — your question is live!")
            st.balloons()
            st.rerun()
        else:
            st.error("Title and content are required!")


def _render_my_posts(uid: int, user: dict):
    st.markdown("#### 📌 Your Posts")
    all_posts = get_posts()
    my_posts = [p for p in all_posts if p.get("user_id") == uid]

    if not my_posts:
        st.info("You haven't posted anything yet. Ask a question or start a discussion!")
        return

    for post in my_posts:
        _render_post_card(post, uid, user)
