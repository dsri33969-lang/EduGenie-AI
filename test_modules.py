import sys
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import os
import json
from quiz_module import clean_json_block
from qna import answer_question_with_gemini
from summary_module import summarize_text
from learning_path import get_learning_recommendations
from explanation_module import explain_topic

def test_quiz_json_cleaning():
    raw_markdown = """```json
[
  {
    "question": "What is the capital of France?",
    "options": ["Paris", "London", "Berlin", "Madrid"],
    "answer": "Paris"
  }
]
```"""
    cleaned = clean_json_block(raw_markdown)
    parsed = json.loads(cleaned)
    assert len(parsed) == 1
    assert parsed[0]["answer"] == "Paris"
    print("[PASS] Quiz JSON cleaner handled markdown fences properly")

def test_quiz_ten_questions():
    from quiz_module import generate_quiz
    quiz = generate_quiz("Solar System", num_questions=10)
    assert isinstance(quiz, list)
    assert len(quiz) == 10
    assert "question" in quiz[0]
    assert len(quiz[0]["options"]) == 4
    print(f"[PASS] 10-Question Quiz generation verified: generated {len(quiz)} MCQs successfully")

def test_qna_and_modules():
    ans = answer_question_with_gemini("Which is the largest ocean?")
    assert len(ans) > 0
    print("[PASS] QnA live generation verified:", ans[:60], "...")

    summary = summarize_text("The water cycle describes how water evaporates, rises, condenses into clouds, and falls back to earth.")
    assert len(summary) > 0
    print("[PASS] Summary live generation verified:", summary[:60], "...")

    recs = get_learning_recommendations("SQL")
    assert len(recs) > 0
    print("[PASS] Learning recommendations live generation verified:", recs[:60], "...")

if __name__ == "__main__":
    print("Testing EduGenie module integration...")
    test_quiz_json_cleaning()
    test_quiz_ten_questions()
    print("All module integration tests passed successfully!")
