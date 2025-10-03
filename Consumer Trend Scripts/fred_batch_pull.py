import argparse
import csv
import os
import sys
from datetime import datetime
import requests

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


def fetch_fred_series(series_id: str, series_name: str, api_key: str, start_date: str) -> list:
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


def write_csv(rows: list, out_path: str) -> None:
    if not rows:
        # still write header for consistency
        with open(out_path, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["series_id", "series_name", "date", "value"])
            w.writeheader()
        return
    with open(out_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Batch pull FRED series to CSVs")
    parser.add_argument("--api-key", required=True, help="FRED API key")
    parser.add_argument("--start", default="1980-01-01", help="Observation start date YYYY-MM-DD (default: 1980-01-01)")
    parser.add_argument("--outdir", default=os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Consumer Trend Data")), help="Output directory (default: ../Consumer Trend Data)")
    args = parser.parse_args()

    ensure_dir(args.outdir)

    print(f"🚚 Pulling {len(SERIES_LIST)} FRED series starting {args.start}")
    print(f"📁 Output → {args.outdir}")

    ok = 0
    for series_id, name in SERIES_LIST:
        try:
            rows = fetch_fred_series(series_id, name, args.api_key, args.start)
            out_path = os.path.join(args.outdir, f"{series_id}.csv")
            write_csv(rows, out_path)
            print(f"✅ {series_id} — {len(rows)} rows → {out_path}")
            ok += 1
        except Exception as e:
            print(f"❌ {series_id} failed: {e}")

    print(f"🎉 Done. Successful: {ok}/{len(SERIES_LIST)}")
    return 0 if ok > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
