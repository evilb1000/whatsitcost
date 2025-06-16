import pandas as pd

# === Load CSV ===
file_path = "/Users/benatwood/PycharmProjects/WhatsItCost/AIBrain/theBehemoth.csv"
df = pd.read_csv(file_path)

# === Clean and prep ===
df["series_id"] = df["series_id"].astype(str).str.strip()
df["month"] = df["month"].astype(str).str.extract(r"M(\d+)").astype(float)
df["year"] = pd.to_numeric(df["year"], errors="coerce")
df["mom_growth"] = pd.to_numeric(df["mom_growth"], errors="coerce")

# === Filter for WPU1017 where MoM growth > 7% (0.07) ===
subset = df[(df["series_id"] == "WPU1017") & (df["mom_growth"] > 0.07)]

# === Sort to find the 5 most recent ===
subset_sorted = subset.sort_values(by=["year", "month"], ascending=False).head(5)

# === Display results ===
if subset_sorted.empty:
    print("❌ No months found where WPU1017 MoM growth exceeded 7%")
else:
    print("✅ Last 5 times WPU1017 MoM growth exceeded 7%:")
    for _, row in subset_sorted.iterrows():
        print(f"• {int(row['month'])}/{int(row['year'])}: {round(row['mom_growth'] * 100, 2)}%")
