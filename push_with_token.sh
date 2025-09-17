#!/bin/bash

echo "🔑 GitHub Personal Access Token Push"
echo "===================================="
echo ""
echo "1. Go to: https://github.com/settings/tokens"
echo "2. Click 'Generate new token (classic)'"
echo "3. Select scopes: 'repo' (full control)"
echo "4. Copy the token"
echo "5. Run this command with your token:"
echo ""
echo "git push https://YOUR_TOKEN@github.com/AntreasCh/jarvis-cv.git main"
echo ""
echo "Or enter your token below:"
read -p "Token: " token
if [ ! -z "$token" ]; then
    echo "Pushing with token..."
    git push https://$token@github.com/AntreasCh/jarvis-cv.git main
else
    echo "No token provided. Please run the command manually."
fi
