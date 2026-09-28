import os
from dotenv import load_dotenv
from gemini_helper import generate_with_gemini

load_dotenv()

def answer_question_with_gemini(question: str) -> str:
    """Answers general knowledge and academic questions using Google Gemini."""
    try:
        api_key = os.getenv("GEMINI_API_KEY", "").strip()
        if not api_key or api_key == "your_gemini_api_key_here":
            return "⚠️ GEMINI_API_KEY is not configured. Please add your key to the .env file."

        return generate_with_gemini(question)
    except Exception as e:
        return f"⚠️ Error in QnA: {e}"

if __name__ == "__main__":
    import sys, io
    if sys.platform == "win32":
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    test_q = "Which is the largest ocean?"
    print(f"Testing QnA with: '{test_q}'")
    print("Response:", answer_question_with_gemini(test_q))
