# EduGenie

## AI-Powered Learning Companion

EduGenie is an AI-powered learning companion designed to help college students learn smarter through personalized and interactive learning support.

## Features

- AI-based Question and Answer
- Concept Explanation
- AI-generated Quizzes
- Text Summarization
- Personalized Learning Paths
- FastAPI Backend
- Interactive Web Interface
- Local AI Model for Concept Explanation
- Gemini AI for Generative Learning Tasks

## AI Models

### Gemini AI
Used for:
- Question and Answer
- Quiz Generation
- Text Summarization
- Personalized Learning Paths

### LaMini-Flan-T5-783M
Used for:
- Concept Explanation
- Simple educational explanations

## Technology Stack

- Python
- FastAPI
- HTML
- CSS
- JavaScript
- Google Gemini API
- Hugging Face Transformers
- PyTorch

## How to Run Locally

1. Clone the repository.
2. Install the required dependencies.
3. Create a `.env` file.
4. Add your Gemini API key.
5. Run the FastAPI server.

```bash
uvicorn main:app --reload
