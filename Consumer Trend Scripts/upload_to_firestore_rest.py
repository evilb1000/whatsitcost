#!/usr/bin/env python3
"""
Upload most recent FRED series data to Firestore using REST API
Creates "Consumer Spending Indicators" collection with latest row from each series
"""

import argparse
import csv
import os
import sys
from datetime import datetime
import requests


def get_latest_row_from_csv(file_path: str) -> dict:
    """Get the most recent row from a CSV file"""
    try:
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            if not rows:
                return {}
            
            # Sort by date to get the latest
            latest_row = max(rows, key=lambda x: x['date'])
            
            # Convert numeric fields
            for field in ['value', 'mom_change', 'yoy_change', 'rolling_12mo_change', 'mom_36mo_avg', 'mom_12mo_avg']:
                if field in latest_row and latest_row[field]:
                    try:
                        latest_row[field] = float(latest_row[field])
                    except ValueError:
                        latest_row[field] = None
            
            return latest_row
    except Exception as e:
        print(f"⚠️  Error reading {file_path}: {e}")
        return {}


def upload_to_firestore_rest(data: dict) -> bool:
    """Upload data to Firestore using REST API"""
    
    # Firebase project config
    project_id = "what-s-it-cost"
    collection_id = "Consumer Spending Indicators"
    
    # Generate document ID based on series_id
    doc_id = data.get('series_id', 'unknown')
    
    # Prepare document data
    doc_data = {
        **data,
        'upload_timestamp': datetime.now().isoformat(),
    }
    
    # Firestore REST API endpoint
    url = f"https://firestore.googleapis.com/v1/projects/{project_id}/databases/(default)/documents/{collection_id}/{doc_id}"
    
    # Convert to Firestore format
    firestore_doc = {
        "fields": {}
    }
    
    for key, value in doc_data.items():
        if value is None:
            continue
        
        if isinstance(value, str):
            firestore_doc["fields"][key] = {"stringValue": str(value)}
        elif isinstance(value, (int, float)):
            firestore_doc["fields"][key] = {"doubleValue": float(value)}
        elif isinstance(value, bool):
            firestore_doc["fields"][key] = {"booleanValue": value}
        else:
            firestore_doc["fields"][key] = {"stringValue": str(value)}
    
    # Make PATCH request to create/update document
    headers = {
        'Content-Type': 'application/json',
    }
    
    try:
        response = requests.patch(url, json=firestore_doc, headers=headers)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to upload {doc_id}: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Upload latest FRED data to Firestore via REST API")
    parser.add_argument("--datadir", 
                       default=os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Consumer Trend Data")),
                       help="Directory containing CSV files")
    parser.add_argument("--series", help="Upload specific series only")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be uploaded")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.datadir):
        print(f"❌ Data directory not found: {args.datadir}")
        return 1
    
    # Get CSV files to process
    csv_files = [f for f in os.listdir(args.datadir) if f.endswith('.csv')]
    if args.series:
        csv_files = [f"{args.series}.csv"] if f"{args.series}.csv" in csv_files else []
    
    if not csv_files:
        print(f"❌ No CSV files found")
        return 1
    
    print(f"📊 Processing {len(csv_files)} CSV files...")
    print(f"🎯 Target: Consumer Spending Indicators collection")
    
    success_count = 0
    
    for csv_file in sorted(csv_files):
        file_path = os.path.join(args.datadir, csv_file)
        latest_row = get_latest_row_from_csv(file_path)
        
        if not latest_row:
            print(f"⚠️  No data for {csv_file}")
            continue
        
        series_id = latest_row.get('series_id', csv_file.replace('.csv', ''))
        series_name = latest_row.get('series_name', series_id)
        date = latest_row.get('date', 'unknown')
        value = latest_row.get('value', 'unknown')
        
        print(f"📤 {series_id}: {series_name} | {date} | {value}")
        
        if args.dry_run:
            print(f"  🧪 DRY RUN - Would upload: {latest_row}")
        else:
            if upload_to_firestore_rest(latest_row):
                print(f"  ✅ Uploaded to Firestore")
                success_count += 1
            else:
                print(f"  ❌ Upload failed")
    
    if not args.dry_run:
        print(f"\n🎉 Upload complete! Success: {success_count}/{len(csv_files)}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
