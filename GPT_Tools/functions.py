def get_latest_rolling_entry(material: str, dataset: dict):
    """
    Returns the latest (most recent date) entry from the rolling dataset for a given material.
    """
    records = dataset.get(material)
    if not records:
        return {"error": f"Material '{material}' not found"}

    try:
        latest = max(records, key=lambda x: x["Date"])
        return {
            "material": material,
            "date": latest["Date"],
            "MoM_3mo_avg": latest.get("MoM_3mo_avg"),
            "YoY_3mo_avg": latest.get("YoY_3mo_avg")
        }
    except Exception as e:
        return {"error": f"Failed to get latest entry: {e}"}
