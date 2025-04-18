import colorsys

def adjust_color(hex_color, target_lightness=None, lightness_change=0, hue_shift=0, saturation_change=0):
    """
    Adjust a HEX color in HSL space.

    - target_lightness: If provided (0 to 1), the lightness is set absolutely to this value.
      Otherwise, lightness_change is applied additively (in percentage points, where 100 => 1 in HSL).
    - lightness_change: Percentage points to add or subtract from lightness (if target_lightness is None).
    - hue_shift: Degrees to shift hue (e.g., +180 for complementary).
    - saturation_change: Percentage points to add or subtract from saturation.
    
    Uses a 'cyclical' approach for lightness and saturation if no target_lightness is provided:
      If the new value goes above 1, it wraps around (subtract 1).
      If it goes below 0, it wraps around (add 1).
    """

    # Strip leading '#' if present
    hex_color = hex_color.lstrip('#')
    
    # Parse the original RGB values
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    
    # Convert from [0..255] range to [0..1] for colorsys
    r /= 255.0
    g /= 255.0
    b /= 255.0
    
    # Convert RGB -> HLS (colorsys uses HLS, also hier: Hue, Lightness, Saturation)
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    
    # Shift hue by (hue_shift / 360)
    h = (h + (hue_shift / 360.0)) % 1.0
    
    # Adjust saturation (cyclically)
    s_new = s + (saturation_change / 100.0)
    if s_new > 1:
        s_new -= 1
    elif s_new < 0:
        s_new += 1

    # Adjust lightness: either set to a target or change it additively (cyclically)
    if target_lightness is not None:
        l_new = target_lightness
    else:
        l_new = l + (lightness_change / 100.0)
        if l_new > 1:
            l_new -= 1
        elif l_new < 0:
            l_new += 1

    # Convert back to RGB
    new_r, new_g, new_b = colorsys.hls_to_rgb(h, l_new, s_new)
    
    # Scale back to [0..255] and format as HEX
    new_r = int(new_r * 255)
    new_g = int(new_g * 255)
    new_b = int(new_b * 255)
    
    return '#{:02x}{:02x}{:02x}'.format(new_r, new_g, new_b)

def adjust_color_rgb(hex_color, target_lightness=None, lightness_change=0, hue_shift=0, saturation_change=0):
    """
    Wrapper function for adjust_color.
    
    Calls adjust_color to get the adjusted HEX color and then converts it to a string 
    of comma-separated RGB values.
    """
    adjusted_hex = adjust_color(
        hex_color,
        target_lightness=target_lightness,
        lightness_change=lightness_change,
        hue_shift=hue_shift,
        saturation_change=saturation_change
    )
    
    # Remove '#' and parse the RGB components
    hex_val = adjusted_hex.lstrip('#')
    r = int(hex_val[0:2], 16)
    g = int(hex_val[2:4], 16)
    b = int(hex_val[4:6], 16)
    
    return f"{r},{g},{b}"

def generate_hex_palette(base_color, count=7):
    """
    Generate a palette of HEX colors from a base color.

    Colors are evenly distributed by hue rotation.

    Args:
        base_color (str): HEX color string like '#ff0000'
        count (int): Number of colors to generate

    Returns:
        list[str]: List of HEX colors
    """
    palette = []
    for i in range(count):
        hue_shift = (360 / count) * i
        hex_color = adjust_color(base_color, hue_shift=hue_shift)
        palette.append(hex_color)
    return palette

def generate_full_palette(
    base_color,
    count=7,
    shades=100,
    invert_lightness=False,
    lightness_change=0,
    hue_shift=0,
    saturation_change=0
):
    """
    Generate a full palette of HEX and RGB colors based on a base color.
    
    For each of the 'count' base colors (generated via hue rotation from the base_color),
    this function creates 'shades' lightness variations. The lightness values can be inverted
    if desired.
    
    Args:
        base_color (str): The base HEX color (e.g., "#ff0000").
        count (int): Number of base colors to generate.
        shades (int): Number of lightness variations to generate per base color.
        invert_lightness (bool): If True, computes lightness in reverse order (from 1 to 0).
        lightness_change (float): Additional lightness adjustment in percentage points.
        hue_shift (float): Additional hue shift in degrees.
        saturation_change (float): Additional saturation adjustment in percentage points.
    
    Returns:
        dict: Dictionary mapping CSS variable names to HEX and RGB values.
              For example:
                '--color-01-00': HEX color,
                '--color-rgb-01-00': corresponding RGB value.
    """
    full_palette = {}
    
    # Generate the base colors by rotating the hue from the given base_color.
    base_colors = generate_hex_palette(base_color, count)
    
    for color_index, color in enumerate(base_colors):
        for shade in range(shades):
            # Calculate target lightness value.
            # When invert_lightness is True, the lightness starts at 1 and decreases to 0,
            # otherwise it increases from 0 to 1.
            # Using (shades - 1) ensures a consistent distribution regardless of the number of shades.
            computed_target = 1 - (shade / (shades - 1)) if invert_lightness else shade / (shades - 1)
            
            # Adjust the HEX color using the computed target lightness and additional parameters.
            hex_value = adjust_color(
                color,
                target_lightness=computed_target,
                lightness_change=lightness_change,
                hue_shift=hue_shift,
                saturation_change=saturation_change
            )
            # Adjust the color and return its RGB representation.
            rgb_value = adjust_color_rgb(
                color,
                target_lightness=computed_target,
                lightness_change=lightness_change,
                hue_shift=hue_shift,
                saturation_change=saturation_change
            )
            
            # Create CSS variable names formatted with two-digit indices.
            full_palette[f'--color-{color_index+1:02d}-{shade:02d}'] = hex_value
            full_palette[f'--color-rgb-{color_index+1:02d}-{shade:02d}'] = rgb_value

    return full_palette

