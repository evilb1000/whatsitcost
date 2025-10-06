## Consumer Trends Data: Pull → Calculate → Upload

This folder contains the end-to-end pipeline for the Consumer Spending dashboard data. It pulls FRED series to CSVs, calculates metrics, and uploads the latest observation per series to Firestore.

### Key Scripts
- `fred_batch_pull.py`: Downloads FRED series into `../Consumer Trend Data` as CSVs
- `calculate_metrics.py`: Adds metrics (MoM, YoY, rolling averages)
  - UNRATE exception: MoM/YoY/12mo are computed in percentage points (diffs), not pct_change
- `upload_to_firestore.py`: Uploads latest rows using Firebase Admin SDK
- `upload_to_firestore_rest.py`: Uploads via Firestore REST (needs auth token)
- `run_consumer_pipeline.py`: Master script chaining the three steps

### Typical Usage (one command)
Run the full pipeline (pull → calculate → upload via Admin SDK):

```bash
python3 "/Users/benatwood/PycharmProjects/WhatsItCost/Consumer Trend Scripts/run_consumer_pipeline.py"
```

### Upload Only (after data/metrics already updated)
Admin SDK uploader (service account JSON must be available):

```bash
python3 "/Users/benatwood/PycharmProjects/WhatsItCost/Consumer Trend Scripts/upload_to_firestore.py" \
  --datadir "/Users/benatwood/PycharmProjects/WhatsItCost/Consumer Trend Data"
```

REST uploader (no Admin SDK, but requires auth):

```bash
python3 "/Users/benatwood/PycharmProjects/WhatsItCost/Consumer Trend Scripts/upload_to_firestore_rest.py" \
  --datadir "/Users/benatwood/PycharmProjects/WhatsItCost/Consumer Trend Data"
```

### Quick Troubleshooting

- Admin SDK not installed / import error
  - Fast fix: create a local venv and install deps, then run uploader
  ```bash
  cd /Users/benatwood/PycharmProjects/WhatsItCost
  python3 -m venv .venv && source .venv/bin/activate
  pip install firebase-admin pandas
  python3 "Consumer Trend Scripts/upload_to_firestore.py" --datadir "Consumer Trend Data"
  ```

- REST uploader returns 403 Missing or insufficient permissions
  - REST writes require an OAuth token. Two options:
    1) Use gcloud user creds (ADC):
    ```bash
    gcloud auth application-default login
    python3 "Consumer Trend Scripts/upload_to_firestore_rest.py" --datadir "Consumer Trend Data"
    ```
    2) Provide a Bearer token explicitly:
    ```bash
    export FIRESTORE_BEARER="$(gcloud auth print-access-token)"
    python3 "Consumer Trend Scripts/upload_to_firestore_rest.py" --datadir "Consumer Trend Data"
    ```

- URL contains control characters
  - Fixed: the REST uploader URL-encodes collection/doc IDs.

### Notes
- Firestore destination collection: `Consumer Spending Indicators`
- Frontend reads this in `frontend/src/components/ConsumerDashboard.jsx`
- UNRATE metrics use percentage-point differences; other series use percent changes

### One-liners
- Recalculate metrics only:
```bash
python3 "Consumer Trend Scripts/calculate_metrics.py" --datadir "Consumer Trend Data"
```

- Upload via Admin SDK only:
```bash
python3 "Consumer Trend Scripts/upload_to_firestore.py" --datadir "Consumer Trend Data"
```

- Upload via REST only (using current gcloud token):
```bash
export FIRESTORE_BEARER="$(gcloud auth print-access-token)"
python3 "Consumer Trend Scripts/upload_to_firestore_rest.py" --datadir "Consumer Trend Data"
```


