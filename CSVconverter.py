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


def JSONconverter(csv_file, json_file, data=None):
    """
    Converts a CSV file with financial transactions to a JSON format.

    Args:
        csv_file (str): Path to the CSV file.
        json_file (str): Path to the JSON file where the converted data will be stored.
        data (dict, optional): Existing data to be appended. Defaults to None.

    Returns:
        dict: A dictionary containing the income, expense breakdown, and transaction log.
    """
    if data is None:
        data = {"income": 0, "expense": 0, "categories": {"income": {}, "expense": {}}, "log": []}

    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            amount = int(row['amount'])
            category = row['category']
            transaction_type = row['type']
            description = row['description']

            if transaction_type == "Income":
                data["income"] += amount
                if description not in data["categories"]["income"]:
                    data["categories"]["income"][description] = 0
                data["categories"]["income"][description] += amount
            else:
                data["expense"] += amount
                if category not in data["categories"]["expense"]:
                    data["categories"]["expense"][category] = 0
                data["categories"]["expense"][category] += amount

            data["log"].append({
                "uuid": row["uuid"],
                "amount": amount,
                "description": description,
                "datetime": datetime.strptime(row["datetime"], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S"),
                "category": category,
                "type": transaction_type,
            })

    data['log'].sort(key=lambda x: datetime.strptime(x['datetime'], "%Y-%m-%d %H:%M:%S"), reverse=True)

    with open(json_file, 'w') as f:
        json.dump(data, f, indent=4)

    return data

if __name__ == "__main__":
    print(f"Output successfilly: {CSVconverter(sys.argv[1])}")