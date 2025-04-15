from colorscheme_generator import adjust_color, adjust_color_rgb, generate_hex_palette, generate_full_palette

def test_generate_hex_palette():
    palette = generate_hex_palette("#ff0000", count=5)
    
    assert len(palette) == 5

    for color in palette:
        assert isinstance(color, str)
        assert color.startswith("#")
        assert len(color) == 7

import re
from colorscheme_generator import (
    generate_full_palette,
    generate_hex_palette,
    adjust_color,
    adjust_color_rgb
)

def test_generate_full_palette_normal_lightness():
    """
    Test generate_full_palette() with invert_lightness set to False.
    
    Verifies that:
    - The returned dictionary contains the expected number of keys.
    - The CSS variable keys are correctly formatted.
    - The HEX and RGB values have the correct format.
    - The last element of the palette is correct.
    """
    count = 3
    shades = 10
    palette = generate_full_palette("#ff0000", count=count, shades=shades, invert_lightness=False)
    
    # Expected dictionary size: (base colors * shades * 2) [HEX and RGB values for each shade]
    expected_length = count * shades * 2
    assert len(palette) == expected_length, "Palette does not contain the expected number of entries"
    
    # Check specific key formats for the first base color
    first_hex_key = "--color-01-00"
    first_rgb_key = "--color-rgb-01-00"
    assert first_hex_key in palette, f"Expected key {first_hex_key} not found in palette"
    assert first_rgb_key in palette, f"Expected key {first_rgb_key} not found in palette"
    
    # Verify HEX format: "#" followed by six hexadecimal digits (case-insensitive)
    hex_value = palette[first_hex_key]
    assert hex_value.startswith("#") and len(hex_value) == 7, "HEX color should be in the format '#rrggbb'"
    assert re.fullmatch(r"#([0-9a-fA-F]{6})", hex_value), "HEX color format is incorrect"
    
    # Verify that the RGB value is in a valid format: "r,g,b" with each component between 0 and 255.
    rgb_value = palette[first_rgb_key]
    parts = rgb_value.split(",")
    assert len(parts) == 3, "RGB value must have three comma-separated components"
    for part in parts:
        assert part.isdigit(), "Each part of the RGB value should be numeric"
        value = int(part)
        assert 0 <= value <= 255, "RGB component must be between 0 and 255"

    # Additional asserts to check the last element (for the last base color)
    # For normal lightness (invert_lightness=False), the computed target for the last shade (shade index = shades-1)
    # should be: (shades-1)/(shades-1) = 1.0.
    last_hex_key = f"--color-{count:02d}-{shades-1:02d}"    # Example: '--color-03-09'
    last_rgb_key = f"--color-rgb-{count:02d}-{shades-1:02d}"   # Example: '--color-rgb-03-09'
    
    # Generate the base colors to calculate the expected value for the last entry.
    base_colors = generate_hex_palette("#ff0000", count)
    expected_last_hex = adjust_color(
         base_colors[-1],
         target_lightness=1.0,  # For the last shade in non-inverted mode.
         lightness_change=0,
         hue_shift=0,
         saturation_change=0
    )
    expected_last_rgb = adjust_color_rgb(
         base_colors[-1],
         target_lightness=1.0,
         lightness_change=0,
         hue_shift=0,
         saturation_change=0
    )
    assert palette[last_hex_key] == expected_last_hex, f"Last HEX entry {last_hex_key} is incorrect"
    assert palette[last_rgb_key] == expected_last_rgb, f"Last RGB entry {last_rgb_key} is incorrect"

def test_generate_full_palette_invert_lightness():
    """
    Test generate_full_palette() with invert_lightness set to True.
    
    Checks that:
    - The total dictionary length is as expected.
    - For the first base color, the lightness distribution is inverted:
      The first shade (shade index 00) should correspond to a target lightness of 1.0,
      and the last shade (shade index corresponding to shades-1) should correspond to 0.0.
    - The last element of the palette for the last base color is also correctly computed.
    """
    count = 3
    shades = 10
    palette = generate_full_palette("#ff0000", count=count, shades=shades, invert_lightness=True)
    
    # Expected dictionary size: (base colors * shades * 2) [HEX and RGB values]
    expected_length = count * shades * 2
    assert len(palette) == expected_length, "Palette does not contain the expected number of entries"
    
    # Retrieve the base colors for computing expected values.
    base_colors = generate_hex_palette("#ff0000", count)
    
    # For the first base color in inverted mode:
    #   For shade index 0, computed_target = 1 - (0/(shades-1)) = 1.0.
    expected_light_hex = adjust_color(
        base_colors[0],
        target_lightness=1.0,
        lightness_change=0,
        hue_shift=0,
        saturation_change=0
    )
    # For shade index (shades-1), computed_target = 1 - ((shades-1)/(shades-1)) = 0.0.
    expected_dark_hex = adjust_color(
        base_colors[0],
        target_lightness=0.0,
        lightness_change=0,
        hue_shift=0,
        saturation_change=0
    )
    assert palette["--color-01-00"] == expected_light_hex, "First shade (inverted) should have target_lightness=1.0"
    assert palette["--color-01-09"] == expected_dark_hex, "Last shade (inverted) should have target_lightness=0.0"
    
    # Additional asserts to check the last element (for the last base color) in inverted mode.
    # For the last base color, at shade index = shades-1, computed target should be 0.0.
    last_hex_key = f"--color-{count:02d}-{shades-1:02d}"    # Expected: '--color-03-09'
    last_rgb_key = f"--color-rgb-{count:02d}-{shades-1:02d}"
    
    expected_last_hex = adjust_color(
         base_colors[-1],
         target_lightness=0.0,  # For the last shade in inverted mode.
         lightness_change=0,
         hue_shift=0,
         saturation_change=0
    )
    expected_last_rgb = adjust_color_rgb(
         base_colors[-1],
         target_lightness=0.0,
         lightness_change=0,
         hue_shift=0,
         saturation_change=0
    )
    assert palette[last_hex_key] == expected_last_hex, f"Last HEX entry {last_hex_key} is incorrect for inverted lightness"
    assert palette[last_rgb_key] == expected_last_rgb, f"Last RGB entry {last_rgb_key} is incorrect for inverted lightness"

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
