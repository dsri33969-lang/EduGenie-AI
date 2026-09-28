import os
import traceback
from dotenv import load_dotenv
from gemini_helper import generate_with_gemini

load_dotenv()

def get_learning_recommendations(topic: str) -> str:
    """Generates structured, multi-level learning recommendations and roadmaps using Gemini."""
    prompt = f"""You are an AI tutor. The student wants to learn about: {topic}.
Suggest a structured and adaptive learning path including key topics, order of learning, and resources (books, courses, videos, tutorials).
Include beginner, intermediate, and advanced levels if needed."""

    try:
        api_key = os.getenv("GEMINI_API_KEY", "").strip()
        if not api_key or api_key == "your_gemini_api_key_here":
            return "⚠️ GEMINI_API_KEY is not configured. Please add your key to the .env file."

        return generate_with_gemini(prompt)

    except Exception as e:
        traceback.print_exc()
        return f"❌ Error occurred: {str(e)}"

if __name__ == "__main__":
    print("Testing learning path module for topic 'SQL'...")
    print(get_learning_recommendations("SQL")[:300] + "...")
