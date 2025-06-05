import requests
import csv

# === CONFIGURE THIS FOR EACH RUN ===
SERIES_ID = "PCU23822X23822X"
START_YEAR = 2008
END_YEAR = 2025
API_KEY = "f7be3dbe922e472aac4b08da9abf3aa3"
OUTPUT_PATH = f"/Users/benatwood/PycharmProjects/WhatsItCost/ScrapedData/scrapedSeries/{SERIES_ID.strip()}_raw.csv"

# === BLS API PULL ===
def pull_series_data(series_id, start_year, end_year):
    url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
    payload = {
        "seriesid": [series_id],
        "startyear": str(start_year),
        "endyear": str(end_year),
        "registrationkey": API_KEY
    }
    res = requests.post(url, json=payload)
    data = res.json()
    output = []

    if "Results" in data:
        for entry in data["Results"]["series"][0]["data"]:
            if entry["period"].startswith("M"):
                output.append({
                    "series_id": series_id.strip(),
                    "year": int(entry["year"]),
                    "month": entry["period"],
                    "value": float(entry["value"]),
                    "mom_growth": None,
                    "yoy_growth": None
                })
    return sorted(output, key=lambda x: (x["year"], x["month"]))

# === SAVE TO CSV ===
def save_to_csv(data, path):
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

# === RUN ===
data = pull_series_data(SERIES_ID, START_YEAR, END_YEAR)
save_to_csv(data, OUTPUT_PATH)
print(f"✅ Saved {len(data)} records for {SERIES_ID.strip()} to {OUTPUT_PATH}")
