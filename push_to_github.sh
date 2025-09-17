#!/bin/bash

echo "🚀 Pushing JARVIS CV Railway fixes to GitHub..."
echo ""

# Check if we're in the right directory
if [ ! -f "start_railway.py" ]; then
    echo "❌ Error: start_railway.py not found. Are you in the right directory?"
    exit 1
fi

echo "✅ Found Railway files, attempting to push..."

# Try different push methods
echo "Method 1: Direct push..."
if git push origin main 2>/dev/null; then
    echo "✅ Successfully pushed!"
    exit 0
fi

echo "Method 2: Push with token URL..."
echo "Please enter your GitHub Personal Access Token:"
read -s TOKEN

if [ -n "$TOKEN" ]; then
    if git push https://$TOKEN@github.com/AntreasCh/jarvis-cv.git main; then
        echo "✅ Successfully pushed with token!"
        exit 0
    fi
fi

echo "❌ All push methods failed."
echo ""
echo "Manual options:"
echo "1. Use GitHub Desktop"
echo "2. Upload files directly to GitHub web interface"
echo "3. Check your GitHub authentication settings"
echo ""
echo "Files ready to push:"
git status --porcelain
