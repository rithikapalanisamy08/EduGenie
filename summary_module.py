import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=api_key)


def summarize_text(text):
    prompt = f"""
Summarize the following educational text clearly and concisely.

Include:
- Main idea
- Important points
- Key terms
- Short conclusion

Text:
{text}
"""

    max_retries = 3

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt
            )

            return response.text

        except Exception as e:

            error_message = str(e)

            # Retry only for temporary server/high-demand errors
            if "503" in error_message or "UNAVAILABLE" in error_message:

                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    print(
                        f"Gemini temporarily unavailable. "
                        f"Retrying in {wait_time} seconds..."
                    )
                    time.sleep(wait_time)

                else:
                    return (
                        "Summary generation failed after multiple retries. "
                        "Gemini is currently experiencing high demand. "
                        "Please try again shortly."
                    )

            else:
                return f"Summary generation failed: {e}"


if __name__ == "__main__":

    sample_text = """
    Artificial Intelligence is a branch of computer science that focuses
    on creating machines capable of performing tasks that normally require
    human intelligence. These tasks include learning, reasoning,
    problem-solving, understanding language, and recognizing patterns.
    AI is widely used in healthcare, education, finance, transportation,
    and many other fields.
    """

    summary = summarize_text(sample_text)

    print("\nEduGenie Summary:")
    print(summary)