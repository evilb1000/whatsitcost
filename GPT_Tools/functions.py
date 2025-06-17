import re

def get_latest_trend_entry(material: str, dataset: dict, date: str = "latest", field: str = None):
    """
    Returns the latest or date-specific entry from the trendline dataset for a given material.
    Each material maps to a list of date-stamped records.
    Optionally returns only a specific field (e.g., MoM or YoY).
    """
    records = dataset.get(material)
    if not records:
        return {"error": f"Material '{material}' not found in dataset."}

    # Ensure all entries have a valid 'Date' key
    dated_records = [r for r in records if "Date" in r and re.match(r"\d{4}-\d{2}", r["Date"])]
    if not dated_records:
        return {"error": f"No valid date entries found for '{material}'."}

    # Find the correct entry
    if date == "latest":
        target = max(dated_records, key=lambda r: r["Date"])
    else:
        target = next((r for r in dated_records if r["Date"] == date), None)
        if not target:
            return {"error": f"No entry found for date '{date}' in '{material}'."}

    if field:
        return {field: target.get(field)}
    return target


def get_trend_mom_summary(material: str, dataset: dict, date: str):
    """
    Returns the MoM and YoY values for a specific material and month from the trendline dataset.
    Expects dataset format:
    {
        "Material Name": [
            { "Date": "YYYY-MM", "MoM": float, "YoY": float },
            ...
        ]
    }
    """
    records = dataset.get(material)
    if not records:
        return {"error": f"Material '{material}' not found in dataset."}

    # Look for exact date match
    match = next((entry for entry in records if entry.get("Date") == date), None)
    if not match:
        return {"error": f"No data for '{material}' in {date}."}

    return {
        "Date": date,
        "MoM": match.get("MoM"),
        "YoY": match.get("YoY")
    }



def get_momentum(material: str, dataset: dict, date: str = None):
    """
    Returns momentum stats for a material: 3-month avg MoM/YoY change + latest single-month values.
    """
    stats = dataset.get(material)
    if not stats:
        return {"error": f"No momentum data found for '{material}'."}

    if date is None:
        # Just return the 3-month averages
        return {
            "3mo_avg_mom": stats.get("3mo_avg_mom"),
            "3mo_avg_yoy": stats.get("3mo_avg_yoy")
        }

    # Try to get specific month-level stats too
    monthly = stats.get("monthly", {}).get(date)
    if not monthly:
        return {
            "3mo_avg_mom": stats.get("3mo_avg_mom"),
            "3mo_avg_yoy": stats.get("3mo_avg_yoy"),
            "note": f"No specific monthly momentum available for {date}."
        }

    return {
        "3mo_avg_mom": stats.get("3mo_avg_mom"),
        "3mo_avg_yoy": stats.get("3mo_avg_yoy"),
        "monthly_mom": monthly.get("mom"),
        "monthly_yoy": monthly.get("yoy")
    }


def get_spikes(material: str, dataset: dict):
    """
    Returns a list of spike months for the given material, if any.
    """
    spikes = dataset.get(material)
    if not spikes:
        return {"note": f"No spikes detected for '{material}'."}
    return {"spike_months": spikes}


def get_volatility(material: str, dataset: dict):
    """
    Placeholder function — volatility.json is not currently implemented.
    """
    vol = dataset.get(material)
    if not vol:
        return {"note": f"No volatility data available for '{material}'."}
    return {"volatility_score": vol}
