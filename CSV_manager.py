import csv
import json
import os

class CSVManager:
    def __init__(self, csv_file_path=None, json_file_path=None):
        self.csv_file_path = csv_file_path
        self.json_file_path = json_file_path

    def set_file_paths(self, csv_file_path, json_file_path):
        self.csv_file_path = csv_file_path
        self.json_file_path = json_file_path

    def csv_to_json(self, action='overwrite'):
        if not self.csv_file_path or not self.json_file_path:
            raise ValueError("File paths must be set before conversion.")
        
        data = None
        if action == 'append' and os.path.exists(self.json_file_path):
            with open(self.json_file_path, 'r') as json_file:
                data = json.load(json_file)
        else:
            data = {
                "income": 0,
                "expense": 0,
                "categories": {
                    "income": {},
                    "expense": {}
                },
                "log": []
            }

        with open(self.csv_file_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                amount = int(row['amount'])
                desc = row['description']
                dt = row['datetime']
                category = row['category']
                transaction_type = row['type']
                uuid_str = row['uuid']

                result = {
                    "uuid": uuid_str,
                    "amount": amount,
                    "description": desc,
                    "datetime": dt,
                    'category': category,
                    'type': transaction_type
                }

                data['log'].insert(0, result)  # 插入到最前面
                data['log'] = sorted(data['log'], key=lambda x: x['datetime'], reverse=True)  # 按時間倒序排序

                if transaction_type == 'Income':
                    data['income'] += amount
                    if category in data['categories']['income']:
                        data['categories']['income'][category] += amount
                    else:
                        data['categories']['income'][category] = amount
                else:
                    data['expense'] += amount
                    if category in data['categories']['expense']:
                        data['categories']['expense'][category] += amount
                    else:
                        data['categories']['expense'][category] = amount

        with open(self.json_file_path, 'w') as json_file:
            json.dump(data, json_file)

    def json_to_csv(self):
        if not self.json_file_path or not self.csv_file_path:
            raise ValueError("File paths must be set before conversion.")

        with open(self.json_file_path, 'r') as json_file:
            data = json.load(json_file)

        csv_columns = ['uuid', 'amount', 'description', 'datetime', 'category', 'type']
        csv_file = self.csv_file_path

        with open(csv_file, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for entry in data['log']:
                writer.writerow(entry)

        return csv_file
