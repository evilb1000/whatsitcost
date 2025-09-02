import requests
import pandas as pd
from datetime import datetime

# === CONFIG ===
API_KEY = "f7be3dbe922e472aac4b08da9abf3aa3"
SERIES_ID = "WPUFD43"
START_YEAR = 2022
END_YEAR = datetime.today().year  # pull through current year
BEHEMOTH_PATH = "/Users/benatwood/PycharmProjects/WhatsItCost/AIBrain/theBehemoth.csv"

# === Pull from BLS API ===
url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
payload = {
    "seriesid": [SERIES_ID],
    "startyear": str(START_YEAR),
    "endyear": str(END_YEAR),
    "registrationkey": API_KEY,
}
res = requests.post(url, json=payload)
res.raise_for_status()
data = res.json()

rows = []
for series in data.get("Results", {}).get("series", []):
    for item in series.get("data", []):
        if item.get("period", "").startswith("M") and item.get("period") != "M13":
            rows.append({
                "Date": pd.to_datetime(f"{item['year']}-{item['period'][1:]:0>2}-01"),
                "value_api": float(item["value"]),
            })

if not rows:
    raise SystemExit("No monthly data returned from BLS API.")

df_api = pd.DataFrame(rows).sort_values("Date")
df_api["mom_api"] = df_api["value_api"].pct_change()

# === Load Behemoth and filter same series/months ===
df_csv = pd.read_csv(BEHEMOTH_PATH)

# Parse Behemoth dates
df_csv = df_csv[df_csv["series_id"] == SERIES_ID].copy()
df_csv["month_num"] = df_csv["month"].astype(str).str.replace("M", "", regex=False).str.zfill(2)
df_csv["Date"] = pd.to_datetime(df_csv["year"].astype(str) + "-" + df_csv["month_num"] + "-01")
df_csv = df_csv[df_csv["Date"] >= pd.to_datetime(f"{START_YEAR}-01-01")].sort_values("Date")

# Ensure numeric
df_csv["value"] = pd.to_numeric(df_csv["value"], errors="coerce")

# Compute MoM from Behemoth values directly (ignore stored mom_growth to avoid scaling mismatches)
df_csv["mom_csv"] = df_csv["value"].pct_change()

# Keep only needed cols
df_csv = df_csv[["Date", "value", "mom_csv"]].rename(columns={"value": "value_csv"})

# === Merge API vs Behemoth on Date ===
cmp = pd.merge(df_api, df_csv, on="Date", how="inner").sort_values("Date")

# Add diffs and pretty month/year
cmp["Month"] = cmp["Date"].dt.strftime("%b")
cmp["Year"] = cmp["Date"].dt.year
cmp["value_diff"] = cmp["value_api"] - cmp["value_csv"]
cmp["mom_diff"] = cmp["mom_api"] - cmp["mom_csv"]

# === Display settings: no truncation, full precision ===
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.set_option("display.max_colwidth", None)
pd.set_option("display.float_format", None)

# === Output comparison ===
cols = ["Month", "Year", "value_api", "value_csv", "value_diff", "mom_api", "mom_csv", "mom_diff"]
print(cmp[cols])
