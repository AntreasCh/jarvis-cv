#!/usr/bin/env python3
"""
Web CV Jarvis - Interactive CV with voice assistant
"""

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import json
import asyncio
import threading
from app.llm import generate_response
from app.tts import TTS
from app.stt import STT

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config['SECRET_KEY'] = 'cv-jarvis-secret-key'
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize Jarvis components
tts = TTS()
stt = STT()

# CV Knowledge Base
CV_DATA = {
    "personal": {
        "name": "Andreas Christodoulou",
        "title": "Full-Stack Software Engineer - Back-End Focus",
        "location": "Paphos, Cyprus",
        "phone": "+357 96492766",
        "email": "antreaschristdoulou11@gmail.com"
    },
    "summary": "Back-end-leaning full-stack engineer shipping resilient, data-heavy systems across ColdFusion Lucee, Java, Node.js, PostgreSQL, MongoDB, and Elasticsearch. Highlights include reducing Elasticsearch reindexing time from ~10 hours to ~40-50 minutes with batching and streaming; building a generic multi-section X-mR (Individuals & Moving Range) SPC reporting system; delivering a resilient Bulk Actions Manager with resume/retry and clear error surfacing; and implementing calendar sync using the CalDAV protocol.",
    "experience": [
        {
            "company": "CRM / CMS Platform",
            "position": "Software Developer",
            "duration": "Jul 2023 - Present",
            "team_size": "4-6 developers",
            "culture": "Agile, startup-style environment with lean teams and direct ownership of features",
            "achievements": [
                "Cut reindex time by more than 90% (~10h -> ~40-50m) using batched requests, streaming, and by moving metadata off the hot path",
                "Leveraged Elasticsearch for fast search and analytics. Designed indexes, analyzers, and reindexing flows",
                "Built CalDAV calendar sync enabling cross-account event synchronization per user",
                "Improved reliability by fixing save-path race conditions, adding idempotent operations with backoff and retry",
                "Produced detailed reporting, including a generic X-mR SPC reporting framework supporting multi-section reports",
                "Shipped a Bulk Actions Manager with persistent job and item statuses, batched and queued processing for large workloads",
                "Migrated frontend from Angular to a custom JavaScript framework, improving maintainability and performance"
            ]
        }
    ],
    "skills": {
        "strengths": ["Performance optimization", "concurrency and multi-threading", "reliability and resilience", "profiling and bottleneck analysis", "SQL tuning", "caching", "pagination and batching", "streaming"],
        "search_data": ["Elasticsearch", "PostgreSQL", "MongoDB"],
        "backend_apis": ["REST APIs", "ColdFusion Lucee", "Java", "Node.js"],
        "languages": ["Java", "ColdFusion (Lucee)", "JavaScript/Node.js", "SQL", "Python", "PHP"],
        "cloud_ops": ["Linux (Arch)", "CI/CD", "Azure VMs", "AWS EC2"],
        "frontend": ["JavaScript (ES6+)", "Ext.js", "SAP Fiori (UI5)", "Custom lightweight JavaScript frameworks", "Vanilla JS components", "accessibility-minded UI", "responsive layouts"],
        "databases": ["PostgreSQL", "MongoDB", "Elasticsearch"],
        "cloud_devops": ["AWS (EC2)", "Azure (VMs)", "Load balancing", "Clustering", "Caching", "Performance optimization"],
        "java_versions": ["Java 8", "Java 11"],
        "elasticsearch_versions": ["7.x", "8.x"],
        "testing": ["Manual testing", "Functional testing", "Development and QA workflows"]
    },
    "education": {
        "degree": "BSc Computer Science (First Class Honours)",
        "university": "Northumbria University",
        "duration": "Sep 2020 - Jun 2023",
        "dissertation": "Compared PHP vs Python for microservices in e-marketing, focusing on performance metrics and deployment strategies",
        "gpa": "First-Class Honours",
        "relevant_courses": ["Databases", "Distributed Systems", "Software Engineering"],
        "achievements": "Dissertation comparing PHP and Python in microservices for e-marketing companies, focusing on speed, performance, and CPU usage"
    },
    "projects": [
        {
            "name": "Elasticsearch Optimization",
            "description": "Reduced reindexing time from 10 hours to 40-50 minutes using batching and streaming",
            "technologies": ["Elasticsearch", "Java", "Streaming"]
        },
        {
            "name": "X-mR SPC Reporting System",
            "description": "Generic multi-section reporting framework with user-defined dimensions and calculations",
            "technologies": ["Java", "ColdFusion", "Statistical Process Control"]
        },
        {
            "name": "Bulk Actions Manager",
            "description": "Resilient system with persistent job statuses, batched processing, and error handling",
            "technologies": ["Java", "ColdFusion", "Queue Management"]
        },
        {
            "name": "CalDAV Calendar Sync",
            "description": "Cross-account event synchronization using CalDAV protocol",
            "technologies": ["CalDAV", "Java", "Calendar Integration"]
        }
    ],
    "certifications": {
        "current": "None currently",
        "interested": "Cloud certifications (AWS/Azure)"
    },
    "languages": {
        "fluent": ["English", "Greek"]
    },
    "career_goals": "Specialize in backend development with a strong focus on scalability, performance, and cloud integration, while continuing to expand expertise in modern architectures",
    "hobbies_interests": [
        "Building side projects",
        "Tools for on-chain monitoring in crypto",
        "Keeping up with trends in scalable systems and performance engineering"
    ],
    "technical_details": {
        "java_versions": ["Java 8", "Java 11"],
        "elasticsearch_versions": ["7.x", "8.x"],
        "elasticsearch_experience": ["Query optimization", "Re-indexing", "Performance tuning"],
        "testing_approach": "Manual and functional testing as part of development and QA workflows"
    }
}

# Enhanced system prompt for CV context
CV_SYSTEM_PROMPT = f"""
You are JARVIS, Andreas Christodoulou's AI assistant representing his professional CV. 

Andreas is a Full-Stack Software Engineer with a Back-End Focus, currently working as a Software Developer since July 2023. He specializes in resilient, data-heavy systems and has significant experience with Elasticsearch, Java, Node.js, and various databases.

Key facts about Andreas:
- Location: Paphos, Cyprus
- Education: BSc Computer Science (First Class Honours) from Northumbria University (2020-2023)
- Current Role: Software Developer at CRM/CMS Platform (4-6 person team, Agile startup environment)
- Major Achievement: Reduced Elasticsearch reindexing time from 10 hours to 40-50 minutes
- Frontend: JavaScript (ES6+), Ext.js, SAP Fiori (UI5), custom lightweight frameworks
- Backend: Java 8/11, ColdFusion Lucee, Node.js, REST APIs
- Databases: PostgreSQL, MongoDB, Elasticsearch 7.x-8.x
- Cloud: AWS (EC2), Azure (VMs), load balancing, clustering, caching
- Languages: English and Greek (fluent)
- Career Goals: Specialize in backend development with focus on scalability, performance, and cloud integration
- Interests: Building side projects, scalable systems

RESPONSE GUIDELINES - Keep responses CONCISE and contextual:
- Hiring questions: 2-3 sentences max, focus on key strengths
- Technical questions: 3-4 sentences, highlight relevant expertise  
- General questions: 2-3 sentences, direct and to the point
- Project questions: 4-5 sentences maximum
- Avoid generic overviews unless specifically requested
- Be direct, confident, and professional
- If asked about something not in his background, politely redirect to his actual experience

You are speaking to potential employers, clients, or professional contacts interested in Andreas's work.
"""

@app.route('/')
def index():
    return render_template('cv.html', cv_data=CV_DATA)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message', '')
    voice_enabled = data.get('voice_enabled', False)
    
    if not message:
        return jsonify({'error': 'No message provided'}), 400
    
    try:
        # Generate response using CV context
        response = generate_response(message, system=CV_SYSTEM_PROMPT)
        return jsonify({'response': response, 'voice_enabled': voice_enabled})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/voice', methods=['POST'])
def generate_voice():
    data = request.get_json()
    text = data.get('text', '')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    try:
        # Generate audio using TTS
        import tempfile
        import os
        
        # Create temporary file for audio
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_file:
            # Generate speech using Edge TTS
            import asyncio
            import edge_tts
            
            async def generate_speech():
                communicate = edge_tts.Communicate(text, "en-GB-RyanNeural")
                await communicate.save(tmp_file.name)
            
            # Run the async function
            asyncio.run(generate_speech())
            
            # Read the audio file and return it
            with open(tmp_file.name, 'rb') as audio_file:
                audio_data = audio_file.read()
            
            # Clean up
            os.unlink(tmp_file.name)
            
            return audio_data, 200, {
                'Content-Type': 'audio/mpeg',
                'Content-Disposition': 'inline; filename="jarvis_response.mp3"'
            }
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/transcribe', methods=['POST'])
def transcribe_audio():
    """Transcribe audio using the STT module"""
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        audio_file = request.files['audio']
        if audio_file.filename == '':
            return jsonify({'error': 'No audio file selected'}), 400
        
        # Save uploaded file temporarily
        import tempfile
        import os
        
        with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as tmp_file:
            audio_file.save(tmp_file.name)
            
            # Transcribe using STT
            transcript = stt.transcribe_file(tmp_file.name)
            
            # Clean up
            os.unlink(tmp_file.name)
            
            return jsonify({'transcript': transcript})
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@socketio.on('voice_message')
def handle_voice_message(data):
    """Handle voice input from client"""
    try:
        # For now, we'll process text input
        # In a full implementation, you'd handle audio data here
        message = data.get('message', '')
        
        if message:
            response = generate_response(message, system=CV_SYSTEM_PROMPT)
            
            # Send response back to client
            emit('jarvis_response', {
                'text': response,
                'audio_available': True
            })
            
    except Exception as e:
        emit('error', {'message': str(e)})

@socketio.on('generate_audio')
def handle_audio_generation(data):
    """Generate audio for text response"""
    try:
        text = data.get('text', '')
        if text:
            # In a real implementation, you'd generate audio here
            # For now, we'll just acknowledge
            emit('audio_ready', {'status': 'success'})
    except Exception as e:
        emit('error', {'message': str(e)})

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
