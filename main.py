from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os
import requests

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
        print(f"📦 Loading: {url}")  # 👈 LOG
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        print(f"✅ Loaded {len(data)} records from {url}")  # 👈 LOG
        return data
    except Exception as e:
        print(f"❌ Error loading {url}: {e}")  # 👈 LOG
        return {}

# === Load Data ===
trends_by_date = load_json_from_github(f"{BASE_URL}/material_trends.json")
trendlines_by_material = load_json_from_github(f"{BASE_URL}/material_trendlines.json")
spikes_by_material = load_json_from_github(f"{BASE_URL}/material_spikes.json")
rolling_by_material = load_json_from_github(f"{BASE_URL}/material_rolling.json")
rolling_12mo_by_material = load_json_from_github(f"{BASE_URL}/material_rolling_12mo.json")
rolling_3yr_by_material = load_json_from_github(f"{BASE_URL}/material_rolling_3yr.json")
correlations_by_material = load_json_from_github(f"{BASE_URL}/material_correlations.json")

# === Aggregate Keys ===
all_keys = set()
check_material = "Precast Concrete Products"  # 👈 LOG this specific one
for name, dataset in [
    ("Rolling", rolling_by_material),
    ("Trendlines", trendlines_by_material),
    ("Spikes", spikes_by_material),
    ("12mo", rolling_12mo_by_material),
    ("3yr", rolling_3yr_by_material),
    ("Correlations", correlations_by_material),
]:
    if check_material in dataset:
        print(f"🧱 Found '{check_material}' in {name}")  # 👈 LOG
    else:
        print(f"⚠️ Missing '{check_material}' in {name}")  # 👈 LOG
    all_keys.update(dataset.keys())

material_list = sorted(all_keys)
print(f"🧠 Final material list contains {len(material_list)} materials")  # 👈 LOG

# === ROUTES ===

@app.get("/")
def root():
    return {"message": "Material Trends API is live!"}

@app.get("/trends/{date}")
def get_trends_for_date(date: str):
    data = trends_by_date.get(date)
    if data is None:
        raise HTTPException(status_code=404, detail="Date not found")
    return data

@app.get("/trendline/{material}")
def get_trendline(material: str):
    data = trendlines_by_material.get(material)
    if data is None:
        raise HTTPException(status_code=404, detail="Material not found")
    return data

@app.get("/spikes/{material}")
def get_spikes(material: str):
    data = spikes_by_material.get(material)
    if data is None:
        raise HTTPException(status_code=404, detail="Material not found")
    return data

@app.get("/rolling/{material}")
def get_rolling_avg(material: str):
    data = rolling_by_material.get(material)
    if data is None:
        raise HTTPException(status_code=404, detail="Material not found")
    return data

@app.get("/rolling-12mo/{material}")
def get_rolling_12mo(material: str):
    data = rolling_12mo_by_material.get(material)
    if data is None:
        raise HTTPException(status_code=404, detail="Material not found")
    return data

@app.get("/rolling-3yr/{material}")
def get_rolling_3yr(material: str):
    data = rolling_3yr_by_material.get(material)
    if data is None:
        raise HTTPException(status_code=404, detail="Material not found")
    return data

@app.get("/correlations/{base}/{target}")
def get_correlation(base: str, target: str):
    base_data = correlations_by_material.get(base)
    if base_data is None or target not in base_data:
        raise HTTPException(status_code=404, detail="Correlation data not found")
    return base_data[target]

# === GPT Chat Endpoint ===

class GPTRequest(BaseModel):
    messages: list

@app.post("/gpt")
def chat_with_gpt(payload: GPTRequest):
    try:
        print("📨 Incoming GPT request:")  # 👈 LOG
        for msg in payload.messages:
            print(f"🗣️ {msg.get('content', '')[:100]}")  # 👈 LOG preview of each user message

        system_message = {
            "role": "system",
            "content": (
                "You are a construction material trends assistant. "
                "You have access to JSON datasets for many materials, including:\n\n"
                + ", ".join(material_list) + "\n\n"
                "Users might refer to materials informally or imprecisely (e.g., 'diesel' means '#2 Diesel Fuel'). "
                "Your job is to map these fuzzy inputs to actual dataset keys, and respond as if the correct dataset was accessed."
            )
        }

        messages = [system_message] + payload.messages

        print("🧠 System prompt preview:")  # 👈 LOG
        print(system_message["content"][:500] + "...")  # preview only

        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages
        )

        reply = response.choices[0].message
        print("✅ GPT response preview:")  # 👈 LOG
        print(reply.content[:300])  # preview only
        return reply

    except Exception as e:
        print(f"❌ GPT ERROR: {e}")  # 👈 LOG
        raise HTTPException(status_code=500, detail=str(e))
