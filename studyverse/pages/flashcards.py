import streamlit as st
import json
from database.db import save_flashcard, get_flashcards, get_decks
from components.styles import SUBJECTS
from services.ai_service import generate_flashcards


def render_flashcards(user: dict):
    uid = user["id"]

    st.markdown("""
    <div>
        <span class="sv-hero-title" style="font-size:2rem;">🃏 Flashcards</span>
        <div style="color:var(--text-secondary); font-size:0.9rem; margin-top:0.2rem;">
            Spaced repetition. Because your brain forgets things faster than you do.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    tab_study, tab_create, tab_ai_gen = st.tabs(["📖 Study Deck", "✏️ Create Cards", "🤖 AI Generate"])

    with tab_create:
        _render_create_tab(uid)

    with tab_ai_gen:
        _render_ai_gen_tab(uid)

    with tab_study:
        _render_study_tab(uid)


def _render_create_tab(uid: int):
    st.markdown("#### ✍️ Create Flashcards")
    cc1, cc2, cc3 = st.columns(3)
    with cc1:
        deck = st.text_input("Deck Name", placeholder="e.g. Biology Chapter 3", key="fc_deck")
    with cc2:
        subject = st.selectbox("Subject", SUBJECTS, key="fc_subject_create")
    with cc3:
        st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("**Card Content:**")
    fc_front = st.text_area("Front (Question / Term)", height=80, placeholder="What is mitosis?", key="fc_front")
    fc_back = st.text_area("Back (Answer / Definition)", height=80, placeholder="The process of cell division...", key="fc_back")

    if st.button("➕ Add Card", key="add_fc_btn"):
        if deck and fc_front and fc_back:
            save_flashcard(uid, deck, subject, fc_front, fc_back)
            st.success("🃏 Card added! +5 XP")
            st.rerun()
        else:
            st.error("Fill in deck name, front, and back!")

    # Show existing decks
    st.markdown("---")
    st.markdown("#### 📦 Your Decks")
    decks = get_decks(uid)
    if decks:
        for d in decks:
            st.markdown(f"""
            <div class="sv-card" style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem; padding:1rem;">
                <div>
                    <span style="font-weight:700;">{d['deck_name']}</span>
                    <span style="color:var(--text-muted); font-size:0.8rem; margin-left:0.8rem;">{d.get('subject','')}</span>
                </div>
                <span class="sv-badge sv-badge-purple">{d['card_count']} cards</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No decks yet. Create your first flashcard above!")


def _render_ai_gen_tab(uid: int):
    st.markdown("#### 🤖 AI-Generated Flashcards")
    st.markdown("""
    <div class="sv-quote-box" style="margin-bottom:1rem;">
        Paste your notes or a topic, and Sage will auto-generate a full flashcard deck.
        It's like having a very studious robot assistant. 🤖📚
    </div>
    """, unsafe_allow_html=True)

    ag1, ag2 = st.columns(2)
    with ag1:
        ai_deck_name = st.text_input("Deck Name", placeholder="e.g. Physics — Waves", key="ai_deck_name")
        ai_subject = st.selectbox("Subject", SUBJECTS, key="ai_fc_subject")
    with ag2:
        ai_num = st.slider("Number of cards", 5, 20, 10, key="ai_fc_num")

    ai_content = st.text_area(
        "Paste your notes / topic description",
        height=150,
        placeholder="Paste lecture notes, textbook content, or just describe the topic...",
        key="ai_fc_content",
    )

    if st.button("✨ Generate Flashcards with AI", key="ai_gen_fc_btn"):
        if not ai_content:
            st.error("Add some content first!")
        elif not ai_deck_name:
            st.error("Give your deck a name!")
        else:
            with st.spinner("🤖 Sage is crafting your flashcards... This is basically free studying."):
                try:
                    cards = generate_flashcards(ai_content, ai_num)
                    if cards:
                        for card in cards:
                            save_flashcard(uid, ai_deck_name, ai_subject, card["front"], card["back"])
                        st.success(f"🎉 Created {len(cards)} flashcards in '{ai_deck_name}'! +{len(cards)*5} XP")
                        st.balloons()
                        # Preview
                        st.markdown("#### Preview:")
                        for i, card in enumerate(cards[:3]):
                            st.markdown(f"""
                            <div class="sv-card" style="margin-bottom:0.5rem;">
                                <div style="color:var(--text-muted); font-size:0.75rem; margin-bottom:0.3rem;">Card {i+1}</div>
                                <div style="font-weight:600;">Q: {card['front']}</div>
                                <div style="color:var(--neon-cyan); margin-top:0.3rem;">A: {card['back']}</div>
                            </div>
                            """, unsafe_allow_html=True)
                        if len(cards) > 3:
                            st.caption(f"...and {len(cards)-3} more cards!")
                    else:
                        st.error("Couldn't generate cards. Try with more content!")
                except Exception as e:
                    st.error(f"AI Error: {e}")


def _render_study_tab(uid: int):
    decks = get_decks(uid)
    if not decks:
        st.markdown("""
        <div class="sv-loading" style="padding:3rem; text-align:center;">
            <div style="font-size:3rem;">🃏</div>
            <div style="font-size:1.1rem; color:var(--text-secondary);">No decks yet!</div>
            <div style="color:var(--text-muted); margin-top:0.5rem;">Create some flashcards or use AI to generate them.</div>
        </div>
        """, unsafe_allow_html=True)
        return

    # Deck selector
    deck_options = [d["deck_name"] for d in decks]
    selected_deck = st.selectbox("Choose a deck to study", deck_options, key="study_deck_select")

    cards = get_flashcards(uid, selected_deck)
    if not cards:
        st.warning("This deck has no cards!")
        return

    deck_info = next((d for d in decks if d["deck_name"] == selected_deck), {})

    # Session state for card index and flip
    state_key = f"fc_idx_{selected_deck}"
    flip_key = f"fc_flip_{selected_deck}"

    if state_key not in st.session_state:
        st.session_state[state_key] = 0
    if flip_key not in st.session_state:
        st.session_state[flip_key] = False

    idx = st.session_state[state_key]
    flipped = st.session_state[flip_key]

    # Progress
    progress = (idx + 1) / len(cards)
    st.progress(progress)
    st.caption(f"Card {idx + 1} of {len(cards)} — {deck_info.get('subject', '')}")

    # Flashcard display
    card = cards[idx]
    showing = card["back"] if flipped else card["front"]
    label = "✅ Answer" if flipped else "❓ Question"
    color = "var(--neon-cyan)" if flipped else "var(--neon-purple)"

    st.markdown(f"""
    <div class="sv-flashcard" style="border-color: {color};">
        <div>
            <div style="color:var(--text-muted); font-size:0.75rem; text-transform:uppercase; 
                        letter-spacing:0.1em; margin-bottom:1rem;">{label}</div>
            <div style="font-size:1.2rem; font-weight:600; color:var(--text-primary); 
                        line-height:1.6; max-width:500px; text-align:center;">
                {showing}
            </div>
            <div style="color:var(--text-muted); font-size:0.8rem; margin-top:1.5rem;">
                {'💡 Click "Flip" to see the question' if flipped else '💡 Click "Flip" to reveal the answer'}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Controls
    cc1, cc2, cc3, cc4 = st.columns(4)
    with cc1:
        if st.button("⬅️ Previous", key="fc_prev", use_container_width=True, disabled=idx == 0):
            st.session_state[state_key] = max(0, idx - 1)
            st.session_state[flip_key] = False
            st.rerun()
    with cc2:
        if st.button("🔄 Flip Card", key="fc_flip_btn", use_container_width=True):
            st.session_state[flip_key] = not flipped
            st.rerun()
    with cc3:
        if st.button("➡️ Next", key="fc_next", use_container_width=True, disabled=idx == len(cards) - 1):
            st.session_state[state_key] = min(len(cards) - 1, idx + 1)
            st.session_state[flip_key] = False
            st.rerun()
    with cc4:
        if st.button("🔀 Shuffle", key="fc_shuffle", use_container_width=True):
            import random
            st.session_state[state_key] = random.randint(0, len(cards) - 1)
            st.session_state[flip_key] = False
            st.rerun()

    if idx == len(cards) - 1 and flipped:
        st.success("🎉 You've gone through all cards in this deck! Great work!")
        st.balloons()
