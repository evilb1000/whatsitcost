import os
import pandas as pd

# === CONFIG ===
data_dir = "/Users/benatwood/PycharmProjects/WhatsItCost/ScrapedData/scrapedSeries"
output_path = "/Users/benatwood/PycharmProjects/WhatsItCost/AIBrain/theBehemoth.csv"

# === COLLECT ALL _raw.csv FILES ===
all_dataframes = []

for filename in os.listdir(data_dir):
    if filename.endswith("_raw.csv"):
        path = os.path.join(data_dir, filename)
        try:
            df = pd.read_csv(path)
            all_dataframes.append(df)
            print(f"✅ Loaded {filename} with {len(df)} rows")
        except Exception as e:
            print(f"❌ Failed to load {filename}: {e}")

# === CONCATENATE & EXPORT ===
if all_dataframes:
    behemoth = pd.concat(all_dataframes, ignore_index=True)
    behemoth.to_csv(output_path, index=False)
    print(f"\n🧠 THE BEHEMOTH IS BORN: {output_path}")
    print(f"📈 Total rows: {len(behemoth)} across {len(all_dataframes)} files")
else:
    print("❌ No dataframes loaded. Check folder or file formatting.")
