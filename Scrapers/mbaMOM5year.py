import pandas as pd

# === Input/output paths ===
INPUT_CSV = "/Users/benatwood/PycharmProjects/WhatsItCost/MBA/material_prices.csv"
OUTPUT_CSV = "/Users/benatwood/PycharmProjects/WhatsItCost/MBA/material_prices_mom.csv"

# === Load data ===
df = pd.read_csv(INPUT_CSV)

# === Normalize ===
df["Value"] = pd.to_numeric(df["Value"], errors="coerce")
df["Series ID"] = df["Series ID"].astype(str).str.strip()
df = df.dropna(subset=["Value"])

# === Sort for correct time order ===
df = df.sort_values(by=["Series ID", "Year", "Month"])

# === MoM % Change ===
df["MoM_Change"] = df.groupby("Series ID")["Value"].pct_change() * 100
df["MoM_Change"] = df["MoM_Change"].fillna(0.0)

# === YoY % Change (12 months back) ===
df["YoY_Change"] = df.groupby("Series ID")["Value"].pct_change(periods=12) * 100
df["YoY_Change"] = df["YoY_Change"].fillna(0.0)

# === Rolling Averages of MoM (%)
df["Rolling_1Y_Avg_MoM"] = df.groupby("Series ID")["MoM_Change"].transform(lambda x: x.rolling(window=12, min_periods=1).mean())
df["Rolling_2Y_Avg_MoM"] = df.groupby("Series ID")["MoM_Change"].transform(lambda x: x.rolling(window=24, min_periods=1).mean())
df["Rolling_3Y_Avg_MoM"] = df.groupby("Series ID")["MoM_Change"].transform(lambda x: x.rolling(window=36, min_periods=1).mean())

# === Calculate % change since Feb 2020 ===
feb_2020_vals = df[(df["Year"] == 2020) & (df["Month"] == 2)].set_index("Series ID")["Value"]
latest_vals = df.sort_values(by=["Year", "Month"]).groupby("Series ID").tail(1).set_index("Series ID")["Value"]
growth_since_feb2020 = ((latest_vals - feb_2020_vals) / feb_2020_vals) * 100
growth_since_feb2020.name = "Pct_Change_Since_Feb2020"
df = df.merge(growth_since_feb2020, how="left", left_on="Series ID", right_index=True)

# === Save result ===
df.to_csv(OUTPUT_CSV, index=False)
print(f"✅ Full dataset with rolling averages and Feb 2020 growth saved to: {OUTPUT_CSV}")
