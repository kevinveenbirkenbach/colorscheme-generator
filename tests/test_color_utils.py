from colorscheme_generator import adjust_color, adjust_color_rgb


def hex_to_rgb(hex_color):
    """Convert HEX color to RGB tuple."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def parse_rgb_string(rgb_string):
    """Convert 'r,g,b' string to RGB tuple of ints."""
    return tuple(map(int, rgb_string.split(',')))


def test_adjust_color():
    expected = hex_to_rgb("#00ffff")
    result = hex_to_rgb(adjust_color("#ff0000", hue_shift=180))
    assert all(abs(a - b) <= 1 for a, b in zip(expected, result))


def test_adjust_color_rgb():
    expected = parse_rgb_string("0,255,255")
    result = parse_rgb_string(adjust_color_rgb("#ff0000", hue_shift=180))
    assert all(abs(a - b) <= 1 for a, b in zip(expected, result))
