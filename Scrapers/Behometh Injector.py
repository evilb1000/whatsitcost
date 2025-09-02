import pandas as pd
import requests
import subprocess

# === CONFIG ===
API_KEY = "f7be3dbe922e472aac4b08da9abf3aa3"
BHEMOTH_PATH = "/Users/benatwood/PycharmProjects/WhatsItCost/AIBrain/theBehemoth.csv"
TARGET_YEAR = 2025
CHUNK_SIZE = 25

# === Load existing data ===
behemoth = pd.read_csv(BHEMOTH_PATH)
unique_series_ids = behemoth['series_id'].unique().tolist()

# === Pull all months from BLS for the target year ===
def fetch_chunk(chunk):
    url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
    payload = {
        "seriesid": chunk,
        "startyear": str(TARGET_YEAR),
        "endyear": str(TARGET_YEAR),
        "registrationkey": API_KEY
    }
    res = requests.post(url, json=payload)
    data = res.json()
    fresh_rows = []

    if "Results" in data:
        for series in data["Results"]["series"]:
            sid = series["seriesID"]
            for item in series["data"]:
                if item["period"][0] == "M" and item["value"] != "":
                    try:
                        series_name = behemoth[behemoth['series_id'] == sid]['series_name'].iloc[0]
                    except IndexError:
                        series_name = "UNKNOWN"
                    new_row = {
                        "series_id": sid,
                        "year": int(item["year"]),
                        "month": item["period"],
                        "value": float(item["value"]),
                        "mom_growth": None,
                        "yoy_growth": None,
                        "series_name": series_name
                    }
                    print(f"🔄 Refreshed: {sid} - {item['year']} {item['period']} = {item['value']}")
                    fresh_rows.append(new_row)
    return fresh_rows

# === Chunked API pull ===
print(f"📡 Refreshing ALL months in {TARGET_YEAR} for all series...")
all_fresh_rows = []

for i in range(0, len(unique_series_ids), CHUNK_SIZE):
    chunk = unique_series_ids[i:i+CHUNK_SIZE]
    fresh_rows = fetch_chunk(chunk)
    all_fresh_rows.extend(fresh_rows)
    print(f"✅ Chunk {i//CHUNK_SIZE + 1}: {len(fresh_rows)} refreshed")

# === Overwrite target year values in theBehemoth ===
if all_fresh_rows:
    fresh_df = pd.DataFrame(all_fresh_rows)

    # Drop old rows from target year for injected series_ids only
    target_series_ids = fresh_df['series_id'].unique()
    updated_df = behemoth[
        ~((behemoth['year'] == TARGET_YEAR) & (behemoth['series_id'].isin(target_series_ids)))
    ]

    # Append refreshed rows
    updated_df = pd.concat([updated_df, fresh_df], ignore_index=True)
    updated_df.to_csv(BHEMOTH_PATH, index=False)
    print(f"\n✅ Injected: {len(fresh_df)} refreshed records for {TARGET_YEAR}")
else:
    updated_df = behemoth.copy()
    print("\n🟡 No fresh data returned from API")

# === Verify ===
post_df = pd.read_csv(BHEMOTH_PATH)
count_rows = post_df[post_df['year'] == TARGET_YEAR].shape[0]
print(f"🔎 Verified: {count_rows} total rows in {TARGET_YEAR} now in theBehemoth.csv")

# === Recalculate Growth ===
def calculate_growth_fields(df):
    df = df.copy()
    df['month_num'] = df['month'].str.extract(r'M(\d+)', expand=False).astype(int)
    df = df.sort_values(by=['series_id', 'year', 'month_num'])

    df['mom_growth'] = None
    df['yoy_growth'] = None

    for sid, group in df.groupby('series_id'):
        group = group.sort_values(['year', 'month_num'])
        group['mom_growth'] = group['value'].pct_change()
        group['yoy_growth'] = group['value'].pct_change(12)
        df.loc[group.index, 'mom_growth'] = group['mom_growth']
        df.loc[group.index, 'yoy_growth'] = group['yoy_growth']

    df = df.drop(columns='month_num')
    return df

updated_df = calculate_growth_fields(post_df)
updated_df.to_csv(BHEMOTH_PATH, index=False)
print("📈 MoM and YoY growth recalculated")

# === Final Cleanup ===
print("🧹 Running unemployment cleanup script...")
subprocess.run([
    "python3",
    "/Users/benatwood/PycharmProjects/WhatsItCost/Scrapers/unemploymentcleanup.py"
])
