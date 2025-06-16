import os
import requests
import csv
from datetime import datetime

# BLS API key and endpoint
API_KEY = "f7be3dbe922e472aac4b08da9abf3aa3"
API_URL = "https://api.bls.gov/publicAPI/v2/timeseries/data/"

# Destination folder and time window
OUTPUT_FOLDER = "/Users/benatwood/PycharmProjects/WhatsItCost/ScrapedData"
END_YEAR = 2025
END_MONTH = "05"

# Legacy Series IDs and start dates
series_info = {
    "WPU062101": ("1980", "06"),
    "WPU101706": ("1982", "06"),
    "WPU102502": ("1983", "12"),
    "WPU107405": ("1981", "06"),
    "WPU107408": ("1983", "12"),
    "WPU1076": ("1980", "06"),
    "WPU1079": ("1981", "06"),
    "WPU1334": ("1980", "06"),
    "WPU1335": ("1980", "06"),
    "WPU1342": ("1984", "12"),
    "WPU13710102": ("1994", "02"),
    "WPU3012": ("2009", "06"),
    "WPU443": ("2009", "03"),
    "WPU4531": ("2009", "03"),
    "WPU4532": ("2009", "03"),
    "WPU80": ("2009", "06"),
    "WPU801": ("2009", "06"),
    "WPU801101": ("2004", "12"),
    "WPU801102": ("2005", "12"),
    "WPU801103": ("2006", "06"),
    "WPU801104": ("2007", "06"),
    "WPUFD4": ("2009", "11"),
    "WPUFD43": ("2009", "11"),
    "WPUFD431": ("2009", "11"),
    "WPUFD432": ("2009", "11")
}

# Collect and log data
all_data = []

for series_id, (start_year, start_month) in series_info.items():
    print(f"Fetching {series_id} from {start_year}-{start_month} to {END_YEAR}-{END_MONTH}...")

    payload = {
        "seriesid": [series_id],
        "startyear": start_year,
        "endyear": str(END_YEAR),
        "registrationkey": API_KEY
    }
    headers = {"Content-type": "application/json"}

    try:
        res = requests.post(API_URL, json=payload, headers=headers)
        res.raise_for_status()
        data = res.json()

        for series in data.get("Results", {}).get("series", []):
            for entry in series["data"]:
                entry_year = entry["year"]
                entry_month = entry["period"][1:]

                if (int(entry_year) > int(start_year)) or (
                        int(entry_year) == int(start_year) and int(entry_month) >= int(start_month)
                ):
                    row = {
                        "series_id": series_id,
                        "year": entry_year,
                        "month": entry_month,
                        "value": entry["value"]
                    }
                    all_data.append(row)
                    print(row)

    except Exception as e:
        print(f"❌ Failed to fetch {series_id}: {e}")

# Generate filename
earliest_year = min(int(v[0]) for v in series_info.values())
timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
filename = f"bls_scrape_{earliest_year}_to_{END_YEAR}_{timestamp}.csv"
filepath = os.path.join(OUTPUT_FOLDER, filename)

# Write to CSV
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
with open(filepath, mode="w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["series_id", "year", "month", "value"])
    writer.writeheader()
    writer.writerows(all_data)

print(f"\n✅ Saved {len(all_data)} records to {filepath}")
