# 🚀 Railway Deployment Guide

## Problem Fixed
The original error was caused by Railway trying to run `web_app.py` which imports `sounddevice` (requiring PortAudio), but Railway doesn't have PortAudio installed by default.

## Solution
Created a Railway-optimized version that:
- ✅ Removes all audio dependencies (`sounddevice`, `faster-whisper`, `webrtcvad`)
- ✅ Uses a dedicated startup script
- ✅ Includes proper Railway configuration
- ✅ Maintains all CV functionality without audio features

## Files Created/Modified

### New Files:
- `start_railway.py` - Railway startup script with debugging
- `railway.json` - Railway configuration
- `aptfile` - System dependencies (if needed)
- `RAILWAY_DEPLOYMENT.md` - This guide

### Modified Files:
- `Procfile` - Now points to `start_railway.py`
- `railway_requirements.txt` - Removed audio dependencies
- `web_app_railway.py` - Added startup logging

## Deployment Steps

1. **Commit all changes:**
   ```bash
   git add .
   git commit -m "Fix Railway deployment - remove audio dependencies"
   git push
   ```

2. **Deploy to Railway:**
   - Railway should automatically detect the `Procfile`
   - It will use `start_railway.py` as the entry point
   - The app will start without audio dependencies

3. **Verify deployment:**
   - Check Railway logs for "Starting JARVIS CV - Railway optimized version"
   - The app should start without PortAudio errors
   - All CV features should work except voice input/output

## Features Available on Railway

✅ **Working:**
- Interactive CV display
- AI chat responses
- All CV data and information
- WebSocket connections
- Text-based interactions

❌ **Disabled (requires audio libraries):**
- Voice input (STT)
- Voice output (TTS)
- Real-time audio recording

## If You Need Audio Features

To enable audio features on Railway, you would need to:

1. Add PortAudio to system dependencies in `aptfile`
2. Include audio libraries in `railway_requirements.txt`
3. Use `web_app.py` instead of `web_app_railway.py`

However, this is not recommended for Railway as:
- Audio libraries are heavy and slow to install
- Railway is optimized for web applications, not audio processing
- Better to use dedicated audio services (AWS Polly, Google TTS, etc.)

## Troubleshooting

If you still get PortAudio errors:
1. Check Railway logs to see which file is being executed
2. Ensure `Procfile` points to `start_railway.py`
3. Verify `railway.json` has correct start command
4. Check that no other files are importing audio modules

## Local Development

For local development with audio features:
```bash
pip install -r requirements.txt
python web_app.py
```

For Railway testing without audio:
```bash
pip install -r railway_requirements.txt
python web_app_railway.py
```
