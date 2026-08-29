#!/bin/bash
# Deploy backend to Render.com (FREE)
# 1. Create account at render.com
# 2. Create New Web Service
# 3. Connect your GitHub repo
# 4. Set root directory to: backend
# 5. Build Command: pip install -r requirements.txt
# 6. Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
# 7. Add Environment Variables:
#    - FORTYGUARD_API_KEY=your_key
#    - OPENAI_API_KEY=your_key (optional)
#    - CORS_ORIGINS=https://your-frontend.vercel.app,http://localhost:5173

echo "Backend deployment guide:"
echo "1. Push code to GitHub"
echo "2. Go to render.com -> New Web Service"
echo "3. Connect repo, set root dir to 'backend'"
echo "4. Set build: pip install -r requirements.txt"
echo "5. Set start: uvicorn main:app --host 0.0.0.0 --port \$PORT"
echo "6. Add env vars in Render dashboard"
