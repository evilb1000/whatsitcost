#!/usr/bin/env python3
"""
Upload Consumer Spending Indicators to Firestore
Follows the same pattern as updateFirestor.py for materialTrends
"""

import argparse
import csv
import os
import sys
import pandas as pd
from datetime import datetime

# Firebase imports
try:
    import firebase_admin
    from firebase_admin import credentials, firestore
except ImportError:
    print("❌ Firebase admin not installed. Run: pip install firebase-admin")
    sys.exit(1)

# === CONFIGURABLE PATHS ===
# Default service account path (can be overridden via args)
DEFAULT_SERVICE_ACCOUNT = "/Volumes/G-DRIVE ArmorATD/WebApp Keys/what-s-it-cost-firebase-adminsdk-fbsvc-79c6da2352.json"


def initialize_firestore(service_account_path: str):
    """Initialize Firebase Admin SDK using service account"""
    try:
        # Use same pattern as updateFirestor.py
        cred = credentials.Certificate(service_account_path)
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred)
        return firestore.client()
    except Exception as e:
        print(f"❌ Error initializing Firebase: {e}")
        return None


def process_csv_files(data_dir: str, collection_name: str, db, dry_run: bool = False):
    """Process CSV files and upload to Firestore - following updateFirestor.py pattern"""
    
    csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
    if not csv_files:
        print(f"❌ No CSV files found in: {data_dir}")
        return False
    
    print(f"📊 Processing {len(csv_files)} CSV files...")
    
    for csv_file in sorted(csv_files):
        file_path = os.path.join(data_dir, csv_file)
        series_id = csv_file.replace('.csv', '')
        
        try:
            # Load CSV using pandas (same method as updateFirestor.py)
            df = pd.read_csv(file_path)
            
            # Get the LATEST observation only (most recent date)
            latest_row = df.sort_values('date').iloc[-1]
            
            series_name = latest_row['series_name']
            date = latest_row['date']
            value = latest_row['value']
            
            # Build observations array with just the latest data (following same structure)
            observations = [{
                "date": date,
                "value": float(value),
                "mom_change": None if pd.isna(latest_row.get('mom_change')) else round(float(latest_row.get('mom_change')), 4),
                "yoy_change": None if pd.isna(latest_row.get('yoy_change')) else round(float(latest_row.get('yoy_change')), 4),
                "rolling_12mo_change": None if pd.isna(latest_row.get('rolling_12mo_change')) else round(float(latest_row.get('rolling_12mo_change')), 4),
                "mom_36mo_avg": None if pd.isna(latest_row.get('mom_36mo_avg')) else round(float(latest_row.get('mom_36mo_avg')), 4),
                "mom_12mo_avg": None if pd.isna(latest_row.get('mom_12mo_avg')) else round(float(latest_row.get('mom_12mo_avg')), 4)
            }]
            
            doc_data = {
                "series_id": series_id,
                "series_name": series_name,
                "observations": observations
            }
            
            print(f"📤 {series_id}: {series_name} | {date} | {value}")
            
            if dry_run:
                print(f"  🧪 DRY RUN - Would upload: {doc_data}")
            else:
                # Upload using same pattern as updateFirestor.py
                db.collection(collection_name).document(series_id).set(doc_data)
                print(f"  ✅ Uploaded to Firestore")
                
        except Exception as e:
            print(f"❌ Error processing {csv_file}: {e}")
    
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Upload latest FRED data to Firestore")
    parser.add_argument("--datadir", 
                       default=os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Consumer Trend Data")),
                       help="Directory containing CSV files (default: ../Consumer Trend Data)")
    parser.add_argument("--collection", default="Consumer Spending Indicators",
                       help="Firestore collection name (default: Consumer Spending Indicators)")
    parser.add_argument("--service-account", default=DEFAULT_SERVICE_ACCOUNT,
                       help=f"Path to Firebase service account JSON (default: {DEFAULT_SERVICE_ACCOUNT})")
    parser.add_argument("--dry-run", action="store_true",
                       help="Show what would be uploaded without actually uploading")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.datadir):
        print(f"❌ Data directory not found: {args.datadir}")
        return 1
    
    if not os.path.exists(args.service_account):
        print(f"❌ Service account file not found: {args.service_account}")
        return 1
    
    if args.dry_run:
        # Initialize Firestore for dry run structure validation
        db = initialize_firestore(args.service_account)
        if not db:
            return 1
    
    print(f"🎯 Target: {args.collection} collection")
    
    if args.dry_run:
        print("🧪 DRY RUN MODE")
        success = process_csv_files(args.datadir, args.collection, None, dry_run=True)
    else:
        # Initialize Firestore
        db = initialize_firestore(args.service_account)
        if not db:
            return 1
        
        success = process_csv_files(args.datadir, args.collection, db, dry_run=False)
    
    if success:
        print(f"\n🎉 {'Validation complete!' if args.dry_run else 'Successfully uploaded to Firestore!'}")
        return 0
    else:
        print("💥 Process failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
