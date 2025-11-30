# Free Deployment Guide

## Option 1: Render (Recommended) ⭐

**Pros:** Easy setup, persistent storage, 750 free hours/month, auto-deploy from Git

### Steps:
1. Push your code to GitHub
2. Go to [render.com](https://render.com) and sign up
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Render will auto-detect `render.yaml`
6. Add environment variable:
   - Key: `GOOGLE_API_KEY`
   - Value: Your Gemini API key
7. Click "Create Web Service"

**Note:** ChromaDB data persists in memory but resets on restart (free tier limitation)

---

## Option 2: Railway

**Pros:** Simple deployment, good free tier (500 hours/month)

### Steps:
1. Push code to GitHub
2. Go to [railway.app](https://railway.app)
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Add environment variables:
   - `GOOGLE_API_KEY`: Your API key
   - `PORT`: 8080 (Railway auto-sets this)
6. Set start command: `python app_legal/main.py`

---

## Option 3: PythonAnywhere

**Pros:** Always-on free tier, persistent storage

### Steps:
1. Sign up at [pythonanywhere.com](https://www.pythonanywhere.com)
2. Upload your code via Git or file upload
3. Create a new web app (Flask)
4. Configure WSGI file to import your app
5. Set environment variables in web app settings
6. Reload the web app

**Limitations:** Free tier has limited CPU/bandwidth

---

## Option 4: Fly.io

**Pros:** Good performance, generous free tier

### Steps:
1. Install Fly CLI: `curl -L https://fly.io/install.sh | sh`
2. Run `fly launch` in your project directory
3. Follow prompts to create app
4. Set secrets: `fly secrets set GOOGLE_API_KEY=your_key`
5. Deploy: `fly deploy`

---

## Important Notes

### ChromaDB Persistence
Free hosting platforms typically don't provide persistent disk storage. Your vector database will reset on each deployment/restart. For production:
- Use a managed vector DB (Pinecone free tier, Weaviate Cloud)
- Or upgrade to paid hosting with persistent volumes

### Environment Variables
Always set `GOOGLE_API_KEY` in your hosting platform's environment variables (never commit to Git).

### Which App to Deploy?
The default configuration deploys Legal Eagle (`app_legal`). To deploy Ghost mode instead:
- Update `render.yaml` or start command to use `app_ghost/main.py`

### Multiple Apps
To run both apps simultaneously, you'll need:
- Two separate deployments (one for each app)
- Or modify the code to run both on different routes

---

## Quick Start (Render)

```bash
# 1. Initialize git (if not already)
git init
git add .
git commit -m "Initial commit"

# 2. Create GitHub repo and push
git remote add origin https://github.com/yourusername/your-repo.git
git push -u origin main

# 3. Go to render.com and connect your repo
# 4. Add GOOGLE_API_KEY environment variable
# 5. Deploy!
```

Your app will be live at: `https://your-app-name.onrender.com`
