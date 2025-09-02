import pandas as pd

# === File path ===
csv_path = "/Users/benatwood/PycharmProjects/WhatsItCost/MBA/material_prices_mom.csv"
output_path = "/Users/benatwood/PycharmProjects/WhatsItCost/MBA/SeptAugBG.csv"

# === Target series IDs in exact display order ===
target_series = [
"CUUR0000SA0","WPUFD4","WPUFD43","WPUFD431","WPUFD432","WPU80","WPU801","WPU801101","WPU801102","WPU801103","WPU801104","WPU801105","PCU23811X23811X",
"PCU23816X23816X","PCU23821X23821X","PCU23822X23822X","WPUIP231200","WPU4531","WPU4532","WPU3012","WPU057303","WPU1394","WPU1322",
"WPU133","WPU1332","WPU1342","WPU0721","WPU1311","WPU13710102","WPUSI004011","WPU062101","WPU1017","WPU102502","WPU102501","WPU1073","WPU107408","WPU1076","WPU1079",
"WPU058102"
]

# === Load and filter ===
df = pd.read_csv(csv_path)
print(f"📥 Loaded {len(df)} total rows from CSV.")

df["Date"] = pd.to_datetime(df["Year"].astype(str) + "-" + df["Month"].astype(str).str.zfill(2))
df["Value"] = pd.to_numeric(df["Value"], errors="coerce")
df = df[df["Series ID"].isin(target_series)]
print(f"🎯 Filtered to {len(df)} rows for {len(target_series)} target series.")

# === Grab latest date and Feb 2020 ===
latest_date = df["Date"].max()
feb_2020_date = pd.to_datetime("2020-02-01")
print(f"📅 Latest date in dataset: {latest_date.strftime('%Y-%m')}")
print(f"📅 Using Feb 2020 baseline for change calculations.")

# === Group and calculate changes ===
results = []
skipped_series = []

for series_id in target_series:
    subset = df[df["Series ID"] == series_id].copy().sort_values("Date")
    latest_row = subset[subset["Date"] == latest_date]
    feb_2020_row = subset[subset["Date"] == feb_2020_date]

    if not latest_row.empty and not feb_2020_row.empty:
        latest_val = latest_row["Value"].values[0]
        feb_2020_val = feb_2020_row["Value"].values[0]
        change_from_feb2020 = ((latest_val - feb_2020_val) / feb_2020_val) * 100
    else:
        print(f"⚠️ Skipping {series_id} due to missing data for latest or Feb 2020.")
        skipped_series.append(series_id)
        continue

    row = latest_row.iloc[0]
    results.append({
        "Series ID": row["Series ID"],
        "Material": row.get("Material", ""),
        "June-2025": row.get("MoM_Change", None),
        "July 2024": row.get("YoY_Change", None),
        "Feb-2020": change_from_feb2020,
        "1Y Rolling Avg": row.get("Rolling_1Y_Avg_MoM", None),
        "2Y Rolling Avg": row.get("Rolling_2Y_Avg_MoM", None),
        "3Y Rolling Avg": row.get("Rolling_3Y_Avg_MoM", None)
    })

# === Output as DataFrame and export ===
final_df = pd.DataFrame(results)

# Apply reindex safely — preserves order, inserts NaNs for missing series
final_df = final_df.set_index("Series ID").reindex(target_series).reset_index()

# Save to CSV
final_df.to_csv(output_path, index=False)
print(f"\n✅ Exported {len(final_df)} rows to: {output_path}")

# === Final debug ===
missing_series = set(target_series) - set(final_df["Series ID"].dropna())
if missing_series:
    print(f"🚨 Series missing from final output (NaN rows): {sorted(missing_series)}")
if skipped_series:
    print(f"⛔ Skipped during processing (missing data): {sorted(skipped_series)}")
