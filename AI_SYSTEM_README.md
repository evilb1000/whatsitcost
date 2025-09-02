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

### AI Callable Functions

The backend uses helpers in `GPT_Tools/functions.py` to fetch and shape data before GPT-4 drafts the final response.

| Function | Trigger (intent/metric) | Inputs | Returns | Usage in AI flow |
|---|---|---|---|---|
| `get_latest_trend_entry` | Material + specific metric/date; general trend lookup | `material: str`, `dataset: dict`, `date: str = "latest"`, `field: str \| None` | Single record or specific field for the given month | Provides core month-specific values used in the final narrative |
| `get_trend_mom_summary` | Material + `mom`/`yoy` summary for a month | `material: str`, `dataset: dict`, `date: str` | `{ Date, MoM, YoY }` for that material/date | Supplies concise MoM/YoY pair included in the model’s summary |
| `get_momentum` | Metric resolved to `momentum` | `material: str`, `dataset: dict`, `date: str \| None` | 3-month averages; if date provided, monthly MoM/YoY | Adds medium-horizon momentum context to GPT prompt |
| `get_spikes` | Metric resolved to `spike` | `material: str`, `dataset: dict` | `{ spike_months: [...] }` or note | Highlights outlier movement months to reference in answer |
| `get_volatility` | Metric resolved to `volatility` | `material: str`, `dataset: dict` | `{ volatility_score }` or note | Optional volatility signal if dataset present |

Details:
- `get_latest_trend_entry`
  - Trigger: General material/month lookup or when a specific `field` (e.g., MoM/YoY key) is needed.
  - Inputs: `material`, `dataset`, optional `date` (defaults `latest`), optional `field`.
  - Returns: The matched record for the month or the specific field.
  - Usage: Forms the backbone of the numeric evidence provided to GPT-4.

- `get_trend_mom_summary`
  - Trigger: When the intent requires MoM/YoY for a given month.
  - Inputs: `material`, `dataset`, `date`.
  - Returns: `{ Date, MoM, YoY }`.
  - Usage: Fed to GPT-4 as a compact summary for the narrative.

- `get_momentum`
  - Trigger: `metric == "momentum"`.
  - Inputs: `material`, `dataset`, optional `date`.
  - Returns: 3-month average MoM/YoY; if `date` provided, adds that month’s MoM/YoY.
  - Usage: Gives multi-month context for trend direction.

- `get_spikes`
  - Trigger: `metric == "spike"`.
  - Inputs: `material`, `dataset`.
  - Returns: List of spike months (or a note if none).
  - Usage: Lets GPT-4 call out standout months.

- `get_volatility`
  - Trigger: `metric == "volatility"`.
  - Inputs: `material`, `dataset`.
  - Returns: `{ volatility_score }` or note.
  - Usage: Optional volatility signal if data available.

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
- This intent resolution determines which of the above AI callable functions is ultimately invoked.

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


