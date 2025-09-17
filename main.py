print("🔥 MAIN.PY LOADED")

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
from typing import Optional
import os
import requests
import json
from GPT_Tools.functions import (
    get_latest_trend_entry,
    get_trend_mom_summary,
    get_momentum,
    get_spikes,
    get_volatility
)

# == cluster logic
from GPT_Tools.material_clusters import CLUSTERS
from material_map import get_material_map
def resolve_cluster(name):
    return CLUSTERS.get(name.lower(), [])
#== entry point for prompt resolution

def resolve_prompt_with_gpt(prompt: str, materials: list) -> dict:
    print("📥 Starting resolve_prompt_with_gpt")
    print(f"📝 Incoming prompt: {prompt}")
    print(f"📦 Material count: {len(materials)}")
    matched_materials = [m for m in materials if m.lower() in prompt.lower()]
    print(f"🔎 Matched materials from prompt: {matched_materials}")


    # 🧠 Exec summary detection — shortcut out
    if not matched_materials and any(phrase in prompt.lower() for phrase in [
        "latest update",
        "latest summary",
        "overall summary",
        "overall update",
        "market snapshot",
        "snapshot overview",
        "high-level update",
        "executive summary",
        "broad market trends",
        "what’s happening in the market",
        "give me the overview",
        "what happened recently",
        "what’s the market doing",
        "summary of latest data",
        "latest market movement",
        "market-wide update",
        "construction trends lately",
        "general pricing trends",
        "current state of the market",
        "latest on construction materials",
        "what's the latest on construction materials",
        "latest construction materials data",
        "construction material update",
        "latest construction material summary",
        "summary of construction materials",
        "overall construction market",
        "how is the construction materials market doing",
        "broad view of construction costs",
        "state of construction prices"
    ]):
        print("🧠 Resolver: Exec summary match — no material to extract.")
        return { "material": None, "metric": None, "date": "latest" }

    # 🧩 Cluster detection — shortcut out
    for cluster_name in CLUSTERS:
        if cluster_name.lower() in prompt.lower():
            print(f"🧠 Resolver: Cluster match → {cluster_name}")
            return { "material": cluster_name, "metric": None, "date": "latest" }

    # 🎯 Fallback to GPT intent extraction
    print("🎯 No shortcut match — falling back to GPT resolution")

    system_prompt = (
            "You are a helpful assistant. A user will send a freeform question about construction materials.\n"
            "From their prompt, extract:\n"
            "- The most relevant material (must be from the provided list)\n"
            "- The requested metric (must be exactly one of: 'momentum', 'volatility', 'spike', or 'rolling')\n"
            "- The most specific date (must be in YYYY-MM format — or use 'latest' for the date only)\n\n"
            "IMPORTANT:\n"
            "- Do not use 'latest' as a metric.\n"
            "- If no metric is specified, default to 'momentum'.\n"
            "- Only use 'latest' in the 'date' field.\n"
            "- Stay strictly clinical. Do not infer causes or offer explanations.\n\n"
            "Return only a valid JSON object like:\n"
            "{ \"material\": \"Asphalt (At Refinery)\", \"metric\": \"momentum\", \"date\": \"2024-11\" }\n\n"
            "Here is the list of materials:\n" +
            "\n".join(f"- {m}" for m in materials)
    )

    messages = [
        { "role": "system", "content": system_prompt },
        { "role": "user", "content": prompt }
    ]

    if client is None:
        print("⚠️ No GPT key present; cannot resolve via GPT")
        raise HTTPException(status_code=400, detail="GPT key not configured for intent resolution.")

    print("📡 Sending prompt to GPT...")
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0
    )

    content = response.choices[0].message.content.strip()
    print(f"🧾 Raw GPT content: {content}")

    try:
        parsed = eval(content)
        print(f"📊 Parsed dict: {parsed}")

        # 🧼 Post-process — force 'latest' only in date field
        if not parsed.get("date") or "lately" in prompt.lower() or "recently" in prompt.lower():
            print("📅 Prompt implies recency or no date provided — setting date to 'latest'")
            parsed["date"] = "latest"

        print(f"🧠 Final parsed values → material: {parsed.get('material')}, metric: {parsed.get('metric')}, date: {parsed.get('date')}")
        return parsed

    except Exception as e:
        print(f"⚠️ Failed to parse GPT response: {e}")
        raise HTTPException(status_code=400, detail="Failed to extract intent from prompt.")



# === Pydantic Models ===
class GPTQuery(BaseModel):
    prompt: str


# === CONFIG ===
BASE_URL = "https://raw.githubusercontent.com/evilb1000/whatsitcost/main/AIBrain/JSONS"
# Allow running without GPT in local/dev
_gpt_key = os.getenv("GPT_KEY") or os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=_gpt_key) if _gpt_key else None

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
snapshot_summary = load_json_from_github(f"{BASE_URL}/latest_snapshot.json")
cluster_data = load_json_from_github(f"{BASE_URL}/cluster_data.json")  # ✅ Added for cluster summaries
# ✅ Added
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
alias_map = get_material_map() or {}

# Common loose aliases → canonical material names (best-effort, non-exhaustive)
ALIASES = {
    "diesel": "#2 Diesel Fuel",
    "diesel fuel": "#2 Diesel Fuel",
    "aluminum shapes": "Aluminum Mill Shapes",
    "aluminum mill": "Aluminum Mill Shapes",
    "aluminium": "Aluminum Mill Shapes",
    "asphalt": "Asphalt (At Refinery)",
    "cement": "Cement",
    "flat glass": "Flatt Glass",
    "glass": "Flatt Glass",
    "rebar": "Fabricated Structural Metal Bar Joists and Rebar",
    "steel": "Steel Mill Products",
    "ppi": "Producer Price Index (PPI For Final Demand",
    "cpi": "Consumer Price Index (CPI-U)",
}
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

@app.get("/trends/{material}/{date}")
def get_trend_for_material_date(material: str, date: str):
    print(f"📅 Looking up MoM/YoY for '{material}' on {date}")
    return get_trend_mom_summary(material, trendlines_by_material, date)


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

# === Visualization helpers and endpoint ===
def parse_months_from_prompt(prompt: str) -> int:
    """
    Extract a timeframe from the prompt. Supports phrases like:
    - "18 months" → 18
    - "2 years" → 24
    Defaults to 24 months if not detected.
    """
    p = prompt.lower()
    # Months explicit
    import re
    m = re.search(r"(\d+)\s*month", p)
    if m:
        try:
            return max(1, int(m.group(1)))
        except Exception:
            pass
    # Years → months
    y = re.search(r"(\d+)\s*year", p)
    if y:
        try:
            return max(1, int(y.group(1)) * 12)
        except Exception:
            pass
    return 24


def build_mom_series(material: str, months: int):
    """
    Build a sequence of {date, value} for MoM over the last N months from trendlines_by_material.
    Skips entries with null MoM.
    """
    records = trendlines_by_material.get(material)
    if not records:
        raise HTTPException(status_code=404, detail=f"Material '{material}' not found")

    # Keep entries that have Date and MoM
    clean = [r for r in records if r.get("Date") and (r.get("MoM") is not None)]
    if not clean:
        raise HTTPException(status_code=404, detail=f"No MoM data for material '{material}'")

    # Sort by Date and slice
    clean = sorted(clean, key=lambda r: r["Date"])  # YYYY-MM sorts lexicographically
    points = clean[-months:]
    return [{"date": r["Date"], "value": r["MoM"]} for r in points]


@app.get("/mom-series/{material}")
def get_mom_series(material: str, months: int = 24):
    print(f"📈 Building MoM series for {material} over last {months} months")
    points = build_mom_series(material, months)
    return {"material": material, "metric": "MoM", "months": months, "points": points}


@app.get("/mom-series-multi")
def get_mom_series_multi(materials: str, months: int = 24):
    """
    materials: comma-separated list of material names
    months: number of months to include
    """
    print(f"📈 Building multi-series MoM for: {materials} over {months} months")
    names = [m.strip() for m in materials.split(",") if m.strip()]
    if not names:
        raise HTTPException(status_code=400, detail="No materials provided")
    if len(names) > 4:
        names = names[:4]
    series_list = []
    for name in names:
        # Try exact match; if not found, try case-insensitive lookup from material_list
        key = name if name in trendlines_by_material else next((m for m in material_list if m.lower() == name.lower()), None)
        if not key:
            series_list.append({"material": name, "error": "Material not found"})
            continue
        try:
            points = build_mom_series(key, months)
            series_list.append({"material": key, "points": points})
        except HTTPException as e:
            series_list.append({"material": key, "error": e.detail})
    return {"metric": "MoM", "months": months, "series": series_list}

# === GPT Chat Endpoint ===

class GPTRequest(BaseModel):
    messages: list

@app.post("/gpt")
async def run_gpt(query: GPTQuery):
    print(f"🧠 GPT Prompt received: {query.prompt}")

    try:
        # Visualization intent: detect chart requests and return chart data payload
        viz_triggers = [
            "chart", "graph", "plot", "visual", "visualize", "visualisation", "visualization",
            "trendline", "trendlines", "trend", "trends"
        ]
        if any(t in query.prompt.lower() for t in viz_triggers):
            print("🖼️ Visualization intent detected — preparing chart data")
            # Collect up to 4 materials mentioned in the prompt (with alias support)
            lowered = query.prompt.lower()
            matched = []
            # 1) Exact substring matches
            for m in material_list:
                if m.lower() in lowered:
                    matched.append(m)
                if len(matched) >= 4:
                    break
            # 2) Alias approximate matches (always run hardcoded ALIASES)
            if len(matched) < 4:
                for alias, canonical in ALIASES.items():
                    if len(matched) >= 4:
                        break
                    if canonical in matched:
                        continue
                    if alias in lowered and canonical in material_list:
                        matched.append(canonical)
            # 3) Try keys from material_map.json (treat keys as aliases if not exact canonical names)
            if len(matched) < 4 and alias_map:
                for alias, series_id in alias_map.items():
                    if len(matched) >= 4:
                        break
                    if alias in matched:
                        continue
                    if alias in material_list and alias.lower() in lowered:
                        matched.append(alias)
            # Do NOT call GPT for viz matching; rely on aliases to avoid API dependency
            if not matched:
                raise HTTPException(status_code=400, detail="Could not determine material(s) for the chart.")

            months = parse_months_from_prompt(query.prompt)
            multi_series = []
            for mat in matched:
                try:
                    pts = build_mom_series(mat, months)
                    multi_series.append({"material": mat, "points": pts})
                except HTTPException as e:
                    multi_series.append({"material": mat, "error": e.detail, "points": []})
            title = ", ".join(matched[:4]) + f" — MoM over last {months} months"
            return {
                "chartData": {
                    "type": "line",
                    "metric": "MoM",
                    "months": months,
                    "series": multi_series,
                    "title": title
                }
            }

        # Step 1: Resolve material, metric, date
        if client is None:
            raise HTTPException(status_code=400, detail="GPT key not configured. Set GPT_KEY or OPENAI_API_KEY.")
        intent = resolve_prompt_with_gpt(query.prompt, material_list)
        # ✨ EXECUTIVE SUMMARY BYPASS (no material → snapshot summary)
        if intent.get("material") is None:
            print("📊 Exec summary triggered — no material provided.")

            snapshot_prompt = (
                    "You are a market analyst assistant. Based on the following snapshot of construction material trends, "
                    "write a clean, structured executive summary **as of the provided snapshot_date**. Follow this format:\n\n"
                    "1. Begin with the core indexes:\n"
                    "   - Consumer Price Index (CPI-U)\n"
                    "   - Producer Price Index (PPI) for Final Demand\n"
                    "   - Final Demand Construction Index\n"
                    "   - Inputs to Construction Industries\n"
                    "   - For each index, include both the month-over-month (MoM) and year-over-year (YoY) percentage change.\n\n"
                    "2. Summarize the overall market direction (clinical statement only):\n"
                    "   - State whether movements are mostly up, down, or stable based on counts.\n"
                    "   - Do not speculate on causes or implications.\n\n"
                    "3. Include the percentage breakdown:\n"
                    "   - % of materials that increased\n"
                    "   - % that decreased\n"
                    "   - % that remained stable\n"
                    "   - Start by stating: 'Out of the [total series count] materials we track...'\n\n"
                    "4. List the standout performers:\n"
                    "   - Top risers with both MoM and YoY percentage increases\n"
                    "   - Top fallers with both MoM and YoY percentage decreases\n\n"
                    "**Formatting & Style Instructions:**\n"
                    "- Structure the output as concise, readable paragraphs — do not use numbered sections or bullet points.\n"
                    "- Each of the four items above should be its own paragraph.\n"
                    "- Use formal, clinical language.\n"
                    "- Do NOT offer reasons, implications, or commentary (e.g., 'indicating demand has gone up', 'doing well', 'due to').\n"
                    "- Only state observed direction and percentages from the data.\n\n"
                    "Snapshot data:\n" + json.dumps(snapshot_summary, indent=2)
            )



            final_response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system",
                     "content": "You summarize construction material market data into concise, expert-level insights."},
                    {"role": "user", "content": snapshot_prompt}
                ],
                temperature=0.5
            )

            result = final_response.choices[0].message.content.strip()
            print(f"📈 Exec Summary GPT Result: {result}")
            return {"response": result}
        material = intent["material"]
        metric = intent["metric"]
        date = intent["date"]
        # ✳️ CLUSTER SUMMARY HANDLER
        if material in cluster_data:
            print(f"📦 Cluster summary triggered for: {material}")

            cluster_blob = cluster_data[material]

            cluster_prompt = (
                f"You are a market analyst assistant. Based on the following data for the '{material}' cluster, "
                f"write a concise, expert-level financial summary. Your tone must be formal and strictly clinical.\n\n"
                f"Cluster data:\n{json.dumps(cluster_blob, indent=2)}\n\n"
                f"**Instructions:**\n"
                f"- Focus only on MoM and YoY changes and magnitudes.\n"
                f"- Highlight major outliers or movers numerically.\n"
                f"- Do not offer reasons, implications, or commentary (no 'indicates', 'suggests', 'demand', 'doing well', 'due to').\n"
                f"- Keep it clean, structured, and free of bullet points or numbered lists."
            )

            final_response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system",
                     "content": "You generate financial summaries for construction material clusters."},
                    {"role": "user", "content": cluster_prompt}
                ],
                temperature=0.5
            )

            result = final_response.choices[0].message.content.strip()
            print(f"📊 Cluster Summary Result: {result}")
            return {"response": result}

        print(f"🔎 Resolved — Material: {material}, Metric: {metric}, Date: {date}")

        # Step 2: Get data for the requested insight
        # ✅ Resolve "latest" to actual date in dataset
        # 🛡️ Validate metric first
        valid_metrics = ["momentum", "volatility", "spike", "rolling"]
        if metric not in valid_metrics:
            print(f"❌ Invalid metric parsed: {metric}")
            raise HTTPException(
                status_code=400,
                detail="I'm sorry, I could not process that metric. Please ask about momentum, volatility, spike, or rolling."
            )

        # ✅ Resolve "latest" to actual date
        if date == "latest":
            all_dates = [entry.get("date") or entry.get("Date") for entry in trendlines_by_material[material]]
            date = max(all_dates)
            print(f"⏱️ 'latest' resolved to → {date}")

        # Step 2: Get data for the requested insight
        trend_output = get_latest_trend_entry(
            material=material,
            dataset=trendlines_by_material,
            date=date,
            field=metric
        )

        summary = get_trend_mom_summary(
            material=material,
            dataset=trendlines_by_material,
            date=date
        )

        combined_summary = {
            "trend_entry": trend_output,
            "mom_trend": summary
        }

        # Step 3: Send to GPT for final chat response
        final_response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a clinical economic reporting assistant. Use ONLY the provided tool output to summarize observed movements.\n"
                        "Rules:\n"
                        "- Do NOT explain causes, implications, or motivations.\n"
                        "- Do NOT use speculative phrasing (e.g., 'indicates', 'suggests', 'due to', 'demand', 'supply', 'doing well').\n"
                        "- Only state direction (up/down/stable) and magnitudes (MoM/YoY percentages).\n"
                    )
                },
                { "role": "user", "content": query.prompt },
                { "role": "assistant", "content": f"Tool output: {combined_summary}" }
            ]
        )

        result = final_response.choices[0].message.content
        print(f"💬 Final GPT Message: {result}")
        return { "response": result }


    except Exception as e:

        print(f"🔥 Error in /gpt handler: {e}")

        return {

            "response": (

                "I'm sorry, I could not process this request. "

                "Please let Ben know at Ben@mbawpa.org. "

                "Copy and paste your query. "

                "The errors can be fixed and will make me smarter."

            )

        }


from pydantic import BaseModel
from resolve_intent import resolve_intent as gpt_resolve_intent

class ResolveIntentRequest(BaseModel):
    user_input: str

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


from explain_data import explain_data

class ExplainRequest(BaseModel):
    material: str
    metric: str

# Add this at the end to run the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

