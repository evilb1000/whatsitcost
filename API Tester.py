import requests

# Config
API_KEY = "f7be3dbe922e472aac4b08da9abf3aa3"
API_URL = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
SERIES_ID = "WPU801101"
START_YEAR = "2024"
END_YEAR = "2025"

# Payload
payload = {
    "seriesid": [SERIES_ID],
    "startyear": START_YEAR,
    "endyear": END_YEAR,
    "registrationkey": API_KEY
}

# Fire request
response = requests.post(API_URL, json=payload)
data = response.json()

# Extract and print months found
if "Results" in data:
    months = [f"{entry['year']}-{entry['periodName']}" for entry in data["Results"]["series"][0]["data"]]
    months_sorted = sorted(months, reverse=True)
    print(f"Returned {len(months_sorted)} observations for {SERIES_ID}:")
    for m in months_sorted:
        print(m)
else:
    print("No data returned or error in request.")
