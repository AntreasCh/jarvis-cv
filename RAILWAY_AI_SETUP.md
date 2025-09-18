# Railway AI-Enabled JARVIS CV

This version includes real AI capabilities and voice features for Railway deployment.

## Features

✅ **Real AI Responses** - Uses OpenAI API (with intelligent fallback)  
✅ **Voice Interface** - Voice recording and response capabilities  
✅ **Interactive CV** - Full CV with clickable elements  
✅ **Mobile-Friendly** - Responsive design  
✅ **PWA Features** - Installable web app  

## Setup

### 1. Environment Variables

Add these to your Railway project:

```
OPENAI_API_KEY=your_openai_api_key_here
```

**Note:** If you don't provide an OpenAI API key, the system will use an intelligent fallback that still provides good responses.

### 2. Deploy

The app will automatically deploy when you push to GitHub. Railway will:

1. Install dependencies from `requirements.txt`
2. Run `web_app_railway_ai.py` as specified in `Procfile`
3. Make the app available at your Railway URL

## How It Works

### AI Responses
- **With OpenAI API**: Uses GPT-3.5-turbo for intelligent, contextual responses
- **Without API Key**: Uses intelligent keyword matching with JARVIS personality

### Voice Features
- **Voice Recording**: Browser-based audio capture
- **Voice Responses**: Placeholder for TTS (can be extended with real TTS APIs)
- **Real-time Communication**: WebSocket support

### CV Data
- Complete CV information embedded in the AI system
- Contextual responses based on Andreas's experience
- Interactive skill tags and project details

## Testing

1. Visit your Railway URL
2. Try asking JARVIS questions like:
   - "Should I hire Andreas?"
   - "Tell me about his Elasticsearch experience"
   - "What projects has he worked on?"
   - "What are his technical strengths?"

## Extending Voice Features

To add real TTS/STT:

1. **TTS**: Integrate with Edge TTS, ElevenLabs, or Azure Speech
2. **STT**: Integrate with OpenAI Whisper, Azure Speech, or Google Speech
3. **Real-time Audio**: Use WebRTC for live audio streaming

## Local Development

To run locally with full features:

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export OPENAI_API_KEY=your_key_here

# Run the app
python web_app_railway_ai.py
```

## Differences from Local Version

| Feature | Local | Railway |
|---------|-------|---------|
| AI | Ollama LLM | OpenAI API + Fallback |
| TTS | edge-tts | Placeholder |
| STT | faster-whisper | Placeholder |
| Voice Recording | Full | Browser-based |
| Dependencies | Heavy | Lightweight |

The Railway version maintains the same user experience while being optimized for cloud deployment.
