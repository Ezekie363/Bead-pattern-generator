from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json, os

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

PALETTES_DIR = os.path.join(os.path.dirname(__file__), 'palettes')

PALETTE_META = {
    'sanbing': {'name': '散兵', 'file': 'sanbing.json'},
    'perler':  {'name': 'Perler', 'file': 'perler.json'},
    'hama':    {'name': 'Hama',   'file': 'hama.json'},
}

@app.route('/')
def index():
    return send_from_directory('../frontend', 'index.html')

@app.route('/api/palettes')
def get_palettes():
    return jsonify([{'id': k, 'name': v['name']} for k, v in PALETTE_META.items()])

if __name__ == '__main__':
    app.run(debug=True, port=5000)
