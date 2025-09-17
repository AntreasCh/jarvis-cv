import os
from dataclasses import dataclass


@dataclass
class Settings:
    whisper_model: str = os.getenv("WHISPER_MODEL", "small")
    use_vad: bool = os.getenv("USE_VAD", "true").lower() == "true"
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3.1:8b")
    voice_rate: int = int(os.getenv("VOICE_RATE", "180"))
    voice_volume: float = float(os.getenv("VOICE_VOLUME", "1.0"))


settings = Settings()
