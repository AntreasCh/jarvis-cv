#!/bin/bash
# Start the Interactive CV with JARVIS

echo "🚀 Starting Andreas Christodoulou's Interactive CV with JARVIS..."
echo "📍 Location: Paphos, Cyprus"
echo "💼 Position: Full-Stack Software Engineer - Back-End Focus"
echo ""
echo "🌐 Web interface will be available at: http://localhost:5000"
echo "🎤 JARVIS is ready to answer questions about Andreas's experience!"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Activate virtual environment and start the web app
source .venv/bin/activate
python web_app.py
