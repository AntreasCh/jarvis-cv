from typing import Optional
import requests

from .config import settings


def generate_response(prompt: str, system: Optional[str] = None, temperature: float = 0.4, max_tokens: int = 200) -> str:
    base_url = settings.ollama_base_url.rstrip("/")
    model = settings.ollama_model
    url = f"{base_url}/api/generate"

    full_prompt = prompt if system is None else f"<|system|>\n{system}\n<|user|>\n{prompt}"

    payload = {
        "model": model,
        "prompt": full_prompt,
        "options": {
            "temperature": temperature,
            "num_predict": max_tokens,
            "top_p": 0.9,
            "repeat_penalty": 1.1,
            "stop": ["\n\n", "User:", "Human:"],
        },
        "stream": False,
    }

    try:
        resp = requests.post(url, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        text = data.get("response") or data.get("message") or ""
        if not text:
            text = "I could not generate a response just now."
        return text.strip()
    except Exception:
        return (
            "[local-fallback] I am online, but the local LLM endpoint is not responding. "
            "Please ensure Ollama is running and the model is available."
        )
