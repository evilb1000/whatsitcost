import pandas as pd

# Load CSV
df = pd.read_csv("/Users/benatwood/PycharmProjects/WhatsItCost/AIBrain/theBehemoth.csv")

# Format date
df["month"] = df["month"].astype(str).str.replace("M", "").str.zfill(2)
df["Date"] = pd.to_datetime(df["year"].astype(str) + "-" + df["month"])

# Force mom_growth to float
df["mom_growth"] = pd.to_numeric(df["mom_growth"], errors="coerce")

# Get latest observation per series
latest = df.sort_values(["series_id", "Date"]).groupby("series_id").tail(1)

# Categorize by decimal thresholds
up_1plus = latest[latest["mom_growth"] >= 0.01]
up_pos = latest[(latest["mom_growth"] > 0) & (latest["mom_growth"] < 0.01)]
no_change = latest[latest["mom_growth"] == 0]
down_neg = latest[(latest["mom_growth"] < 0) & (latest["mom_growth"] > -0.01)]
down_1plus = latest[latest["mom_growth"] <= -0.01]

# Output category counts
print("📊 Total unique series:", latest["series_id"].nunique())
print("📈 Rose ≥ 1% MoM:", len(up_1plus))
print("📈 Rose > 0% and < 1% MoM:", len(up_pos))
print("⚖️ No change MoM:", len(no_change))
print("📉 Dropped < 1% MoM:", len(down_neg))
print("📉 Dropped ≥ 1% MoM:", len(down_1plus))

# Top 5 risers
top_risers = latest.sort_values("mom_growth", ascending=False).head(5)
top_fallers = latest.sort_values("mom_growth", ascending=True).head(5)

# Ensure no truncation
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 1000)
pd.set_option("display.colheader_justify", 'left')
pd.set_option("display.float_format", '{:.2f}'.format)

# Output detailed top movers
print("\n🔥 Top 5 MoM Risers:")
print(top_risers[["series_id", "series_name", "Date", "mom_growth"]])

print("\n💀 Top 5 MoM Fallers:")
print(top_fallers[["series_id", "series_name", "Date", "mom_growth"]])
