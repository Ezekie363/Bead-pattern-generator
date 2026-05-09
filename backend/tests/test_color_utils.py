import sys, os
import pytest
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from color_utils import hex_to_rgb, rgb_to_lab, find_nearest_color, precompute_palette_labs

def test_hex_to_rgb_white():
    assert hex_to_rgb('#FFFFFF') == (255, 255, 255)

def test_hex_to_rgb_black():
    assert hex_to_rgb('#000000') == (0, 0, 0)

def test_hex_to_rgb_color():
    assert hex_to_rgb('#FF8000') == (255, 128, 0)

def test_rgb_to_lab_white():
    L, a, b = rgb_to_lab((255, 255, 255))
    assert abs(L - 100.0) < 1.0

def test_rgb_to_lab_black():
    L, a, b = rgb_to_lab((0, 0, 0))
    assert abs(L) < 1.0

def test_find_nearest_color_exact():
    palette = [
        {'code': 'R', 'name': '红', 'hex': '#FF0000'},
        {'code': 'G', 'name': '绿', 'hex': '#00FF00'},
        {'code': 'B', 'name': '蓝', 'hex': '#0000FF'},
    ]
    result = find_nearest_color((0, 0, 200), palette)
    assert result['code'] == 'B'

def test_find_nearest_color_approximate():
    palette = [
        {'code': 'W', 'name': '白', 'hex': '#FFFFFF'},
        {'code': 'K', 'name': '黑', 'hex': '#000000'},
    ]
    result = find_nearest_color((240, 240, 240), palette)
    assert result['code'] == 'W'


def test_precompute_palette_labs_shape():
    palette = [
        {'code': 'R', 'name': '红', 'hex': '#FF0000'},
        {'code': 'G', 'name': '绿', 'hex': '#00FF00'},
        {'code': 'B', 'name': '蓝', 'hex': '#0000FF'},
    ]
    labs = precompute_palette_labs(palette)
    assert isinstance(labs, np.ndarray)
    assert labs.shape == (3, 3)


def test_find_nearest_color_empty_palette():
    with pytest.raises(ValueError, match="Palette cannot be empty"):
        find_nearest_color((255, 0, 0), [])


def test_find_nearest_color_with_precomputed_labs():
    palette = [
        {'code': 'R', 'name': '红', 'hex': '#FF0000'},
        {'code': 'G', 'name': '绿', 'hex': '#00FF00'},
        {'code': 'B', 'name': '蓝', 'hex': '#0000FF'},
    ]
    palette_labs = precompute_palette_labs(palette)
    result = find_nearest_color((0, 0, 200), palette, palette_labs=palette_labs)
    assert result['code'] == 'B'
