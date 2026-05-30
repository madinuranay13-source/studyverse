import sqlite3
import json
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "studyverse.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            display_name TEXT,
            avatar_emoji TEXT DEFAULT '🎓',
            xp INTEGER DEFAULT 0,
            level INTEGER DEFAULT 1,
            streak INTEGER DEFAULT 0,
            last_active DATE,
            reputation INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT NOT NULL,
            content TEXT,
            subject TEXT,
            tags TEXT,
            is_pinned INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT NOT NULL,
            description TEXT,
            subject TEXT,
            priority TEXT DEFAULT 'medium',
            status TEXT DEFAULT 'pending',
            due_date DATE,
            completed_at TIMESTAMP,
            ai_summary TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS flashcards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            deck_name TEXT,
            subject TEXT,
            front TEXT NOT NULL,
            back TEXT NOT NULL,
            ease_factor REAL DEFAULT 2.5,
            interval INTEGER DEFAULT 1,
            repetitions INTEGER DEFAULT 0,
            next_review DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS study_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            session_type TEXT DEFAULT 'pomodoro',
            subject TEXT,
            duration_minutes INTEGER,
            started_at TIMESTAMP,
            ended_at TIMESTAMP,
            notes TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS quiz_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            subject TEXT,
            total_questions INTEGER,
            correct_answers INTEGER,
            score_percent REAL,
            topics TEXT,
            taken_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS community_posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT NOT NULL,
            content TEXT,
            subject TEXT,
            post_type TEXT DEFAULT 'question',
            upvotes INTEGER DEFAULT 0,
            view_count INTEGER DEFAULT 0,
            is_answered INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS community_replies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER,
            user_id INTEGER,
            content TEXT,
            upvotes INTEGER DEFAULT 0,
            is_accepted INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (post_id) REFERENCES community_posts(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS ai_chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            role TEXT,
            content TEXT,
            session_id TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS achievements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            achievement_key TEXT,
            achieved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS subject_performance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            subject TEXT,
            study_minutes INTEGER DEFAULT 0,
            quiz_avg REAL DEFAULT 0,
            notes_count INTEGER DEFAULT 0,
            tasks_done INTEGER DEFAULT 0,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    """)

    conn.commit()
    conn.close()


# ── User helpers ──────────────────────────────────────────────────────────────

def get_or_create_user(username: str, display_name: str = None):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    if not user:
        dn = display_name or username
        c.execute(
            "INSERT INTO users (username, display_name) VALUES (?, ?)",
            (username, dn),
        )
        conn.commit()
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = c.fetchone()
    conn.close()
    return dict(user)


def update_user_xp(user_id: int, xp_gain: int):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT xp, level FROM users WHERE id = ?", (user_id,))
    row = c.fetchone()
    new_xp = row["xp"] + xp_gain
    new_level = 1 + new_xp // 500
    c.execute(
        "UPDATE users SET xp = ?, level = ?, last_active = ? WHERE id = ?",
        (new_xp, new_level, datetime.now().date(), user_id),
    )
    conn.commit()
    conn.close()


def update_streak(user_id: int):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT streak, last_active FROM users WHERE id = ?", (user_id,))
    row = c.fetchone()
    today = datetime.now().date()
    last = row["last_active"]
    streak = row["streak"]
    if last:
        from datetime import timedelta
        last_date = datetime.strptime(str(last), "%Y-%m-%d").date()
        if (today - last_date).days == 1:
            streak += 1
        elif (today - last_date).days > 1:
            streak = 1
    else:
        streak = 1
    c.execute(
        "UPDATE users SET streak = ?, last_active = ? WHERE id = ?",
        (streak, today, user_id),
    )
    conn.commit()
    conn.close()
    return streak


def get_user_stats(user_id: int):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = dict(c.fetchone())

    c.execute("SELECT COUNT(*) as cnt FROM notes WHERE user_id = ?", (user_id,))
    user["notes_count"] = c.fetchone()["cnt"]

    c.execute("SELECT COUNT(*) as cnt FROM tasks WHERE user_id = ? AND status = 'done'", (user_id,))
    user["tasks_done"] = c.fetchone()["cnt"]

    c.execute("SELECT COUNT(*) as cnt FROM tasks WHERE user_id = ?", (user_id,))
    user["tasks_total"] = c.fetchone()["cnt"]

    c.execute("SELECT SUM(duration_minutes) as total FROM study_sessions WHERE user_id = ?", (user_id,))
    res = c.fetchone()
    user["total_study_minutes"] = res["total"] or 0

    c.execute("SELECT AVG(score_percent) as avg FROM quiz_results WHERE user_id = ?", (user_id,))
    res = c.fetchone()
    user["quiz_avg"] = round(res["avg"] or 0, 1)

    c.execute("SELECT COUNT(*) as cnt FROM flashcards WHERE user_id = ?", (user_id,))
    user["flashcard_count"] = c.fetchone()["cnt"]

    conn.close()
    return user


# ── Notes ─────────────────────────────────────────────────────────────────────

def save_note(user_id, title, content, subject, tags=""):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "INSERT INTO notes (user_id, title, content, subject, tags) VALUES (?, ?, ?, ?, ?)",
        (user_id, title, content, subject, tags),
    )
    conn.commit()
    conn.close()
    update_user_xp(user_id, 10)


def get_notes(user_id, subject=None):
    conn = get_connection()
    c = conn.cursor()
    if subject:
        c.execute("SELECT * FROM notes WHERE user_id = ? AND subject = ? ORDER BY is_pinned DESC, updated_at DESC", (user_id, subject))
    else:
        c.execute("SELECT * FROM notes WHERE user_id = ? ORDER BY is_pinned DESC, updated_at DESC", (user_id,))
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows


def delete_note(note_id):
    conn = get_connection()
    conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    conn.commit()
    conn.close()


def pin_note(note_id, pinned: bool):
    conn = get_connection()
    conn.execute("UPDATE notes SET is_pinned = ? WHERE id = ?", (int(pinned), note_id))
    conn.commit()
    conn.close()


# ── Tasks ─────────────────────────────────────────────────────────────────────

def save_task(user_id, title, description, subject, priority, due_date, ai_summary=""):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "INSERT INTO tasks (user_id, title, description, subject, priority, due_date, ai_summary) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (user_id, title, description, subject, priority, due_date, ai_summary),
    )
    conn.commit()
    conn.close()
    update_user_xp(user_id, 5)


def get_tasks(user_id, status=None):
    conn = get_connection()
    c = conn.cursor()
    if status:
        c.execute("SELECT * FROM tasks WHERE user_id = ? AND status = ? ORDER BY due_date ASC", (user_id, status))
    else:
        c.execute("SELECT * FROM tasks WHERE user_id = ? ORDER BY due_date ASC", (user_id,))
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows


def update_task_status(task_id, status):
    conn = get_connection()
    conn.execute(
        "UPDATE tasks SET status = ?, completed_at = ? WHERE id = ?",
        (status, datetime.now() if status == "done" else None, task_id),
    )
    conn.commit()
    conn.close()


# ── Flashcards ────────────────────────────────────────────────────────────────

def save_flashcard(user_id, deck_name, subject, front, back):
    conn = get_connection()
    conn.execute(
        "INSERT INTO flashcards (user_id, deck_name, subject, front, back) VALUES (?, ?, ?, ?, ?)",
        (user_id, deck_name, subject, front, back),
    )
    conn.commit()
    conn.close()
    update_user_xp(user_id, 5)


def get_flashcards(user_id, deck_name=None):
    conn = get_connection()
    c = conn.cursor()
    if deck_name:
        c.execute("SELECT * FROM flashcards WHERE user_id = ? AND deck_name = ?", (user_id, deck_name))
    else:
        c.execute("SELECT * FROM flashcards WHERE user_id = ?", (user_id,))
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows


def get_decks(user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT DISTINCT deck_name, subject, COUNT(*) as card_count FROM flashcards WHERE user_id = ? GROUP BY deck_name", (user_id,))
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows


# ── Study sessions ────────────────────────────────────────────────────────────

def log_study_session(user_id, subject, duration_minutes, session_type="pomodoro"):
    conn = get_connection()
    conn.execute(
        "INSERT INTO study_sessions (user_id, session_type, subject, duration_minutes, started_at, ended_at) VALUES (?, ?, ?, ?, ?, ?)",
        (user_id, session_type, subject, duration_minutes, datetime.now(), datetime.now()),
    )
    conn.commit()
    conn.close()
    update_user_xp(user_id, duration_minutes // 5)
    update_streak(user_id)


def get_study_sessions(user_id, days=30):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "SELECT * FROM study_sessions WHERE user_id = ? AND started_at >= datetime('now', ?) ORDER BY started_at DESC",
        (user_id, f"-{days} days"),
    )
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows


# ── Quiz results ──────────────────────────────────────────────────────────────

def save_quiz_result(user_id, subject, total, correct, topics=""):
    score = round((correct / total) * 100, 1) if total > 0 else 0
    conn = get_connection()
    conn.execute(
        "INSERT INTO quiz_results (user_id, subject, total_questions, correct_answers, score_percent, topics) VALUES (?, ?, ?, ?, ?, ?)",
        (user_id, subject, total, correct, score, topics),
    )
    conn.commit()
    conn.close()
    update_user_xp(user_id, int(score // 5))
    return score


def get_quiz_results(user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM quiz_results WHERE user_id = ? ORDER BY taken_at DESC", (user_id,))
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows


# ── Community ─────────────────────────────────────────────────────────────────

def create_post(user_id, title, content, subject, post_type="question"):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "INSERT INTO community_posts (user_id, title, content, subject, post_type) VALUES (?, ?, ?, ?, ?)",
        (user_id, title, content, subject, post_type),
    )
    post_id = c.lastrowid
    conn.commit()
    conn.close()
    update_user_xp(user_id, 15)
    return post_id


def get_posts(subject=None, post_type=None):
    conn = get_connection()
    c = conn.cursor()
    query = """
        SELECT p.*, u.display_name, u.avatar_emoji, u.level,
               (SELECT COUNT(*) FROM community_replies r WHERE r.post_id = p.id) as reply_count
        FROM community_posts p
        JOIN users u ON p.user_id = u.id
        WHERE 1=1
    """
    params = []
    if subject:
        query += " AND p.subject = ?"
        params.append(subject)
    if post_type:
        query += " AND p.post_type = ?"
        params.append(post_type)
    query += " ORDER BY p.upvotes DESC, p.created_at DESC"
    c.execute(query, params)
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows


def upvote_post(post_id):
    conn = get_connection()
    conn.execute("UPDATE community_posts SET upvotes = upvotes + 1 WHERE id = ?", (post_id,))
    conn.commit()
    conn.close()


def add_reply(post_id, user_id, content):
    conn = get_connection()
    conn.execute(
        "INSERT INTO community_replies (post_id, user_id, content) VALUES (?, ?, ?)",
        (post_id, user_id, content),
    )
    conn.commit()
    conn.close()
    update_user_xp(user_id, 10)


def get_replies(post_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT r.*, u.display_name, u.avatar_emoji, u.level
        FROM community_replies r
        JOIN users u ON r.user_id = u.id
        WHERE r.post_id = ?
        ORDER BY r.is_accepted DESC, r.upvotes DESC
    """, (post_id,))
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows


# ── AI Chat History ───────────────────────────────────────────────────────────

def save_chat_message(user_id, role, content, session_id):
    conn = get_connection()
    conn.execute(
        "INSERT INTO ai_chat_history (user_id, role, content, session_id) VALUES (?, ?, ?, ?)",
        (user_id, role, content, session_id),
    )
    conn.commit()
    conn.close()


def get_chat_history(user_id, session_id, limit=20):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "SELECT role, content FROM ai_chat_history WHERE user_id = ? AND session_id = ? ORDER BY created_at DESC LIMIT ?",
        (user_id, session_id, limit),
    )
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return list(reversed(rows))


# ── Analytics ─────────────────────────────────────────────────────────────────

def get_performance_data(user_id):
    conn = get_connection()
    c = conn.cursor()

    # Study time per subject
    c.execute("""
        SELECT subject, SUM(duration_minutes) as total_minutes
        FROM study_sessions WHERE user_id = ? AND subject IS NOT NULL
        GROUP BY subject ORDER BY total_minutes DESC
    """, (user_id,))
    study_by_subject = [dict(r) for r in c.fetchall()]

    # Quiz scores per subject
    c.execute("""
        SELECT subject, AVG(score_percent) as avg_score, COUNT(*) as quiz_count
        FROM quiz_results WHERE user_id = ?
        GROUP BY subject
    """, (user_id,))
    quiz_by_subject = [dict(r) for r in c.fetchall()]

    # Daily study time (last 14 days)
    c.execute("""
        SELECT DATE(started_at) as date, SUM(duration_minutes) as minutes
        FROM study_sessions WHERE user_id = ? AND started_at >= datetime('now', '-14 days')
        GROUP BY DATE(started_at) ORDER BY date
    """, (user_id,))
    daily_study = [dict(r) for r in c.fetchall()]

    # Task completion
    c.execute("""
        SELECT status, COUNT(*) as cnt FROM tasks WHERE user_id = ? GROUP BY status
    """, (user_id,))
    task_status = {r["status"]: r["cnt"] for r in c.fetchall()}

    conn.close()
    return {
        "study_by_subject": study_by_subject,
        "quiz_by_subject": quiz_by_subject,
        "daily_study": daily_study,
        "task_status": task_status,
    }
