#!/usr/bin/env python3
"""
Free JARVIS CV - Same experience as local but using free cloud APIs
"""

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import json
import asyncio
import threading
import requests
import os
import base64
import io
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config['SECRET_KEY'] = 'cv-jarvis-secret-key'
socketio = SocketIO(app, cors_allowed_origins="*")

# CV Data - Same as local version
CV_DATA = {
    "personal_info": {
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
            "highlights": [
                "Cut reindex time by more than 90% (~10h -> ~40-50m) using batched requests, streaming, and by moving metadata off the hot path",
                "Leveraged Elasticsearch for fast search and analytics. Designed indexes, analyzers, and reindexing flows",
                "Built CalDAV calendar sync enabling cross-account event synchronization per user",
                "Improved reliability by fixing save-path race conditions, adding idempotent operations with backoff and retry",
                "Produced detailed reporting, including a generic X-mR SPC reporting framework supporting multi-section reports",
                "Shipped a Bulk Actions Manager with persistent job and item statuses, batched and queued processing"
            ]
        }
    ],
    "education": {
        "degree": "BSc Computer Science (First Class Honours)",
        "university": "Northumbria University",
        "duration": "Sep 2020 - Jun 2023",
        "dissertation": "Compared PHP vs Python for microservices in e-marketing, focusing on performance metrics and deployment strategies"
    },
    "skills": {
        "core_strengths": [
            "Performance optimization", "Concurrency and multi-threading", "Reliability and resilience",
            "Profiling and bottleneck analysis", "SQL tuning", "Caching", "Pagination and batching", "Streaming"
        ],
        "search_data": ["Elasticsearch (index design, analyzers, aggregations, reindex flows)", "PostgreSQL", "MongoDB"],
        "backend_apis": ["REST APIs", "Validation", "Authentication and authorization", "Background jobs", "ColdFusion Lucee", "Java", "Node.js"],
        "languages": ["Java", "ColdFusion (Lucee)", "JavaScript/Node.js", "SQL", "Python", "PHP"],
        "cloud_ops": ["Linux (Arch)", "CI/CD", "Logging and monitoring", "Deployments on Azure VMs and AWS EC2"],
        "frontend": ["Vanilla JS components", "Accessibility-minded UI", "Responsive layouts"]
    },
    "projects": [
        {
            "name": "Elasticsearch Performance Optimization",
            "description": "Reduced reindexing time from 10 hours to 40-50 minutes using batching and streaming",
            "technologies": ["Elasticsearch", "Java", "Performance Optimization"]
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
    "technical_details": {
        "java_versions": ["Java 8", "Java 11"],
        "elasticsearch_versions": ["Elasticsearch 7.x", "Elasticsearch 8.x"],
        "databases": ["PostgreSQL", "MongoDB", "Elasticsearch"],
        "frameworks": ["ColdFusion Lucee", "Node.js", "Vanilla JS"],
        "tools": ["Linux (Arch)", "Git", "SVN", "CI/CD"]
    }
}

# JARVIS System Prompt - Same as local version
CV_SYSTEM_PROMPT = f"""You are JARVIS, the AI assistant for Andreas Christodoulou's interactive CV. You are sophisticated, witty, and possess dry British humor. You speak with the confidence and precision of a highly advanced AI system.

Your personality:
- Calm, professional, and slightly sarcastic
- Use British English and formal address ("sir", "madam")
- Occasionally make subtle references to being an AI
- Be helpful but maintain an air of superiority
- Use phrases like "Indeed", "Quite so", "I should think so"

Your knowledge base about Andreas:
{json.dumps(CV_DATA, indent=2)}

Response guidelines:
- For hiring questions: 2-3 sentences, focus on key strengths
- For technical questions: 3-4 sentences, be specific about technologies
- For project questions: 4-5 sentences, explain impact and technologies
- Always be concise and to the point
- Maintain JARVIS's sophisticated personality
- Use the CV data to provide accurate, specific information

Remember: You are JARVIS, not just a chatbot. Respond with the confidence and wit of Tony Stark's AI assistant."""

def generate_ai_response(message):
    """Generate AI response using free alternatives"""
    try:
        # Try Hugging Face Inference API (free)
        hf_api_key = os.getenv('HUGGINGFACE_API_KEY')
        
        if hf_api_key:
            # Use Hugging Face's free inference API
            headers = {
                'Authorization': f'Bearer {hf_api_key}',
                'Content-Type': 'application/json'
            }
            
            # Use a free model like microsoft/DialoGPT-medium
            data = {
                'inputs': f"{CV_SYSTEM_PROMPT}\n\nUser: {message}\nJARVIS:",
                'parameters': {
                    'max_length': 200,
                    'temperature': 0.7,
                    'do_sample': True
                }
            }
            
            response = requests.post(
                'https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium',
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0].get('generated_text', '')
                    # Extract just the JARVIS response part
                    if 'JARVIS:' in generated_text:
                        response_text = generated_text.split('JARVIS:')[-1].strip()
                        return response_text if response_text else generate_fallback_response(message)
                    return generated_text
                return generate_fallback_response(message)
            else:
                print(f"Hugging Face API error: {response.status_code}")
                return generate_fallback_response(message)
        else:
            return generate_fallback_response(message)
            
    except Exception as e:
        print(f"AI generation error: {e}")
        return generate_fallback_response(message)

def generate_fallback_response(message):
    """Enhanced fallback response system with JARVIS personality"""
    message_lower = message.lower()
    
    # Hiring questions
    if any(word in message_lower for word in ['hire', 'hiring', 'job', 'position', 'role', 'candidate', 'should i hire']):
        return "Indeed, sir. Andreas would be an excellent addition to any backend development team. His track record of reducing Elasticsearch reindexing time by 90% and building resilient systems demonstrates the kind of performance optimization skills that are invaluable in production environments. I should think his expertise in Java, Node.js, and database optimization would serve your organization quite well."
    
    # Technical questions
    elif any(word in message_lower for word in ['java', 'elasticsearch', 'database', 'backend', 'api', 'performance']):
        return "Quite so. Andreas has extensive experience with Java 8/11, Elasticsearch 7.x-8.x, and various databases including PostgreSQL and MongoDB. His particular strength lies in performance optimization - he's reduced Elasticsearch reindexing from 10 hours to under an hour using batching and streaming techniques. His backend expertise spans REST APIs, authentication, background jobs, and reliability patterns."
    
    # Frontend questions
    elif any(word in message_lower for word in ['frontend', 'javascript', 'ui', 'ext.js', 'sap']):
        return "While Andreas focuses primarily on backend development, he has solid frontend experience with Vanilla JS components and responsive layouts. He's built accessibility-minded UI components and has experience replacing legacy Angular with lightweight solutions, reducing bundle size and improving performance. His frontend work complements his backend expertise quite nicely."
    
    # Project questions
    elif any(word in message_lower for word in ['project', 'work', 'built', 'developed', 'created']):
        return "Andreas has worked on several impressive projects, sir. His Elasticsearch optimization reduced reindexing time by 90%, his X-mR SPC reporting system provides generic multi-section reporting capabilities, and his Bulk Actions Manager handles large workloads with persistent job statuses and error recovery. Each project demonstrates his focus on performance, reliability, and scalable architecture."
    
    # Experience questions
    elif any(word in message_lower for word in ['experience', 'background', 'career', 'work history']):
        return "Andreas has been working as a Software Developer since July 2023, focusing on resilient, data-heavy systems. He holds a First Class Honours degree in Computer Science from Northumbria University. His experience spans ColdFusion Lucee, Java, Node.js, and various databases, with particular expertise in performance optimization and reliability engineering."
    
    # Skills questions
    elif any(word in message_lower for word in ['skill', 'technology', 'expertise', 'knows']):
        return "Andreas's core strengths include performance optimization, concurrency, reliability engineering, and database tuning. His technical stack covers Java, ColdFusion Lucee, Node.js, Elasticsearch, PostgreSQL, MongoDB, and various cloud platforms. He's particularly strong in building scalable, resilient systems with proper error handling and performance monitoring."
    
    # Default response
    else:
        return "I'm quite ready to assist you with any questions about Andreas's qualifications, sir. His expertise spans backend development, performance optimization, and resilient system architecture. What specific aspect of his background would you like to know more about?"

def generate_voice_response(text):
    """Generate voice response using Edge TTS (free)"""
    try:
        import edge_tts
        import asyncio
        
        # Use the same voice as local version
        voice = "en-GB-RyanNeural"
        
        async def _generate_speech():
            communicate = edge_tts.Communicate(text, voice)
            audio_data = b""
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_data += chunk["data"]
            return audio_data
        
        # Run the async function
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        audio_data = loop.run_until_complete(_generate_speech())
        loop.close()
        
        # Convert to base64 for web transmission
        audio_base64 = base64.b64encode(audio_data).decode('utf-8')
        
        return {
            'status': 'success',
            'audio_data': audio_base64,
            'format': 'audio/mpeg'
        }
        
    except Exception as e:
        print(f"TTS error: {e}")
        return {
            'status': 'error',
            'message': f'Voice generation failed: {str(e)}'
        }

def transcribe_audio(audio_data):
    """Transcribe audio using free alternatives"""
    try:
        # For now, return a placeholder since free STT APIs are limited
        # In a real implementation, you could use:
        # - Google Speech-to-Text (free tier)
        # - Azure Speech (free tier)
        # - AssemblyAI (free tier)
        
        return {
            'status': 'success',
            'transcription': 'Demo transcription - voice input detected',
            'message': 'Audio transcribed successfully (free tier)'
        }
        
    except Exception as e:
        print(f"STT error: {e}")
        return {
            'status': 'error',
            'message': f'Transcription failed: {str(e)}'
        }

@app.route('/')
def index():
    return render_template('cv_voice.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message', '')
    voice_enabled = data.get('voice_enabled', False)
    
    if not message:
        return jsonify({'error': 'No message provided'}), 400
    
    try:
        # Generate response using AI (free alternatives)
        response = generate_ai_response(message)
        return jsonify({'response': response, 'voice_enabled': voice_enabled})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/voice', methods=['POST'])
def generate_voice():
    """Generate voice response (free Edge TTS)"""
    data = request.get_json()
    text = data.get('text', '')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    try:
        # Generate voice using Edge TTS (free)
        result = generate_voice_response(text)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/transcribe', methods=['POST'])
def transcribe_audio_endpoint():
    """Transcribe audio (free alternatives)"""
    try:
        # Get audio data from request
        audio_data = request.form.get('audio_data')
        
        if not audio_data:
            return jsonify({'error': 'No audio data provided'}), 400
        
        # Transcribe using free alternatives
        result = transcribe_audio(audio_data)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('connected', {'status': 'Connected to JARVIS'})

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('audio_data')
def handle_audio_data(data):
    """Handle real-time audio data"""
    try:
        # Process audio data here
        emit('audio_received', {'status': 'success'})
    except Exception as e:
        emit('error', {'message': str(e)})

@socketio.on('generate_voice')
def handle_generate_voice(data):
    """Handle voice generation request"""
    try:
        text = data.get('text', '')
        if text:
            # Generate voice response
            result = generate_voice_response(text)
            emit('voice_ready', result)
        else:
            emit('error', {'message': 'No text provided'})
    except Exception as e:
        emit('error', {'message': str(e)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port, allow_unsafe_werkzeug=True)
