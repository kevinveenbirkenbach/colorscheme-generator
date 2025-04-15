from colorscheme_generator import adjust_color, adjust_color_rgb, generate_hex_palette, generate_full_palette

def test_generate_hex_palette():
    palette = generate_hex_palette("#ff0000", count=5)
    
    assert len(palette) == 5

    for color in palette:
        assert isinstance(color, str)
        assert color.startswith("#")
        assert len(color) == 7


def test_generate_full_palette():
    palette = generate_full_palette("#ff0000", count=3, shades=10)

    # Expect correct number of variables: count * shades * 2 (HEX + RGB)
    expected_length = 3 * 10 * 2
    assert len(palette) == expected_length

    keys = list(palette.keys())

    # Check that the first key is --color-0-00
    assert keys[0] == "--color-1-00"

    # Check that the last key is --color-rgb-2-09 (count=3 => index 0–2, shades=10 => 00–09)
    assert keys[-1] == "--color-rgb-3-09"

    # Check naming and value formats
    for var_name, value in palette.items():
        assert var_name.startswith("--color-")

        if "-rgb-" in var_name:
            parts = value.split(",")
            assert len(parts) == 3
            for part in parts:
                assert part.isdigit()
                assert 0 <= int(part) <= 255
        else:
            assert value.startswith("#")
            assert len(value) == 7

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
