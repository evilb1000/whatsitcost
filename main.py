from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
import os

# === CONFIG ===
DATA_DIR = "/Users/benatwood/PycharmProjects/WhatsItCost/AIBrain"

app = FastAPI(title="Material Trends API")

# === Enable CORS ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 🔒 Set your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Load JSON Helper ===
def load_json(file_name):
    try:
        with open(os.path.join(DATA_DIR, file_name), "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# === Load Data ===
trends_by_date = load_json("material_trends.json")
trendlines_by_material = load_json("material_trendlines.json")
spikes_by_material = load_json("material_spikes.json")
rolling_by_material = load_json("material_rolling.json")
rolling_12mo_by_material = load_json("material_rolling_12mo.json")
rolling_3yr_by_material = load_json("material_rolling_3yr.json")
correlations_by_material = load_json("material_correlations.json")

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
