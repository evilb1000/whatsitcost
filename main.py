print("🔥 MAIN.PY LOADED")

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
from typing import Optional
import os
import requests
from GPT_Tools.functions import (
    get_latest_trend_entry,
    get_trend_mom_summary,
    get_momentum,
    get_spikes,
    get_volatility
)



# === Pydantic Models ===
class GPTQuery(BaseModel):
    material: str
    date: str
    metric: Optional[str] = None
    prompt: str

# === CONFIG ===
BASE_URL = "https://raw.githubusercontent.com/evilb1000/whatsitcost/main/AIBrain/JSONS"
client = OpenAI(api_key=os.getenv("GPT_KEY"))

app = FastAPI(title="Material Trends API")

# === Enable CORS ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Load JSON Helper ===
def load_json_from_github(url):
    try:
        print(f"📦 Loading: {url}")
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        print(f"✅ Loaded {len(data)} records from {url}")
        return data
    except Exception as e:
        print(f"❌ Error loading {url}: {e}")
        return {}

# === Load Data ===
print("🚚 Initializing dataset loading from GitHub...")
trends_by_date = load_json_from_github(f"{BASE_URL}/material_trends.json")
trendlines_by_material = load_json_from_github(f"{BASE_URL}/material_trendlines.json")
spikes_by_material = load_json_from_github(f"{BASE_URL}/material_spikes.json")
rolling_by_material = load_json_from_github(f"{BASE_URL}/material_rolling.json")
rolling_12mo_by_material = load_json_from_github(f"{BASE_URL}/material_rolling_12mo.json")
rolling_3yr_by_material = load_json_from_github(f"{BASE_URL}/material_rolling_3yr.json")
correlations_by_material = load_json_from_github(f"{BASE_URL}/material_correlations.json")
print("✅ Finished loading datasets.")

# === Aggregate Keys ===
all_keys = set()
check_material = "Precast Concrete Products"
print("🔍 Verifying material presence across datasets...")
for name, dataset in [
    ("Rolling", rolling_by_material),
    ("Trendlines", trendlines_by_material),
    ("Spikes", spikes_by_material),
    ("12mo", rolling_12mo_by_material),
    ("3yr", rolling_3yr_by_material),
    ("Correlations", correlations_by_material),
]:
    if check_material in dataset:
        print(f"🧱 Found '{check_material}' in {name}")
    else:
        print(f"⚠️ Missing '{check_material}' in {name}")
    all_keys.update(dataset.keys())

material_list = sorted(all_keys)
print(f"🧠 Final material list contains {len(material_list)} materials")

# === ROUTES ===

@app.get("/latest-trend/{material}")
def latest_trend(material: str):
    print(f"📈 Fetching latest trend entry for: {material}")
    return get_latest_trend_entry(material, trendlines_by_material)

@app.get("/")
def root():
    print("🌐 Root endpoint accessed")
    return {"message": "Material Trends API is live!"}

@app.get("/trends/{date}")
def get_trends_for_date(date: str):
    print(f"📅 Looking up trends for date: {date}")
    data = trends_by_date.get(date)
    if data is None:
        print(f"❌ No data for date: {date}")
        raise HTTPException(status_code=404, detail="Date not found")
    return data

@app.get("/trendline/{material}")
def get_trendline(material: str):
    print(f"📊 Getting trendline for: {material}")
    data = trendlines_by_material.get(material)
    if data is None:
        print(f"❌ No trendline found for: {material}")
        raise HTTPException(status_code=404, detail="Material not found")
    return data

@app.get("/spikes/{material}")
def get_spikes(material: str):
    print(f"📉 Checking for spikes in: {material}")
    data = spikes_by_material.get(material)
    if data is None:
        print(f"❌ No spike data found for: {material}")
        raise HTTPException(status_code=404, detail="Material not found")
    return data

@app.get("/rolling/{material}")
def get_rolling_avg(material: str):
    print(f"📊 Getting rolling average for: {material}")
    data = rolling_by_material.get(material)
    if data is None:
        print(f"❌ No rolling data found for: {material}")
        raise HTTPException(status_code=404, detail="Material not found")
    return data

@app.get("/rolling-12mo/{material}")
def get_rolling_12mo(material: str):
    print(f"📆 Getting 12-month rolling data for: {material}")
    data = rolling_12mo_by_material.get(material)
    if data is None:
        print(f"❌ No 12mo data found for: {material}")
        raise HTTPException(status_code=404, detail="Material not found")
    return data

@app.get("/rolling-3yr/{material}")
def get_rolling_3yr(material: str):
    print(f"📅 Getting 3-year rolling data for: {material}")
    data = rolling_3yr_by_material.get(material)
    if data is None:
        print(f"❌ No 3yr data found for: {material}")
        raise HTTPException(status_code=404, detail="Material not found")
    return data

@app.get("/correlations/{base}/{target}")
def get_correlation(base: str, target: str):
    print(f"🔗 Fetching correlation from {base} to {target}")
    base_data = correlations_by_material.get(base)
    if base_data is None or target not in base_data:
        print(f"❌ Correlation not found: {base} → {target}")
        raise HTTPException(status_code=404, detail="Correlation data not found")
    return base_data[target]

# === GPT Chat Endpoint ===

class GPTRequest(BaseModel):
    messages: list

@app.post("/gpt")
async def run_gpt(query: GPTQuery):
    print(f"🧠 GPT Query incoming: {query.dict()}")
    try:
        # === Updated Trend Entry ===
        tool_response = get_latest_trend_entry(
            material=query.material,
            dataset=trendlines_by_material,
            date=query.date,
            field=query.metric
        )
        print(f"🛠️ Trend Tool Output: {tool_response}")

        # === MoM Trend Summary ===
        trend_mom_response = get_trend_mom_summary(
            material=query.material,
            dataset=trends_by_date,
            date=query.date
        )
        print(f"📈 MoM Trend Output: {trend_mom_response}")

        # === Combine Outputs into One Payload ===
        combined_summary = {
            "trend_entry": tool_response,
            "mom_trend": trend_mom_response
        }


        # === GPT Call ===
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a highly skilled economic analyst specializing in construction materials. "
                        "Use the information from the tool output provided to answer user queries about price trends, "
                        "momentum, volatility, or co-movements of materials like precast concrete, diesel, steel, etc. "
                        "Speak clearly and directly, without hedging, and summarize in plain English."
                    )
                },
                {
                    "role": "user",
                    "content": query.prompt
                },
                {
                    "role": "assistant",
                    "content": f"Tool output: {combined_summary}"
                }
            ]
        )

        result = response.choices[0].message.content
        print(f"💬 GPT Response: {result}")
        return {"response": result}

    except Exception as e:
        print(f"🔥 GPT Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# === RESOLVE INTENT ===

class ResolveIntentRequest(BaseModel):
    user_input: str

from resolve_intent import resolve_intent as gpt_resolve_intent

@app.post("/resolve-intent")
def handle_resolve_intent(payload: ResolveIntentRequest):
    print(f"🔍 Resolving intent for: {payload.user_input}")
    result = gpt_resolve_intent(payload.user_input, material_list)

    material = result.get("material")
    metric = result.get("metric")
    print(f"🧠 Resolved → Material: {material}, Metric: {metric}")

    if not material or not metric:
        print(f"❌ Intent resolution failed for input: {payload.user_input}")
        raise HTTPException(status_code=400, detail="Intent could not be resolved.")

    metric_to_endpoint = {
        "yoy": f"/trends/{{DATE}}",
        "mom": f"/trends/{{DATE}}",
        "rolling": f"/rolling/{material}",
        "rolling_12mo": f"/rolling-12mo/{material}",
        "rolling_3yr": f"/rolling-3yr/{material}",
        "spike": f"/spikes/{material}",
        "trendline": f"/trendline/{material}"
    }

    endpoint = metric_to_endpoint.get(metric)
    if not endpoint:
        print(f"❌ Unknown metric: {metric}")
        raise HTTPException(status_code=400, detail=f"Unknown metric '{metric}'")

    print(f"🚀 GPT mapped '{payload.user_input}' → {endpoint}")
    return {"material": material, "metric": metric, "endpoint": endpoint}

from resolve_intent import resolve_intent
from fetch_data import fetch_data

class UserInputRequest(BaseModel):
    user_input: str

@app.post("/resolve-and-fetch")
def resolve_and_fetch(payload: UserInputRequest):
    print(f"🔍 Incoming query: {payload.user_input}")

    intent = resolve_intent(payload.user_input)
    material = intent.get("material")
    metric = intent.get("metric")

    print(f"🧩 Intent resolved → Material: {material}, Metric: {metric}")
    if not material or not metric:
        print("❌ Failed to resolve intent.")
        return {"error": "Failed to resolve intent", "raw_response": intent}

    data = fetch_data(material, metric)
    if data is None:
        print(f"❌ No data fetched for {material} | {metric}")
        return {"error": "Failed to fetch data from backend"}

    print(f"📦 Fetched data for {material} | {metric}")
    return {
        "material": material,
        "metric": metric,
        "data": data
    }

from explain_data import explain_data

class ExplainRequest(BaseModel):
    material: str
    metric: str

@app.post("/explain")
def explain(payload: ExplainRequest):
    print(f"📖 Explaining data for: {payload.material} | {payload.metric}")
    result = explain_data(payload.material, payload.metric)
    print(f"✅ Explanation generated.")
    return {"explanation": result}
