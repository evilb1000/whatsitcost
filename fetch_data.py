# fetch_data.py

import requests
import os

BASE_URL = "https://raw.githubusercontent.com/evilb1000/whatsitcost/main/AIBrain/JSONS"

# Maps the metric from GPT to its corresponding API path format
def metric_to_endpoint(metric, material):
    if metric == "yoy" or metric == "mom":
        return f"/trends/latest"
    elif metric == "rolling_12mo":
        return f"/rolling-12mo/{material}"
    elif metric == "rolling_3yr":
        return f"/rolling-3yr/{material}"
    elif metric == "rolling":
        return f"/rolling/{material}"
    elif metric == "trendline":
        return f"/trendline/{material}"
    elif metric == "spike":
        return f"/spikes/{material}"
    else:
        return None

# Makes a request to the GitHub-stored JSONS and fetches the relevant material data
def fetch_data(material: str, metric: str):
    try:
        if metric in ["yoy", "mom"]:
            # Trends are stored by date, not by material
            response = requests.get(f"{BASE_URL}/material_trends.json")
            response.raise_for_status()
            data = response.json()
            latest_date = sorted(data.keys())[-1]
            values = data.get(latest_date, {})
            return {
                "date": latest_date,
                "material": material,
                "value": values.get(material),
                "metric": metric
            }
        else:
            endpoint = metric_to_endpoint(metric, material)
            if not endpoint:
                return {"error": "Unsupported metric."}

            # Strip leading slash for direct GitHub access
            clean_path = endpoint.lstrip("/").replace("/", "_")
            url = f"{BASE_URL}/{clean_path}.json"
            response = requests.get(url)
            response.raise_for_status()
            return response.json()

    except Exception as e:
        print(f"❌ Failed to fetch data for {material} / {metric}: {e}")
        return {"error": str(e)}
