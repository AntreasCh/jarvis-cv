import asyncio
import os
import subprocess
import tempfile
import threading
import time
from typing import Optional

from .config import settings


class TTS:
    def __init__(self) -> None:
        self._festival_available = None
        self._edge_tts_available = None
        self._pyttsx3_engine = None
        self._lock = threading.Lock()
        # Use a male British voice that sounds more like Jarvis
        self._edge_voice = "en-GB-RyanNeural"  # Male British voice - good quality and speed

    def _check_festival(self) -> bool:
        if self._festival_available is None:
            try:
                # Check if festival is available
                result = subprocess.run(['which', 'festival'], capture_output=True, text=True)
                self._festival_available = result.returncode == 0
            except Exception:
                self._festival_available = False
        return self._festival_available

    def _check_edge_tts(self) -> bool:
        if self._edge_tts_available is None:
            try:
                import edge_tts
                import pygame
                pygame.mixer.init()
                self._edge_tts_available = True
            except Exception:
                self._edge_tts_available = False
        return self._edge_tts_available

    def _get_pyttsx3_engine(self) -> Optional[object]:
        if self._pyttsx3_engine is None:
            try:
                import pyttsx3  # type: ignore
                engine = pyttsx3.init()
                
                # Try to find a male voice
                voices = engine.getProperty('voices')
                if voices:
                    # Look for male voices first - prioritize British Received Pronunciation
                    male_voice = None
                    for voice in voices:
                        if 'received pronunciation' in voice.name.lower():
                            male_voice = voice
                            break
                    
                    # If no RP voice, try other British male voices
                    if not male_voice:
                        for voice in voices:
                            if any(indicator in voice.name.lower() for indicator in ['great britain', 'en-gb', 'lancaster', 'west midlands']):
                                male_voice = voice
                                break
                    
                    # If still no male voice found, try other indicators
                    if not male_voice:
                        for voice in voices:
                            if any(indicator in voice.name.lower() for indicator in ['david', 'alex', 'daniel', 'male', 'man']):
                                male_voice = voice
                                break
                    
                    if male_voice:
                        engine.setProperty('voice', male_voice.id)
                
                # Jarvis-like settings: slower, more deliberate, deeper male voice
                engine.setProperty("rate", 140)  # Slower, more deliberate
                engine.setProperty("volume", 0.95)  # Good volume
                engine.setProperty("pitch", 0.5)  # Much lower pitch for deep male voice
                
                self._pyttsx3_engine = engine
            except Exception:
                self._pyttsx3_engine = False  # Mark as failed to avoid retrying
        return self._pyttsx3_engine if self._pyttsx3_engine is not False else None

    def _preprocess_text(self, text: str) -> str:
        """Preprocess text to sound more like Jarvis."""
        # Clean up text for better TTS
        text = text.replace("...", ".")  # Remove excessive dots
        text = text.replace("  ", " ")  # Remove double spaces
        
        # Add Jarvis-style prefixes for certain responses
        if text.startswith("I'm") or text.startswith("I am"):
            text = "Indeed, " + text.lower()
        elif text.startswith("Yes") or text.startswith("No"):
            text = "Certainly, " + text.lower()
        elif "error" in text.lower() or "problem" in text.lower():
            text = "I must inform you, " + text.lower()
            
        return text

    def say(self, text: str) -> None:
        if not text:
            return
        
        # Preprocess text for Jarvis-like delivery
        processed_text = self._preprocess_text(text)
        
        with self._lock:
            # Add a minimal delay before speaking (Jarvis thinking)
            time.sleep(0.1)
            
            # Try Edge TTS first (fastest and good quality)
            if self._check_edge_tts():
                self._say_with_edge_tts(processed_text)
            elif self._check_festival():
                self._say_with_festival(processed_text)
            else:
                # Fallback to pyttsx3
                engine = self._get_pyttsx3_engine()
                if engine is not None:
                    try:
                        engine.say(processed_text)
                        engine.runAndWait()
                    except Exception:
                        # Ignore cleanup errors
                        pass

    def _say_with_edge_tts(self, text: str) -> None:
        """Use Microsoft Edge TTS for much better voice quality."""
        try:
            import edge_tts
            import pygame
            
            # Create temporary file for audio
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_file:
                # Run the async function in a new event loop
                asyncio.run(self._generate_speech(text, tmp_file.name))
                
                # Play the audio
                pygame.mixer.music.load(tmp_file.name)
                pygame.mixer.music.play()
                
                # Wait for playback to finish
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)
                
                # Clean up
                os.unlink(tmp_file.name)
                
        except Exception as e:
            print(f"Edge TTS failed: {e}, falling back to pyttsx3")
            # Fallback to pyttsx3
            engine = self._get_pyttsx3_engine()
            if engine is not None:
                try:
                    engine.say(text)
                    engine.runAndWait()
                except Exception:
                    pass

    def _say_with_festival(self, text: str) -> None:
        """Use Festival TTS for better voice quality with optimizations."""
        try:
            # Use festival with optimized settings for faster response
            # Use a more direct approach with less overhead
            cmd = ['festival', '--tts']
            process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            process.stdin.write(text.encode())
            process.stdin.close()
            
            # Don't wait for completion - let it run in background for better responsiveness
            # The audio will play while we continue
            process.wait()
            
        except Exception as e:
            print(f"Festival failed: {e}, falling back to Edge TTS")
            # Fallback to Edge TTS
            self._say_with_edge_tts(text)

    async def _generate_speech(self, text: str, output_file: str) -> None:
        """Generate speech using edge-tts."""
        import edge_tts
        
        # Use a male British voice with Jarvis-like characteristics
        communicate = edge_tts.Communicate(text, self._edge_voice)
        await communicate.save(output_file)
