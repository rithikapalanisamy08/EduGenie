
import os
import json
import re
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=api_key)


def clean_json_block(text):
    """Extract JSON from the AI response."""
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


def generate_quiz(passage):
    """Generate a quiz based on the user's actual input."""

    if not passage or not passage.strip():
        return {"error": "Please enter a topic or passage first."}

    prompt = f"""
You are EduGenie, an educational quiz generator.

USER INPUT:
{passage}

TASK:
Create exactly 3 multiple-choice questions based ONLY on
the user's input above.

STRICT RULES:
1. Identify the actual topic of the user's input first.
2. Every question must test knowledge of that topic.
3. Do not use fixed, sample, or unrelated questions.
4. Do not assume the topic is Python.
5. If the input is a short topic name, create questions
   about that topic using your knowledge.
6. If the input is a passage, prioritize information
   explicitly present in the passage.
7. Each question must have exactly four options: A, B, C, D.
8. Only one option must be correct.
9. correct_answer must contain only A, B, C, or D.
10. Avoid duplicate questions.
11. Return ONLY a valid JSON array. No Markdown.

FORMAT:
[
  {{
    "question": "Question text",
    "options": {{
      "A": "First option",
      "B": "Second option",
      "C": "Third option",
      "D": "Fourth option"
    }},
    "correct_answer": "A"
  }}
]
"""

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )

            if not response.text:
                raise ValueError("The AI returned an empty response.")

            cleaned = clean_json_block(response.text)
            quiz = json.loads(cleaned)

            if not isinstance(quiz, list) or len(quiz) != 3:
                raise ValueError("Expected exactly 3 questions.")

            for question in quiz:
                if not isinstance(question, dict):
                    raise ValueError("Invalid question format.")

                if not question.get("question"):
                    raise ValueError("A question is missing its text.")

                options = question.get("options")

                if not isinstance(options, dict) or set(options) != {
                    "A", "B", "C", "D"
                }:
                    raise ValueError(
                        "Each question must have options A, B, C and D."
                    )

                answer = question.get("correct_answer")

                if answer not in {"A", "B", "C", "D"}:
                    raise ValueError("Invalid correct answer.")

            return quiz

        except Exception as e:
            error_message = str(e)
            temporary = (
                "503" in error_message
                or "UNAVAILABLE" in error_message
                or "429" in error_message
                or "RESOURCE_EXHAUSTED" in error_message
            )

            if temporary and attempt < 2:
                time.sleep(2 ** attempt)
                continue

            if temporary:
                return {
                    "error": (
                        "Gemini is temporarily unavailable or busy. "
                        "Please try again shortly."
                    )
                }

            return {"error": f"Quiz generation failed: {e}"}


if __name__ == "__main__":
    sample_passage = """
    Machine Learning is a branch of Artificial Intelligence.
    It allows computers to learn patterns from data.
    """

    quiz = generate_quiz(sample_passage)
    print(json.dumps(quiz, indent=4, ensure_ascii=False))
