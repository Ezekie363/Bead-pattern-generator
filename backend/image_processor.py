import io
from PIL import Image
from color_utils import find_nearest_color, precompute_palette_labs


def process_image(image_data: bytes, palette: list, width: int, height: int) -> dict:
    img = Image.open(io.BytesIO(image_data)).convert('RGB')
    img = img.resize((width, height), Image.LANCZOS)

    try:
        pixels = list(img.get_flattened_data())  # Pillow 14+
    except AttributeError:
        pixels = list(img.getdata())
    palette_labs = precompute_palette_labs(palette)
    color_map = {c['code']: c for c in palette}

    grid = []
    color_counts = {}

    for row_idx in range(height):
        row = []
        for col_idx in range(width):
            pixel = pixels[row_idx * width + col_idx]
            nearest = find_nearest_color(pixel, palette, palette_labs)
            code = nearest['code']
            row.append(code)
            color_counts[code] = color_counts.get(code, 0) + 1
        grid.append(row)

    stats = [
        {
            'code': code,
            'count': count,
            'hex': color_map[code]['hex'],
            'name': color_map[code]['name'],
        }
        for code, count in sorted(color_counts.items(), key=lambda x: -x[1])
    ]

    return {'grid': grid, 'stats': stats, 'width': width, 'height': height}
