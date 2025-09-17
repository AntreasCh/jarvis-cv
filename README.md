# Andreas Christodoulou - Interactive CV with JARVIS

An interactive web-based CV featuring JARVIS, an AI assistant that can answer questions about Andreas's professional background, experience, and projects.

## 🌟 Features

- **Interactive Web Interface** - Modern, responsive design
- **AI-Powered JARVIS** - Answers questions about Andreas's experience
- **Voice & Text Input** - Multiple ways to interact
- **Professional Knowledge Base** - Detailed information about projects, skills, and achievements
- **Real-time Chat** - WebSocket-based communication
- **Local & Private** - Everything runs on your machine

## 🚀 Quick Start

### Option 1: Interactive CV (Recommended)
```bash
# Start the web-based interactive CV
./start_cv.sh
```
Then open http://localhost:5000 in your browser.

### Option 2: Command Line Interface
```bash
# Text mode
python -m app.main --text

# Audio mode (requires microphone)
python -m app.main --audio
```

## 📋 Setup

1) **Install Dependencies**
```bash
# Create virtual environment
python3 -m venv .venv && source .venv/bin/activate

# Install Python packages
pip install -r requirements.txt

# Install system dependencies (Arch Linux)
sudo pacman -S portaudio festival festival-english espeak-ng
```

2) **Install Ollama (for AI responses)**
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.1:8b
```

3) **Start the Interactive CV**
```bash
./start_cv.sh
```

## 🎯 What JARVIS Can Tell You About Andreas

- **Experience**: Current role as Software Developer, major achievements
- **Projects**: Elasticsearch optimization, SPC reporting system, Bulk Actions Manager
- **Skills**: Performance optimization, concurrency, Elasticsearch, Java, Node.js
- **Education**: BSc Computer Science from Northumbria University
- **Technical Details**: Specific implementations and technologies used

## 💬 Example Questions

- "Tell me about Andreas's experience with Elasticsearch"
- "What projects has he worked on?"
- "What are his strongest technical skills?"
- "Where did he study and what was his dissertation about?"
- "How did he reduce reindexing time from 10 hours to 40 minutes?"

## 🛠️ Technical Stack

- **Backend**: Flask, SocketIO, Ollama (Llama 3.1)
- **AI/ML**: faster-whisper (STT), Edge TTS (voice)
- **Frontend**: HTML5, CSS3, JavaScript, WebSocket
- **Data**: Structured CV knowledge base
- **Deployment**: Local development, ready for VPS deployment

## 🌐 Deployment

The web interface is ready for deployment to any VPS or cloud platform:

```bash
# Production deployment
gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:5000 web_app:app
```

## 📁 Project Structure

```
jarvis/
├── app/                 # Core Jarvis modules
│   ├── main.py         # CLI interface
│   ├── llm.py          # AI/LLM integration
│   ├── tts.py          # Text-to-speech
│   └── stt.py          # Speech-to-text
├── templates/          # Web templates
│   └── cv.html         # Interactive CV interface
├── web_app.py          # Flask web server
├── start_cv.sh         # Quick start script
└── requirements.txt    # Python dependencies
```

## 🎨 Customization

To customize for your own CV:
1. Update `CV_DATA` in `web_app.py` with your information
2. Modify the system prompt in `CV_SYSTEM_PROMPT`
3. Update the HTML template with your styling
4. Deploy to your preferred platform

## 📞 Contact

**Andreas Christodoulou**
- 📧 Email: antreaschristdoulou11@gmail.com
- 📍 Location: Paphos, Cyprus
- 💼 Position: Full-Stack Software Engineer - Back-End Focus