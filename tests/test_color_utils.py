from colorscheme_generator import adjust_color, adjust_color_rgb

def test_adjust_color():
    assert adjust_color("#ff0000", hue_shift=180) == "#00ffff"

def test_adjust_color_rgb():
    assert adjust_color_rgb("#ff0000", hue_shift=180) == "0,255,255"
