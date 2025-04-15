from colorscheme_generator import adjust_color, adjust_color_rgb

def test_adjust_color():
    assert adjust_color("#336699", target_lightness=0.5).startswith("#")

def test_adjust_color_rgb():
    assert adjust_color_rgb("#336699", target_lightness=0.5).count(",") == 2
