#!/usr/bin/env python3
"""
JARVIS CV - Interactive Resume with AI Assistant
Railway-optimized version without Ollama dependency
"""

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Ensure we're not importing any audio-related modules
print("Starting JARVIS CV - Railway optimized version")
print("Audio features disabled for cloud deployment")

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config['SECRET_KEY'] = 'your-secret-key-here'
socketio = SocketIO(app, cors_allowed_origins="*")

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

# Simple AI responses without Ollama
def generate_ai_response(message):
    """Generate AI response based on message content"""
    message_lower = message.lower()
    
    # Hiring questions
    if any(word in message_lower for word in ['hire', 'hiring', 'job', 'position', 'role', 'candidate']):
        return "Andreas is an excellent candidate for backend development roles. His 90% performance improvement on Elasticsearch reindexing and experience with Java, Node.js, and scalable systems make him ideal for senior backend positions. He's particularly strong in performance optimization and has proven leadership experience mentoring junior developers."
    
    # Technical questions
    elif any(word in message_lower for word in ['java', 'elasticsearch', 'database', 'backend', 'api', 'performance']):
        return "Andreas has extensive experience with Java 8/11, Elasticsearch 7.x-8.x, PostgreSQL, and MongoDB. He specializes in performance optimization, having reduced reindexing time from 10 hours to 50 minutes. His expertise includes query optimization, batching, streaming, and building resilient systems with proper error handling."
    
    # Frontend questions
    elif any(word in message_lower for word in ['frontend', 'javascript', 'ui', 'ext.js', 'sap']):
        return "While Andreas focuses on backend development, he has solid frontend experience with JavaScript (ES6+), Ext.js, SAP Fiori (UI5), and custom lightweight frameworks. He successfully migrated a frontend from Angular to a custom JavaScript framework, improving maintainability and performance."
    
    # Experience questions
    elif any(word in message_lower for word in ['experience', 'work', 'company', 'projects']):
        return "Andreas has been working as a Software Developer since July 2023 at a CRM/CMS Platform. He works in a 4-6 person agile team and has delivered major projects including Elasticsearch optimization, CalDAV calendar sync, and a Bulk Actions Manager. His work environment is startup-style with direct ownership of features."
    
    # Education questions
    elif any(word in message_lower for word in ['education', 'university', 'degree', 'study']):
        return "Andreas holds a BSc Computer Science (First Class Honours) from Northumbria University (2020-2023). His dissertation compared PHP vs Python for microservices in e-marketing, focusing on performance metrics. He studied databases, distributed systems, and software engineering, building a strong foundation for backend development."
    
    # General questions
    else:
        return "Andreas is a Full-Stack Software Engineer with a Back-End Focus, currently working as a Software Developer. He specializes in resilient, data-heavy systems and has significant experience with Elasticsearch, Java, Node.js, and various databases. He's based in Paphos, Cyprus, and is fluent in English and Greek."

@app.route('/')
def index():
    return render_template('cv.html', cv_data=CV_DATA)

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        message = data.get('message', '')
        voice_enabled = data.get('voice_enabled', False)
        
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Generate AI response
        response = generate_ai_response(message)
        
        return jsonify({
            'response': response,
            'voice_enabled': voice_enabled
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/voice', methods=['POST'])
def voice():
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # For Railway, we'll return a simple response
        # In production, you'd integrate with a TTS service
        return jsonify({
            'message': 'Voice response generated',
            'audio_url': None  # No audio for now
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/transcribe', methods=['POST'])
def transcribe():
    try:
        # For Railway, we'll return a simple response
        # In production, you'd integrate with a STT service
        return jsonify({
            'transcript': 'Voice transcription not available in demo mode',
            'error': None
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
