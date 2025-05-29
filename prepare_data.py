import pandas as pd
import json

# === LOAD DATA ===
df = pd.read_csv("10_year_historic.csv")

# === FORMAT DATE ===
df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m")

# === PIVOT TO WIDE FORMAT ===
df_pivot = df.pivot(index="Date", columns="Series Name", values="Value")
df_pivot = df_pivot.sort_index()

# === CALCULATE MOM AND YOY ===
df_mom = df_pivot.pct_change() * 100
df_yoy = df_pivot.pct_change(periods=12) * 100

# === STRUCTURE INTO JSON ===
result = {}
for date in df_pivot.index:
    date_str = date.strftime("%Y-%m")
    result[date_str] = {}

    for series in df_pivot.columns:
        mom = df_mom.at[date, series] if pd.notna(df_mom.at[date, series]) else None
        yoy = df_yoy.at[date, series] if pd.notna(df_yoy.at[date, series]) else None

        if mom is not None or yoy is not None:
            result[date_str][series] = {
                "MoM": round(mom, 2) if mom is not None else None,
                "YoY": round(yoy, 2) if yoy is not None else None
            }

# === WRITE TO JSON ===
import pandas as pd
import json

# === LOAD CSV ===
df = pd.read_csv("10_year_historic.csv")
df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m")
df_pivot = df.pivot(index="Date", columns="Series Name", values="Value").sort_index()
df_mom = df_pivot.pct_change(fill_method=None) * 100
df_yoy = df_pivot.pct_change(periods=12, fill_method=None) * 100

# === material_trends.json (DATE-BASED STRUCTURE) ===
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
with open("material_trends.json", "w") as f:
    json.dump(material_trends, f, indent=2)
print("✅ material_trends.json")

# === material_trendlines.json (MATERIAL-BASED STRUCTURE) ===
trendlines = {}
for series in df_pivot.columns:
    trendlines[series] = []
    for date in df_pivot.index:
        date_str = date.strftime("%Y-%m")
        mom = df_mom.at[date, series]
        yoy = df_yoy.at[date, series]
        trendlines[series].append({
            "Date": date_str,
            "MoM": round(mom, 2) if pd.notna(mom) else None,
            "YoY": round(yoy, 2) if pd.notna(yoy) else None
        })
with open("material_trendlines.json", "w") as f:
    json.dump(trendlines, f, indent=2)
print("✅ material_trendlines.json")

# === material_spikes.json (Spike Events ±5%) ===
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
with open("material_spikes.json", "w") as f:
    json.dump(spikes, f, indent=2)
print("✅ material_spikes.json")

# === material_rolling.json (3-month Rolling Averages) ===
rolling = {}
df_mom_rolling = df_mom.rolling(3).mean()
df_yoy_rolling = df_yoy.rolling(3).mean()
for series in df_pivot.columns:
    rolling[series] = []
    for date in df_pivot.index:
        date_str = date.strftime("%Y-%m")
        mom = df_mom_rolling.at[date, series]
        yoy = df_yoy_rolling.at[date, series]
        if pd.notna(mom) or pd.notna(yoy):
            rolling[series].append({
                "Date": date_str,
                "MoM_3mo_avg": round(mom, 2) if pd.notna(mom) else None,
                "YoY_3mo_avg": round(yoy, 2) if pd.notna(yoy) else None
            })
with open("material_rolling.json", "w") as f:
    json.dump(rolling, f, indent=2)
print("✅ material_rolling.json")

# === material_correlations.json (Lag 0–3 MoM Correlations) ===
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
with open("material_correlations.json", "w") as f:
    json.dump(correlations, f, indent=2)
print("✅ material_correlations.json")
