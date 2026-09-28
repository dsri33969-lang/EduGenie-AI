# 💡 EduGenie: Google Gemini Powered Learning Assistant

EduGenie is a lightweight AI-powered educational assistant designed to simplify learning through generative AI. Designed for students of all academic levels, EduGenie integrates cloud-based intelligence (Google Gemini) and optional local instruction-tuned models (LaMini-Flan-T5) with an intuitive web interface built on FastAPI, HTML5, and CSS3.

---

## 🚀 Key Features & Scenarios

1. **Ask EduGenie a Question (Q&A)**: Get smart, accurate, and concise answers to academic or general knowledge questions (e.g., *"Which is the largest ocean?"*).
2. **Need an Explanation? (Concept Breakdown)**: Understand complex concepts through simplified explanations tailored for school students (e.g., *"Photosynthesis"* or *"Quantum Computing"*).
3. **Summarize a Paragraph**: Condense lengthy academic passages into clear, digestible summaries for fast revision.
4. **Generate a Quiz**: Create 3 interactive Multiple-Choice Questions (MCQs) with 4 options from any topic or passage, complete with instant answer verification (✅ Correct / ❌ Incorrect).
5. **Personalized Learning Recommendations**: Generate a structured, multi-level roadmap (Beginner, Intermediate, Advanced) with timelines, key topics, and curated resources (books, tutorials, courses).

---

## 📁 Project Architecture & Folder Structure

```
EduGenie-AI/
├── .vscode/
│   ├── launch.json           # VS Code 1-click debug/run configuration
│   └── settings.json         # VS Code workspace settings
├── static/
│   └── style.css             # Responsive styling for cards, inputs & quiz UI
├── templates/
│   └── index.html            # Frontend HTML template with live interactive fetch
├── .env.example              # Template for environment configuration
├── .env                      # API keys & local model configuration (git-ignored)
├── .gitignore                # Git ignore rules for virtual environments & secrets
├── explanation_module.py     # Concept explanation logic (LaMini-Flan-T5 / Gemini)
├── learning_path.py          # Structured learning roadmaps (Gemini)
├── main.py                   # FastAPI server, static mounts & REST API routes
├── qna.py                    # Academic Q&A handler (Gemini)
├── quiz_module.py            # Quiz generation with JSON extraction (Gemini)
├── requirements.txt          # Python dependencies
├── summary_module.py         # Passage summarization (Gemini)
└── README.md                 # Documentation & setup guide
```

---

## 🛠️ Prerequisites

- **Python 3.10+** (Tested on Python 3.10, 3.11, 3.12, 3.14)
- **Google Gemini API Key**:
  1. Visit [Google AI Studio](https://aistudio.google.com/).
  2. Sign in with your Google account.
  3. Click **Get API key** -> **Create API key**.
  4. Copy the generated key.

---

## 💻 Installation & Setup Instructions

### 1. Clone or Open the Workspace in VS Code
Open VS Code, select **File > Open Folder...**, and choose `EduGenie-AI`.

### 2. Create and Activate a Virtual Environment (Recommended)

**On Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**On macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Required Dependencies
Run:
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
# Windows PowerShell
copy .env.example .env

# macOS / Linux
cp .env.example .env
```
Open `.env` and insert your Gemini API Key:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
USE_LOCAL_EXPLANATION_MODEL=true
```
> **Note**: Setting `USE_LOCAL_EXPLANATION_MODEL=true` will download the HuggingFace `MBZUAI/LaMini-Flan-T5-783M` model weights on first explanation request. If you prefer to use Gemini for explanations as well (faster without local download), set it to `false`.

---

## 🏃 Running the Application

### Option A: Via VS Code (1-Click Run)
1. In VS Code, press `Ctrl+Shift+D` (or click the Run & Debug icon on the sidebar).
2. Select **Run EduGenie (FastAPI)** from the dropdown.
3. Press **F5** or click the green Play button.

### Option B: Via Terminal / Command Line
From the project root directory, run:
```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Once started, open your web browser and navigate to:
👉 **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

## 🧪 Testing & Verification Guide

### 1. Web Interface Functional Testing
- **Ask a Question**: Type *"Which is the largest ocean?"* -> Click **Get Answer**.
- **Need an Explanation?**: Type *"Photosynthesis"* -> Click **Explain**.
- **Summarize a Paragraph**: Paste any long educational text -> Click **Summarize**.
- **Generate a Quiz**: Type *"Pythagoras theorem"* -> Click **Generate Quiz**.
  - Select one option for each question.
  - Click **Check Answer** under each question to verify interactive feedback (✅ Correct / ❌ Incorrect).
- **Learning Recommendations**: Type *"SQL"* or *"Machine Learning"* -> Click **Get Recommendations** to inspect the multi-level roadmap.

### 2. API Endpoints Testing (Swagger / OpenAPI)
FastAPI provides automated documentation out of the box. Open:
👉 **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

You can test individual endpoints directly:
| Endpoint | Method | Params / Payload | Description |
|---|---|---|---|
| `/qa` | `GET` | `?question=What is gravity?` | Question Answering |
| `/explain` | `POST` | `{"topic": "Quantum Computing"}` | Concept Explanation |
| `/summarize` | `POST` | `{"text": "Long text here..."}` | Passage Summarization |
| `/quiz` | `POST` | `{"text": "Solar System"}` | 3-MCQ Quiz Generation |
| `/learn/recommendations` | `GET` | `?topic=Python` | Adaptive Learning Path |
| `/health` | `GET` | None | Service Health Status |
