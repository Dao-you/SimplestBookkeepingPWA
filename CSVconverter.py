import json
import csv
import sys
from datetime import datetime

def CSVconverter(filename="log"):
    # Load the JSON data
    with open(f'{filename}.json', 'r') as json_file:
        data = json.load(json_file)

    # Extract the log data
    log_data = data['log']

    # Define the CSV file name
    if filename == "log":
        filename = f"./logs/{datetime.now().strftime('%Y_%m_%d')}"
    csv_file = f'{filename}.csv'

    # Write the data to CSV
    with open(csv_file, 'w', newline='') as csvfile:
        fieldnames = ['uuid', 'amount', 'description', 'datetime', 'type', 'category']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for entry in log_data:
            writer.writerow(entry)
    return csv_file


if __name__ == "__main__":
    print(f"Output successfilly: {CSVconverter(sys.argv[1])}")