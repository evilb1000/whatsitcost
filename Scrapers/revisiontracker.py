import requests
import pandas as pd
from pathlib import Path
from datetime import datetime

# === CONFIG ===
API_KEY = "f7be3dbe922e472aac4b08da9abf3aa3"
BEHEMOTH_PATH = Path("/Users/benatwood/PycharmProjects/WhatsItCost/AIBrain/theBehemoth.csv")

# === OUTPUTS (same folder as Behemoth) ===
OUT_DIR = BEHEMOTH_PATH.parent
TRACKER_PATH = OUT_DIR / "revision_tracker.csv"                 # long-form vintages
RUN_TAG = datetime.now().strftime("%Y-%m-%d")                   # snapshot/vintage id for this run
CHUNK_SIZE = 40

# === 1) Read Behemoth to get series list (+ names) ===
behemoth = pd.read_csv(BEHEMOTH_PATH, dtype={"series_id": str})
series_meta = (
    behemoth[["series_id", "series_name"]]
    .drop_duplicates()
    .sort_values("series_id")
    .reset_index(drop=True)
)
series_ids = series_meta["series_id"].tolist()

# === 2) Pull latest monthly observation for each series from BLS ===
def fetch_latest_for_chunk(chunk_ids):
    url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
    payload = {
        "seriesid": chunk_ids,
        "startyear": "2000",     # wide window; we'll just take the latest obs per series
        "endyear": str(datetime.today().year),
        "registrationkey": API_KEY,
    }
    r = requests.post(url, json=payload, timeout=60)
    r.raise_for_status()
    data = r.json()
    out = []
    for series in data.get("Results", {}).get("series", []):
        sid = series.get("seriesID")
        # BLS returns reverse-chronological; find the first real monthly obs (M01..M12)
        latest_item = None
        for item in series.get("data", []):
            p = item.get("period", "")
            if p.startswith("M") and p != "M13" and item.get("value", "") != "":
                latest_item = item
                break
        if latest_item:
            year = int(latest_item["year"])
            month_num = int(latest_item["period"][1:])
            value = float(latest_item["value"])
            # preliminary flag via footnotes (code 'P')
            is_prelim = any((fn or {}).get("code") == "P" for fn in latest_item.get("footnotes", []))
            out.append({
                "series_id": sid,
                "date_ym": f"{year:04d}-{month_num:02d}",
                "value_latest": value,
                "is_prelim": is_prelim,
            })
    return out

rows = []
for i in range(0, len(series_ids), CHUNK_SIZE):
    chunk = series_ids[i:i+CHUNK_SIZE]
    rows.extend(fetch_latest_for_chunk(chunk))

if not rows:
    raise SystemExit("No data returned from BLS API.")

latest_df = pd.DataFrame(rows)
latest_df = latest_df.merge(series_meta, on="series_id", how="left")
latest_df["run_tag"] = RUN_TAG  # vintage identifier for this snapshot

# === 3) Append to revision tracker (do NOT overwrite prior vintages) ===
if TRACKER_PATH.exists():
    tracker = pd.read_csv(TRACKER_PATH, dtype={"series_id": str})
    tracker = pd.concat([tracker, latest_df], ignore_index=True)
else:
    tracker = latest_df.copy()

# Persist tracker with full precision; never drop history
tracker.to_csv(TRACKER_PATH, index=False, float_format="%.10f")

# === 4) Compare this run vs previous run to find revisions (side-by-side) ===
# Build a diff only if we have an earlier run_tag
run_tags = sorted(tracker["run_tag"].unique())
if len(run_tags) >= 2:
    prev_tag = run_tags[-2]
    curr_tag = run_tags[-1]

    prev = tracker[tracker["run_tag"] == prev_tag][["series_id", "date_ym", "value_latest", "is_prelim"]]
    curr = tracker[tracker["run_tag"] == curr_tag][["series_id", "date_ym", "value_latest", "is_prelim"]]

    cmp = curr.merge(prev, on=["series_id", "date_ym"], how="outer", suffixes=("_curr", "_prev"))
    cmp["value_delta"] = cmp["value_latest_curr"] - cmp["value_latest_prev"]

    # Optional: save a per-run diff report next to tracker
    diff_path = OUT_DIR / f"revision_changes_{curr_tag}_vs_{prev_tag}.csv"
    cmp.to_csv(diff_path, index=False, float_format="%.10f")

    # Print a quick, complete summary (no truncation)
    pd.set_option("display.max_rows", None)
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", None)
    pd.set_option("display.max_colwidth", None)
    pd.set_option("display.float_format", None)

    print(f"\nRevisions detected (current run {curr_tag} vs previous {prev_tag}):")
    print(cmp.sort_values(["date_ym","series_id"]))
else:
    print(f"Initialized tracker at {TRACKER_PATH}. Next run will produce a side-by-side revisions file.")
