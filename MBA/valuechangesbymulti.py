import pandas as pd

# === File path ===
csv_path = "/Users/benatwood/PycharmProjects/WhatsItCost/MBA/material_prices_mom.csv"

# === Target series IDs ===
target_series = [
    "WPU057303", "WPU1394", "WPU136", "WPU1361", "WPU1322",
    "WPU133", "WPU1331", "WPU1332", "WPU1333", "WPU1334",
    "WPU1335", "WPU1342", "WPU0721", "WPU1311", "WPU13710102",
    "WPU1392", "WPUSI004011", "WPU062101", "WPU1017", "WPU101706",
    "WPU102502", "WPU102501", "WPU1073", "WPU107405", "WPU1074051",
    "WPU10740514", "WPU10740553", "WPU107408", "WPU1076", "WPU1079",
    "WPU112", "WPU07120105"
]


# === Load and filter ===
df = pd.read_csv(csv_path)
df = df[df["Series ID"].isin(target_series)]

# === Create Date column ===
df["Date"] = pd.to_datetime(df["Year"].astype(str) + "-" + df["Month"].astype(str).str.zfill(2))

# === Grab latest date only ===
latest_date = df["Date"].max()
df = df[df["Date"] == latest_date]

# === Keep and reorder columns ===
columns_to_keep = [
    "Material", "Series ID", "Date", "Value", "MoM_Change", "YoY_Change", "Rolling_3Y_Avg_MoM"
]
df = df[columns_to_keep]

# === Sort from biggest loss to biggest gain ===
df = df.sort_values(by="MoM_Change")

# === Display settings ===
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.set_option('display.float_format', '{:.2f}'.format)

# === Display result ===
print(df)
