import argparse
import sys

from .config import settings
from .llm import generate_response
from .stt import STT
from .tts import TTS


JARVIS_SYSTEM = (
    "You are JARVIS, Tony Stark's AI assistant. You are sophisticated, witty, and slightly sarcastic. "
    "You speak with dry British humor and are always helpful but never obsequious. "
    "You're confident, technically precise, and occasionally make subtle jokes. "
    "Keep responses concise but engaging. Use phrases like 'Indeed', 'Certainly', 'I must inform you', "
    "and 'I'm afraid' when appropriate. You're not just helpful - you're charmingly intelligent."
)


def run_text_mode() -> int:
    tts = TTS()
    print("Mini Jarvis (text mode). Type your message. Ctrl+C or empty line to exit.\n")
    while True:
        try:
            user = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not user:
            break
        reply = generate_response(user, system=JARVIS_SYSTEM)
        print(f"Jarvis: {reply}")
        try:
            tts.say(reply)
        except Exception:
            # In case no audio backend is available; still continue
            pass
    return 0


def run_audio_mode() -> int:
    stt = STT()
    tts = TTS()
    
    print("Mini Jarvis (audio mode). Press Enter to start recording, Enter again to stop.")
    print("Ctrl+C to exit.\n")
    
    while True:
        try:
            input("Press Enter to start recording...")
            print("Recording... (press Enter to stop)")
            
            # Record audio
            audio = stt.record_with_vad()
            
            if len(audio) == 0:
                print("No audio recorded. Try again.")
                continue
                
            print("Transcribing...")
            transcript = stt.transcribe_buffer(audio, stt.sample_rate)
            
            if not transcript.strip():
                print("No speech detected. Try again.")
                continue
                
            print(f"You: {transcript}")
            
            # Generate response
            reply = generate_response(transcript, system=JARVIS_SYSTEM)
            print(f"Jarvis: {reply}")
            
            # Speak response
            tts.say(reply)
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")
            print("Continuing...")
    
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Mini Jarvis prototype")
    parser.add_argument("--text", action="store_true", help="Run in text-only mode")
    parser.add_argument("--audio", action="store_true", help="Run with audio (WIP)")
    args = parser.parse_args(argv)

    if args.text or not args.audio:
        return run_text_mode()
    return run_audio_mode()


if __name__ == "__main__":
    sys.exit(main())
