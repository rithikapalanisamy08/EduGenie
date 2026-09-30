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
    """Remove Markdown code blocks from Gemini JSON response."""

    text = text.strip()

    if text.startswith("```json"):
        text = text[7:]

    elif text.startswith("```"):
        text = text[3:]

    if text.endswith("```"):
        text = text[:-3]

    return text.strip()


def generate_quiz(passage):

    prompt = f"""
Create exactly 3 multiple-choice questions from the passage below.

Each question must contain:
- question
- four options: A, B, C, D
- correct_answer

The questions must be based only on the given passage.

Return ONLY valid JSON.

Required JSON format:

[
  {{
    "question": "Question text",
    "options": {{
      "A": "Option A",
      "B": "Option B",
      "C": "Option C",
      "D": "Option D"
    }},
    "correct_answer": "A"
  }}
]

Passage:
{passage}
"""

    max_retries = 3

    for attempt in range(max_retries):

        try:
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )

            cleaned_response = clean_json_block(response.text)

            quiz = json.loads(cleaned_response)

            if not isinstance(quiz, list) or len(quiz) != 3:
                raise ValueError("Quiz must contain exactly 3 questions.")

            return quiz

        except Exception as e:

            error_message = str(e)

            if "503" in error_message or "UNAVAILABLE" in error_message:

                if attempt < max_retries - 1:

                    wait_time = 2 ** attempt

                    print(
                        f"Gemini temporarily unavailable. "
                        f"Retrying in {wait_time} seconds..."
                    )

                    time.sleep(wait_time)

                else:

                    return {
                        "error": (
                            "Gemini is currently experiencing high demand. "
                            "Please try again shortly."
                        )
                    }

            else:

                return {
                    "error": f"Quiz generation failed: {e}"
                }


if __name__ == "__main__":

    sample_passage = """
    Machine Learning is a branch of Artificial Intelligence.
    It allows computers to learn patterns from data without being
    explicitly programmed for every task. Machine Learning includes
    supervised learning, unsupervised learning, and reinforcement learning.
    """

    quiz = generate_quiz(sample_passage)

    print("\nEduGenie Quiz:")

    print(
        json.dumps(
            quiz,
            indent=4,
            ensure_ascii=False
        )
    )