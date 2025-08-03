from datetime import datetime
import uuid

class TransactionManager:
    def __init__(self, file_manager):
        self.file_manager = file_manager

    def add_transaction(self, user_input, category, transaction_type):
        if not user_input:
            return "Data Preview"
        
        try:
            amount, desc = user_input.split('/', 1)
            amount = int(amount)
            # `trim` is not a valid Python string method. Using `strip` removes
            # leading and trailing whitespace from the description so that
            # accidental spaces don't get persisted into the log.
            desc = str(desc).strip()
            dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            uuid_str = str(uuid.uuid4())
            result = {"uuid": uuid_str, "amount": amount, "description": desc, "datetime": dt, 'category': category, 'type': transaction_type}
            
            data = self.file_manager.read_log()
            data['log'].insert(0, result)
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

            self.file_manager.write_log(data)
            return "Save Successfully!"
        except Exception as e:
            print(e)
            if user_input == '/zero':
                self.file_manager.reset_log()
                return "Data Have Been Reset."
            elif user_input == '/delete':
                self.delete_latest_entry()
                return "Deleted Latest Data."
            else:
                return "Error: Invalid input format."

    def update_transaction(self, uuid_str, amount, desc, category, transaction_type):
        data = self.file_manager.read_log()
        entry = next((item for item in data['log'] if item['uuid'] == uuid_str), None)
        if not entry:
            return '<h1>Entry not found<h1>', 404
        
        old_amount = entry['amount']
        old_category = entry['category']
        old_type = entry['type']

        if old_type == 'Income':
            data['income'] -= old_amount
            data['categories']['income'][old_category] -= old_amount
        else:
            data['expense'] -= old_amount
            data['categories']['expense'][old_category] -= old_amount

        entry.update({
            "amount": amount,
            "description": desc,
            "category": category,
            "type": transaction_type,
            "datetime": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

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

        self.file_manager.write_log(data)
        return "Entry updated successfully!"

    def delete_transaction(self, uuid_str):
        data = self.file_manager.read_log()
        entry = next((item for item in data['log'] if item['uuid'] == uuid_str), None)
        if not entry:
            return '<h1>Entry not found<h1>', 404
        
        if entry['type'] == 'Income':
            data['income'] -= entry['amount']
            data['categories']['income'][entry['category']] -= entry['amount']
        else:
            data['expense'] -= entry['amount']
            data['categories']['expense'][entry['category']] -= entry['amount']
        
        data['log'] = [item for item in data['log'] if item['uuid'] != uuid_str]
        self.file_manager.write_log(data)
        return "Entry deleted successfully!"

    def delete_latest_entry(self):
        data = self.file_manager.read_log()
        latest_entry = data['log'][0]
        if latest_entry['type'] == 'Income':
            data['income'] -= latest_entry['amount']
            data['categories']['income'][latest_entry['category']] -= latest_entry['amount']
        else:
            data['expense'] -= latest_entry['amount']
            data['categories']['expense'][latest_entry['category']] -= latest_entry['amount']
        del data['log'][0]
        self.file_manager.write_log(data)
