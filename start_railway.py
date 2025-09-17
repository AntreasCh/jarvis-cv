#!/usr/bin/env python3
"""
Railway startup script - ensures correct app is launched
"""

import os
import sys

def main():
    print("🚀 Starting JARVIS CV on Railway...")
    print(f"Python version: {sys.version}")
    print(f"Working directory: {os.getcwd()}")
    print(f"Available files: {os.listdir('.')}")
    
    # Check if we're in the right environment
    if 'RAILWAY_ENVIRONMENT' in os.environ:
        print("✅ Running in Railway environment")
    else:
        print("⚠️  Not in Railway environment, but continuing...")
    
    # Import and run the Railway-optimized app
    try:
        from web_app_railway import app, socketio
        port = int(os.environ.get('PORT', 5000))
        print(f"🌐 Starting server on port {port}")
        socketio.run(app, host='0.0.0.0', port=port, debug=False)
    except Exception as e:
        print(f"❌ Error starting app: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
