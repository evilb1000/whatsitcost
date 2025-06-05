import requests
import csv
import time

# === CONFIGURE ===
SERIES_ID = "CES2000000001"
CHUNKS = [(1986, 1996), (1997, 2007), (2008, 2018), (2019, 2025)]
API_KEY = "f7be3dbe922e472aac4b08da9abf3aa3"
OUTPUT_PATH = f"/Users/benatwood/PycharmProjects/WhatsItCost/ScrapedData/scrapedSeries/{SERIES_ID.strip()}_raw.csv"

# === BLS API SINGLE CHUNK PULL ===
def pull_chunk(series_id, start, end):
    url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
    payload = {
        "seriesid": [series_id],
        "startyear": str(start),
        "endyear": str(end),
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
    return output

# === COMBINED CHUNK PULL ===
def pull_series_in_chunks(series_id, chunks):
    all_data = []
    for start, end in chunks:
        print(f"📦 Pulling {series_id} from {start} to {end}...")
        chunk_data = pull_chunk(series_id, start, end)
        all_data.extend(chunk_data)
        time.sleep(1)  # polite pause to avoid throttling
    return sorted(all_data, key=lambda x: (x["year"], x["month"]))

# === SAVE TO CSV ===
def save_to_csv(data, path):
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["series_id", "year", "month", "value", "mom_growth", "yoy_growth"])
        writer.writeheader()
        writer.writerows(data)

# === RUN ===
data = pull_series_in_chunks(SERIES_ID, CHUNKS)
save_to_csv(data, OUTPUT_PATH)
print(f"✅ Saved {len(data)} records for {SERIES_ID.strip()} to {OUTPUT_PATH}")
