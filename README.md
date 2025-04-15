# Colorscheme Generator 🎨

A lightweight Python utility to generate dynamic color schemes from a single base color.

Provides HSL-based color transformations for theming, UI design, and CSS variable generation.

Optimized for integration in Python projects, Flask applications, and Ansible roles.

---

## Installation 🚀

This package is available via Kevin's Package Manager:  
https://github.com/kevinveenbirkenbach/package-manager

Add to your `requirements.txt`:

```
colorscheme-generator @ https://github.com/kevinveenbirkenbach/colorscheme-generator/archive/refs/tags/0.1.0.zip
```

Or install manually inside your Python project:

```bash
pip install git+https://github.com/kevinveenbirkenbach/colorscheme-generator.git
```

---

## Usage 🐍

Example usage in a Python script:

```python
from colorscheme_generator import adjust_color, adjust_color_rgb

base_color = "#ff0000"

print(adjust_color(base_color, hue_shift=180))
# -> '#00ffff'

print(adjust_color_rgb(base_color, hue_shift=180))
# -> '0,255,255'
```

---

## About 🧑‍💻

Developed with ❤️ by Kevin Veen-Birkenbach  
https://www.veen.world

This package is part of Kevin's personal ecosystem and package management strategy.

More information about the design and development can be found in this conversation:  
👉 [ChatGPT Conversation](https://chatgpt.com/share/67fe6c23-b810-800f-9915-b5fa68a987a6)

---

## License 📜

MIT License