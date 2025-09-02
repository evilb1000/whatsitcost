import pandas as pd


def king_correct_unemployment_yoy_and_mom():
    path = "/Users/benatwood/PycharmProjects/WhatsItCost/AIBrain/theBehemoth.csv"

    # Load the Behemoth
    df = pd.read_csv(path)

    # Target series
    sid = "LNS14000000"
    sub_df = df[df["series_id"] == sid].copy()

    # Parse month number for sorting
    sub_df["month_num"] = sub_df["month"].str.extract(r"M(\d+)", expand=False).astype(int)
    sub_df = sub_df.sort_values(["year", "month_num"])

    values = sub_df["value"].values
    mom_point_change = [None] * len(values)
    yoy_point_change = [None] * len(values)

    # Point-over-month
    for i in range(1, len(values)):
        mom_point_change[i] = round(values[i] - values[i - 1], 4)

    # Point-over-year
    for i in range(12, len(values)):
        yoy_point_change[i] = round(values[i] - values[i - 12], 4)

    # Apply corrections
    df.loc[sub_df.index, "mom_growth"] = mom_point_change
    df.loc[sub_df.index, "yoy_growth"] = yoy_point_change

    # Save back to file
    df.to_csv(path, index=False)
    print(f"👑 The Behemoth now rules with corrected MoM + YoY % point changes for {sid}.")


# Run it
king_correct_unemployment_yoy_and_mom()
