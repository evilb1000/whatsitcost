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
        # Always return full record, even if field was specified
        if field:
            print(f"📌 Field '{field}' was requested, but returning full record for GPT to interpret.")
        else:
            print("📌 No specific field requested. Returning full record.")

        return {
            "material": material,
            "date": record["Date"],
            "MoM_3mo_avg": record.get("MoM_3mo_avg"),
            "YoY_3mo_avg": record.get("YoY_3mo_avg")
        }


    except Exception as e:
        print(f"🔥 Exception caught: {e}")
        return {"error": f"Failed to get entry: {e}"}


def get_trend_mom_summary(material: str, dataset: dict, date: str = None):
    """
    Returns the MoM trend summary for a specific material and date from the material_trends.json dataset.
    """
    print(f"📈 [MoM] Requested material: '{material}', date: '{date}'")

    if not date:
        return {"error": "Date is required for MoM trend lookup."}

    data_for_date = dataset.get(date)
    if not data_for_date:
        print(f"❌ [MoM] No data available for date: {date}")
        return {"error": f"No data available for date: {date}"}

    material_data = data_for_date.get(material)
    if not material_data:
        print(f"❌ [MoM] Material '{material}' not found in data for {date}")
        return {"error": f"Material '{material}' not found in data for {date}"}

    print(f"✅ [MoM] Found MoM trend data for '{material}' on {date}: {material_data}")
    return {
        "material": material,
        "date": date,
        "MoM_change": material_data
    }
