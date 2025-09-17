# 🚀 Deploy JARVIS CV to Railway

## Quick Setup (5 minutes):

### 1. **Push to GitHub:**
```bash
git init
git add .
git commit -m "Initial JARVIS CV commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/jarvis-cv.git
git push -u origin main
```

### 2. **Deploy on Railway:**
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your `jarvis-cv` repository
5. Railway will auto-detect it's a Python app
6. Add environment variables:
   - `OLLAMA_BASE_URL=https://your-ollama-instance.railway.app` (or use a cloud LLM)
   - `OLLAMA_MODEL=llama3.1:8b`

### 3. **Access Your CV:**
- Railway will give you a URL like: `https://jarvis-cv-production.railway.app`
- Open this on your phone!

## Alternative: Render.com

### 1. **Same GitHub setup as above**

### 2. **Deploy on Render:**
1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Click "New" → "Web Service"
4. Connect your repository
5. Settings:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python web_app.py`
   - **Environment:** Python 3

## 📱 Mobile Access:
Once deployed, you can:
- Open the URL on your phone
- Use voice input (microphone)
- Install as PWA (Progressive Web App)
- Share with potential employers!

## 🔧 Notes:
- The free tiers have limitations (sleep after inactivity)
- For production, consider upgrading to paid plans
- Ollama might need a cloud instance for production use
