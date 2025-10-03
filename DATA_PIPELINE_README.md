# 🚀 WhatsItCost Data Pipeline - Complete Guide

This document explains how data flows from the Bureau of Labor Statistics (BLS) API through your entire system to the frontend display.

## 📊 **Data Flow Overview**

```
BLS API → Raw CSV Files → theBehemoth.csv → JSON Processing → GitHub → Render Backend → Firestore → Frontend
```

---

## 🔍 **Phase 1: Data Collection (BLS Scraping)**

### **Individual Series Scraping**
**File**: `Scrapers/MasterScraper.py`
- **Purpose**: Scrapes individual BLS series one at a time
- **Input**: BLS API with specific `SERIES_ID`
- **Output**: Raw CSV files in `ScrapedData/scrapedSeries/`
- **Format**: `{SERIES_ID}_raw.csv`

**Configuration**:
```python
SERIES_ID = "PCU23822X23822X"  # Change for each run
START_YEAR = 2008
END_YEAR = 2025
API_KEY = "f7be3dbe922e472aac4b08da9abf3aa3"
```

**Data Structure**:
```csv
series_id,year,month,value,mom_growth,yoy_growth
PCU23822X23822X,2025,M01,123.45,,
PCU23822X23822X,2025,M02,124.67,,
```

### **Bulk Data Refresh**
**File**: `Scrapers/Behometh Injector.py`
- **Purpose**: Refreshes ALL series for a target year
- **Input**: BLS API for all series in chunks of 25
- **Output**: Updates `theBehemoth.csv` with fresh data
- **Trigger**: Manual execution or scheduled runs

**What It Does**:
1. Loads existing `theBehemoth.csv`
2. Fetches fresh data for target year (e.g., 2025)
3. Overwrites old values with new ones
4. Recalculates growth rates (MoM, YoY)

---

## 🗂️ **Phase 2: Data Consolidation**

### **The Master File: `theBehemoth.csv`**
**Location**: `AIBrain/theBehemoth.csv`
**Purpose**: Single source of truth for all construction material data

**Data Structure**:
```csv
series_id,year,month,value,mom_growth,yoy_growth,series_name
CES2000000001,2025,M01,4908.0,0.5,2.1,Construction Employment
WPU057303,2025,M01,3.45,-1.2,5.3,#2 Diesel Fuel
```

**Contains**:
- All BLS series IDs
- Monthly values from 1986-present
- Calculated month-over-month growth
- Calculated year-over-year growth
- Human-readable series names

---

## 🔄 **Phase 3: Data Processing & JSON Generation**

### **Main Processing Script**
**File**: `prepare_data.py`
**Purpose**: Converts `theBehemoth.csv` into multiple JSON files for the backend

**Generated Files**:
1. **`material_trends.json`** - Date-based material performance
2. **`material_trendlines.json`** - Series-based trend data
3. **`material_spikes.json`** - Anomaly detection (>5% changes)
4. **`material_rolling.json`** - 3-month rolling averages
5. **`material_rolling_12mo.json`** - 12-month rolling averages
6. **`material_rolling_3yr.json`** - 3-year rolling averages
7. **`material_correlations.json`** - Cross-material correlations
8. **`latest_snapshot.json`** - Executive summary data
9. **`cluster_data.json`** - Material grouping analysis

**Processing Logic**:
- Converts month format (M01 → 01)
- Creates date objects for sorting
- Calculates percentage changes
- Applies rolling averages
- Detects statistical spikes

---

## 🚀 **Phase 4: Automated Pipeline**

### **Master Updater**
**File**: `Scrapers/master_updater.py`
**Purpose**: Orchestrates the entire data pipeline automatically

**Pipeline Order**:
```python
pipeline_steps = [
    "Behometh Injector.py",           # Refresh BLS data
    "prepare_data.py",                # Generate JSONs
    "cluster_JSON_creator.py",        # Create material clusters
    "execsummary.py"                  # Generate executive summary
]
```

**What Happens**:
1. **Refreshes** all BLS data for current year
2. **Processes** data into JSON format
3. **Creates** material clusters and summaries
4. **Commits** all changes to Git automatically
5. **Pushes** to GitHub (triggers Render deployment)

**Git Auto-Commit**:
```bash
commit_msg = f"🧠 Auto-sync: BLS JSONs + Exec Summary [auto-sync-{timestamp}]"
```

---

## ☁️ **Phase 5: Data Distribution**

### **GitHub Storage**
**Location**: `AIBrain/JSONS/` directory
**Purpose**: Version-controlled storage accessible to Render backend

**Files Stored**:
- All processed JSON files
- Executive summaries
- Cluster data
- Historical snapshots

### **Render Backend Access**
**File**: `main.py`
**Purpose**: Serves data via FastAPI endpoints

**Data Loading**:
```python
BASE_URL = "https://raw.githubusercontent.com/evilb1000/whatsitcost/main/AIBrain/JSONS"
# Loads all JSON files from GitHub
```

**API Endpoints**:
- `/trends/{material}/{date}` - Material trends
- `/spikes/{material}` - Anomaly detection
- `/rolling/{material}` - Rolling averages
- `/gpt` - AI-powered analysis

---

## 🔥 **Phase 6: Frontend Data Sync**

### **Firestore Upload**
**File**: `frontend/updateFirestor.py`
**Purpose**: Syncs `theBehemoth.csv` to Firebase for frontend access

**Process**:
1. **Reads** `theBehemoth.csv`
2. **Processes** dates and growth calculations
3. **Uploads** to Firestore collection `materialTrends`
4. **Structures** data for frontend consumption

**Data Structure in Firestore**:
```json
{
  "series_id": "CES2000000001",
  "series_name": "Construction Employment",
  "observations": [
    {
      "date": "2025-07",
      "value": 4908.0,
      "mom_growth": 0.5,
      "yoy_growth": 2.1
    }
  ]
}
```

### **Frontend Display**
**File**: `frontend/src/components/MaterialTrends.jsx`
**Purpose**: Displays data from Firestore

**Data Flow**:
1. **Fetches** from Firestore `materialTrends` collection
2. **Processes** observations for display
3. **Shows** latest BLS month automatically
4. **Displays** material trends in organized tables

---

## ⚡ **How to Run the Pipeline**

### **Manual Execution**
```bash
# 1. Refresh BLS data
python Scrapers/Behometh\ Injector.py

# 2. Process into JSONs
python prepare_data.py

# 3. Create clusters and summaries
python GPT_Tools/cluster_JSON_creator.py
python Scrapers/execsummary.py

# 4. Sync to Firestore (for frontend)
cd frontend
python updateFirestor.py
```

### **Automated Pipeline**
```bash
# Run the complete pipeline
python Scrapers/master_updater.py
```

---

## 🔧 **Configuration & Dependencies**

### **Required API Keys**
- **BLS API**: `f7be3dbe922e472aac4b08da9abf3aa3`
- **OpenAI**: Set via `GPT_KEY` environment variable
- **Firebase**: Service account JSON file

### **File Paths**
- **CSV Storage**: `AIBrain/theBehemoth.csv`
- **JSON Output**: `AIBrain/JSONS/`
- **Raw Scraped Data**: `ScrapedData/scrapedSeries/`
- **Firebase Keys**: `/Volumes/G-DRIVE ArmorATD/WebApp Keys/`

### **Dependencies**
```bash
pip install pandas requests firebase-admin
npm install firebase
```

---

## 📈 **Data Refresh Schedule**

### **Recommended Frequency**
- **BLS Data**: Monthly (after BLS releases)
- **JSON Processing**: After each BLS update
- **Firestore Sync**: After JSON processing
- **Git Commits**: After successful pipeline completion

### **Automation Options**
- **Cron jobs** for scheduled updates
- **GitHub Actions** for automated deployments
- **Render webhooks** for backend updates

---

## 🚨 **Troubleshooting**

### **Common Issues**
1. **BLS API Limits**: 25 series per request, 500/day
2. **Date Format Errors**: Check month conversion (M01 → 01)
3. **Growth Calculation**: Ensure proper sorting before pct_change()
4. **Firestore Upload**: Verify service account permissions

### **Debug Commands**
```bash
# Check data integrity
python -c "import pandas as pd; df=pd.read_csv('AIBrain/theBehemoth.csv'); print(df.info())"

# Verify JSON generation
ls -la AIBrain/JSONS/

# Test Firestore connection
cd frontend && python updateFirestor.py
```

---

## 🎯 **Key Benefits of This Architecture**

1. **Single Source of Truth**: `theBehemoth.csv` contains all data
2. **Automated Processing**: Pipeline handles all transformations
3. **Version Control**: Git tracks all data changes
4. **Multiple Outputs**: JSONs for backend, Firestore for frontend
5. **Scalable**: Easy to add new series or modify processing
6. **Auditable**: Complete data lineage from BLS to frontend

---

**This pipeline ensures your construction material data flows seamlessly from BLS collection through analysis to user display, with full automation and version control.** 🚀





