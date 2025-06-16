import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import matplotlib.dates as mdates

# Set up chart to open in separate window
plt.switch_backend('tkagg')

# Load the data
file_path = "/Users/benatwood/PycharmProjects/WhatsItCost/AIBrain/theBehemoth.csv"
df = pd.read_csv(file_path)

# Fix month and datetime formatting
df['month'] = df['month'].str.extract(r'M(\d+)', expand=False).astype(str).str.zfill(2)
df['date'] = pd.to_datetime(df['year'].astype(str) + '-' + df['month'] + '-01')

# Filter for desired series
series_ids = ['CUUR0000SA0', 'WPUFD4']
series_names = {
    'CUUR0000SA0': 'Consumer Price Index (CPI-U)',
    'WPUFD4': 'Producer Price Index (PPI For Final Demand)'
}

filtered = df[df['series_id'].isin(series_ids)].copy()

# Pivot and convert MoM growth to percent
pivoted = filtered.pivot(index='date', columns='series_id', values='mom_growth') * 100
pivoted = pivoted.loc[pivoted.index >= pivoted.index.max() - pd.DateOffset(months=18)]

# Plot
plt.figure(figsize=(10, 6))
for sid in series_ids:
    plt.plot(pivoted.index, pivoted[sid], label=series_names[sid])


plt.title("Month Over Month Growth for unadjusted CPI and PPI Indexes (Last 18 Months)")
plt.xlabel("Date", fontweight='bold')
plt.ylabel("MoM Growth (%)", fontweight='bold')

# ✅ Bold y-axis tick labels (not the line)
plt.tick_params(axis='y', labelsize=10)
plt.gca().yaxis.set_tick_params(labelsize=10)
for label in plt.gca().get_yticklabels():
    label.set_fontweight('bold')

# ✅ American-style x-axis formatting
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
plt.xticks(rotation=45)

# ✅ Bold x-axis tick labels
for label in plt.gca().get_xticklabels():
    label.set_fontweight('bold')


# ✅ Clean grid
plt.grid(False)
plt.legend()
plt.tight_layout()
plt.show()
