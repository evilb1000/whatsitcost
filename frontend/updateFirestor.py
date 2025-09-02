import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore

# === PATHS ===
CSV_PATH = "/Users/benatwood/PycharmProjects/WhatsItCost/AIBrain/theBehemoth.csv"
SERVICE_ACCOUNT_PATH = "/Volumes/G-DRIVE ArmorATD/WebApp Keys/what-s-it-cost-firebase-adminsdk-fbsvc-79c6da2352.json"

# === FIRESTORE INIT ===
cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
firebase_admin.initialize_app(cred)
db = firestore.client()

# === LOAD AND PROCESS CSV ===
df = pd.read_csv(CSV_PATH)
df["month"] = df["month"].str.replace("M", "").str.zfill(2)
df["Date"] = pd.to_datetime(df["year"].astype(str) + "-" + df["month"])
df = df.sort_values(["series_id", "Date"])

unemp_id = "LNS14000000"

# Copy existing columns so we don't nuke unemployment values
df["mom_growth"] = df["mom_growth"]
df["yoy_growth"] = df["yoy_growth"]

# Get mask of all rows NOT in unemployment series
non_unemp_mask = df["series_id"] != unemp_id

# Do the calculation ONLY for non-unemployment rows
df.loc[non_unemp_mask, "mom_growth"] = (
    df[non_unemp_mask].groupby("series_id")["value"].pct_change() * 100
)
df.loc[non_unemp_mask, "yoy_growth"] = (
    df[non_unemp_mask].groupby("series_id")["value"].pct_change(periods=12) * 100
)




# === GET LAST 36 OBS PER SERIES ===
latest_36 = df.groupby("series_id").tail(36)

# === FORMAT AND UPLOAD ===
for series_id, group in latest_36.groupby("series_id"):
    data = []
    name = group["series_name"].iloc[0]
    for _, row in group.sort_values("Date").iterrows():
        data.append({
            "date": row["Date"].strftime("%Y-%m-%d"),  # Use full date format for proper parsing
            "value": row["value"],
            "mom_growth": None if pd.isna(row["mom_growth"]) else round(row["mom_growth"], 2),
            "yoy_growth": None if pd.isna(row["yoy_growth"]) else round(row["yoy_growth"], 2)
        })

    doc_data = {
        "series_id": series_id,
        "series_name": name,
        "observations": data
    }

    db.collection("materialTrends").document(series_id).set(doc_data)

print("✅ Uploaded all series to Firestore (materialTrends)")
