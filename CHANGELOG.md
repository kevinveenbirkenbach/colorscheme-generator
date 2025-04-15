# Changelog

All notable changes to this project will be documented in this file.

This project adheres to [Semantic Versioning](https://semver.org/).

---

## [0.3.0] - 2025-04-16
### Added
- Added a new parameter `invert_lightness` to the `generate_full_palette()` function. When enabled, it inverts the progression of the target lightness (from 1.0 down to 0.0) instead of the normal progression (0.0 to 1.0).
- Included additional tests to verify that the last palette entries (both HEX and RGB) are correctly computed when using the new `invert_lightness` parameter.

### Changed
- Updated `generate_full_palette()` to forward all parameters (including the new `invert_lightness`) to the underlying color adjustment functions (`adjust_color` and `adjust_color_rgb`).

---

## [0.2.0] - 2025-04-15
### Added
- New function `generate_hex_palette(base_color, count)`  
  Generates a list of HEX colors by evenly distributing the hue around the color wheel.

- New function `generate_full_palette(base_color, count, shades)`  
  Generates a full color palette including lightness variations for each base color.  
  Returns a dictionary with CSS variable names for HEX and RGB values:
  - `--color-{color_index}-{shade}`
  - `--color-rgb-{color_index}-{shade}`

### Changed
- Internal improvements to testing:
  - Added tests for `generate_hex_palette`
  - Added tests for `generate_full_palette`
  - Improved test coverage for edge cases and variable naming.

---

## [0.1.0] - 2025-04-15
### Initial Release
- First public release of `colorscheme-generator`.
- Provides HSL-based color adjustment functions:
  - `adjust_color(hex_color, ...)`
  - `adjust_color_rgb(hex_color, ...)`
- Supports basic color manipulation:
  - Hue shift
  - Lightness adjustment
  - Saturation adjustment
- Optimized for Python projects, Flask applications, and Ansible roles.