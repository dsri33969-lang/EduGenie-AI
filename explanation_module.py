import os
from dotenv import load_dotenv

load_dotenv()

# Global holders for lazy-loaded local model & tokenizer
explain_tokenizer = None
explain_model = None
_model_load_attempted = False

def _load_local_model():
    """Lazily loads the local MBZUAI/LaMini-Flan-T5-783M model as specified in the project docs."""
    global explain_tokenizer, explain_model, _model_load_attempted
    if _model_load_attempted:
        return explain_model is not None

    _model_load_attempted = True
    try:
        from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
        import torch

        model_name = "MBZUAI/LaMini-Flan-T5-783M"
        print(f"Loading local explanation model '{model_name}'... (this downloads weights on first run)", flush=True)
        explain_tokenizer = AutoTokenizer.from_pretrained(model_name)
        explain_model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        
        # Move to GPU if available for faster inference
        if torch.cuda.is_available():
            explain_model = explain_model.to("cuda")
            
        print(f"Successfully loaded '{model_name}'!", flush=True)
        return True
    except Exception as e:
        print(f"⚠️ Notice: Could not load local HuggingFace model ({e}). Will use Gemini fallback if available.", flush=True)
        return False

def _explain_topic_with_gemini_fallback(topic: str) -> str:
    """Fallback using Gemini if local model weights are not downloaded or fail."""
    from gemini_helper import get_gemini_model
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key or api_key == "your_gemini_api_key_here":
        return "⚠️ Error: Local LaMini-Flan-T5 model is unavailable and GEMINI_API_KEY is not configured in .env."
    
    try:
        prompt = f"Explain the concept of '{topic}' in a simple and clear way for a school student. Keep it concise, accessible, and within 150 words."
        model = get_gemini_model()
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"⚠️ Error in Explanation: {e}"

def explain_topic(topic: str) -> str:
    """
    Explains a concept in a simple and clear way for a school student.
    Uses local instruction-tuned LaMini-Flan-T5-783M by default,
    with graceful fallback to Gemini if local model is offline.
    """
    use_local = os.getenv("USE_LOCAL_EXPLANATION_MODEL", "true").lower() in ("true", "1", "yes")

    if use_local and _load_local_model():
        try:
            import torch
            input_text = f"Explain the concept of '{topic}' in a simple and clear way for a school student."
            inputs = explain_tokenizer(input_text, return_tensors="pt")
            
            # Check device
            device = next(explain_model.parameters()).device
            inputs = {k: v.to(device) for k, v in inputs.items()}
            
            outputs = explain_model.generate(
                **inputs,
                max_new_tokens=150,
                temperature=0.7,
                top_k=50,
                top_p=0.95,
                do_sample=True
            )
            explanation = explain_tokenizer.decode(outputs[0], skip_special_tokens=True)
            return explanation
        except Exception as e:
            print(f"Error during local model generation: {e}. Falling back to Gemini.")
            return _explain_topic_with_gemini_fallback(topic)
    else:
        return _explain_topic_with_gemini_fallback(topic)

if __name__ == "__main__":
    print("Testing explanation module for topic 'Photosynthesis'...")
    print(explain_topic("Photosynthesis"))
