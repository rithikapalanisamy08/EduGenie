from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from qna import ask_question
from explanation_module import explain_concept
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import generate_learning_path

app = FastAPI(title="EduGenie")

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def home():
    return FileResponse("templates/index.html")


@app.post("/ask", response_class=HTMLResponse)
async def ask(question: str = Form(...)):
    answer = ask_question(question)

    return f"""
    <div class="result-content">
        <h3>EduGenie Answer</h3>
        <p><strong>Question:</strong> {question}</p>
        <div class="answer-box">
            {answer}
        </div>
    </div>
    """


@app.post("/explain", response_class=HTMLResponse)
async def explain(topic: str = Form(...)):
    explanation = explain_concept(topic)

    return f"""
    <div class="result-content">
        <h3>Concept Explanation</h3>
        <p><strong>Concept:</strong> {topic}</p>
        <div class="answer-box">
            {explanation}
        </div>
    </div>
    """


@app.post("/quiz", response_class=HTMLResponse)
async def quiz(passage: str = Form(...)):
    quiz_result = generate_quiz(passage)

    if isinstance(quiz_result, dict) and "error" in quiz_result:
        return f"""
        <div class="result-content error">
            <h3>Quiz Error</h3>
            <p>{quiz_result["error"]}</p>
        </div>
        """

    quiz_html = ""

    for index, question in enumerate(quiz_result, start=1):
        options = question["options"]

        quiz_html += f"""
        <div class="quiz-question">
            <h3>Question {index}</h3>

            <p><strong>{question["question"]}</strong></p>

            <p>A. {options["A"]}</p>
            <p>B. {options["B"]}</p>
            <p>C. {options["C"]}</p>
            <p>D. {options["D"]}</p>

            <p>
                <strong>Correct Answer:</strong>
                {question["correct_answer"]}
            </p>
        </div>
        """

    return f"""
    <div class="result-content">
        <h3>Generated Quiz</h3>
        {quiz_html}
    </div>
    """


@app.post("/summary", response_class=HTMLResponse)
async def summary(text: str = Form(...)):
    summary_result = summarize_text(text)

    return f"""
    <div class="result-content">
        <h3>Summary</h3>

        <div class="answer-box">
            {summary_result}
        </div>
    </div>
    """


@app.post("/learning-path", response_class=HTMLResponse)
async def learning_path(
    topic: str = Form(...),
    level: str = Form(...)
):
    learning_result = generate_learning_path(topic, level)

    return f"""
    <div class="result-content">
        <h3>Personalized Learning Path</h3>

        <p><strong>Topic:</strong> {topic}</p>
        <p><strong>Learner Level:</strong> {level}</p>

        <div class="answer-box">
            {learning_result}
        </div>
    </div>
    """


@app.get("/health")
async def health_check():
    return {
        "status": "running",
        "app": "EduGenie"
    }
