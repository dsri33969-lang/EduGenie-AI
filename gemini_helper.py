import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

_cached_model_list = None

def get_candidate_model_names() -> list:
    """Returns an ordered list of candidate text-generation Gemini models available for this API key."""
    global _cached_model_list
    if _cached_model_list:
        return _cached_model_list

    # If specified by user in .env
    custom_model = os.getenv("GEMINI_MODEL", "").strip()
    if custom_model:
        _cached_model_list = [custom_model]
        return _cached_model_list

    preferred_order = [
        "gemini-3.8-flash",
        "gemini-3.7-flash",
        "gemini-3.6-flash",
        "gemini-3.5-flash",
        "gemini-flash-latest",
        "gemini-pro-latest",
        "gemini-2.5-flash-lite",
        "gemini-2.5-flash",
        "gemini-1.5-pro",
        "gemini-1.5-flash"
    ]

    candidates = []
    try:
        # Filter for text models only
        available = [
            m.name for m in genai.list_models()
            if hasattr(m, 'supported_generation_methods')
            and 'generateContent' in m.supported_generation_methods
            and not any(x in m.name for x in ['-tts', '-image', '-transcribe', 'clip', 'lyria', 'robotics', 'computer-use', 'banana'])
        ]

        for pref in preferred_order:
            for avail in available:
                if pref in avail and avail not in candidates:
                    candidates.append(avail)

        for avail in available:
            if avail not in candidates:
                candidates.append(avail)

    except Exception as e:
        print(f"Notice: Could not list models ({e}). Using standard defaults.", flush=True)

    if not candidates:
        candidates = [
            "models/gemini-3.8-flash",
            "models/gemini-3.7-flash",
            "models/gemini-3.5-flash",
            "models/gemini-flash-latest"
        ]

    _cached_model_list = candidates
    return _cached_model_list

def get_gemini_model(model_name: str = None) -> genai.GenerativeModel:
    """Returns an initialized GenerativeModel."""
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key or api_key == "your_gemini_api_key_here":
        raise ValueError("GEMINI_API_KEY is not configured in .env file.")
    genai.configure(api_key=api_key)

    if model_name:
        return genai.GenerativeModel(model_name=model_name)

    candidates = get_candidate_model_names()
    return genai.GenerativeModel(model_name=candidates[0])

def generate_with_gemini(prompt: str) -> str:
    """
    Generates text content using Gemini with automatic failover across candidate models
    to handle 404 (model not found) and 429 (rate-limit / quota exhausted) transparently.
    """
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key or api_key == "your_gemini_api_key_here":
        raise ValueError("GEMINI_API_KEY is not configured in .env file.")
    genai.configure(api_key=api_key)

    candidates = get_candidate_model_names()
    last_error = None

    for model_name in candidates:
        try:
            model = genai.GenerativeModel(model_name=model_name)
            response = model.generate_content(prompt)
            if hasattr(response, "text") and response.text:
                return response.text.strip()
            elif hasattr(response, "parts") and response.parts:
                return response.parts[0].text.strip()
        except Exception as e:
            err_str = str(e)
            last_error = e
            # Failover to next candidate model if current model encounters 404, 429, or non-text part
            if any(k in err_str for k in ["404", "429", "ResourceExhausted", "NotFound", "inline_data", "unsupported"]):
                print(f"EduGenie: Trying failover from '{model_name}'...", flush=True)
                continue
            else:
                raise e

    if last_error:
        raise last_error
    raise RuntimeError("No working Gemini model could generate a response.")
