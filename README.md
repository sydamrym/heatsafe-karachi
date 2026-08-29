# HeatSafe Karachi

**AI-Powered Hyperlocal Heat Risk Intelligence Platform**

> *"Karachi has 15 million people and one weather forecast. Here is why that is a problem."*

HeatSafe Karachi uses **FortyGuard's 2-meter precision temperature intelligence** to identify heat-risk areas across Karachi and provide actionable safety recommendations for citizens, schools, construction sites, and city administrators.



## What It Does


**Live Heat Risk Map** : Interactive Leaflet map showing temperature variations across 4 Karachi neighborhoods 
**AI Safety Analysis** : Natural language alerts generated from real-time temperature + wet-bulb data 
**Contextual Actions** : School dismissal alerts, construction break recommendations, market closure advisories 
**Safest Window Calculator** : Recommends safest times for outdoor activity per neighborhood 
**Multi-Index Risk Engine** : Combines dry temp, apparent temp, heat index, and wet-bulb temperature 



##  Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   React +       │────▶│  FastAPI Backend │────▶│  FortyGuard API │
│   Leaflet UI    │◄────│  (Python)        │◄────│  (Heatmaps +    │
│                 │     │                  │     │  Env Params)    │
└─────────────────┘     └──────────────────┘     └─────────────────┘
        │                        │
        ▼                        ▼
   Risk Color Map          OpenAI GPT-4o-mini
   Area Detail Cards       (Natural language alerts)
```

**Tech Stack:**
- **Frontend:** React 18, Leaflet, Vite, Lucide Icons
- **Backend:** FastAPI, Python 3.12, httpx (async)
- **Data:** FortyGuard Temperature API (heatmaps + env_params)
- **AI:** OpenAI GPT-4o-mini (fallback engine included)
- **Deploy:** Render (backend) + Vercel (frontend)



##  Quick Start (Local Development)

### Step 1: Clone & Setup Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Configure Environment

```bash
cp .env.example .env
# Edit .env and add your keys:
# FORTYGUARD_API_KEY=your_fortyguard_key
# OPENAI_API_KEY=your_openai_key (optional, has fallback)
```

### Step 3: Start Backend

```bash
uvicorn main:app --reload --port 8000
```

Backend will be at: `http://localhost:8000`
API docs at: `http://localhost:8000/docs`

### Step 4: Setup Frontend

```bash
cd frontend
npm install
```

### Step 5: Configure Frontend

```bash
cp .env.example .env
# Edit .env:
# VITE_API_URL=http://localhost:8000
```

### Step 6: Start Frontend

```bash
npm run dev
```

Frontend will be at: `http://localhost:5173`

---

##  API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /api/areas` | List all Karachi test areas |
| `GET /api/dashboard?date=YYYY-MM-DD&time=HH:MM` | **Main endpoint** — full dashboard with all areas, risk levels, AI summaries |
| `GET /api/area/{area_id}` | Detailed heatmap GeoJSON for a single area |

---

##  Karachi Test Areas

| Area | Type | Why It Matters |
|------|------|----------------|
| **Clifton** | Coastal/Affluent | Sea breeze = cooler. Baseline comparison. |
| **Korangi** | Industrial | High concrete, low ventilation = heat island. |
| **Saddar** | Commercial Dense | Heavy traffic, markets = high exposure. |
| **Lyari** | Dense Residential | Limited green cover = vulnerable population. |



##  Risk Engine Logic

```
Wet Bulb >= 32°C  → EXTREME (Life-threatening)
Wet Bulb >= 28°C  → DANGER  (Outdoor work must stop)
Apparent >= 40°C  → HIGH    (Severely limit activity)
Apparent >= 35°C  → CAUTION (Limit strenuous activity)
Else              → SAFE
```

**Why wet-bulb?** Wet-bulb temperature measures the body's ability to cool via sweating. At 35°C wet-bulb, even healthy humans die within hours. This is the most important metric for heat safety.


##  Deploy to Production 

### Backend → Render.com

1. Push code to **GitHub**
2. Go to [render.com](https://render.com) → **New Web Service**
3. Connect your repo
4. **Root Directory:** `backend`
5. **Build Command:** `pip install -r requirements.txt`
6. **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
7. **Environment Variables:**
   - `FORTYGUARD_API_KEY` = your key
   - `OPENAI_API_KEY` = your key (optional)
   - `CORS_ORIGINS` = `https://your-frontend.vercel.app,http://localhost:5173`

### Frontend → Vercel

```bash
cd frontend
npm install -g vercel
vercel --prod
```

Then in Vercel dashboard, add environment variable:
- `VITE_API_URL` = `https://your-backend.onrender.com`

---

##  Fallback Strategy

If FortyGuard API is slow or fails:
- Backend gracefully returns cached/estimated data
- Frontend shows "Data temporarily unavailable" with historical context
- **Demo tip:** If API is down during your pitch, switch `USE_MOCK = True` in `backend/app/routers/heatmap.py` and redeploy in 2 minutes

---

##  Why This Wins

1. **Real API Integration** — Every number comes from FortyGuard's live API
2. **Actionable Intelligence** — Not just a map, but "what do I do about it?"
3. **Contextual Awareness** — Schools, hospitals, markets get specific recommendations
4. **Public Health Impact** — Wet-bulb temperature = the metric that actually kills people
5. **Scalable Vision** — One city today, every South Asian megacity tomorrow

---

##  Project Structure

```
heatsafe-karachi/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py          # Env vars
│   │   ├── models.py          # Pydantic schemas
│   │   ├── data.py            # Karachi areas + landmarks
│   │   ├── fortyguard_client.py  # API wrapper
│   │   ├── risk_engine.py     # Risk calculation logic
│   │   ├── ai_recommendations.py # OpenAI integration
│   │   └── routers/
│   │       └── heatmap.py     # API routes
│   ├── main.py                # FastAPI entry
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── main.jsx
│   │   ├── App.jsx            # Main layout
│   │   ├── App.css            # Global styles
│   │   └── components/
│   │       ├── HeatMap.jsx    # Leaflet map
│   │       ├── AreaCard.jsx   # Detail panel
│   │       └── CityAlert.jsx  # Alert banner
│   ├── package.json
│   ├── vite.config.js
│   └── .env.example
├── scripts/
│   ├── deploy-backend.sh
│   └── deploy-frontend.sh
└── README.md
```



## ⚡ Emergency Demo Tips

**If API is slow during demo:**
```python
# In backend/app/routers/heatmap.py, line 12:
USE_MOCK = True  # Switch to mock data instantly
```

**If you need to show the API is real:**
- Open browser dev tools → Network tab
- Show the `GET /api/dashboard` request
- Activity IDs are logged in backend console

**If judges ask about accuracy:**
- "We use FortyGuard's Large Temperature Models, validated against ground sensors, recognized by NVIDIA"
- "Wet-bulb is the gold standard for human heat stress — not just temperature"