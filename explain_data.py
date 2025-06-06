# AIBrain/explain_data.py

import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("GPT_KEY"))

def explain_data(material: str, metric: str) -> str:
    try:
        system_prompt = (
            "You are a construction material trends assistant. Your job is to explain, in plain terms, "
            "what kind of data is being displayed to the user based on a given material and metric. "
            "Do not hallucinate. Use simple, direct language. Keep it to one short paragraph."
        )

        user_prompt = (
            f"The user is viewing data for the material '{material}' with the metric '{metric}'. "
            f"Briefly explain what they are seeing."
        )

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"❌ Error in explain_data: {e}")
        return "Error generating explanation."
