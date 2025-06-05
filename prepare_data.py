import pandas as pd
import json
import os

# === PATHS ===
INPUT_CSV = "/Users/benatwood/PycharmProjects/WhatsItCost/AIBrain/theBehemoth.csv"
OUTPUT_DIR = "/Users/benatwood/PycharmProjects/WhatsItCost/AIBrain/JSONS"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# === LOAD AND PREP DATA ===
df = pd.read_csv(INPUT_CSV)
df["month"] = df["month"].astype(str).str.replace("M", "").str.zfill(2)
df["Date"] = pd.to_datetime(df["year"].astype(str) + "-" + df["month"], format="%Y-%m")
df_pivot = df.pivot(index="Date", columns="series_name", values="value").sort_index()
df_mom = df_pivot.pct_change(fill_method=None) * 100
df_yoy = df_pivot.pct_change(periods=12, fill_method=None) * 100

# === material_trends.json ===
material_trends = {}
for date in df_pivot.index:
    date_str = date.strftime("%Y-%m")
    material_trends[date_str] = {}
    for series in df_pivot.columns:
        mom = df_mom.at[date, series]
        yoy = df_yoy.at[date, series]
        if pd.notna(mom) or pd.notna(yoy):
            material_trends[date_str][series] = {
                "MoM": round(mom, 2) if pd.notna(mom) else None,
                "YoY": round(yoy, 2) if pd.notna(yoy) else None
            }
with open(os.path.join(OUTPUT_DIR, "material_trends.json"), "w") as f:
    json.dump(material_trends, f, indent=2)
print("✅ material_trends.json")

# === material_trendlines.json ===
trendlines = {}
for series in df_pivot.columns:
    trendlines[series] = []
    series_mom = df_mom[series]
    series_yoy = df_yoy[series]
    for date in df_pivot.index:
        date_str = date.strftime("%Y-%m")
        mom = series_mom.at[date] if date in series_mom.index else None
        yoy = series_yoy.at[date] if date in series_yoy.index else None
        trendlines[series].append({
            "Date": date_str,
            "MoM": round(mom, 2) if pd.notna(mom) else None,
            "YoY": round(yoy, 2) if pd.notna(yoy) else None
        })
with open(os.path.join(OUTPUT_DIR, "material_trendlines.json"), "w") as f:
    json.dump(trendlines, f, indent=2)
print("✅ material_trendlines.json")

# === material_spikes.json ===
spikes = {}
threshold = 5
for series in df_pivot.columns:
    spikes[series] = []
    for date in df_pivot.index:
        date_str = date.strftime("%Y-%m")
        mom = df_mom.at[date, series]
        yoy = df_yoy.at[date, series]
        if pd.notna(mom) and abs(mom) >= threshold:
            spikes[series].append({ "Date": date_str, "Type": "MoM", "Change": round(mom, 2) })
        if pd.notna(yoy) and abs(yoy) >= threshold:
            spikes[series].append({ "Date": date_str, "Type": "YoY", "Change": round(yoy, 2) })
with open(os.path.join(OUTPUT_DIR, "material_spikes.json"), "w") as f:
    json.dump(spikes, f, indent=2)
print("✅ material_spikes.json")

# === material_rolling.json ===
rolling = {}
df_mom_rolling = df_mom.rolling(3).mean()
df_yoy_rolling = df_yoy.rolling(3).mean()
for series in df_pivot.columns:
    rolling[series] = []
    series_mom = df_mom_rolling[series].dropna()
    series_yoy = df_yoy_rolling[series].dropna()
    valid_dates = series_mom.index.union(series_yoy.index).sort_values()
    for date in valid_dates:
        mom = series_mom[date] if date in series_mom else None
        yoy = series_yoy[date] if date in series_yoy else None
        if pd.notna(mom) or pd.notna(yoy):
            rolling[series].append({
                "Date": date.strftime("%Y-%m"),
                "MoM_3mo_avg": round(mom, 2) if pd.notna(mom) else None,
                "YoY_3mo_avg": round(yoy, 2) if pd.notna(yoy) else None
            })
with open(os.path.join(OUTPUT_DIR, "material_rolling.json"), "w") as f:
    json.dump(rolling, f, indent=2)
print("✅ material_rolling.json")

# === material_correlations.json ===
correlations = {}
for base in df_pivot.columns:
    correlations[base] = {}
    for target in df_pivot.columns:
        if base == target:
            continue
        lags = {}
        for lag in range(0, 4):
            shifted = df_mom[target].shift(lag)
            corr = df_mom[base].corr(shifted)
            lags[f"lag_{lag}"] = round(corr, 3) if pd.notna(corr) else None
        correlations[base][target] = lags
with open(os.path.join(OUTPUT_DIR, "material_correlations.json"), "w") as f:
    json.dump(correlations, f, indent=2)
print("✅ material_correlations.json")

# === material_rolling_12mo.json ===
rolling_12mo = {}
df_mom_12mo = df_mom.rolling(12).mean()
df_yoy_12mo = df_yoy.rolling(12).mean()
for series in df_pivot.columns:
    rolling_12mo[series] = []
    series_mom = df_mom_12mo[series].dropna()
    series_yoy = df_yoy_12mo[series].dropna()
    valid_dates = series_mom.index.union(series_yoy.index).sort_values()
    for date in valid_dates:
        mom = series_mom[date] if date in series_mom else None
        yoy = series_yoy[date] if date in series_yoy else None
        if pd.notna(mom) or pd.notna(yoy):
            rolling_12mo[series].append({
                "Date": date.strftime("%Y-%m"),
                "MoM_12mo_avg": round(mom, 2) if pd.notna(mom) else None,
                "YoY_12mo_avg": round(yoy, 2) if pd.notna(yoy) else None
            })
with open(os.path.join(OUTPUT_DIR, "material_rolling_12mo.json"), "w") as f:
    json.dump(rolling_12mo, f, indent=2)
print("✅ material_rolling_12mo.json")


# === material_rolling_3yr.json ===
rolling_3yr = {}
df_mom_3yr = df_mom.rolling(36).mean()
df_yoy_3yr = df_yoy.rolling(36).mean()
for series in df_pivot.columns:
    rolling_3yr[series] = []
    series_mom = df_mom_3yr[series].dropna()
    series_yoy = df_yoy_3yr[series].dropna()
    valid_dates = series_mom.index.union(series_yoy.index).sort_values()
    for date in valid_dates:
        mom = series_mom[date] if date in series_mom else None
        yoy = series_yoy[date] if date in series_yoy else None
        if pd.notna(mom) or pd.notna(yoy):
            rolling_3yr[series].append({
                "Date": date.strftime("%Y-%m"),
                "MoM_3yr_avg": round(mom, 2) if pd.notna(mom) else None,
                "YoY_3yr_avg": round(yoy, 2) if pd.notna(yoy) else None
            })
with open(os.path.join(OUTPUT_DIR, "material_rolling_3yr.json"), "w") as f:
    json.dump(rolling_3yr, f, indent=2)
print("✅ material_rolling_3yr.json")
