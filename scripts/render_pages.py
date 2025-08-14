import os
import sys
import json
import shutil

# Allow importing from repository root
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from flask import render_template
from bot import app

OUTPUT_DIR = 'public'

# Use sample data
CATEGORIES_FILE = 'example_categories.json'
LOG_FILE = 'example_log.json'

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)
shutil.copytree('static', os.path.join(OUTPUT_DIR, 'static'), dirs_exist_ok=True)
shutil.copy('manifest.json', OUTPUT_DIR)
shutil.copy('sw.js', OUTPUT_DIR)

# Provide API data files for front-end scripts
shutil.copy(LOG_FILE, os.path.join(OUTPUT_DIR, 'get_log'))
shutil.copy(CATEGORIES_FILE, os.path.join(OUTPUT_DIR, 'get_categories'))


def replace_paths(html: str) -> str:
    replacements = {
        'href="/manifest.json"': 'href="manifest.json"',
        "fetch('/get_log')": "fetch('get_log')",
        "fetch('/get_categories')": "fetch('get_categories')",
        'href="/edit_categories"': 'href="edit_categories.html"',
        'href="/load_CSV"': 'href="load_CSV.html"',
        'href="/chart"': 'href="chart.html"',
    }
    for old, new in replacements.items():
        html = html.replace(old, new)
    return html


# Replace url_for to generate relative static paths
@app.context_processor
def override_url_for():
    def _url_for(endpoint, **values):
        if endpoint == 'static':
            filename = values.get('filename', '')
            return f'static/{filename}'
        return endpoint
    return dict(url_for=_url_for)


with app.app_context():
    with open(CATEGORIES_FILE) as f:
        categories = json.load(f)
    with open(LOG_FILE) as f:
        log_data = json.load(f)
    entry = log_data['log'][0]

    pages = {
        'index.html': render_template('home.html', expenseCategory=categories['expense'], incomeCategory=categories['income']),
        'edit_categories.html': render_template('edit_categories.html', categories=categories),
        'chart.html': render_template('chart.html'),
        'load_CSV.html': render_template('load_CSV.html'),
        'result.html': render_template('result.html', info='Demo preview message'),
        'edit_log.html': render_template('edit_log.html', entry=entry, expenseCategory=categories['expense'], incomeCategory=categories['income']),
    }

    for filename, html in pages.items():
        html = replace_paths(html)
        with open(os.path.join(OUTPUT_DIR, filename), 'w', encoding='utf-8') as f:
            f.write(html)
