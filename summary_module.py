import os
from dotenv import load_dotenv
from gemini_helper import generate_with_gemini

load_dotenv()

def summarize_text(text: str) -> str:
    """Summarizes educational passages or long text into concise, simple language."""
    try:
        api_key = os.getenv("GEMINI_API_KEY", "").strip()
        if not api_key or api_key == "your_gemini_api_key_here":
            return "⚠️ GEMINI_API_KEY is not configured. Please add your key to the .env file."

        prompt = f"Summarize the following text in simple language:\n\n{text}"
        return generate_with_gemini(prompt)
    except Exception as e:
        return f"⚠️ Error in Summary: {e}"

if __name__ == "__main__":
    sample = "The Industrial Revolution began in the late 18th century in Great Britain and gradually spread across the world..."
    print("Testing summary module...")
    print(summarize_text(sample))
