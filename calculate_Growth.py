import csv

# === CONFIGURE ===
INPUT_PATH = "/Users/benatwood/PycharmProjects/WhatsItCost/ScrapedData/scrapedSeries/CES2000000001_raw.csv"

# === LOAD DATA ===
def load_csv(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))

# === GROWTH CALC ===
def calculate_growth(data):
    # Convert month label "M01" → 1 for easy sorting
    for row in data:
        row["month_num"] = int(row["month"].replace("M", ""))
        row["year"] = int(row["year"])
        row["value"] = float(row["value"])

    # Sort by date
    data.sort(key=lambda x: (x["year"], x["month_num"]))

    for i, row in enumerate(data):
        curr_val = row["value"]
        year = row["year"]
        month = row["month_num"]

        # MoM
        if i > 0:
            prev = data[i - 1]
            if prev["year"] * 12 + prev["month_num"] == year * 12 + month - 1:
                prev_val = prev["value"]
                row["mom_growth"] = round((curr_val - prev_val) / prev_val, 6)
            else:
                row["mom_growth"] = ""
        else:
            row["mom_growth"] = ""

        # YoY
        for j in range(i - 12, i):
            if j >= 0:
                prev = data[j]
                if prev["year"] == year - 1 and prev["month_num"] == month:
                    prev_val = prev["value"]
                    row["yoy_growth"] = round((curr_val - prev_val) / prev_val, 6)
                    break
        else:
            row["yoy_growth"] = ""

    return data

# === SAVE UPDATED FILE ===
def save_csv(data, path):
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["series_id", "year", "month", "value", "mom_growth", "yoy_growth"])
        writer.writeheader()
        for row in data:
            writer.writerow({
                "series_id": row["series_id"],
                "year": row["year"],
                "month": row["month"],
                "value": row["value"],
                "mom_growth": row["mom_growth"],
                "yoy_growth": row["yoy_growth"]
            })

# === RUN ===
data = load_csv(INPUT_PATH)
enriched = calculate_growth(data)
save_csv(enriched, INPUT_PATH)
print(f"✅ Updated file saved with MoM and YoY growth metrics at {INPUT_PATH}")
