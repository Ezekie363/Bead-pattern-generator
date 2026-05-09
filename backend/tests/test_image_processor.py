import sys, os, io
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from PIL import Image
from image_processor import process_image

PALETTE = [
    {'code': 'W', 'name': '白', 'hex': '#FFFFFF'},
    {'code': 'K', 'name': '黑', 'hex': '#000000'},
    {'code': 'R', 'name': '红', 'hex': '#FF0000'},
]

def _make_image_bytes(color=(255, 0, 0), size=(10, 10)):
    img = Image.new('RGB', size, color)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return buf.getvalue()

def test_process_returns_correct_grid_size():
    data = _make_image_bytes()
    result = process_image(data, PALETTE, 4, 4)
    assert result['width'] == 4
    assert result['height'] == 4
    assert len(result['grid']) == 4
    assert len(result['grid'][0]) == 4

def test_process_maps_red_to_red():
    data = _make_image_bytes(color=(255, 0, 0))
    result = process_image(data, PALETTE, 3, 3)
    assert all(code == 'R' for row in result['grid'] for code in row)

def test_process_stats_count():
    data = _make_image_bytes(color=(255, 0, 0))
    result = process_image(data, PALETTE, 3, 3)
    assert result['stats'][0]['code'] == 'R'
    assert result['stats'][0]['count'] == 9

def test_process_stats_sorted_by_count_desc():
    # Create a mostly-white image with one black pixel
    img = Image.new('RGB', (4, 4), (255, 255, 255))
    img.putpixel((0, 0), (0, 0, 0))
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    result = process_image(buf.getvalue(), PALETTE, 4, 4)
    counts = [s['count'] for s in result['stats']]
    assert counts == sorted(counts, reverse=True)
