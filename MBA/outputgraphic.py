import pandas as pd

# === File path ===
csv_path = "/Users/benatwood/PycharmProjects/WhatsItCost/MBA/material_prices_mom.csv"
output_path = "/Users/benatwood/PycharmProjects/WhatsItCost/MBA/June July BG.csv"

# === Target series IDs in exact display order ===
target_series = [
    "CUUR0000SA0", "WPUFD4", "WPUFD43", "WPUFD431", "WPUFD432",
    "WPU80", "WPU801", "WPU801101", "WPU801102", "WPU801103",
    "WPU801104", "WPU801105", "WPU802", "PCU23811X23811X", "PCU23816X23816X",
    "PCU23821X23821X", "PCU23822X23822X", "WPUIP231200", "WPU4531", "WPU4532",
    "WPU3012", "WPU057303", "WPU1394", "WPU136", "WPU1361", "WPU1322",
    "WPU133", "WPU1331", "WPU1332", "WPU1333", "WPU1334", "WPU1335",
    "WPU1342", "WPU0721", "WPU1311", "WPU13710102", "WPU1392", "WPUSI004011",
    "WPU062101", "WPU1017", "WPU101706", "WPU102502", "WPU102501", "WPU1073",
    "WPU107405", "WPU1074051", "WPU10740514", "WPU10740553", "WPU107408",
    "WPU1076", "WPU1079", "WPU112", "WPU07120105", "WPU058102", "WPU1321",
    "WPU1012", "WPU101212", "WPU102301"
]

# === Load and filter ===
df = pd.read_csv(csv_path)
df["Date"] = pd.to_datetime(df["Year"].astype(str) + "-" + df["Month"].astype(str).str.zfill(2))
df["Value"] = pd.to_numeric(df["Value"], errors="coerce")
df = df[df["Series ID"].isin(target_series)]

# === Grab latest date and Feb 2020 ===
latest_date = df["Date"].max()
feb_2020_date = pd.to_datetime("2020-02-01")

# === Group and calculate changes ===
results = []
for series_id in target_series:
    subset = df[df["Series ID"] == series_id].copy().sort_values("Date")
    latest_row = subset[subset["Date"] == latest_date]
    feb_2020_row = subset[subset["Date"] == feb_2020_date]

    if not latest_row.empty and not feb_2020_row.empty:
        latest_val = latest_row["Value"].values[0]
        feb_2020_val = feb_2020_row["Value"].values[0]
        change_from_feb2020 = ((latest_val - feb_2020_val) / feb_2020_val) * 100
    else:
        change_from_feb2020 = None

    final_row = subset[subset["Date"] == latest_date]
    if not final_row.empty:
        row = final_row.iloc[0]
        results.append({
            "Series ID": row["Series ID"],
            "Material": row.get("Material", ""),
            "Apr-2025": row["MoM_Change"],
            "May 2024": row["YoY_Change"],
            "Feb-2020": change_from_feb2020,
            "1Y Rolling Avg": row.get("Rolling_1Y_Avg_MoM", None),
            "2Y Rolling Avg": row.get("Rolling_2Y_Avg_MoM", None),
            "3Y Rolling Avg": row.get("Rolling_3Y_Avg_MoM", None)
        })

# === Output as DataFrame and export ===
final_df = pd.DataFrame(results)
final_df = final_df.set_index("Series ID").loc[target_series].reset_index()

# Save to CSV
final_df.to_csv(output_path, index=False)
print(f"✅ Exported to: {output_path}")
