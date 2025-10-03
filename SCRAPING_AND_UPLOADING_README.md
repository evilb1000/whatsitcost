# Scraping and Uploading Process Documentation

## Overview
This document explains our complete data pipeline from scraping BLS (Bureau of Labor Statistics) data to making it available in our web application and AI system.

## Data Sources

### Primary Source: Bureau of Labor Statistics (BLS)
- **Website**: https://www.bls.gov/
- **Data Type**: Producer Price Index (PPI) and Consumer Price Index (CPI) data
- **Format**: CSV files with monthly pricing data
- **Update Frequency**: Monthly (typically released mid-month for previous month)

## Scraping Process

### Main Scraping Scripts

#### 1. `Scrapers/MasterScraper.py`
- **Purpose**: Primary scraper that orchestrates the entire scraping process
- **Function**: Downloads the latest BLS data files and processes them
- **Output**: Raw CSV files in `ScrapedData/scrapedSeries/`

#### 2. `Scrapers/MasterChunkScraper.py`
- **Purpose**: Handles large-scale scraping operations
- **Function**: Processes data in chunks for better performance
- **Use Case**: When scraping multiple years of historical data

#### 3. `Scrapers/Master_updater.py`
- **Purpose**: Updates existing data with new monthly releases
- **Function**: Incremental updates rather than full re-scraping
- **Efficiency**: Only downloads and processes new data

#### 4. `Scrapers/Behometh Injector.py`
- **Purpose**: Processes and consolidates scraped data
- **Function**: Combines multiple CSV files into the main dataset
- **Output**: Creates `AIBrain/theBehemoth.csv` (master dataset)

#### 5. `Scrapers/revisiontracker.py`
- **Purpose**: Tracks data revisions and updates
- **Function**: Maintains version control of scraped data
- **Output**: `AIBrain/revision_tracker.csv`

### Data Processing Scripts

#### 6. `theBehemoth.py`
- **Purpose**: Main data processing engine
- **Function**: Transforms raw scraped data into structured format
- **Output**: Processes data for AI consumption

#### 7. `material_map.py`
- **Purpose**: Creates mapping between material names and series IDs
- **Function**: Standardizes material naming across datasets
- **Output**: `AIBrain/material_map.json`

## Uploading Process

### Step 1: Data Processing and JSON Generation

#### AI Brain JSON Files
The following JSON files are generated for the AI system:

1. **`AIBrain/JSONS/material_trends.json`**
   - **Content**: 547 records of material trend data
   - **Purpose**: Provides trend analysis for materials
   - **Usage**: AI uses this for trend-based queries

2. **`AIBrain/JSONS/material_trendlines.json`**
   - **Content**: 80 records of material trendline data
   - **Purpose**: Chart visualization data
   - **Usage**: Powers the chart generation feature

3. **`AIBrain/JSONS/material_spikes.json`**
   - **Content**: 80 records of material spike data
   - **Purpose**: Identifies significant price movements
   - **Usage**: AI alerts for unusual price changes

4. **`AIBrain/JSONS/material_rolling.json`**
   - **Content**: 80 records of rolling average data
   - **Purpose**: Smoothed price trends
   - **Usage**: AI analysis of price stability

5. **`AIBrain/JSONS/material_rolling_12mo.json`**
   - **Content**: 80 records of 12-month rolling data
   - **Purpose**: Year-over-year comparisons
   - **Usage**: AI provides annual trend analysis

6. **`AIBrain/JSONS/material_rolling_3yr.json`**
   - **Content**: 80 records of 3-year rolling data
   - **Purpose**: Long-term trend analysis
   - **Usage**: AI provides multi-year insights

7. **`AIBrain/JSONS/material_correlations.json`**
   - **Content**: 80 records of material correlation data
   - **Purpose**: Identifies relationships between materials
   - **Usage**: AI suggests related materials and market connections

8. **`AIBrain/JSONS/latest_snapshot.json`**
   - **Content**: 7 records of current market snapshot
   - **Purpose**: Real-time market overview
   - **Usage**: AI provides current market status

9. **`AIBrain/JSONS/cluster_data.json`**
   - **Content**: 4 records of material cluster data
   - **Purpose**: Groups related materials
   - **Usage**: AI organizes materials by market segments

### Step 2: GitHub Upload
- **Repository**: https://github.com/evilb1000/whatsitcost
- **Location**: `AIBrain/JSONS/` directory
- **Process**: JSON files are committed and pushed to GitHub
- **Access**: Backend loads data from GitHub URLs

### Step 3: Firestore Upload

#### Frontend Data Upload
- **Script**: `frontend/updateFirestor.py`
- **Purpose**: Uploads processed data to Firestore for frontend consumption
- **Data**: Material trends, latest snapshots, and market data
- **Access**: Frontend components read from Firestore

#### Firestore Collections
1. **Material Trends**: Historical pricing data
2. **Latest Snapshots**: Current market status
3. **Market Clusters**: Grouped material data
4. **User Interactions**: Chat history and preferences

### Step 4: Backend Data Loading

#### Runtime Data Loading
The backend (`main.py`) loads data from multiple sources:

1. **GitHub JSONs**: 
   - Loads all 9 JSON files from GitHub URLs
   - Verifies data integrity and completeness
   - Creates material mapping for AI queries

2. **Material Map**:
   - Loads `material_map.json` for name resolution
   - Enables fuzzy matching and aliases
   - Powers the chart visualization system

3. **Data Verification**:
   - Checks for material presence across datasets
   - Validates data consistency
   - Reports loading status and errors

## Data Flow Summary

```
BLS Website → Scrapers → Raw CSV → Processing → JSON Files → GitHub → Backend
                                                      ↓
                                              Firestore → Frontend
```

## Update Schedule

### Monthly Process
1. **BLS Data Release** (mid-month)
2. **Run Master Scraper** to get latest data
3. **Process with theBehemoth.py** to generate JSONs
4. **Commit to GitHub** (auto-deploys backend)
5. **Update Firestore** with new data
6. **Verify AI System** is working with new data

### Automation
- **GitHub**: Auto-deploys backend when JSONs are updated
- **Render**: Backend automatically restarts with new data
- **Firestore**: Manual update via `updateFirestor.py`

## Key Files and Their Roles

| File | Purpose | Output |
|------|---------|--------|
| `MasterScraper.py` | Downloads BLS data | Raw CSV files |
| `theBehemoth.py` | Processes raw data | Structured datasets |
| `material_map.py` | Creates name mapping | `material_map.json` |
| `updateFirestor.py` | Uploads to Firestore | Firestore collections |
| `main.py` | Backend API | Loads from GitHub |

## Troubleshooting

### Common Issues
1. **BLS Website Changes**: Update scraper selectors
2. **Data Format Changes**: Modify processing scripts
3. **GitHub Access**: Check repository permissions
4. **Firestore Quotas**: Monitor usage limits
5. **Backend Crashes**: Check JSON file integrity

### Verification Steps
1. Check `AIBrain/revision_tracker.csv` for latest update
2. Verify JSON files are committed to GitHub
3. Test backend data loading in logs
4. Confirm Firestore collections are updated
5. Test AI queries and chart generation

## Dependencies

### Python Packages
- `requests`: HTTP requests for scraping
- `pandas`: Data processing and manipulation
- `firebase-admin`: Firestore integration
- `fastapi`: Backend API framework
- `openai`: AI integration

### External Services
- **BLS Website**: Data source
- **GitHub**: JSON file hosting
- **Firestore**: Frontend data storage
- **Render**: Backend hosting
- **Firebase Hosting**: Frontend hosting

---

*Last Updated: [Current Date]*
*Maintained by: Big Alpha Kings Development Team*





