# Predictive Intelligence Engine

Ek full-stack Business Intelligence project — real CSV data par forecasting,
churn/attrition analysis, Monte Carlo scenario simulation aur ek RAG-based
knowledge search karta hai. Backend aur Frontend do bilkul alag folders mein
hain taaki dono independently run/deploy ho sakein.

```
predictive-intelligence-engine/
├── backend/            # FastAPI + SQLite — saara API aur database yahin hai
│   ├── app/
│   │   ├── agents/      # 5 Python agents (analysis, forecasting, scenario, rag, decision)
│   │   ├── routes/      # Har API endpoint apni file mein
│   │   ├── database.py  # SQLite connection setup
│   │   ├── models.py    # Database tables (SQLAlchemy)
│   │   ├── schemas.py   # API response shapes (Pydantic)
│   │   └── main.py      # FastAPI app + route registration
│   ├── data/
│   │   ├── cleaned/     # Original real datasets (CSV)
│   │   ├── uploaded/    # Jo CSV upload hongi wo yahan save hoti hain
│   │   └── knowledge/   # RAG knowledge base (markdown notes, real data se)
│   ├── requirements.txt
│   └── run.py           # `python run.py` se server start
│
└── frontend/            # Plain HTML/CSS/JS — koi build step nahi chahiye
    ├── index.html
    ├── css/              # variables.css, layout.css, components.css
    └── js/               # config, api, nav, charts + har page ki alag file
```

## Kya real hai is project mein (fake mock-data nahi)

- Har number backend ke real CSV datasets (customer churn, employee HR
  attrition, retail/warehouse sales) se compute hota hai.
- **Database**: SQLite (`backend/data/app.db`) — har prediction run, scenario
  simulation aur upload database mein log hota hai. "Reports & History" page
  yeh real history dikhata hai.
- **RAG Knowledge Base**: `backend/data/knowledge/*.md` files mein asli
  computed insights likhe hain (jaise "Pune attrition 50.9%"), aur RAG agent
  in par persistent ChromaDB search karta hai. Gemini answers isi retrieved
  evidence par grounded hain, with local fallback when the provider is busy.
- **Forecasting**: Holt-Winters exponential smoothing (jab enough data ho),
  warna safe weighted-moving-average fallback — kabhi crash nahi karega.

---

## Kaise Run Karein

### 1. Backend start karo (pehle yeh)

```bash
cd backend
python -m venv venv                     # optional but recommended
source venv/bin/activate                # Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

Backend `http://127.0.0.1:8000` par chalega. Check karne ke liye browser
mein `http://127.0.0.1:8000/docs` kholo — Swagger UI mein saare endpoints
dikhenge aur wahin se test bhi kar sakte ho.

### 2. Frontend kholo (dusra terminal)

Sabse simple tarika — `frontend/index.html` ko seedha double-click karke
browser mein khol do. Backend `http://127.0.0.1:8000` par already CORS
allow karta hai (`allow_origins=["*"]`), isliye yeh direct file-open se bhi
chalega.

Agar aap ek local server se serve karna chahte ho (recommended, kuch
browsers file:// se fetch block karte hain):

```bash
cd frontend
python -m http.server 5500
```

Phir browser mein `http://127.0.0.1:5500` kholo.

### 3. Dono alag machine/host par deploy karna ho to

`frontend/index.html` ke `<head>` mein yeh line change kar do:

```html
<meta name="backend-url" content="https://your-backend-domain.com" />
```

---

## API Endpoints (backend)

| Method | Endpoint          | Kya karta hai |
|--------|-------------------|---------------|
| GET    | `/api/health`     | Backend zinda hai ya nahi |
| GET    | `/api/predict`    | Dashboard KPIs + forecast + decision (main endpoint) |
| GET    | `/api/analysis`   | Correlation, outliers, descriptive stats |
| GET    | `/api/scenario`   | Monte Carlo revenue simulation |
| POST   | `/api/upload`     | CSV upload → classify → DB me save |
| GET    | `/api/knowledge`  | RAG search (query param `q`) |
| GET    | `/api/history`    | Database se past runs |
| GET    | `/api/datasets`   | Available datasets ki list |

Poori interactive documentation: `http://127.0.0.1:8000/docs`

---

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy + SQLite, pandas, numpy, scikit-learn,
  statsmodels
- **Frontend**: Plain HTML/CSS/JS (no framework, no build step), Chart.js
  for graphs
- **Database**: SQLite (file-based, zero setup)

## Hackathon Demo Tips

1. Sabse pehle Dashboard page dikhao — real-time KPIs, forecast chart.
2. Data Upload page pe apni koi CSV daal ke dikhao ki backend usko
   auto-classify kar deta hai.
3. Scenario Simulator ke sliders move karke live Monte Carlo dikhao.
4. Knowledge Base me kuch pucho jaise "why do customers churn" — RAG agent
   se real answer aayega.
5. Reports page pe jitni baar tumne demo ke dauraan endpoints hit kiye
   honge, sab history yahan dikh jayegi — proof ki database sach me kaam
   kar raha hai.
