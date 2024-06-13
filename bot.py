from flask import Flask, request, render_template, send_from_directory, send_file
from datetime import datetime
import json
import os

app = Flask(__name__)

LOG_FILE = 'log.json'

def init_log():
    if not os.path.isfile(LOG_FILE) or os.stat(LOG_FILE).st_size == 0:
        with open(LOG_FILE, 'w') as f:
            data = {"sum": 0, "log": []}
            json.dump(data, f)

@app.route('/', methods=['GET', 'POST'])
def home():
    init_log()
    if request.method == 'POST':
        
        user_input = request.form['content_of_textbox'].strip()
        category   = request.form['category']

        with open(LOG_FILE, 'r') as f:
            data = json.load(f)
        if user_input == '':
            return render_template('result.html', data=data, info="Data Preview")
        try:
            amount, desc = user_input.split('/', 1)
            amount = int(amount)
            desc = str(desc).strip()
            dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            result = {"amount": amount, "description": desc, "datetime": dt, 'category': category}
            with open(LOG_FILE, 'r') as f:
                data = json.load(f)
            data['log'].insert(0, result)
            data['sum'] += amount
            with open(LOG_FILE, 'w') as f:
                json.dump(data, f)

            # Display the sum and the input log as a table
            return render_template('result.html', data=data, info="Save Successfully!")
        except Exception as e:
            if user_input == '/zero':
                os.remove(LOG_FILE)
                init_log()
                with open(LOG_FILE, 'r') as f:
                    data = json.load(f)
                return render_template('result.html', data=data, info="Data Have Been Reset.")
            elif user_input == '/delete':
                data['sum'] -= data['log'][0]['amount']
                del data['log'][0]
                with open(LOG_FILE, 'w') as f:
                    json.dump(data, f)
                return render_template('result.html', data=data, info="Deleted Latest Data.")
            else:
                return f'<h1>Error: Invalid input format.</h1>'
    return render_template('home.html')

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
