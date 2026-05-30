bash

cat > /home/claude/studyverse/components/styles.py << 'ENDOFFILE'
DARK_THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&family=Syne:wght@700;800&display=swap');

:root {
  --bg-primary:       #05050f;
  --bg-secondary:     #0a0a1a;
  --bg-card:          rgba(255,255,255,0.04);
  --bg-card-hover:    rgba(255,255,255,0.07);
  --border-glow:      rgba(120,80,255,0.3);
  --border-subtle:    rgba(255,255,255,0.08);
  --neon-purple:      #7b4fff;
  --neon-cyan:        #00d4ff;
  --neon-green:       #00ff88;
  --neon-pink:        #ff4d9d;
  --neon-orange:      #ff8c42;
  --text-primary:     #f0eeff;
  --text-secondary:   rgba(240,238,255,0.6);
  --text-muted:       rgba(240,238,255,0.35);
  --font-display:     'Syne', sans-serif;
  --font-body:        'Space Grotesk', sans-serif;
  --font-mono:        'JetBrains Mono', monospace;
  --radius-lg:        16px;
  --radius-md:        12px;
  --radius-sm:        8px;
  --shadow-glow:      0 0 40px rgba(123,79,255,0.15);
  --shadow-card:      0 8px 32px rgba(0,0,0,0.4);
  --transition:       all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
  background: var(--bg-primary) !important;
  color: var(--text-primary) !important;
  font-family: var(--font-body) !important;
}

[data-testid="stSidebar"] {
  background: rgba(5,5,15,0.95) !important;
  border-right: 1px solid var(--border-subtle) !important;
  backdrop-filter: blur(20px);
}

[data-testid="stSidebar"]::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 2px;
  background: linear-gradient(90deg, var(--neon-purple), var(--neon-cyan));
}

[data-testid="stHeader"] {
  background: rgba(5,5,15,0.9) !important;
  backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--border-subtle);
}

.main .block-container {
  padding: 2rem 2.5rem !important;
  max-width: 1200px !important;
}

h1, h2, h3, h4 {
  font-family: var(--font-display) !important;
  color: var(--text-primary) !important;
  letter-spacing: -0.02em;
}

h1 { font-size: 2.4rem !important; font-weight: 800 !important; }
h2 { font-size: 1.8rem !important; font-weight: 700 !important; }
h3 { font-size: 1.35rem !important; font-weight: 700 !important; }

p, li, span, label, div {
  font-family: var(--font-body) !important;
  color: var(--text-primary);
}

/* ── INPUT FIELDS — light background, dark text so you can read what you type ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stNumberInput > div > div > input,
.stDateInput > div > div > input {
  background: #1e1e2e !important;
  border: 1px solid rgba(123,79,255,0.4) !important;
  border-radius: var(--radius-md) !important;
  color: #f0eeff !important;
  font-family: var(--font-body) !important;
  transition: var(--transition);
  caret-color: #7b4fff !important;
}

.stTextInput > div > div > input::placeholder,
.stTextArea > div > div > textarea::placeholder {
  color: rgba(240,238,255,0.35) !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
  border-color: var(--neon-purple) !important;
  box-shadow: 0 0 0 3px rgba(123,79,255,0.2) !important;
  background: #252535 !important;
}

/* Selectbox */
.stSelectbox > div > div,
.stMultiSelect > div > div {
  background: #1e1e2e !important;
  border: 1px solid rgba(123,79,255,0.4) !important;
  border-radius: var(--radius-md) !important;
  color: #f0eeff !important;
  font-family: var(--font-body) !important;
}

/* Buttons */
.stButton > button {
  background: linear-gradient(135deg, var(--neon-purple), #5b2be0) !important;
  color: white !important;
  border: none !important;
  border-radius: var(--radius-md) !important;
  font-family: var(--font-body) !important;
  font-weight: 600 !important;
  font-size: 0.9rem !important;
  padding: 0.6rem 1.4rem !important;
  transition: var(--transition) !important;
  letter-spacing: 0.01em;
  box-shadow: 0 4px 20px rgba(123,79,255,0.3) !important;
}

.stButton > button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 30px rgba(123,79,255,0.5) !important;
}

.stButton > button:active {
  transform: translateY(0) !important;
}

[data-testid="baseButton-secondary"] {
  background: var(--bg-card) !important;
  border: 1px solid var(--border-subtle) !important;
  box-shadow: none !important;
}

[data-testid="baseButton-secondary"]:hover {
  background: var(--bg-card-hover) !important;
  border-color: var(--neon-purple) !important;
  box-shadow: 0 0 15px rgba(123,79,255,0.2) !important;
}

[data-testid="metric-container"] {
  background: var(--bg-card) !important;
  border: 1px solid var(--border-subtle) !important;
  border-radius: var(--radius-lg) !important;
  padding: 1.2rem !important;
  backdrop-filter: blur(10px);
  transition: var(--transition);
}

[data-testid="metric-container"]:hover {
  border-color: var(--border-glow) !important;
  background: var(--bg-card-hover) !important;
  transform: translateY(-2px);
  box-shadow: var(--shadow-glow);
}

[data-testid="stMetricValue"] {
  font-family: var(--font-display) !important;
  font-size: 2rem !important;
  font-weight: 800 !important;
  background: linear-gradient(135deg, var(--neon-purple), var(--neon-cyan));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

[data-testid="stMetricLabel"] {
  color: var(--text-secondary) !important;
  font-size: 0.8rem !important;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.streamlit-expanderHeader {
  background: var(--bg-card) !important;
  border: 1px solid var(--border-subtle) !important;
  border-radius: var(--radius-md) !important;
  color: var(--text-primary) !important;
  font-weight: 600 !important;
}

.streamlit-expanderContent {
  background: rgba(5,5,15,0.6) !important;
  border: 1px solid var(--border-subtle) !important;
  border-top: none !important;
  border-radius: 0 0 var(--radius-md) var(--radius-md) !important;
}

.stTabs [data-baseweb="tab-list"] {
  background: var(--bg-card) !important;
  border-radius: var(--radius-md) !important;
  padding: 4px !important;
  gap: 4px;
}

.stTabs [data-baseweb="tab"] {
  background: transparent !important;
  color: var(--text-secondary) !important;
  border-radius: var(--radius-sm) !important;
  font-weight: 500 !important;
  font-family: var(--font-body) !important;
  transition: var(--transition) !important;
}

.stTabs [aria-selected="true"] {
  background: linear-gradient(135deg, var(--neon-purple), #5b2be0) !important;
  color: white !important;
  box-shadow: 0 4px 15px rgba(123,79,255,0.4) !important;
}

.stRadio > div { gap: 0.3rem !important; }

.stRadio label {
  background: transparent !important;
  border-radius: var(--radius-sm) !important;
  padding: 0.6rem 0.8rem !important;
  transition: var(--transition) !important;
  cursor: pointer;
  color: var(--text-secondary) !important;
}

.stRadio label:hover {
  background: var(--bg-card-hover) !important;
  color: var(--text-primary) !important;
}

.stProgress > div > div > div > div {
  background: linear-gradient(90deg, var(--neon-purple), var(--neon-cyan)) !important;
  border-radius: 99px !important;
}

.stProgress > div > div > div {
  background: var(--bg-card) !important;
  border-radius: 99px !important;
}

.stSuccess, .stInfo, .stWarning, .stError {
  border-radius: var(--radius-md) !important;
  border: none !important;
  backdrop-filter: blur(10px);
}

.stSuccess {
  background: rgba(0,255,136,0.1) !important;
  border-left: 3px solid var(--neon-green) !important;
  color: var(--neon-green) !important;
}

.stInfo {
  background: rgba(0,212,255,0.1) !important;
  border-left: 3px solid var(--neon-cyan) !important;
}

.stWarning {
  background: rgba(255,140,66,0.1) !important;
  border-left: 3px solid var(--neon-orange) !important;
}

.stError {
  background: rgba(255,77,157,0.1) !important;
  border-left: 3px solid var(--neon-pink) !important;
}

hr { border-color: var(--border-subtle) !important; }

::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg-secondary); }
::-webkit-scrollbar-thumb {
  background: var(--neon-purple);
  border-radius: 99px;
  opacity: 0.5;
}

[data-testid="stChatMessageContent"] {
  background: var(--bg-card) !important;
  border: 1px solid var(--border-subtle) !important;
  border-radius: var(--radius-lg) !important;
  font-family: var(--font-body) !important;
}

code, pre {
  font-family: var(--font-mono) !important;
  background: rgba(0,0,0,0.4) !important;
  border: 1px solid var(--border-subtle) !important;
  border-radius: var(--radius-sm) !important;
}

[data-testid="stDataFrame"] {
  border: 1px solid var(--border-subtle) !important;
  border-radius: var(--radius-md) !important;
  overflow: hidden;
}

.stCheckbox label { color: var(--text-primary) !important; }
.stSlider > div > div > div { color: var(--text-primary) !important; }

#MainMenu, footer, [data-testid="stToolbar"] { visibility: hidden; }

@keyframes pulse-glow {
  0%, 100% { box-shadow: 0 0 20px rgba(123,79,255,0.3); }
  50% { box-shadow: 0 0 40px rgba(123,79,255,0.6); }
}

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-6px); }
}

@keyframes shimmer {
  0% { background-position: -200% center; }
  100% { background-position: 200% center; }
}

@keyframes slide-in {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}

.sv-card {
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: 1.5rem;
  transition: var(--transition);
  animation: slide-in 0.3s ease;
}

.sv-card:hover {
  border-color: var(--border-glow);
  background: var(--bg-card-hover);
  box-shadow: var(--shadow-glow);
  transform: translateY(-2px);
}

.sv-card-glow {
  background: var(--bg-card);
  border: 1px solid var(--border-glow);
  border-radius: var(--radius-lg);
  padding: 1.5rem;
  animation: pulse-glow 3s ease-in-out infinite;
}

.sv-badge {
  display: inline-flex;
  align-items: center;
  padding: 0.2rem 0.7rem;
  border-radius: 99px;
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 0.04em;
}

.sv-badge-purple { background: rgba(123,79,255,0.2); color: var(--neon-purple); border: 1px solid rgba(123,79,255,0.3); }
.sv-badge-cyan   { background: rgba(0,212,255,0.2);  color: var(--neon-cyan);   border: 1px solid rgba(0,212,255,0.3); }
.sv-badge-green  { background: rgba(0,255,136,0.2);  color: var(--neon-green);  border: 1px solid rgba(0,255,136,0.3); }
.sv-badge-pink   { background: rgba(255,77,157,0.2); color: var(--neon-pink);   border: 1px solid rgba(255,77,157,0.3); }
.sv-badge-orange { background: rgba(255,140,66,0.2); color: var(--neon-orange); border: 1px solid rgba(255,140,66,0.3); }

.sv-gradient-text {
  background: linear-gradient(135deg, var(--neon-purple), var(--neon-cyan));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.sv-neon-text-green {
  color: var(--neon-green);
  text-shadow: 0 0 20px rgba(0,255,136,0.5);
}

.sv-hero-title {
  font-family: var(--font-display) !important;
  font-size: 3rem;
  font-weight: 800;
  background: linear-gradient(135deg, var(--neon-purple) 0%, var(--neon-cyan) 50%, var(--neon-green) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1.1;
  letter-spacing: -0.03em;
}

.sv-stat-card {
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: 1.5rem;
  text-align: center;
  transition: var(--transition);
  position: relative;
  overflow: hidden;
}

.sv-stat-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 2px;
  background: linear-gradient(90deg, var(--neon-purple), var(--neon-cyan));
  border-radius: var(--radius-lg) var(--radius-lg) 0 0;
}

.sv-stat-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-glow);
  border-color: var(--border-glow);
}

.sv-quote-box {
  background: linear-gradient(135deg, rgba(123,79,255,0.08), rgba(0,212,255,0.05));
  border: 1px solid rgba(123,79,255,0.2);
  border-radius: var(--radius-lg);
  padding: 1.2rem 1.5rem;
  font-style: italic;
  color: var(--text-secondary);
  font-size: 0.95rem;
  position: relative;
}

.sv-quote-box::before {
  content: '"';
  position: absolute;
  top: -0.5rem;
  left: 1rem;
  font-size: 3rem;
  font-family: var(--font-display);
  color: var(--neon-purple);
  line-height: 1;
}

.sv-task-card {
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 1rem 1.2rem;
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  transition: var(--transition);
}

.sv-task-card:hover {
  border-color: var(--border-glow);
  background: var(--bg-card-hover);
}

.sv-priority-high   { border-left: 3px solid var(--neon-pink) !important; }
.sv-priority-medium { border-left: 3px solid var(--neon-orange) !important; }
.sv-priority-low    { border-left: 3px solid var(--neon-green) !important; }

.sv-flashcard {
  background: var(--bg-card);
  border: 1px solid var(--border-glow);
  border-radius: var(--radius-lg);
  padding: 3rem 2rem;
  text-align: center;
  min-height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: var(--transition);
  animation: float 3s ease-in-out infinite;
}

.sv-flashcard:hover {
  box-shadow: 0 0 40px rgba(123,79,255,0.4);
  transform: scale(1.02);
}

.sv-xp-bar {
  height: 8px;
  background: var(--bg-card);
  border-radius: 99px;
  overflow: hidden;
}

.sv-xp-fill {
  height: 100%;
  border-radius: 99px;
  background: linear-gradient(90deg, var(--neon-purple), var(--neon-cyan));
  transition: width 0.8s cubic-bezier(0.4,0,0.2,1);
}

.sv-pomodoro-ring {
  width: 200px;
  height: 200px;
  border-radius: 50%;
  border: 6px solid var(--bg-card);
  border-top-color: var(--neon-purple);
  border-right-color: var(--neon-cyan);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  box-shadow: 0 0 40px rgba(123,79,255,0.3), inset 0 0 40px rgba(0,0,0,0.5);
}

.sv-streak-fire {
  font-size: 2.5rem;
  animation: float 2s ease-in-out infinite;
  display: inline-block;
}

.sv-community-post {
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: 1.2rem 1.5rem;
  margin-bottom: 0.8rem;
  transition: var(--transition);
  cursor: pointer;
}

.sv-community-post:hover {
  border-color: var(--border-glow);
  background: var(--bg-card-hover);
  box-shadow: var(--shadow-glow);
}

.sv-reply {
  background: rgba(123,79,255,0.05);
  border: 1px solid rgba(123,79,255,0.15);
  border-radius: var(--radius-md);
  padding: 1rem;
  margin: 0.5rem 0 0.5rem 1.5rem;
}

.sv-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--neon-purple), var(--neon-cyan));
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  flex-shrink: 0;
}

.sv-shimmer {
  background: linear-gradient(90deg, var(--bg-card) 25%, var(--bg-card-hover) 50%, var(--bg-card) 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

.sv-achievement {
  background: linear-gradient(135deg, rgba(255,215,0,0.1), rgba(255,140,0,0.1));
  border: 1px solid rgba(255,215,0,0.3);
  border-radius: var(--radius-md);
  padding: 0.8rem 1rem;
  display: flex;
  align-items: center;
  gap: 0.8rem;
}

.nav-active {
  color: var(--neon-purple) !important;
  font-weight: 700 !important;
}

.quiz-option {
  width: 100%;
  padding: 0.8rem 1.2rem;
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  color: var(--text-primary);
  text-align: left;
  cursor: pointer;
  transition: var(--transition);
  font-family: var(--font-body);
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.quiz-option:hover {
  border-color: var(--neon-purple);
  background: var(--bg-card-hover);
}

.quiz-correct {
  border-color: var(--neon-green) !important;
  background: rgba(0,255,136,0.1) !important;
}

.quiz-wrong {
  border-color: var(--neon-pink) !important;
  background: rgba(255,77,157,0.1) !important;
}

.sv-sidebar-brand {
  font-family: var(--font-display) !important;
  font-weight: 800;
  font-size: 1.5rem;
  background: linear-gradient(135deg, var(--neon-purple), var(--neon-cyan));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: -0.02em;
}

.sv-sidebar-sub {
  font-size: 0.7rem;
  color: var(--text-muted);
  letter-spacing: 0.15em;
  text-transform: uppercase;
}

.sv-loading {
  text-align: center;
  padding: 3rem;
  color: var(--text-secondary);
}

.sv-note-card {
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: 1.2rem;
  margin-bottom: 0.8rem;
  transition: var(--transition);
  position: relative;
  overflow: hidden;
}

.sv-note-card::after {
  content: '';
  position: absolute;
  bottom: 0; left: 0; right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, var(--neon-purple), transparent);
  opacity: 0;
  transition: var(--transition);
}

.sv-note-card:hover::after { opacity: 1; }
.sv-note-card:hover {
  border-color: var(--border-glow);
  background: var(--bg-card-hover);
}

.sv-pinned { border-top: 2px solid var(--neon-orange) !important; }

.subject-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  display: inline-block;
  margin-right: 6px;
}

.sv-meme-strip {
  background: linear-gradient(90deg, rgba(123,79,255,0.05), rgba(0,212,255,0.05));
  border-top: 1px solid var(--border-subtle);
  border-bottom: 1px solid var(--border-subtle);
  padding: 0.5rem 1rem;
  font-size: 0.8rem;
  color: var(--text-muted);
  font-style: italic;
  text-align: center;
}

.sv-level-badge {
  background: linear-gradient(135deg, var(--neon-purple), #5b2be0);
  color: white;
  padding: 0.2rem 0.6rem;
  border-radius: 99px;
  font-size: 0.75rem;
  font-weight: 700;
  display: inline-block;
}
</style>
"""

STUDENT_QUOTES = [
    "\"I'll start studying after this one YouTube video.\" — Every student, always 📺",
    "\"I work best under pressure.\" (Translation: I forgot until now) ⏰",
    "\"Sleep is for the weak.\" — Me, 3am before an exam 🌙",
    "\"The flashcards are basically done... I just need to write on them.\" 📚",
    "\"One more episode, then I'll study.\" (Currently: Season 3, Episode 7) 🎬",
    "\"I'll remember it. I don't need to write it down.\" — Famous last words 🧠",
    "\"All-nighter? More like an all-fighter.\" ☕💪",
    "\"My dog ate my motivation.\" 🐕",
    "\"Studying is just speedrunning forgetting.\" Any%",
    "\"Is it procrastination if I'm procrastinating productively?\" 🤔",
    "\"The exam can't hurt me if I don't sleep and become transcendent.\" ✨",
    "\"Notes? Oh you mean the notebook I'll open the night before?\" 📓",
]

ACHIEVEMENT_DEFINITIONS = {
    "first_note":     {"emoji": "📝", "title": "Note Taker",     "desc": "Created your first note"},
    "note_hoarder":   {"emoji": "📚", "title": "Note Hoarder",   "desc": "Created 25 notes"},
    "task_crusher":   {"emoji": "✅", "title": "Task Crusher",   "desc": "Completed 10 tasks"},
    "quiz_ace":       {"emoji": "🎯", "title": "Quiz Ace",       "desc": "Scored 100% on a quiz"},
    "study_streak_7": {"emoji": "🔥", "title": "On Fire",        "desc": "7-day study streak"},
    "flashcard_fan":  {"emoji": "🃏", "title": "Flashcard Fan",  "desc": "Created 50 flashcards"},
    "community_star": {"emoji": "⭐", "title": "Community Star", "desc": "Got 10 upvotes"},
    "night_owl":      {"emoji": "🦉", "title": "Night Owl",      "desc": "Studied past midnight"},
    "early_bird":     {"emoji": "🐦", "title": "Early Bird",     "desc": "Studied before 7am"},
    "level_10":       {"emoji": "🏆", "title": "Scholar",        "desc": "Reached Level 10"},
    "pomodoro_pro":   {"emoji": "🍅", "title": "Pomodoro Pro",   "desc": "Completed 20 Pomodoro sessions"},
    "sage_talker":    {"emoji": "🤖", "title": "Sage Whisperer", "desc": "Had 50 AI conversations"},
}

SUBJECTS = [
    "Mathematics", "Physics", "Chemistry", "Biology", "English",
    "History", "Geography", "Computer Science", "Economics",
    "Psychology", "Philosophy", "Literature", "Art", "Music", "Other"
]

SUBJECT_COLORS = {
    "Mathematics":      "#7b4fff",
    "Physics":          "#00d4ff",
    "Chemistry":        "#00ff88",
    "Biology":          "#ff4d9d",
    "English":          "#ff8c42",
    "History":          "#ffd700",
    "Geography":        "#4fc3f7",
    "Computer Science": "#a78bfa",
    "Economics":        "#34d399",
    "Psychology":       "#f472b6",
    "Philosophy":       "#60a5fa",
    "Literature":       "#fb923c",
    "Art":              "#e879f9",
    "Music":            "#4ade80",
    "Other":            "#94a3b8",
}
ENDOFFILE
echo "Done"
