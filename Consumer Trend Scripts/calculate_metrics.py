#!/usr/bin/env python3
"""
Calculate metrics for FRED series data
Adds: MoM change, Rolling 12-month change, 36-month MoM avg, 12-month MoM avg, YoY change
"""

import argparse
import csv
import os
import sys
from pathlib import Path
from typing import List, Dict, Optional
import pandas as pd


def load_csv(file_path: str) -> pd.DataFrame:
    """Load CSV and ensure proper data types"""
    df = pd.read_csv(file_path)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date').reset_index(drop=True)
    return df


def calculate_mom_change(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate month-over-month percentage change"""
    df['mom_change'] = df['value'].pct_change() * 100
    return df


def calculate_yoy_change(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate year-over-year percentage change (12 months prior)"""
    df['yoy_change'] = df['value'].pct_change(periods=12) * 100
    return df


def calculate_rolling_12mo_change(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate rolling 12-month percentage change"""
    df['rolling_12mo_change'] = df['value'].pct_change(periods=12) * 100
    return df


# === Percentage-point calculations for rate series (e.g., UNRATE) ===
def calculate_mom_change_points(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate month-over-month change in percentage points (simple diff)."""
    df['mom_change'] = df['value'].diff(1)
    return df


def calculate_yoy_change_points(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate year-over-year change in percentage points (simple 12-month diff)."""
    df['yoy_change'] = df['value'].diff(12)
    return df


def calculate_rolling_12mo_change_points(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate 12-month change in percentage points (alias of YoY diff)."""
    df['rolling_12mo_change'] = df['value'].diff(12)
    return df


def calculate_36mo_mom_avg(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate 36-month rolling average of MoM changes"""
    # Respect existing mom_change if already computed (e.g., UNRATE points)
    if 'mom_change' not in df.columns:
        df['mom_change'] = df['value'].pct_change() * 100
    df['mom_36mo_avg'] = df['mom_change'].rolling(window=36, min_periods=1).mean()
    return df


def calculate_12mo_mom_avg(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate 12-month rolling average of MoM changes"""
    # Respect existing mom_change if already computed (e.g., UNRATE points)
    if 'mom_change' not in df.columns:
        df['mom_change'] = df['value'].pct_change() * 100
    df['mom_12mo_avg'] = df['mom_change'].rolling(window=12, min_periods=1).mean()
    return df


def process_series(file_path: str) -> None:
    """Process a single CSV file and add calculated metrics"""
    print(f"📊 Processing: {os.path.basename(file_path)}")
    
    try:
        # Load data
        df = load_csv(file_path)
        
        if len(df) < 2:
            print(f"⚠️  Skipping {file_path} - insufficient data")
            return
        
        # Calculate all metrics
        filename = os.path.basename(file_path)
        is_unrate = filename.startswith('UNRATE')

        if is_unrate:
            # Use percentage-point changes for rates
            df = calculate_mom_change_points(df)
            df = calculate_yoy_change_points(df)
            df = calculate_rolling_12mo_change_points(df)
        else:
            # Default: percentage changes
            df = calculate_mom_change(df)
            df = calculate_yoy_change(df)
            df = calculate_rolling_12mo_change(df)

        # Rolling averages operate on MoM change regardless of units
        df = calculate_36mo_mom_avg(df)
        df = calculate_12mo_mom_avg(df)
        
        # Round to 4 decimal places for readability
        numeric_cols = ['mom_change', 'yoy_change', 'rolling_12mo_change', 'mom_36mo_avg', 'mom_12mo_avg']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = df[col].round(4)
        
        # Save back to CSV
        df.to_csv(file_path, index=False)
        print(f"✅ Updated: {os.path.basename(file_path)} ({len(df)} rows)")
        
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Calculate metrics for FRED series CSVs")
    parser.add_argument("--datadir", 
                       default=os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Consumer Trend Data")),
                       help="Directory containing CSV files (default: ../Consumer Trend Data)")
    parser.add_argument("--file", help="Process specific file only")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.datadir):
        print(f"❌ Data directory not found: {args.datadir}")
        return 1
    
    if args.file:
        # Process single file
        file_path = os.path.join(args.datadir, args.file)
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            return 1
        process_series(file_path)
    else:
        # Process all CSV files in directory
        csv_files = [f for f in os.listdir(args.datadir) if f.endswith('.csv')]
        if not csv_files:
            print(f"❌ No CSV files found in: {args.datadir}")
            return 1
        
        print(f"🚀 Processing {len(csv_files)} CSV files in: {args.datadir}")
        for csv_file in sorted(csv_files):
            file_path = os.path.join(args.datadir, csv_file)
            process_series(file_path)
    
    print("🎉 All calculations complete!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
