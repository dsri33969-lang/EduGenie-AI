import os
import re
import json
from dotenv import load_dotenv
from gemini_helper import generate_with_gemini

load_dotenv()

def clean_json_block(text: str) -> str:
    """Removes Markdown ```json code fences if present."""
    cleaned = re.sub(r"```(?:json)?\n?(.*?)```", r"\1", text, flags=re.DOTALL).strip()
    match = re.search(r"(\[.*\])", cleaned, flags=re.DOTALL)
    if match:
        return match.group(1).strip()
    return cleaned

def generate_quiz(text: str, num_questions: int = 10) -> list:
    """
    Generates multiple-choice questions (MCQs) with 4 options and correct answers
    from a given topic or passage using Gemini. Defaults to 10 questions.
    """
    try:
        api_key = os.getenv("GEMINI_API_KEY", "").strip()
        if not api_key or api_key == "your_gemini_api_key_here":
            return [{"error": "⚠️ GEMINI_API_KEY is not configured in .env."}]

        # Ensure valid integer range between 1 and 20
        count = max(1, min(int(num_questions), 20))

        prompt = f"""You are a quiz generator.

From the following topic or passage, create exactly {count} multiple-choice questions. Each question should include:
- A "question"
- A list of 4 "options"
- A correct "answer" that must exactly match one of the options.

Format your output as **valid JSON** array with no surrounding text, like this:
[
  {{
    "question": "What is ...?",
    "options": ["A", "B", "C", "D"],
    "answer": "A"
  }}
]

Topic or Passage:
{text}"""

        quiz_text = generate_with_gemini(prompt)
        cleaned_text = clean_json_block(quiz_text)
        quiz_data = json.loads(cleaned_text)
        return quiz_data

    except Exception as e:
        return [{"error": f"⚠️ Error in Quiz: {str(e)}"}]

if __name__ == "__main__":
    import sys, io
    if sys.platform == "win32":
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    print("Testing quiz generator for 'The Solar System' (10 questions)...")
    res = generate_quiz("The Solar System", num_questions=10)
    print(f"Generated {len(res)} questions:")
    for i, q in enumerate(res, 1):
        if "question" in q:
            print(f"  {i}. {q['question']} (Answer: {q.get('answer')})")
        else:
            print("  Error:", q)
