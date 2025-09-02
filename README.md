# 🏗️ WhatsItCost - Construction Materials Market Intelligence Platform

A full-stack application combining a React frontend with a FastAPI backend, powered by GPT-4 for intelligent construction material market analysis.

## 🏗️ Architecture

- **Frontend**: React + Vite + Tailwind CSS, hosted on Firebase
- **Backend**: FastAPI + Python, hosted on Render
- **AI**: OpenAI GPT-4 integration for natural language queries
- **Data**: BLS (Bureau of Labor Statistics) API integration
- **Database**: Firestore for frontend data, GitHub for backend data storage

## 🚀 Quick Start

### Prerequisites
- **Node.js** (v18 or higher)
- **Python 3.12+**
- **OpenAI API Key** (for GPT functionality)

### 1. Clone and Setup
```bash
git clone https://github.com/evilb1000/whatsitcost.git
cd whatsitcost
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
**Frontend will be available at:** `http://localhost:5173/`

### 3. Backend Setup (Optional - Production backend is live)
```bash
# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set OpenAI API key
export GPT_KEY="your_openai_api_key_here"

# Run backend locally
python main.py
```
**Backend will be available at:** `http://localhost:8000/`

## 🔑 Environment Variables

### Required for Local Backend
```bash
export GPT_KEY="your_openai_api_key_here"
```

### Optional
```bash
export OPENAI_API_KEY="your_openai_api_key_here"  # Alternative to GPT_KEY
```

## 🌐 Production URLs

- **Frontend**: Firebase hosting (configured in `frontend/firebase.json`)
- **Backend**: `https://whatsitcost.onrender.com`
- **GitHub Data**: `https://raw.githubusercontent.com/evilb1000/whatsitcost/main/AIBrain/JSONS/`

## 📁 Project Structure

```
WhatsItCost/
├── frontend/                 # React frontend application
│   ├── src/                  # React source code
│   ├── public/               # Static assets
│   ├── package.json          # Frontend dependencies
│   ├── firebase.json         # Firebase configuration
│   └── vite.config.js        # Vite build configuration
├── main.py                   # FastAPI backend server
├── AIBrain/                  # Data storage and analysis
│   └── JSONS/                # Market data JSON files
├── GPT_Tools/                # AI and GPT integration tools
├── Scrapers/                 # BLS data collection scripts
├── MBA/                      # Market analysis tools
├── requirements.txt           # Python dependencies
└── .gitignore               # Git ignore rules
```

## 🧪 Development Workflow

### Frontend Development
```bash
cd frontend
npm run dev          # Start development server
npm run build        # Build for production
npm run preview      # Preview production build
```

### Backend Development
```bash
# The backend is primarily deployed on Render
# For local development, ensure environment variables are set
source .venv/bin/activate
python main.py
```

## 🔌 API Endpoints

### Core Endpoints
- `GET /` - Health check
- `GET /trends/{material}/{date}` - Material trends data
- `GET /spikes/{material}` - Price spike detection
- `GET /rolling/{material}` - Rolling averages
- `POST /gpt` - GPT-powered chat interface

### GPT Chat
The frontend includes a GPT chat assistant that connects to the backend for intelligent market analysis queries.

## 🚀 Deployment

### Frontend (Firebase)
```bash
cd frontend
npm run build
firebase deploy
```

### Backend (Render)
- Connected to GitHub repository
- Auto-deploys on push to main branch
- Environment variables configured in Render dashboard

## 🔧 Troubleshooting

### Frontend Won't Start
- Ensure Node.js is installed and up to date
- Clear `node_modules` and reinstall: `rm -rf node_modules && npm install`
- Check for port conflicts on 5173

### Backend Connection Issues
- Verify `GPT_KEY` environment variable is set
- Check if production backend is responding: `curl https://whatsitcost.onrender.com/`
- Ensure virtual environment is activated: `source .venv/bin/activate`

### GPT Integration Not Working
- Verify OpenAI API key is valid and has credits
- Check backend logs for API errors
- Ensure backend is accessible from frontend

### Automated Pipeline Issues
- **Import errors**: Check Python path in `GPT_Tools/cluster_JSON_creator.py`
- **Firestore sync fails**: Ensure `firebase-admin` is installed: `pip install firebase-admin`
- **Pipeline stops mid-way**: Check individual script outputs for specific errors
- **Data not updating**: Verify `theBehemoth.csv` has fresh data before running pipeline

## 🔄 Automated Data Pipeline

The platform features a fully automated data synchronization pipeline that ensures your frontend always displays the latest market data:

### Pipeline Steps (Automated)
1. **BLS Data Scraping** - Fresh data from Bureau of Labor Statistics
2. **Data Processing** - CSV to JSON conversion with trend analysis
3. **Cluster Analysis** - Material categorization and grouping
4. **Executive Summary** - Market snapshot generation
5. **🔥 Firestore Sync** - **Automatic frontend data update**

### Run the Full Pipeline
```bash
# One command updates everything from BLS to frontend
python Scrapers/master_updater.py
```

### Git Integration
The pipeline automatically commits changes with descriptive messages:
```bash
🧠 Auto-sync: BLS JSONs + Exec Summary + Firestore [auto-sync-20250829-1124]
```

**What happens automatically:**
- ✅ Scrapes fresh BLS data for all 558+ series
- ✅ Processes data into analysis-ready JSONs
- ✅ Updates Firestore with latest 36 observations per series
- ✅ Commits changes to Git with descriptive messages
- ✅ Pushes to GitHub for backup and collaboration

**No more manual Firestore updates!** Your frontend automatically stays in sync with the latest market data.

## 📊 Data Sources

- **BLS API**: Economic data and material prices (automated daily scraping)
- **GitHub**: JSON storage for processed market data + version control
- **Firestore**: Frontend data persistence (automatically synchronized)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test both frontend and backend
5. Submit a pull request

## 📞 Support

For issues or questions:
- **Email**: Ben@mbawpa.org
- **Repository**: https://github.com/evilb1000/whatsitcost

## 🎯 Key Features

- **Real-time market analysis** using GPT-4
- **Material price tracking** and trend analysis
- **Intelligent query processing** in natural language
- **Responsive web interface** with Tailwind CSS
- **Firebase hosting** for scalability
- **Render backend** for reliability
- **🔥 Automated data synchronization** - Frontend always shows latest BLS month
- **📅 Latest BLS Month Display** - Shows current data freshness (e.g., "Latest BLS Month: July 2025")
- **🔄 Zero-touch updates** - Run one command, everything stays in sync

---

**Happy coding! 🚀**
