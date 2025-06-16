import pandas as pd
import requests
import math

# === CONFIG ===
API_KEY = "f7be3dbe922e472aac4b08da9abf3aa3"
BHEMOTH_PATH = "/Users/benatwood/PycharmProjects/WhatsItCost/AIBrain/theBehemoth.csv"
TARGET_YEAR = 2025
TARGET_MONTH = "M05"
CHUNK_SIZE = 25

# === Load existing data ===
behemoth = pd.read_csv(BHEMOTH_PATH)
existing_keys = set(zip(behemoth['series_id'], behemoth['year'], behemoth['month']))
unique_series_ids = behemoth['series_id'].unique().tolist()

# === Pull May 2025 for a chunk of series ===
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
    new_rows = []

    if "Results" in data:
        for series in data["Results"]["series"]:
            sid = series["seriesID"]
            for item in series["data"]:
                if item["period"] == TARGET_MONTH and int(item["year"]) == TARGET_YEAR:
                    key = (sid, int(item["year"]), item["period"])
                    if key not in existing_keys:
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
                        print(f"🆕 New row fetched: {sid} - {item['year']} {item['period']} = {item['value']}")
                        new_rows.append(new_row)
    return new_rows

# === Chunked Execution ===
print(f"📡 Fetching May {TARGET_YEAR} values in chunks of {CHUNK_SIZE}...")

all_new_rows = []
for i in range(0, len(unique_series_ids), CHUNK_SIZE):
    chunk = unique_series_ids[i:i+CHUNK_SIZE]
    new_rows = fetch_chunk(chunk)
    all_new_rows.extend(new_rows)
    print(f"✅ Chunk {i//CHUNK_SIZE + 1}: {len(new_rows)} new records")

# === Inject and Save ===
if all_new_rows:
    new_df = pd.DataFrame(all_new_rows)
    updated_df = pd.concat([behemoth, new_df], ignore_index=True)
    updated_df.to_csv(BHEMOTH_PATH, index=False)
    print(f"\n✅ Total Injected: {len(new_df)} new records into theBehemoth.csv")
else:
    updated_df = behemoth.copy()
    print("\n🟡 No new data to inject — May 2025 already complete.")

# === Check for May 2025 Presence Post-Save ===
post_df = pd.read_csv(BHEMOTH_PATH)
may_rows = post_df[(post_df['year'] == 2025) & (post_df['month'] == 'M05')]
print(f"🔎 Confirmed in file: {len(may_rows)} total May 2025 rows")

# === Final Step: Recalculate Growth ===
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
print("📈 Growth fields updated (MoM + YoY)")
