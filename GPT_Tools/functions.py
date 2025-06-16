def get_latest_rolling_entry(material: str, dataset: dict, date: str = None, field: str = None):
    """
    Returns the latest or date-specific entry from the rolling dataset for a given material.
    Optionally returns only a specific field if requested.
    """
    print(f"🔍 Incoming request: material='{material}', date='{date}', field='{field}'")

    records = dataset.get(material)
    if not records:
        print(f"❌ Material not found in dataset: '{material}'")
        return {"error": f"Material '{material}' not found"}

    print(f"✅ Found {len(records)} records for '{material}'")

    try:
        if date:
            print(f"🔎 Searching for record with exact date: {date}")
            available_dates = [r["Date"] for r in records]
            print(f"📅 Available dates: {available_dates}")

            record = next((r for r in records if r["Date"] == date), None)

            if not record:
                print(f"❌ No matching date found for: {date}")
                return {"error": f"No data for {material} on {date}"}
            else:
                print(f"✅ Found record for date {date}: {record}")
        else:
            record = max(records, key=lambda x: x["Date"])
            print(f"🕓 No date provided, using latest: {record['Date']}")

        # Return requested field
        if field:
            value = record.get(field, "N/A")
            print(f"📌 Returning specific field '{field}': {value}")
            return {
                "material": material,
                "date": record["Date"],
                field: value
            }
        else:
            print("📌 Returning full record with MoM and YoY")
            return {
                "material": material,
                "date": record["Date"],
                "MoM_3mo_avg": record.get("MoM_3mo_avg"),
                "YoY_3mo_avg": record.get("YoY_3mo_avg")
            }

    except Exception as e:
        print(f"🔥 Exception caught: {e}")
        return {"error": f"Failed to get entry: {e}"}
