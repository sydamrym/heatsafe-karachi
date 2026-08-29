#!/bin/bash
# HeatSafe Karachi - One-command setup

echo " Setting up HeatSafe Karachi..."

# Backend
echo " Installing backend dependencies..."
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ..

# Frontend
echo " Installing frontend dependencies..."
cd frontend
npm install
cd ..

echo " Setup complete!"
echo ""
echo "Next steps:"
echo "1. Copy backend/.env.example to backend/.env and add your keys"
echo "2. Copy frontend/.env.example to frontend/.env"
echo "3. Terminal 1: cd backend && source venv/bin/activate && uvicorn main:app --reload"
echo "4. Terminal 2: cd frontend && npm run dev"
echo "5. Open http://localhost:5173"
