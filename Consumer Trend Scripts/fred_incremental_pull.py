#!/usr/bin/env python3
"""
FRED Batch Puller - Incremental Update Version
Pulls only new data since last update, preserves historical data
"""

import argparse
import csv
import os
import sys
from datetime import datetime, timedelta
import requests
from pathlib import Path

FRED_BASE = "https://api.stlouisfed.org/fred/series/observations"

SERIES_LIST = [
    # id, human-friendly name
    ("TOTALSA", "Total Vehicle Sales (SAAR)"),
    ("RSAFS", "Advance Retail Sales: Retail Trade and Food Services"),
    ("RSXFS", "Advance Retail Sales: Retail Trade"),
    ("RSMVPD", "Advance Retail Sales: Motor Vehicle and Parts Dealers"),
    ("RSFSDP", "Advance Retail Sales: Food Services and Drinking Places"),
    ("RSFHFS", "Advance Retail Sales: Furniture and Home Furnishings Stores"),
    ("RSEAS", "Advance Retail Sales: Electronics and Appliance Stores"),
    ("HOUST", "New Privately-Owned Housing Units Started: Total Units"),
    ("GDP", "Gross Domestic Product (SAAR, Quarterly)"),
    ("UNRATE", "Unemployment Rate"),
    ("CPIAUCSL", "CPI-U: All Items"),
    ("PPIACO", "Producer Price Index: All Commodities"),
    ("DGS10", "10-Year Treasury Constant Maturity Rate (Daily)"),
    ("FEDFUNDS", "Federal Funds Effective Rate (Daily)"),
    ("PAYEMS", "All Employees: Total Nonfarm"),
    ("INDPRO", "Industrial Production Index: Total Index"),
    ("PCEPI", "Personal Consumption Expenditures: Chain-type Price Index"),
    ("UMCSENT", "University of Michigan: Consumer Sentiment"),
    ("FRGSHPUSM649NCIS", "Cass Freight Index: Shipments"),
    ("TTLCONS", "Total Construction Spending: Total Construction in the United States"),
]


def get_last_date_from_csv(file_path: str) -> str:
    """Get the last date from existing CSV file"""
    if not os.path.exists(file_path):
        return "1980-01-01"  # Start from beginning if no file exists
    
    try:
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            if not rows:
                return "1980-01-01"
            # Get last date and add 1 day for incremental pull
            last_date = max(row['date'] for row in rows)
            last_dt = datetime.strptime(last_date, '%Y-%m-%d')
            next_dt = last_dt + timedelta(days=1)
            return next_dt.strftime('%Y-%m-%d')
    except Exception as e:
        print(f"⚠️  Error reading {file_path}: {e}, starting from 1980-01-01")
        return "1980-01-01"


def fetch_fred_series(series_id: str, series_name: str, api_key: str, start_date: str) -> list:
    """Fetch FRED series data from start_date onwards"""
    params = {
        "series_id": series_id,
        "api_key": api_key,
        "file_type": "json",
        "observation_start": start_date,
    }
    resp = requests.get(FRED_BASE, params=params, timeout=60)
    resp.raise_for_status()
    data = resp.json()
    observations = data.get("observations", [])
    rows = []
    for obs in observations:
        date_str = obs.get("date")
        value_str = obs.get("value")
        # FRED uses "." for missing values
        if value_str is None or value_str == ".":
            continue
        try:
            value = float(value_str)
        except ValueError:
            continue
        rows.append({
            "series_id": series_id,
            "series_name": series_name,
            "date": date_str,
            "value": value,
        })
    return rows


def append_to_csv(new_rows: list, file_path: str) -> None:
    """Append new rows to existing CSV or create new file"""
    if not new_rows:
        return
    
    # Check if file exists to determine if we need headers
    file_exists = os.path.exists(file_path)
    
    with open(file_path, "a" if file_exists else "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(new_rows[0].keys()))
        if not file_exists:
            w.writeheader()
        w.writerows(new_rows)


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Incremental FRED series update")
    parser.add_argument("--api-key", required=True, help="FRED API key")
    parser.add_argument("--outdir", 
                       default=os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Consumer Trend Data")),
                       help="Output directory (default: ../Consumer Trend Data)")
    parser.add_argument("--force-full", action="store_true", 
                       help="Force full refresh from 1980-01-01 (replaces all data)")
    parser.add_argument("--series", help="Update specific series only")
    
    args = parser.parse_args()
    
    ensure_dir(args.outdir)
    
    series_to_process = SERIES_LIST
    if args.series:
        series_to_process = [(s_id, s_name) for s_id, s_name in SERIES_LIST if s_id == args.series]
        if not series_to_process:
            print(f"❌ Series '{args.series}' not found in list")
            return 1
    
    print(f"🚚 {'Full refresh' if args.force_full else 'Incremental update'} for {len(series_to_process)} FRED series")
    print(f"📁 Output → {args.outdir}")
    
    ok = 0
    for series_id, name in series_to_process:
        try:
            out_path = os.path.join(args.outdir, f"{series_id}.csv")
            
            if args.force_full:
                # Full refresh - start from 1980
                start_date = "1980-01-01"
                print(f"🔄 Full refresh: {series_id}")
            else:
                # Incremental - start from day after last date
                start_date = get_last_date_from_csv(out_path)
                print(f"📈 Incremental: {series_id} from {start_date}")
            
            # Fetch new data
            rows = fetch_fred_series(series_id, name, args.api_key, start_date)
            
            if args.force_full:
                # Replace entire file
                with open(out_path, "w", newline="") as f:
                    if rows:
                        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
                        w.writeheader()
                        w.writerows(rows)
                    else:
                        w = csv.DictWriter(f, fieldnames=["series_id", "series_name", "date", "value"])
                        w.writeheader()
            else:
                # Append new data
                append_to_csv(rows, out_path)
            
            print(f"✅ {series_id} — {len(rows)} new rows → {out_path}")
            ok += 1
            
        except Exception as e:
            print(f"❌ {series_id} failed: {e}")
    
    print(f"🎉 Done. Successful: {ok}/{len(series_to_process)}")
    return 0 if ok > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
