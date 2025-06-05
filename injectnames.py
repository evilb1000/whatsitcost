import os
import pandas as pd

# === CONFIG ===
mapping_file = "/Users/benatwood/PycharmProjects/WhatsItCost/DesiredSeries/seriesnamesupdate/nameinjector.csv"
data_folder = "/Users/benatwood/PycharmProjects/WhatsItCost/ScrapedData/scrapedSeries"

print(f"📂 Loading mapping file from: {mapping_file}")
mapping_df = pd.read_csv(mapping_file)
print(f"📄 Mapping file loaded. Columns: {list(mapping_df.columns)}")

# Normalize column names and values
mapping_df.columns = mapping_df.columns.str.strip().str.lower()
mapping_df["series_id"] = mapping_df["series_id"].str.upper()

if 'series_id' not in mapping_df.columns or 'series_name' not in mapping_df.columns:
    raise ValueError("❌ 'series_id' and/or 'series_name' columns are missing in mapping file")

series_map = dict(zip(mapping_df["series_id"], mapping_df["series_name"]))
print(f"🔢 Loaded {len(series_map)} series mappings.\n")

# === INJECT SERIES NAME ===
files_found = 0
files_modified = 0
for filename in os.listdir(data_folder):
    if not filename.endswith("_raw.csv"):
        continue

    files_found += 1
    series_id = filename.replace("_raw.csv", "").upper()
    file_path = os.path.join(data_folder, filename)

    print(f"🔍 Checking: {filename} (Series ID: {series_id})")

    if series_id not in series_map:
        print(f"   ⚠️ No match for {series_id} in mapping file. Skipping.")
        continue

    try:
        df = pd.read_csv(file_path)
        df["series_name"] = series_map[series_id]
        df.to_csv(file_path, index=False)
        print(f"   ✅ Injected '{series_map[series_id]}' into {filename}")
        files_modified += 1
    except Exception as e:
        print(f"   ❌ Failed to process {filename}: {e}")

print(f"\n🏁 Done. Processed {files_found} files, modified {files_modified}.")
