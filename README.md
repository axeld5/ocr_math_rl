# Text Image Generator with Augmentations

This project provides tools to generate images from text with random augmentations, which can be useful for OCR training, data augmentation, or creating visually interesting text images.

## Features

- Generate images from text with customizable styling
- Apply random augmentations to the generated images
- Command-line interface for easy use
- Support for custom fonts

## Installation

1. Clone this repository
2. Install the required dependencies:

```bash
pip install pillow numpy
```

## Usage

### Command Line Interface

The easiest way to use this tool is through the command-line interface:

```bash
python text_image_cli.py "Your text here" --output output/my_image.png
```

Options:
- `--output` or `-o`: Specify the output path (default: output/augmented_text.png)
- `--font` or `-f`: Specify a custom TTF font file

### Python API

You can also use the Python API directly:

```python
from text_image_generator import generate_augmented_text_image, save_augmented_text_image

# Generate an image without saving
img = generate_augmented_text_image("Your text here")

# Generate and save an image
saved_path = save_augmented_text_image("Your text here", "output/my_image.png")
```

## Examples

```python
# Basic usage
from text_image_generator import save_augmented_text_image

save_augmented_text_image("Hello, World!", "output/hello_world.png")

# With a custom font
save_augmented_text_image("Styled Text", "output/styled_text.png", font_path="path/to/font.ttf")
```

## How It Works

1. The text is first converted to an image using the `create_text_image` function, which applies various styling options like font size, colors, shadows, etc.
2. The generated image is then passed to the `random_augment` function, which applies random augmentations like stretching, compression, rotation, color changes, blur, and noise.

## Customization

You can customize the text image generation and augmentation process by modifying the parameters in the `generate_augmented_text_image` function in `text_image_generator.py`.
