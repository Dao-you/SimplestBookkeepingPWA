import json
import os

class FileManager:
    def __init__(self, log_file, categories_file):
        self.log_file = log_file
        self.categories_file = categories_file

    def init_log(self):
        if not os.path.isfile(self.log_file) or os.stat(self.log_file).st_size == 0:
            self.reset_log()

    def reset_log(self):
        data = {
            "income": 0,
            "expense": 0,
            "categories": {
                "income": {},
                "expense": {}
            },
            "log": []
        }
        self.write_log(data)

    def init_categories(self):
        if not os.path.isfile(self.categories_file) or os.stat(self.categories_file).st_size == 0:
            categories = {
                "expense": ["Dining", "Household", "Transportation", "Entertainment", "Healthcare"],
                "income": ["Salary", "Freelance", "Investment", "Rental", "Gifts"]
            }
            self.write_categories(categories)

    def read_log(self):
        with open(self.log_file, 'r') as f:
            return json.load(f)

    def write_log(self, data):
        with open(self.log_file, 'w') as f:
            json.dump(data, f)

    def read_categories(self):
        with open(self.categories_file, 'r') as f:
            return json.load(f)

    def write_categories(self, categories):
        with open(self.categories_file, 'w') as f:
            json.dump(categories, f)
