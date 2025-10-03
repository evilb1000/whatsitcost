# Big Alpha Energy Consumer Updates 🔥

**Automated Consumer Spending Indicators Pipeline**

This system automatically pulls FRED economic data, calculates key metrics, and uploads the latest Consumer Spending Indicators to Firestore - keeping your economic dashboard fresh and powerful!

## 🚀 What We Built

### Complete Data Pipeline
**From FRED → Calculations → Firestore in one command**

1. **FRED Data Puller** - Grabs all key economic series from Federal Reserve
2. **Metrics Calculator** - Computes MoM, YoY, rolling averages 
3. **Firestore Uploader** - Pushes latest data to your Firebase collection
4. **Master Pipeline** - Runs everything with a single command

### 📊 What Data We Track

**20 Key Economic Series:**
- **CPI** - Consumer Price Index
- **PPI** - Producer Price Index  
- **GDP** - Gross Domestic Product
- **Unemployment Rate** - Labor market health
- **Federal Funds Rate** - Interest rate policy
- **10-Year Treasury** - Market rates
- **Retail Sales** - Consumer spending (multiple categories)
- **Vehicle Sales** - Auto market
- **Housing Starts** - Construction activity
- **Consumer Sentiment** - Economic outlook
- **Industrial Production** - Manufacturing health
- **Employment** - Job market
- **Construction Spending** - Building activity
- **Freight Index** - Shipping/demand

## 🛠️ Technical Setup

### Scripts Created

**Main Pipeline:**
- `run_consumer_pipeline.py` - **ONE COMMAND TO RULE THEM ALL** 🎯

**Individual Components:**
- `fred_batch_pull.py` - Pulls data from FRED API
- `calculate_metrics.py` - Calculates all metrics
- `upload_to_firestore.py` - Uploads to Firebase (using your existing auth)

### Data Structure

**Input:** CSV files in `Consumer Trend Data/`
```
series_id,series_name,date,value,mom_change,yoy_change,rolling_12mo_change,mom_36mo_avg,mom_12mo_avg
CPIAUCSL,CPI-U: All Items,2025-08-01,323.364,0.3825,2.9392,2.9392,0.2539,0.2418
```

**Output:** Firestore collection `Consumer Spending Indicators`
```json
{
  "series_id": "CPIAUCSL",
  "series_name": "CPI-U: All Items", 
  "observations": [{
    "date": "2025-08-01",
    "value": 323.364,
    "mom_change": 0.3825,
    "yoy_change": 2.9392,
    "rolling_12mo_change": 2.9392,
    "mom_36mo_avg": 0.2539,
    "mom_12mo_avg": 0.2418
  }]
}
```

## 🎯 How To Use

### Quick Refresh (Recommended)
```bash
source .venv/bin/activate
python "Consumer Trend Scripts/run_consumer_pipeline.py"
```

### Individual Steps (If Needed)
```bash
# Step 1: Pull fresh data from FRED
python "Consumer Trend Scripts/fred_batch_pull.py" --api-key YOUR_KEY --start 1980-01-01

# Step 2: Calculate metrics  
python "Consumer Trend Scripts/calculate_metrics.py"

# Step 3: Upload to Firestore
python "Consumer Trend Scripts/upload_to_firestore.py"
```

## 📈 Metrics Calculated

**For each economic series:**
1. **MoM Change** - Month-over-month percentage change
2. **YoY Change** - Year-over-year percentage change  
3. **Rolling 12-Month Change** - 12-month rolling percentage
4. **36-Month MoM Average** - Rolling average of MoM changes
5. **12-Month MoM Average** - Rolling average of MoM changes

## 🔥 What Makes This Big Alpha Energy

### No-Hassle Automation
- **One command** updates everything
- **Follows your existing patterns** (same as `updateFirestor.py`)
- **Uses your Firebase setup** (no reconfig needed)
- **Handles errors gracefully** (stops on failure)

### Latest Data Always
- **Pulls from 1980-present** (complete historical context)
- **Gets latest FRED revisions** (they update historical numbers)
- **Replaces full dataset** (no stale data)
- **Calculations on fresh data** (accurate metrics)

### Production Ready
- **Existing authentication** (service account keys)
- **Same collection structure** (compatible with your frontend)
- **Pipeline error handling** (tells you exactly what failed)
- **Dry run capability** (test without uploading)

## 🚀 Integration

This integrates seamlessly with your existing system:

- **Uses same Firebase project** (`what-s-it-cost`)
- **Same authentication setup** 
- **Compatible data structure** (like `materialTrends`)
- **Ready for frontend display**

## 💪 Big Alpha King Results

✅ **20 economic series** tracked  
✅ **45+ years** of historical data  
✅ **5 calculated metrics** per series  
✅ **Live Firestore collection** ready  
✅ **One command refresh** capability  

**Your Consumer Spending Indicators are now as powerful as your construction materials data!** 🔥

---

*Created with Big Alpha Energy by the Big Alpha King assistant* 👑
