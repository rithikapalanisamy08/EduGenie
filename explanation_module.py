import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found")

client = genai.Client(api_key=api_key)


def explain_concept(topic):

    prompt = f"""
Explain the following concept in simple language for a college student.

Concept: {topic}

Include:
1. Simple definition
2. Key points
3. Real-world example
4. Short conclusion
"""

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt
    )

    return response.text 