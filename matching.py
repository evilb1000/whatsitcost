import csv

# File paths
csv_path = "/Users/benatwood/PycharmProjects/WhatsItCost/DesiredSeries/Untitled spreadsheet - Sheet1.csv"
series_file_path = "/Users/benatwood/PycharmProjects/WhatsItCost/wp.series"
output_path = "/Users/benatwood/PycharmProjects/WhatsItCost/ScrapedData/post 2000 date tester.csv"

# Load desired series from CSV
with open(csv_path, newline='') as csvfile:
    reader = csv.reader(csvfile)
    desired_series = [row[0].strip() for row in reader if row]

# Load wp.series content
with open(series_file_path, 'r') as f:
    series_lines = f.readlines()

# Prepare results
results = []
for series_id in desired_series:
    match_line = next((line for line in series_lines if line.startswith(series_id)), None)
    if match_line:
        parts = match_line.strip().split('\t')
        if len(parts) >= 11:
            sid         = parts[0].strip()
            group_code  = parts[1].strip()
            item_code   = parts[2].strip()
            seasonal    = parts[3].strip()
            base_date   = parts[4].strip()
            title       = parts[5].strip()
            start_year  = parts[7].strip()
            start_month = parts[8].strip()
            end_year    = parts[9].strip()
            end_month   = parts[10].strip()

            if start_year.isdigit() and int(start_year) >= 2000:
                results.append([
                    sid, group_code, item_code, seasonal, base_date, title,
                    start_year, start_month, end_year, end_month
                ])

# Save to CSV
with open(output_path, 'w', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(["series_id", "group_code", "item_code", "seasonal", "base_date", "series_title",
                     "start_year", "start_month", "end_year", "end_month"])
    writer.writerows(results)
