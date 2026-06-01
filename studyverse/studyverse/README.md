# ⚡ Studyverse — Student Intelligence Platform

> *"Study smarter. Procrastinate less. (We know. We know.)"*

A production-grade, AI-powered student platform built with **Streamlit** + **Claude AI**. Dark glassmorphism UI, real analytics, and enough features to make your Google Docs notes feel inadequate.

---

## 🚀 Features

| Module | What it does |
|--------|-------------|
| 🏠 **Dashboard** | XP system, streak tracking, charts, task overview |
| 🤖 **AI Assistant (Sage)** | Streaming chat, quiz gen, flashcard gen, summarizer |
| 📝 **Notes** | Rich markdown notes, pinning, tagging, AI summarization |
| ✅ **Tasks** | Homework manager with deadlines, priorities, AI analysis |
| 🃏 **Flashcards** | Deck manager + AI auto-generation + study mode |
| 🍅 **Pomodoro** | Focus timer with session logging + streak tracking |
| 🎯 **Quiz** | AI-generated MCQs with instant feedback & scoring |
| 📈 **Analytics** | Performance radar, study heatmap, AI weakness detection |
| 🌐 **Community** | Q&A forum, upvotes, threaded replies, reputation system |
| 🛠️ **Toolkit** | Summarizer, mnemonics, study planner, concept explainer, solver |

---

## 📁 Project Structure

```
studyverse/
├── app.py                    # Main entry point
├── requirements.txt          # Dependencies
├── .gitignore
├── .streamlit/
│   ├── config.toml           # Streamlit dark theme config
│   └── secrets.toml.example  # API key template
├── database/
│   ├── __init__.py
│   └── db.py                 # SQLite ORM layer (all DB operations)
├── services/
│   ├── __init__.py
│   └── ai_service.py         # Anthropic Claude API integration
├── components/
│   ├── __init__.py
│   └── styles.py             # Global CSS, quotes, constants
├── pages/
│   ├── __init__.py
│   ├── dashboard.py
│   ├── ai_assistant.py
│   ├── notes.py
│   ├── tasks.py
│   ├── flashcards.py
│   ├── pomodoro.py
│   ├── quiz.py
│   ├── analytics.py
│   ├── community.py
│   └── toolkit.py
└── utils/
    ├── __init__.py
    └── helpers.py            # Utility functions
```

---

## ⚙️ Setup & Installation

### 1. Clone / Extract

```bash
# If cloned from GitHub:
git clone https://github.com/yourusername/studyverse.git
cd studyverse

# If you downloaded the ZIP:
unzip studyverse.zip
cd studyverse
```

### 2. Create Virtual Environment (recommended)

```bash
python -m venv venv

# macOS / Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up API Key

You need an **Anthropic API key** for all AI features.

**Option A — Secrets file (recommended for local dev):**
```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Now edit .streamlit/secrets.toml and paste your key:
# ANTHROPIC_API_KEY = "sk-ant-..."
```

**Option B — Environment variable:**
```bash
export ANTHROPIC_API_KEY="sk-ant-your-key-here"
```

Get your key at: https://console.anthropic.com

### 5. Run the App

```bash
streamlit run app.py
```

Open your browser to **http://localhost:8501** 🎉

---

## ☁️ Deploy to Streamlit Cloud

1. Push your repo to GitHub (make sure `secrets.toml` is in `.gitignore` ✅)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **New app** → select your repo → set **Main file**: `app.py`
4. Go to **Advanced settings → Secrets** and add:
   ```toml
   ANTHROPIC_API_KEY = "sk-ant-your-key-here"
   ```
5. Click **Deploy** 🚀

---

## 🗄️ Database

Studyverse uses **SQLite** (zero-config, file-based). The database `studyverse.db` is auto-created on first run in the project root.

Tables: `users`, `notes`, `tasks`, `flashcards`, `study_sessions`, `quiz_results`, `community_posts`, `community_replies`, `ai_chat_history`, `achievements`, `subject_performance`

---

## 🤖 AI Features (require API key)

- **Sage Chat** — streaming conversations with context memory
- **Quiz Generator** — JSON-structured MCQs with explanations
- **Flashcard Generator** — auto-generates card decks from notes
- **Summarizer** — 4 styles: concise, detailed, ELI5, exam-focus
- **Concept Explainer** — 5 complexity levels from ELI5 to Expert
- **Problem Solver** — step-by-step homework solutions
- **Mnemonics Generator** — acronyms, stories, rhymes
- **Study Plan Generator** — personalized exam prep schedules
- **Weakness Analyzer** — AI analysis of your quiz/study patterns

---

## 🎮 XP & Gamification

| Action | XP Gained |
|--------|-----------|
| Create a note | +10 XP |
| Add a task | +5 XP |
| Complete a task | logged |
| Create a flashcard | +5 XP |
| Study session (per 5 min) | +1 XP |
| Quiz score (per 5%) | +1 XP |
| Community post | +15 XP |
| Reply to post | +10 XP |

Level up every **500 XP**. Daily study = streak 🔥

---

## 📦 Key Dependencies

| Package | Purpose |
|---------|---------|
| `streamlit` | UI framework |
| `anthropic` | Claude AI API |
| `plotly` | Interactive charts |
| `pandas` | Data manipulation |
| `sqlite3` | Built-in, no install needed |

---

## 🛠️ Customization

- **Add subjects**: Edit `SUBJECTS` list in `components/styles.py`
- **Add quotes**: Edit `STUDENT_QUOTES` in `components/styles.py`
- **Change colors**: Edit CSS variables in `DARK_THEME_CSS`
- **Add AI personas**: Modify `SYSTEM_PROMPT` in `services/ai_service.py`
- **Add pages**: Create in `pages/`, register in `pages/__init__.py` and `app.py`

---

## 📄 License

MIT — do whatever you want, just don't submit this as your CS assignment. 

*(Just kidding. Kind of.)*

---

*Built with ☕, 🍅, and an unhealthy amount of Claude AI.*
