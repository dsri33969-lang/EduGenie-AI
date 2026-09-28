from fastapi import FastAPI, Query, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import os

from qna import answer_question_with_gemini
from explanation_module import explain_topic
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations

app = FastAPI(title="EduGenie: Google Gemini Powered Learning Assistant")

# Enable CORS for broad compatibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure static and templates folders exist
os.makedirs("static", exist_ok=True)
os.makedirs("templates", exist_ok=True)

# Mount static files and setup Jinja2 templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Renders the main EduGenie web interface."""
    return templates.TemplateResponse(request=request, name="index.html")

# Q&A - GET API using Gemini
@app.get("/qa")
async def answer_question(question: str = Query(...)):
    """GET endpoint to answer questions via Gemini."""
    answer = answer_question_with_gemini(question)
    return {"answer": answer}

# Explanation - POST API
@app.post("/explain")
async def explain_api(request: Request):
    """POST endpoint to explain concepts simply for students."""
    data = await request.json()
    topic = data.get("topic")
    if not topic:
        return JSONResponse(content={"error": "Please provide a topic."}, status_code=400)
    explanation = explain_topic(topic)
    return {"topic": topic, "explanation": explanation}

# Summarization - POST API
@app.post("/summarize")
async def summarize_api(request: Request):
    """POST endpoint to summarize paragraphs into concise text."""
    data = await request.json()
    text = data.get("text")
    if not text:
        return JSONResponse(content={"error": "Please provide text to summarize."}, status_code=400)
    summary = summarize_text(text)
    return {"summary": summary}

# Quiz Generation - POST API
@app.post("/quiz")
async def quiz_api(request: Request):
    """POST endpoint to generate MCQs with 4 options and answers."""
    data = await request.json()
    text = data.get("text")
    num_questions = data.get("num_questions", 10)
    if not text:
        return JSONResponse(content={"error": "Please provide text or topic for quiz."}, status_code=400)
    quiz = generate_quiz(text, num_questions=num_questions)
    print(f"Generated quiz: {len(quiz)} questions") # DEBUG
    return JSONResponse(content={"quiz": quiz})

# Learning Recommendations - GET API
@app.get("/learn/recommendations")
async def learning_recommendation_api(topic: str = Query(...)):
    """GET endpoint to suggest structured learning roadmaps."""
    recommendation = get_learning_recommendations(topic)
    return {"topic": topic, "recommendation": recommendation}

@app.get("/health")
async def health_check():
    """Health status endpoint."""
    return {"status": "ok", "app": "EduGenie"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
