import tempfile
import wave
from typing import Optional

import numpy as np
import sounddevice as sd

from .config import settings


class STT:
    def __init__(self) -> None:
        self._model = None
        self.sample_rate = 16000
        self.chunk_duration = 0.1  # 100ms chunks for VAD

    def _ensure_model(self) -> None:
        if self._model is None:
            try:
                from faster_whisper import WhisperModel  # type: ignore
            except Exception as exc:  # pragma: no cover
                raise RuntimeError(
                    "faster-whisper is not installed. Install requirements or use --text mode."
                ) from exc
            # Default to int8 for CPU speed; users can tweak later
            self._model = WhisperModel(settings.whisper_model, compute_type="int8")

    def _save_audio_to_file(self, audio_data: np.ndarray) -> str:
        """Save audio data to a temporary WAV file."""
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
            with wave.open(tmp_file.name, 'wb') as wav_file:
                wav_file.setnchannels(1)  # Mono
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(self.sample_rate)
                # Convert float32 to int16
                audio_int16 = (audio_data * 32767).astype(np.int16)
                wav_file.writeframes(audio_int16.tobytes())
            return tmp_file.name

    def transcribe_file(self, wav_path: str) -> str:
        self._ensure_model()
        assert self._model is not None
        segments, _info = self._model.transcribe(wav_path)
        text_parts = [seg.text for seg in segments]
        return " ".join(text_parts).strip()

    def transcribe_buffer(self, audio: np.ndarray, sample_rate: int) -> str:
        """Transcribe audio buffer directly."""
        self._ensure_model()
        assert self._model is not None
        
        # Resample if needed
        if sample_rate != self.sample_rate:
            # Simple resampling - in production you'd use librosa or scipy
            ratio = self.sample_rate / sample_rate
            new_length = int(len(audio) * ratio)
            audio = np.interp(np.linspace(0, len(audio), new_length), 
                            np.arange(len(audio)), audio)
        
        # Save to temp file and transcribe
        temp_file = self._save_audio_to_file(audio)
        try:
            return self.transcribe_file(temp_file)
        finally:
            import os
            try:
                os.unlink(temp_file)
            except OSError:
                pass

    def record_audio(self, duration: float = 5.0) -> np.ndarray:
        """Record audio for specified duration."""
        print(f"Recording for {duration} seconds...")
        audio = sd.rec(int(duration * self.sample_rate), 
                      samplerate=self.sample_rate, 
                      channels=1, 
                      dtype=np.float32)
        sd.wait()  # Wait until recording is finished
        return audio.flatten()

    def record_with_vad(self, max_duration: float = 10.0, silence_threshold: float = 0.01) -> np.ndarray:
        """Record audio with Voice Activity Detection."""
        if not settings.use_vad:
            return self.record_audio(max_duration)
        
        try:
            import webrtcvad
            vad = webrtcvad.Vad(2)  # Aggressiveness level 0-3
        except ImportError:
            print("webrtcvad not available, falling back to timed recording")
            return self.record_audio(max_duration)
        
        print("Recording with VAD (speak now, silence to stop)...")
        chunk_size = int(self.sample_rate * self.chunk_duration)
        audio_chunks = []
        silence_count = 0
        max_silence_chunks = int(2.0 / self.chunk_duration)  # 2 seconds of silence
        
        def audio_callback(indata, frames, time, status):
            if status:
                print(f"Audio callback status: {status}")
            audio_chunks.append(indata.copy())
        
        with sd.InputStream(samplerate=self.sample_rate, 
                          channels=1, 
                          dtype=np.float32,
                          blocksize=chunk_size,
                          callback=audio_callback):
            for _ in range(int(max_duration / self.chunk_duration)):
                sd.sleep(int(self.chunk_duration * 1000))
                
                if len(audio_chunks) > 0:
                    # Convert to int16 for VAD
                    chunk = audio_chunks[-1].flatten()
                    chunk_int16 = (chunk * 32767).astype(np.int16)
                    
                    # Check for voice activity
                    try:
                        is_speech = vad.is_speech(chunk_int16.tobytes(), self.sample_rate)
                        if is_speech:
                            silence_count = 0
                        else:
                            silence_count += 1
                            
                        if silence_count >= max_silence_chunks:
                            print("Silence detected, stopping recording...")
                            break
                    except Exception:
                        # VAD failed, continue recording
                        pass
        
        if audio_chunks:
            return np.concatenate(audio_chunks).flatten()
        else:
            return np.array([], dtype=np.float32)
