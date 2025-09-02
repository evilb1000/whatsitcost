## AI System Diagnostic — How It Works Today

This document explains the current AI functionality end-to-end without proposing changes.

### Overview
- **Purpose**: Answer natural-language questions about construction material trends and generate executive/cluster summaries.
- **Model**: OpenAI GPT-4 via the official SDK.
- **Where it runs**: FastAPI backend (Render). Frontend React app calls the backend.
- **Primary data**: Processed JSONs hosted on GitHub (`AIBrain/JSONS/*`), synced from BLS pipeline.

### Components
- **Frontend** (`frontend/src/components/GPTChatAssistant.jsx`)
  - Sends `POST /gpt` to backend with `{ prompt: string }`.
  - Displays returned assistant text.
  - Backend base URL: `https://whatsitcost.onrender.com`.

- **Backend** (`main.py`)
  - Loads public JSON datasets from GitHub on startup:
    - `material_trends.json`, `material_trendlines.json`, `material_spikes.json`, `material_rolling.json`, `material_rolling_12mo.json`, `material_rolling_3yr.json`, `material_correlations.json`, `latest_snapshot.json`, `cluster_data.json`.
  - Exposes REST endpoints for trends/rolling/spikes/correlations.
  - AI endpoints use GPT-4 for:
    1) Intent resolution and routing of user prompts
    2) Executive summary generation from `latest_snapshot.json`
    3) Cluster summary generation from `cluster_data.json`
    4) Final natural-language response generation using tool outputs

### Request Flow (Chat)
1. Frontend sends `POST /gpt` with `{ prompt }`.
2. Backend resolves intent via `resolve_prompt_with_gpt()`:
   - Fast-paths:
     - If the prompt looks like an executive summary request (no material keywords + snapshot-y phrases) → bypass to snapshot summary.
     - If the prompt names a known cluster (from `CLUSTERS`) → handle as a cluster summary.
   - Otherwise calls GPT-4 with a system prompt to extract `{ material, metric, date }` where:
     - `metric` ∈ { `momentum`, `volatility`, `spike`, `rolling` } (defaults to `momentum` if unspecified)
     - `date` is `YYYY-MM` or `latest`
3. If `date == "latest"`, the backend resolves it to the latest available date for the material.
4. Backend gathers data for the chosen material/metric/date using helpers in `GPT_Tools/functions.py`:
   - `get_latest_trend_entry`, `get_trend_mom_summary`, etc.
5. Backend calls GPT-4 again with a system prompt and the tool output to produce the final fluent answer.
6. Response returned as `{ response: string }` to the frontend.

### Executive Summary Path
- Trigger: Broad/snapshot-style prompts with no material match.
- Data source: `latest_snapshot.json` (already loaded in memory).
- Process: Backend crafts a strict prompt and calls GPT-4 to produce a 4-paragraph professional narrative summary.

### Cluster Summary Path
- Trigger: If `material` matches a known cluster name (`GPT_Tools/material_clusters.py`).
- Data source: `cluster_data.json` slice for that cluster.
- Process: Backend prompts GPT-4 to write a concise formal summary focusing on MoM/YoY and standouts.

### Resolve-Intent Endpoint (auxiliary)
- `POST /resolve-intent` (in `main.py`) -> uses `resolve_intent.py`.
- `resolve_intent.py` calls GPT-4 with a material list from `material_map.py`, returning `{ material, metric }` where `metric` ∈ { `yoy`, `mom`, `rolling_12mo`, `rolling_3yr`, `spike`, `trendline` }.

### Environment and Secrets
- OpenAI key read from `GPT_KEY` (also supports `OPENAI_API_KEY` per README examples).
- Backend is permissive CORS for the web app.

### Data Contracts and Formats
- Firestore stores observation dates as `YYYY-MM` (unchanged).
- Backend JSON datasets are fetched from `https://raw.githubusercontent.com/evilb1000/whatsitcost/main/AIBrain/JSONS` at startup.
- The chat endpoint returns: `{ response: string }`.

### Error Handling (Chat)
- If GPT parsing fails or an invalid metric is requested, API returns a user-friendly fallback message.
- If a material/metric dataset is missing, endpoints return 404 with specific error messages.

### Operational Notes
- Logging: Console prints trace each step (dataset loads, intent resolution, resolved dates, GPT outputs).
- Model: All chat/intents use `gpt-4` with low/zero temperature depending on task.
- Frontend includes a disclaimer modal before first use.

### Quick Manual Test
1) Exec Summary: `POST /gpt` with a prompt like "Give me the latest market snapshot" → returns 4-paragraph summary.
2) Cluster: `POST /gpt` with "Summarize the Metals cluster" → returns cluster narrative.
3) Material metric: `POST /gpt` with "What’s the momentum for Rebar in 2025-06?" → returns focused analysis.

### Known Limits
- Strictly depends on GitHub-hosted JSONs being current (pipeline must be run).
- OpenAI API availability/credits required.
- Date must be `YYYY-MM` or `latest` per current prompts.


