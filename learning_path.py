import os
import time

from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=api_key)


def generate_learning_path(topic, level="Beginner"):

    prompt = f"""
Create a personalized learning path for the following topic:

Topic: {topic}
Learner Level: {level}

The learning path must be suitable for a college student.

Organize the learning journey in the following order:

1. Prerequisites
2. Beginner Level
3. Intermediate Level
4. Advanced Level
5. Practical Activities
6. Mini Project Ideas
7. Learning Resources
   - Videos
   - Articles
   - Books
8. Final Learning Goal

For each level:
- Explain the concepts clearly.
- Arrange topics from easier to harder.
- Make the progression logical.
- Include practical learning activities.

For the resources section:
- Suggest useful types of videos, articles, and books.
- Do not invent specific URLs.
- Mention resource names or search topics where appropriate.

Make the learning path practical, clear, and easy to follow.
Adapt the recommendations to the learner's level.
"""

    max_retries = 3

    for attempt in range(max_retries):

        try:

            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt
            )

            return response.text

        except Exception as e:

            error_message = str(e)

            # Handle quota exceeded error
            if "429" in error_message or "RESOURCE_EXHAUSTED" in error_message:

                return (
                    "Gemini API quota exceeded. "
                    "Please try again after the quota resets."
                )

            # Handle temporary server error
            elif "503" in error_message or "UNAVAILABLE" in error_message:

                if attempt < max_retries - 1:

                    wait_time = 2 ** attempt

                    print(
                        f"Gemini temporarily unavailable. "
                        f"Retrying in {wait_time} seconds..."
                    )

                    time.sleep(wait_time)

                else:

                    return (
                        "Learning path generation failed after multiple retries. "
                        "Gemini is currently experiencing high demand. "
                        "Please try again shortly."
                    )

            else:

                return f"Learning path generation failed: {e}"


if __name__ == "__main__":

    learning_path = generate_learning_path(
        "Python Programming",
        "Beginner"
    )

    print("\nEduGenie Learning Path:")
    print(learning_path)