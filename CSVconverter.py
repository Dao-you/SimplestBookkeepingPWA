import json
import csv
import sys

# Load the JSON data
with open(f'{sys.argv[1]}.json', 'r') as json_file:
    data = json.load(json_file)

# Extract the log data
log_data = data['log']

# Define the CSV file name
csv_file = f'{sys.argv[1]}.csv'

# Write the data to CSV
with open(csv_file, 'w', newline='') as csvfile:
    fieldnames = ['amount', 'description', 'datetime', 'category']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for entry in log_data:
        writer.writerow(entry)
