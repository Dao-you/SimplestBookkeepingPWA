from flask import Flask, request, render_template, send_from_directory, send_file, jsonify, redirect, url_for
from datetime import datetime
import os
import uuid
import json
from file_manager import FileManager
from CSV_manager import CSVManager

app = Flask(__name__)

file_manager = FileManager('log.json', 'categories.json')
csv_manager = CSVManager()

@app.route('/', methods=['GET', 'POST'])
def home():
    file_manager.init_log()
    if request.method == 'POST':
        action = request.form['action']
        if action == 'new':
            return handle_new_transaction()
        elif action == 'update':
            return handle_update_transaction()
        elif action == 'delete':
            return handle_delete_transaction()
    else:
        file_manager.init_categories()
        categories = file_manager.read_categories()
        return render_template('home.html', expenseCategory=categories['expense'], incomeCategory=categories['income'])

def handle_new_transaction():
    user_input = request.form['content_of_textbox']
    category = request.form['category']
    transaction_type = request.form['transaction_type']

    if user_input == '':
        return render_template('result.html', info="Data Preview")

    try:
        amount, desc = user_input.split('/', 1)
        amount = int(amount)
        desc = str(desc).strip()
        dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        uuid_str = str(uuid.uuid4())
        result = {"uuid": uuid_str, "amount": amount, "description": desc, "datetime": dt, 'category': category, 'type': transaction_type}

        data = file_manager.read_log()
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

        file_manager.write_log(data)
        return render_template('result.html', info="Save Successfully!")
    except Exception as e:
        print(e)
        if user_input == '/zero':
            file_manager.reset_log()
            return render_template('result.html', info="Data Have Been Reset.")
        elif user_input == '/delete':
            data = file_manager.read_log()
            latest_entry = data['log'][0]
            if latest_entry['type'] == 'Income':
                data['income'] -= latest_entry['amount']
                data['categories']['income'][latest_entry['category']] -= latest_entry['amount']
            else:
                data['expense'] -= latest_entry['amount']
                data['categories']['expense'][latest_entry['category']] -= latest_entry['amount']
            del data['log'][0]
            file_manager.write_log(data)
            return render_template('result.html', info="Deleted Latest Data.")
        else:
            return render_template('result.html', info="Error: Invalid input format.")

def handle_update_transaction():
    uuid_str = request.form['uuid']
    data = file_manager.read_log()
    entry = next((item for item in data['log'] if item['uuid'] == uuid_str), None)
    if entry:
        amount = int(request.form['amount'])
        desc = request.form['description']
        category = request.form['category']
        transaction_type = request.form['transaction_type']
        dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if entry['type'] == 'Income':
            data['income'] -= entry['amount']
            data['categories']['income'][entry['category']] -= entry['amount']
        else:
            data['expense'] -= entry['amount']
            data['categories']['expense'][entry['category']] -= entry['amount']

        entry.update({
            "amount": amount,
            "description": desc,
            "category": category,
            "type": transaction_type,
            "datetime": dt
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

        file_manager.write_log(data)
        return render_template('result.html', info="Entry updated successfully!")
    else:
        return '<h1>Entry not found<h1>', 404

def handle_delete_transaction():
    uuid_str = request.form['uuid']
    data = file_manager.read_log()
    entry = next((item for item in data['log'] if item['uuid'] == uuid_str), None)
    if entry:
        if entry['type'] == 'Income':
            data['income'] -= entry['amount']
            data['categories']['income'][entry['category']] -= entry['amount']
        else:
            data['expense'] -= entry['amount']
            data['categories']['expense'][entry['category']] -= entry['amount']
        data['log'] = [item for item in data['log'] if item['uuid'] != uuid_str]
        file_manager.write_log(data)
        return render_template('result.html', info="Entry updated successfully!")
    else:
        return '<h1>Entry not found<h1>', 404

@app.route('/edit_categories', methods=['GET', 'POST'])
def edit_categories():
    file_manager.init_categories()
    if request.method == 'POST':
        try:
            new_categories = request.form.to_dict(flat=False)
            new_categories = {k: v for k, v in new_categories.items() if v}
            if 'expense' not in new_categories:
                new_categories['expense'] = ["Dining", "Household", "Transportation", "Entertainment", "Healthcare"]
            if 'income'  not in new_categories:
                new_categories['income']  = ["Salary", "Freelance", "Investment", "Rental", "Gifts"]
            file_manager.write_categories(new_categories)
            return redirect(url_for('home'))
        except Exception as e:
            print(str(e))
            return render_template('edit_categories.html', categories={}, error=str(e))
    else:
        categories = file_manager.read_categories()
        return render_template('edit_categories.html', categories=categories)

@app.route('/get_log', methods=['GET'])
def get_log():
    data = file_manager.read_log()
    return jsonify(data)

@app.route('/get_CSV', methods=['GET'])
def get_CSV():
    csv_manager.set_file_paths('output.csv', 'log.json')
    csv_manager.json_to_csv()
    return send_file('output.csv')

@app.route('/load_CSV', methods=['GET', 'POST'])
def load_CSV():
    if request.method == "GET":
        return render_template("load_CSV.html")
    elif request.method == 'POST':
        file = request.files['file']
        action = request.form['action']
        if not file:
            return "No file uploaded.", 400

        csv_file_path = f"uploaded_{str(uuid.uuid4())}.csv"
        file.save(csv_file_path)

        csv_manager.set_file_paths(csv_file_path, 'log.json')
        csv_manager.csv_to_json(action)
        os.remove(csv_file_path)
        return render_template("result.html", info="File upload successed.")

@app.route('/clear', methods=['GET'])
def clear():
    file_manager.reset_log()
    return render_template('result.html', info="Data Have Been Reset.")

@app.route('/edit_log/<uuid_str>', methods=['GET'])
def edit_log(uuid_str):
    data = file_manager.read_log()
    entry = next((item for item in data['log'] if item['uuid'] == uuid_str), None)
    if entry:
        categories = file_manager.read_categories()
        return render_template('edit_log.html', entry=entry, expenseCategory=categories['expense'], incomeCategory=categories['income'])
    else:
        return '<h1>Entry not found<h1>', 404

@app.route('/chart', methods=['GET'])
def chart():
    return render_template('chart.html')

@app.route('/manifest.json')
def serve_manifest():
    return send_file('manifest.json', mimetype='application/manifest+json')

@app.route('/sw.js')
def serve_sw():
    return send_file('sw.js', mimetype='application/javascript')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/test')
def connection_test():
    return 'OK'

if __name__ == '__main__':

    try:
        with open("SSHconfig.json", 'r') as f:
            keys = json.load(f)
            SSH_KEY = ( keys["SSL_CERT_PATH"], keys["SSL_KEY_PATH"] )
            with open(keys["SSL_CERT_PATH"], 'r') as f:
                pass
            with open(keys["SSL_KEY_PATH"] , 'r') as f:
                pass

    except:
        SSH_KEY = ( "", "" )

    if SSH_KEY[0] != "" and SSH_KEY[1] != "":
        app.run(host='0.0.0.0', debug=False, port=5000, ssl_context=SSH_KEY)
    else:
        print("Failed to load SSH keys, run it on HTTP without some PWA eatures!")
        app.run(host='0.0.0.0', debug=False, port=5000)
