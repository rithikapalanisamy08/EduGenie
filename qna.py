import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=api_key)


def ask_question(question):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=question
    )

    return response.text


if __name__ == "__main__":
    answer = ask_question("What is Artificial Intelligence?")
    print("\nEduGenie Answer:")
    print(answer)