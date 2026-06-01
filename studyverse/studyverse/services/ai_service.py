import anthropic
import os
import json
import streamlit as st
from typing import Generator


def get_client():
    api_key = os.environ.get("ANTHROPIC_API_KEY") or st.secrets.get("ANTHROPIC_API_KEY", "")
    return anthropic.Anthropic(api_key=api_key)


SYSTEM_PROMPT = """You are Sage, the AI study companion inside Studyverse — a cutting-edge student intelligence platform.

You are:
- Extremely knowledgeable across all academic subjects
- Encouraging but honest (you'll tell students when they're wrong, kindly)
- Slightly witty — you occasionally drop a relatable student joke or meme reference
- Adaptive — you explain concepts at whatever level the student needs (ELI5 to PhD level)
- Focused on *understanding*, not just answers

Your capabilities:
1. Explain concepts at multiple levels of complexity
2. Solve homework problems step-by-step (showing work, not just answers)
3. Generate practice quizzes with instant feedback
4. Create flashcard content
5. Summarize notes and documents
6. Detect knowledge gaps and suggest study plans
7. Generate mnemonics, analogies, and memory tricks
8. Provide exam strategies and tips

Personality quirks:
- You sometimes say "Okay, let's cook 🧑‍🍳" before solving something complex
- You celebrate correct answers with "YESSS let's go! 🔥"
- You gently roast procrastination: "Starting 2 hours before the deadline? Bold strategy. Let's make it work."
- You use emojis moderately (not excessively)

Always format math and code properly. Use markdown. Keep responses structured and scannable.
"""


def stream_ai_response(messages: list, system: str = SYSTEM_PROMPT) -> Generator:
    """Stream AI response token by token."""
    client = get_client()
    with client.messages.stream(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        system=system,
        messages=messages,
    ) as stream:
        for text in stream.text_stream:
            yield text


def get_ai_response(messages: list, system: str = SYSTEM_PROMPT) -> str:
    """Get full AI response (non-streaming)."""
    client = get_client()
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        system=system,
        messages=messages,
    )
    return response.content[0].text


def generate_quiz(subject: str, topic: str, difficulty: str, num_questions: int = 5) -> list:
    """Generate a quiz with questions and answers."""
    system = """You are a quiz generator. Return ONLY valid JSON — no markdown, no explanation.
Format: [{"question": "...", "options": ["A", "B", "C", "D"], "correct": 0, "explanation": "..."}]
correct is the 0-based index of the correct option."""

    prompt = f"""Generate {num_questions} multiple-choice questions about {topic} in {subject}.
Difficulty: {difficulty}. Mix conceptual and applied questions.
Return ONLY the JSON array."""

    response = get_ai_response([{"role": "user", "content": prompt}], system=system)
    try:
        clean = response.strip().replace("```json", "").replace("```", "").strip()
        return json.loads(clean)
    except Exception:
        return []


def generate_flashcards(content: str, num_cards: int = 8) -> list:
    """Generate flashcards from content."""
    system = """You are a flashcard generator. Return ONLY valid JSON — no markdown, no preamble.
Format: [{"front": "question or term", "back": "answer or definition"}]"""

    prompt = f"""Create {num_cards} high-quality flashcards from this content:

{content}

Focus on key concepts, definitions, and important facts. Return ONLY the JSON array."""

    response = get_ai_response([{"role": "user", "content": prompt}], system=system)
    try:
        clean = response.strip().replace("```json", "").replace("```", "").strip()
        return json.loads(clean)
    except Exception:
        return []


def summarize_content(content: str, style: str = "concise") -> str:
    """Summarize notes or assignments."""
    styles = {
        "concise": "Create a concise bullet-point summary (max 8 bullets). Focus on key takeaways.",
        "detailed": "Create a detailed structured summary with sections and sub-points.",
        "eli5": "Explain this like I'm 12. Use simple language and fun analogies.",
        "exam": "Create an exam-focused summary highlighting likely test topics and key facts to memorize.",
    }

    prompt = f"""{styles.get(style, styles['concise'])}

Content to summarize:
{content}"""

    return get_ai_response([{"role": "user", "content": prompt}])


def analyze_weaknesses(quiz_results: list, study_sessions: list) -> str:
    """Analyze student performance and identify weaknesses."""
    data = {
        "quiz_results": quiz_results[-10:] if quiz_results else [],
        "study_sessions": study_sessions[-20:] if study_sessions else [],
    }

    prompt = f"""Analyze this student's performance data and provide:
1. Top 3 strength areas 💪
2. Top 3 areas needing improvement ⚠️  
3. Specific study recommendations 📚
4. A motivational message (keep it real, slightly humorous) 😄

Performance data:
{json.dumps(data, indent=2, default=str)}

Keep the response concise, actionable, and encouraging."""

    return get_ai_response([{"role": "user", "content": prompt}])


def generate_study_plan(subject: str, exam_date: str, current_level: str, topics: str) -> str:
    """Generate a personalized study plan."""
    prompt = f"""Create a detailed study plan for:
- Subject: {subject}
- Exam date: {exam_date}
- Current knowledge level: {current_level}
- Topics to cover: {topics}

Include:
1. Week-by-week schedule
2. Daily time recommendations
3. Resource suggestions
4. Review strategy
5. Day-before-exam tips

Make it realistic and motivating. Add one funny/relatable student tip."""

    return get_ai_response([{"role": "user", "content": prompt}])


def explain_concept(concept: str, level: str = "intermediate") -> str:
    """Explain a concept at a specific complexity level."""
    levels = {
        "beginner": "Explain as if to a complete beginner or 10-year-old. Use simple analogies and no jargon.",
        "intermediate": "Explain clearly for a high school or early college student. Balance depth with accessibility.",
        "advanced": "Explain in depth for an advanced student. Include nuances, edge cases, and connections to related concepts.",
        "expert": "Explain at a graduate/expert level. Include technical details, mathematical underpinnings where relevant.",
    }

    prompt = f"""{levels.get(level, levels['intermediate'])}

Concept to explain: {concept}

Structure your explanation with:
- Core idea (1-2 sentences)
- Detailed explanation
- Real-world example or analogy
- Common misconceptions (if any)
- Key takeaway"""

    return get_ai_response([{"role": "user", "content": prompt}])


def solve_problem(problem: str) -> str:
    """Solve a homework problem step by step."""
    prompt = f"""Solve this problem step by step. Show ALL work. 

Problem: {problem}

Format:
**Understanding the Problem:** (what are we solving?)
**Approach:** (strategy/method)
**Solution:**
Step 1: ...
Step 2: ...
...
**Final Answer:** (clearly stated)
**Verification:** (check your work if applicable)
**Key Concept:** (what principle does this demonstrate?)"""

    return get_ai_response([{"role": "user", "content": prompt}])


def generate_mnemonics(topic: str, items: str) -> str:
    """Generate memory tricks for a list of items."""
    prompt = f"""Create creative mnemonics and memory tricks for:
Topic: {topic}
Items to memorize: {items}

Include:
1. Acronym or acrostic (if applicable)
2. Visual memory palace suggestion
3. Rhyme or song (if items ≤ 8)
4. Story method
5. Quick association trick

Make them memorable and slightly silly — the weirder, the better for memory!"""

    return get_ai_response([{"role": "user", "content": prompt}])
