from flask import Flask, request, render_template, send_from_directory, send_file, jsonify, redirect, url_for
from datetime import datetime
import json
import os
import uuid
from CSVconverter import CSVconverter

app = Flask(__name__)

LOG_FILE = 'log.json'
CATEGORIES_FILE = 'categories.json'

def init_log():
    if not os.path.isfile(LOG_FILE) or os.stat(LOG_FILE).st_size == 0:
        with open(LOG_FILE, 'w') as f:
            data = {"income": 0, "expense": 0, "log": []}
            json.dump(data, f)

@app.route('/', methods=['GET', 'POST'])
def home():
    init_log()
    if request.method == 'POST':
        if request.form['action'] == 'new':
            user_input = request.form['content_of_textbox']
            category = request.form['category']
            transaction_type = request.form['transaction_type']

            with open(LOG_FILE, 'r') as f:
                data = json.load(f)
            if user_input == '':
                return render_template('result.html', info="Data Preview")
            try:
                amount, desc = user_input.split('/', 1)
                amount = int(amount)
                desc = str(desc).strip()
                dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                uuid_str = str(uuid.uuid4())
                result = {"uuid": uuid_str, "amount": amount, "description": desc, "datetime": dt, 'category': category, 'type': transaction_type}

                with open(LOG_FILE, 'r') as f:
                    data = json.load(f)
                data['log'].insert(0, result)
                if transaction_type == 'Income':
                    data['income'] += amount
                else:
                    data['expense'] += amount
                with open(LOG_FILE, 'w') as f:
                    json.dump(data, f)

                return render_template('result.html', info="Save Successfully!")
            except Exception as e:
                print(e)
                if user_input == '/zero':
                    os.remove(LOG_FILE)
                    init_log()
                    return render_template('result.html', info="Data Have Been Reset.")
                elif user_input == '/delete':
                    latest_entry = data['log'][0]
                    if latest_entry['type'] == 'Income':
                        data['income'] -= latest_entry['amount']
                    else:
                        data['expense'] -= latest_entry['amount']
                    del data['log'][0]
                    with open(LOG_FILE, 'w') as f:
                        json.dump(data, f)
                    return render_template('result.html', info="Deleted Latest Data.")
                else:
                    return render_template('result.html', info="Error: Invalid input format.")
        
        elif request.form['action'] == 'update':
            uuid_str = request.form['uuid']
            with open(LOG_FILE, 'r') as f:
                data = json.load(f)
                entry = next((item for item in data['log'] if item['uuid'] == uuid_str), None)
            if entry:
                amount = int(request.form['amount'])
                desc = request.form['description']
                category = request.form['category']
                transaction_type = request.form['transaction_type']
                dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                # Update the entry
                data['income'] -= entry['amount'] if entry['type'] == 'Income' else 0
                data['expense'] -= entry['amount'] if entry['type'] == 'Expense' else 0
                entry.update({
                    "amount": amount,
                    "description": desc,
                    "category": category,
                    "type": transaction_type,
                    "datetime": dt
                })
                data['income'] += amount if transaction_type == 'Income' else 0
                data['expense'] += amount if transaction_type == 'Expense' else 0

                with open(LOG_FILE, 'w') as f:
                    json.dump(data, f)

                return render_template('result.html', info="Entry updated successfully!")
            else:
                return '<h1>Entry not found<h1>', 404
        
        elif request.form['action'] == 'delete':
            uuid_str = request.form['uuid']
            with open(LOG_FILE, 'r') as f:
                data = json.load(f)
                entry = next((item for item in data['log'] if item['uuid'] == uuid_str), None)
            if entry:
                if entry['type'] == 'Income':
                    data['income'] -= entry['amount']
                else:
                    data['expense'] -= entry['amount']
                data['log'] = [item for item in data['log'] if item['uuid'] != uuid_str]

                with open(LOG_FILE, 'w') as f:
                    json.dump(data, f)

                return render_template('result.html', info="Entry updated successfully!")
            else:
                return '<h1>Entry not found<h1>', 404


    else: # GET
        
        try:
            with open('categories.json', 'r') as f:
                data = json.load(f)
                expense = data['expense']
                income  = data['income']
                del data
        except:
            expense = ['Dining', 'Household', 'Transportation', 'Entertainment', 'Healthcare']
            income  = ['Salary', 'Freelance', 'Investment', 'Rental', 'Gifts']

        return render_template(
            template_name_or_list = 'home.html', 
            expenseCategory = expense, 
            incomeCategory  = income
        )

@app.route('/edit_categories', methods=['GET', 'POST'])
def edit_categories():
    # Ensure the categories file exists
    if not os.path.isfile(CATEGORIES_FILE):
        categories = {
            "expense": ["Dining", "Household", "Transportation", "Entertainment", "Healthcare"],
            "income": ["Salary", "Freelance", "Investment", "Rental", "Gifts"]
        }
        with open(CATEGORIES_FILE, 'w') as f:
            json.dump(categories, f)
    
    if request.method == 'POST':
        try:
            new_categories = request.form.to_dict(flat=False)
            new_categories = {k: v for k, v in new_categories.items() if v}
            with open(CATEGORIES_FILE, 'w') as f:
                json.dump(new_categories, f)
            return redirect(url_for('home'))
        except Exception as e:
            return render_template('edit_categories.html', categories={}, error=str(e))

    else:
        with open(CATEGORIES_FILE, 'r') as f:
            categories = json.load(f)
        return render_template('edit_categories.html', categories=categories)

@app.route('/get_log', methods=['GET'])
def get_log():
    with open(LOG_FILE, 'r') as f:
        data = json.load(f)
    return jsonify(data)

@app.route('/get_CSV', methods=['GET'])
def get_CSV():
    CSV = CSVconverter()
    return send_file(CSV)

@app.route('/edit_log/<uuid_str>', methods=['GET'])
def edit_log(uuid_str):
    with open(LOG_FILE, 'r') as f:
        data = json.load(f)
        entry = next((item for item in data['log'] if item['uuid'] == uuid_str), None)

        try:
            with open('categories.json', 'r') as f:
                data = json.load(f)
                expense = data['expense']
                income  = data['income']
                del data
        except:
            expense = ['Dining', 'Household', 'Transportation', 'Entertainment', 'Healthcare']
            income  = ['Salary', 'Freelance', 'Investment', 'Rental', 'Gifts']

        if entry:
            return render_template(
            template_name_or_list = 'edit_log.html', 
            entry = entry,
            expenseCategory = expense, 
            incomeCategory  = income
    )
        else:
            return '<h1>Entry not found<h1>', 404

@app.route('/manifest.json')
def serve_manifest():
    return send_file('manifest.json', mimetype='application/manifest+json')

@app.route('/sw.js')
def serve_sw():
    return send_file('sw.js', mimetype='application/javascript')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/test')
def connection_test():
    return 'OK'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000,
            # ssl_context=('/etc/letsencrypt/live/daoyou.duckdns.org/fullchain.pem',
            #              '/etc/letsencrypt/live/daoyou.duckdns.org/privkey.pem'   )
            )
