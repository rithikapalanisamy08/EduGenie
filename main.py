
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from html import escape
import json

from qna import ask_question
from explanation_module import explain_concept
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import generate_learning_path


app = FastAPI(title="EduGenie - AI Learning Companion")

app.mount("/static", StaticFiles(directory="static"), name="static")


def safe_text(value):
    """Safely display text inside HTML."""
    return escape(str(value))


def error_html(title, message):
    return f"""
    <div class="result-content error">
        <h3>{safe_text(title)}</h3>
        <p>{safe_text(message)}</p>
    </div>
    """


@app.get("/", response_class=HTMLResponse)
async def home():
    return FileResponse("templates/index.html")


@app.post("/ask", response_class=HTMLResponse)
async def ask(question: str = Form(...)):
    question = question.strip()

    if not question:
        return error_html(
            "Input Required",
            "Please enter your question."
        )

    try:
        answer = ask_question(question)

        if isinstance(answer, dict) and "error" in answer:
            return error_html("Answer Error", answer["error"])

        return f"""
        <div class="result-content">
            <h3>EduGenie Answer</h3>
            <p><strong>Question:</strong> {safe_text(question)}</p>
            <div class="answer-box">{safe_text(answer)}</div>
        </div>
        """

    except Exception:
        return error_html(
            "Answer Error",
            "Unable to answer right now. Please try again."
        )


@app.post("/explain", response_class=HTMLResponse)
async def explain(topic: str = Form(...)):
    topic = topic.strip()

    if not topic:
        return error_html(
            "Input Required",
            "Please enter a concept to explain."
        )

    try:
        explanation = explain_concept(topic)

        if isinstance(explanation, dict) and "error" in explanation:
            return error_html("Explanation Error", explanation["error"])

        return f"""
        <div class="result-content">
            <h3>Concept Explanation</h3>
            <p><strong>Concept:</strong> {safe_text(topic)}</p>
            <div class="answer-box">{safe_text(explanation)}</div>
        </div>
        """

    except Exception:
        return error_html(
            "Explanation Error",
            "Unable to explain this topic right now. Please try again."
        )


@app.post("/quiz", response_class=HTMLResponse)
async def quiz(passage: str = Form(...)):
    passage = passage.strip()

    if not passage:
        return error_html(
            "Input Required",
            "Please enter a topic or passage to generate a quiz."
        )

    try:
        quiz_result = generate_quiz(passage)

        if isinstance(quiz_result, dict) and "error" in quiz_result:
            return error_html(
                "Quiz Generation Error",
                quiz_result["error"]
            )

        if not isinstance(quiz_result, list) or not quiz_result:
            return error_html(
                "Quiz Unavailable",
                "No questions were generated. Please try again."
            )

        quiz_id = "edugenie-quiz"

        quiz_html = ""

        for index, question in enumerate(quiz_result, start=1):
            if not isinstance(question, dict):
                return error_html(
                    "Quiz Format Error",
                    "The AI returned an invalid question format."
                )

            options = question.get("options", {})
            correct_answer = question.get("correct_answer", "")
            question_text = question.get("question", "")

            if (
                not isinstance(options, dict)
                or any(key not in options for key in ["A", "B", "C", "D"])
                or correct_answer not in ["A", "B", "C", "D"]
                or not question_text
            ):
                return error_html(
                    "Quiz Format Error",
                    "The AI returned an incomplete question. Please try again."
                )

            quiz_html += f"""
            <div class="quiz-question"
                 style="padding:15px;margin:15px 0;
                        border:1px solid #ddd;border-radius:10px;">

                <h3>Question {index}</h3>

                <p><strong>{safe_text(question_text)}</strong></p>

                <div class="quiz-options">
            """

            for key in ["A", "B", "C", "D"]:
                quiz_html += f"""
                    <label style="display:block;padding:6px;">
                        <input type="radio"
                               name="answer_{index}"
                               value="{key}">
                        {key}. {safe_text(options[key])}
                    </label>
                """

            quiz_html += f"""
                </div>
                <p class="quiz-feedback"
                   data-correct="{correct_answer}"
                   hidden></p>
            </div>
            """

        return f"""
        <div class="result-content" id="{quiz_id}">
            <h3>Generated Quiz</h3>

            <p><strong>Topic / Input:</strong> {safe_text(passage)}</p>

            {quiz_html}

            <button type="button"
                    onclick="submitEduGenieQuiz()">
                Submit Answers
            </button>

            <h3 id="edugenie-quiz-score" aria-live="polite"></h3>
        </div>

        <script>
        function submitEduGenieQuiz() {{
            const container = document.getElementById("{quiz_id}");
            const questions = container.querySelectorAll(".quiz-question");

            let score = 0;
            let unanswered = 0;

            questions.forEach((question) => {{
                const selected = question.querySelector(
                    'input[type="radio"]:checked'
                );
                const feedback = question.querySelector(".quiz-feedback");
                const correct = feedback.dataset.correct;

                feedback.hidden = false;

                if (!selected) {{
                    unanswered++;
                    feedback.textContent =
                        "Not answered. Correct answer: " + correct;
                }} else if (selected.value === correct) {{
                    score++;
                    feedback.textContent = "Correct!";
                }} else {{
                    feedback.textContent =
                        "Incorrect. Correct answer: " + correct;
                }}
            }});

            const scoreElement = document.getElementById(
                "edugenie-quiz-score"
            );

            scoreElement.textContent =
                "Your Score: " + score + " / " + questions.length +
                (unanswered > 0
                    ? " | Unanswered: " + unanswered
                    : "");
        }}
        </script>
        """

    except Exception:
        return error_html(
            "Quiz Error",
            "Unable to generate the quiz right now. Please try again."
        )


@app.post("/summary", response_class=HTMLResponse)
async def summary(text: str = Form(...)):
    text = text.strip()

    if not text:
        return error_html(
            "Input Required",
            "Please enter text to summarize."
        )

    try:
        summary_result = summarize_text(text)

        if isinstance(summary_result, dict) and "error" in summary_result:
            return error_html("Summary Error", summary_result["error"])

        return f"""
        <div class="result-content">
            <h3>Summary</h3>
            <div class="answer-box">{safe_text(summary_result)}</div>
        </div>
        """

    except Exception:
        return error_html(
            "Summary Error",
            "Unable to summarize the text right now. Please try again."
        )


@app.post("/learning-path", response_class=HTMLResponse)
async def learning_path(
    topic: str = Form(...),
    level: str = Form(...)
):
    topic = topic.strip()
    level = level.strip()

    if not topic or not level:
        return error_html(
            "Input Required",
            "Please enter a topic and select your learning level."
        )

    try:
        learning_result = generate_learning_path(topic, level)

        if isinstance(learning_result, dict) and "error" in learning_result:
            return error_html(
                "Learning Path Error",
                learning_result["error"]
            )

        return f"""
        <div class="result-content">
            <h3>Personalized Learning Path</h3>

            <p><strong>Topic:</strong> {safe_text(topic)}</p>
            <p><strong>Learner Level:</strong> {safe_text(level)}</p>

            <div class="answer-box">{safe_text(learning_result)}</div>
        </div>
        """

    except Exception:
        return error_html(
            "Learning Path Error",
            "Unable to create a learning path right now. Please try again."
        )


@app.get("/health")
async def health_check():
    return {
        "status": "running",
        "app": "EduGenie"
    }
