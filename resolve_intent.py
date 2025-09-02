# resolve_intent.py

import os
import json
from openai import OpenAI
from material_map import get_material_map

_gpt_key = os.getenv("GPT_KEY") or os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=_gpt_key) if _gpt_key else None

# === Load material map ===
material_map = get_material_map()
material_list = list(material_map.keys())

def resolve_intent(user_input: str) -> dict:
    try:
        if client is None:
            print("⚠️ resolve_intent: No GPT key configured; returning empty result")
            return {}
        system_prompt = (
            "You are an intent resolver for a construction materials AI system.\n"
            "You will be given a user input. Your job is to extract:\n"
            "1. The specific material name (from the list provided).\n"
            "2. The type of metric being requested.\n"
            "Valid metrics include: 'yoy', 'mom', 'rolling_12mo', 'rolling_3yr', 'spike', or 'trendline'.\n"
            "Return your answer as a JSON object with keys 'material' and 'metric'.\n"
            "Do not explain your answer. Do not include extra commentary."
        )

        material_list_string = ", ".join(material_list)
        user_prompt = (
            f"Material list:\n{material_list_string}\n\n"
            f"User input: {user_input}"
        )

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )

        reply = response.choices[0].message.content.strip()

        try:
            parsed = json.loads(reply)
            return {
                "material": parsed.get("material"),
                "metric": parsed.get("metric")
            }
        except json.JSONDecodeError:
            print("❌ GPT returned non-JSON format:")
            print(reply)
            return {}

    except Exception as e:
        print(f"❌ Error resolving intent: {e}")
        return {}
