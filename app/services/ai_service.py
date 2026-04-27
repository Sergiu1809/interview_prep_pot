from anthropic import Anthropic
from dotenv import load_dotenv
import os

load_dotenv()

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


def generate_question(topic: str, difficulty: str, question_number: int) -> str:
    prompt = prompt = f"""You are a strict but fair technical interviewer conducting a real interview.

Topic: {topic}
Difficulty: {difficulty}
Question number: {question_number}

Your task: Ask one technical interview question.

Rules:
- The question must be clear and unambiguous — the candidate must immediately understand what is being asked
- One question only, no follow-up questions inside it
- No introduction, no "Sure!", no "Great question!" — just the question itself
- No hints, no examples, no partial answers
- The difficulty must match the level specified:
    easy = foundational concepts
    medium = practical application
    hard = deep understanding or edge cases
"""
    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=256,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return message.content[0].text.strip()
