def get_latest_rolling_entry(material: str, dataset: dict, date: str = None, field: str = None):
    """
    Returns the latest or date-specific entry from the rolling dataset for a given material.
    Optionally returns only a specific field if requested.
    """
    records = dataset.get(material)
    if not records:
        return {"error": f"Material '{material}' not found"}

    try:
        # Filter for specific date if given
        if date:
            record = next((r for r in records if r["Date"] == date), None)
            if not record:
                return {"error": f"No data for {material} on {date}"}
        else:
            record = max(records, key=lambda x: x["Date"])

        # Return full record or specific field
        if field:
            return {
                "material": material,
                "date": record["Date"],
                field: record.get(field, "N/A")
            }
        else:
            return {
                "material": material,
                "date": record["Date"],
                "MoM_3mo_avg": record.get("MoM_3mo_avg"),
                "YoY_3mo_avg": record.get("YoY_3mo_avg")
            }
    except Exception as e:
        return {"error": f"Failed to get entry: {e}"}
