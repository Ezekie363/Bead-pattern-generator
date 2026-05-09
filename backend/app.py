from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json, os

from image_processor import process_image

app = Flask(__name__, static_folder='../frontend', static_url_path='')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB upload limit
CORS(app, origins=['http://localhost:5000', 'http://127.0.0.1:5000'])

PALETTES_DIR = os.path.join(os.path.dirname(__file__), 'palettes')

PALETTE_META = {
    'sanbing': {'name': '散兵', 'file': 'sanbing.json'},
    'perler':  {'name': 'Perler', 'file': 'perler.json'},
    'hama':    {'name': 'Hama',   'file': 'hama.json'},
}


def load_palette(palette_id: str) -> list:
    meta = PALETTE_META[palette_id]
    path = os.path.join(PALETTES_DIR, meta['file'])
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/api/palettes')
def get_palettes():
    return jsonify([{'id': k, 'name': v['name']} for k, v in PALETTE_META.items()])


@app.route('/api/process', methods=['POST'])
def process():
    if 'image' not in request.files:
        return jsonify({'error': '未上传图片'}), 400

    image_file = request.files['image']
    palette_id = request.form.get('palette', 'sanbing')
    try:
        width = int(request.form.get('width', 48))
        height = int(request.form.get('height', 48))
    except ValueError:
        return jsonify({'error': '尺寸参数无效'}), 400

    if palette_id not in PALETTE_META:
        return jsonify({'error': '无效的色板 ID'}), 400
    if not (1 <= width <= 200) or not (1 <= height <= 200):
        return jsonify({'error': '尺寸超出范围（1-200）'}), 400

    palette = load_palette(palette_id)
    image_data = image_file.read()

    try:
        result = process_image(image_data, palette, width, height)
    except Exception as e:
        return jsonify({'error': f'图像处理失败：{str(e)}'}), 500

    return jsonify(result)


if __name__ == '__main__':
    debug = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(debug=debug, port=5000)
