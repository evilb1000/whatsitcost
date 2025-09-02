import os
import sys
from pathlib import Path

import pandas as pd


def resolve_csv_path() -> Path:
    """
    Resolve the absolute path to AIBrain/theBehemoth.csv, preferring the
    known local absolute path, with a fallback to a repo-relative path.
    """
    candidates = [
        Path("/Users/benatwood/PycharmProjects/WhatsItCost/AIBrain/theBehemoth.csv"),
        Path(__file__).resolve().parent / "AIBrain" / "theBehemoth.csv",
    ]
    for p in candidates:
        if p.exists():
            return p
    raise FileNotFoundError("Could not locate AIBrain/theBehemoth.csv")


def load_series_last_13_months(series_id: str) -> pd.DataFrame:
    csv_path = resolve_csv_path()
    df = pd.read_csv(csv_path)

    # Normalize month and build a YYYY-MM date string consistent with pipeline usage
    df["month"] = df["month"].astype(str).str.replace("M", "", regex=False).str.zfill(2)
    df["Date"] = pd.to_datetime(df["year"].astype(str) + "-" + df["month"])

    # Filter requested series and sort by Date
    s = df[df["series_id"] == series_id].copy()
    if s.empty:
        return s

    s = s.sort_values("Date")

    # Keep last 13 observations
    s = s.tail(13)

    # Present clean columns
    s["date"] = s["Date"].dt.strftime("%Y-%m")
    cols = [
        "series_id",
        "series_name",
        "date",
        "value",
        "mom_growth",
        "yoy_growth",
    ]
    # Only include columns that exist
    cols = [c for c in cols if c in s.columns]
    return s[cols].reset_index(drop=True)


def main():
    # Fixed target per request; allow override via CLI for convenience
    target_series = "WPU057303"
    if len(sys.argv) > 1 and sys.argv[1].strip():
        target_series = sys.argv[1].strip()

    try:
        out = load_series_last_13_months(target_series)
    except FileNotFoundError as e:
        print(f"❌ {e}")
        sys.exit(1)

    if out.empty:
        print(f"No rows found for series_id '{target_series}'.")
        sys.exit(2)

    print(f"✅ Last 13 months for {target_series}:")
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()


