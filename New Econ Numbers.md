## National and Regional Econ Articles – Data Fetchers

This project fetches public economic data series (FRED/BLS/BEA) and saves them as CSVs.

### Quickstart

1. Create a Python virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Add your FRED API key to a `.env` file:

```
FRED_API_KEY=YOUR_KEY_HERE
```

3. Fetch FRED TOTALSA (Total Vehicle Sales, SAAR) to `data/fred_totalsa.csv`:

```bash
python "scripts/FRED Auto Sales/fetch_fred_series.py" --series-id TOTALSA --output data/fred_totalsa.csv --start 1980-01-01
```

### Notes
- Respects the FRED API: `https://api.stlouisfed.org/fred/series/observations`
- Output CSV contains columns: `date,value`

---

### Credentials and Series (for quick reference)

- FRED API Key: `6af5cb112e0c7a9ac1a27238e7848047`

- Default FRED series pulled by the updater:
  - TOTALSA — Total Vehicle Sales (SAAR)
  - RSAFS — Advance Retail Sales: Retail Trade and Food Services
  - RSXFS — Advance Retail Sales: Retail Trade
  - RSMVPD — Advance Retail Sales: Motor Vehicle and Parts Dealers
  - RSFSDP — Advance Retail Sales: Food Services and Drinking Places
  - RSFHFS — Advance Retail Sales: Furniture and Home Furnishings Stores
  - RSEAS — Advance Retail Sales: Electronics and Appliance Stores
  - HOUST — New Privately-Owned Housing Units Started: Total Units
  - GDP — Gross Domestic Product (SAAR, Quarterly)
  - UNRATE — Unemployment Rate
  - CPIAUCSL — CPI-U: All Items
  - PPIACO — Producer Price Index: All Commodities
  - DGS10 — 10-Year Treasury Constant Maturity Rate (Daily)
  - FEDFUNDS — Federal Funds Effective Rate (Daily)
  - PAYEMS — All Employees: Total Nonfarm
  - INDPRO — Industrial Production Index: Total Index
  - PCEPI — Personal Consumption Expenditures: Chain-type Price Index
  - UMCSENT — University of Michigan: Consumer Sentiment
  - FRGSHPUSM649NCIS — Cass Freight Index: Shipments
  - TTLCONS — Total Construction Spending: Total Construction in the United States

- Updater command (runs all defaults and overwrites CSVs with Mon YYYY dates):
```bash
python "scripts/FRED Auto Sales/update_fred_series.py" --since 1980-01-01 --api-key 6af5cb112e0c7a9ac1a27238e7848047
```
