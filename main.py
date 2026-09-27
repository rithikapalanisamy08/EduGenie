from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from qna import ask_question
from explanation_module import explain_concept
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import generate_learning_path


app = FastAPI(title="EduGenie")


# --------------------------------------------------
# Static Files
# --------------------------------------------------

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


# --------------------------------------------------
# HTML Templates
# --------------------------------------------------

templates = Jinja2Templates(
    directory="templates"
)


# --------------------------------------------------
# Home Page
# --------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    template = templates.get_template("index.html")

    return HTMLResponse(
        template.render(request=request)
    )


# --------------------------------------------------
# Question & Answer
# --------------------------------------------------

@app.post("/ask", response_class=HTMLResponse)
async def ask(
    question: str = Form(...)
):

    answer = ask_question(question)

    return f"""
    <!DOCTYPE html>
    <html>

    <head>
        <title>EduGenie - Answer</title>
    </head>

    <body style="
        font-family: Arial;
        max-width: 800px;
        margin: 50px auto;
    ">

        <h1>EduGenie</h1>

        <h2>Your Question:</h2>

        <p>{question}</p>

        <h2>EduGenie Answer</h2>

        <div style="
            padding: 20px;
            background: #f2f2f2;
            white-space: pre-wrap;
        ">
            {answer}
        </div>

        <br>

        <a href="/">
            Back to EduGenie
        </a>

    </body>

    </html>
    """


# --------------------------------------------------
# Concept Explanation
# --------------------------------------------------

@app.post("/explain", response_class=HTMLResponse)
async def explain(
    topic: str = Form(...)
):

    explanation = explain_concept(topic)

    return f"""
    <!DOCTYPE html>
    <html>

    <head>
        <title>EduGenie - Concept Explanation</title>
    </head>

    <body style="
        font-family: Arial;
        max-width: 800px;
        margin: 50px auto;
    ">

        <h1>EduGenie</h1>

        <h2>Concept:</h2>

        <p>{topic}</p>

        <h2>Concept Explanation</h2>

        <div style="
            padding: 20px;
            background: #f2f2f2;
            white-space: pre-wrap;
        ">
            {explanation}
        </div>

        <br>

        <a href="/">
            Back to EduGenie
        </a>

    </body>

    </html>
    """


# --------------------------------------------------
# Quiz Generation
# --------------------------------------------------

@app.post("/quiz", response_class=HTMLResponse)
async def quiz(
    passage: str = Form(...)
):

    print(
        f"Quiz requested for passage length: {len(passage)}",
        flush=True
    )

    try:

        quiz_result = generate_quiz(passage)

        print(
            "Quiz response received.",
            flush=True
        )

    except Exception as e:

        print(
            f"Quiz Error: {e}",
            flush=True
        )

        quiz_result = {
            "error": str(e)
        }


    # Error handling

    if isinstance(quiz_result, dict) and "error" in quiz_result:

        quiz_html = f"""
        <div style="
            padding: 20px;
            background: #ffe6e6;
            border-radius: 10px;
            color: #b00020;
        ">

            <strong>Error:</strong>

            {quiz_result["error"]}

        </div>
        """

    else:

        quiz_html = ""

        for index, question in enumerate(
            quiz_result,
            start=1
        ):

            options = question["options"]

            quiz_html += f"""
            <div style="
                padding: 20px;
                margin-bottom: 20px;
                background: #f2f2f2;
                border-radius: 10px;
            ">

                <h3>
                    Question {index}
                </h3>

                <p>
                    <strong>
                        {question["question"]}
                    </strong>
                </p>

                <p>
                    A. {options["A"]}
                </p>

                <p>
                    B. {options["B"]}
                </p>

                <p>
                    C. {options["C"]}
                </p>

                <p>
                    D. {options["D"]}
                </p>

                <p>
                    <strong>
                        Correct Answer:
                    </strong>

                    {question["correct_answer"]}
                </p>

            </div>
            """


    return f"""
    <!DOCTYPE html>
    <html>

    <head>
        <title>EduGenie - Quiz</title>
    </head>

    <body style="
        font-family: Arial;
        max-width: 800px;
        margin: 50px auto;
    ">

        <h1>EduGenie</h1>

        <h2>Quiz Generated</h2>

        <h3>Based on your passage:</h3>

        <div style="
            padding: 15px;
            background: #eeeeee;
            border-radius: 10px;
            white-space: pre-wrap;
        ">
            {passage}
        </div>

        <br>

        {quiz_html}

        <br>

        <a href="/">
            Back to EduGenie
        </a>

    </body>

    </html>
    """


# --------------------------------------------------
# Summarization
# --------------------------------------------------

@app.post("/summary", response_class=HTMLResponse)
async def summary(
    text: str = Form(...)
):

    summary_result = summarize_text(text)

    return f"""
    <!DOCTYPE html>
    <html>

    <head>
        <title>EduGenie - Summary</title>
    </head>

    <body style="
        font-family: Arial;
        max-width: 800px;
        margin: 50px auto;
    ">

        <h1>EduGenie</h1>

        <h2>Summary</h2>

        <div style="
            padding: 20px;
            background: #f2f2f2;
            white-space: pre-wrap;
        ">
            {summary_result}
        </div>

        <br>

        <a href="/">
            Back to EduGenie
        </a>

    </body>

    </html>
    """


# --------------------------------------------------
# Learning Path
# --------------------------------------------------

@app.post("/learning-path", response_class=HTMLResponse)
async def learning_path(
    topic: str = Form(...),
    level: str = Form(...)
):

    print(
        f"Learning Path requested: {topic} - {level}",
        flush=True
    )

    try:

        print(
            "Calling Gemini for Learning Path...",
            flush=True
        )

        learning_result = generate_learning_path(
            topic,
            level
        )

        print(
            "Learning Path response received.",
            flush=True
        )

    except Exception as e:

        print(
            f"Learning Path Error: {e}",
            flush=True
        )

        learning_result = (
            f"Learning Path generation failed: {e}"
        )


    return f"""
    <!DOCTYPE html>
    <html>

    <head>
        <title>EduGenie - Learning Path</title>
    </head>

    <body style="
        font-family: Arial;
        max-width: 800px;
        margin: 50px auto;
    ">

        <h1>EduGenie</h1>

        <h2>Learning Path</h2>

        <p>
            <strong>Topic:</strong>
            {topic}
        </p>

        <p>
            <strong>Learner Level:</strong>
            {level}
        </p>

        <div style="
            padding: 20px;
            background: #f2f2f2;
            white-space: pre-wrap;
            border-radius: 10px;
        ">
            {learning_result}
        </div>

        <br>

        <a href="/">
            Back to EduGenie
        </a>

    </body>

    </html>
    """


# --------------------------------------------------
# Health Check
# --------------------------------------------------

@app.get("/health")
async def health_check():

    return {
        "status": "running",
        "app": "EduGenie"
    }