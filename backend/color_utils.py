import numpy as np


def hex_to_rgb(hex_color: str) -> tuple:
    h = hex_color.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_lab(rgb: tuple) -> tuple:
    r, g, b = [x / 255.0 for x in rgb]

    def linearize(c):
        return ((c + 0.055) / 1.055) ** 2.4 if c > 0.04045 else c / 12.92

    r, g, b = linearize(r), linearize(g), linearize(b)

    # sRGB -> XYZ (D65)
    x = r * 0.4124564 + g * 0.3575761 + b * 0.1804375
    y = r * 0.2126729 + g * 0.7151522 + b * 0.0721750
    z = r * 0.0193339 + g * 0.1191920 + b * 0.9503041

    # Normalize by D65 white point
    x /= 0.95047
    y /= 1.00000
    z /= 1.08883

    def f(t):
        return t ** (1/3) if t > 0.008856 else (903.3 * t + 16) / 116

    fx, fy, fz = f(x), f(y), f(z)
    L = 116 * fy - 16
    a = 500 * (fx - fy)
    b_val = 200 * (fy - fz)
    return (L, a, b_val)


def find_nearest_color(pixel_rgb: tuple, palette: list) -> dict:
    pixel_lab = np.array(rgb_to_lab(pixel_rgb))
    min_dist = float('inf')
    nearest = palette[0]
    for color in palette:
        color_lab = np.array(rgb_to_lab(hex_to_rgb(color['hex'])))
        dist = float(np.sum((pixel_lab - color_lab) ** 2))
        if dist < min_dist:
            min_dist = dist
            nearest = color
    return nearest
