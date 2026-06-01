import streamlit as st
from datetime import datetime, date
import humanize
import pytz


def time_ago(dt_str: str) -> str:
    """Return human-readable relative time."""
    try:
        if not dt_str:
            return ""
        dt = datetime.strptime(str(dt_str)[:19], "%Y-%m-%d %H:%M:%S")
        return humanize.naturaltime(datetime.now() - dt)
    except Exception:
        return str(dt_str)[:10]


def format_duration(minutes: int) -> str:
    """Format minutes into readable duration."""
    if minutes < 60:
        return f"{minutes}m"
    hours = minutes // 60
    mins = minutes % 60
    if mins == 0:
        return f"{hours}h"
    return f"{hours}h {mins}m"


def get_level_title(level: int) -> str:
    titles = {
        1: "Freshman",
        2: "Sophomore",
        3: "Junior",
        4: "Senior",
        5: "Graduate",
        6: "Scholar",
        7: "Expert",
        8: "Master",
        9: "Professor",
        10: "Legend",
    }
    if level >= 10:
        return "Legend ✨"
    return titles.get(level, f"Level {level}")


def get_xp_for_level(level: int) -> int:
    return level * 500


def days_until(date_str: str) -> int:
    try:
        target = datetime.strptime(str(date_str), "%Y-%m-%d").date()
        return (target - date.today()).days
    except Exception:
        return 0


def truncate(text: str, max_len: int = 100) -> str:
    if not text:
        return ""
    return text[:max_len] + ("..." if len(text) > max_len else "")


def subject_emoji(subject: str) -> str:
    emojis = {
        "Mathematics": "🔢",
        "Physics": "⚛️",
        "Chemistry": "🧪",
        "Biology": "🧬",
        "English": "📖",
        "History": "🏛️",
        "Geography": "🌍",
        "Computer Science": "💻",
        "Economics": "📊",
        "Psychology": "🧠",
        "Philosophy": "🤔",
        "Literature": "📚",
        "Art": "🎨",
        "Music": "🎵",
        "Other": "📝",
    }
    return emojis.get(subject, "📝")
