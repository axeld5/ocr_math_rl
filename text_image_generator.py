import random
import os
from PIL import Image
from create_text_image import create_text_image
from text_augmentations import random_augment

def generate_augmented_text_image(text, font_path=None):
    """
    Generate an image of the given text with random augmentations.
    
    Args:
        text (str): The text to generate an image for
        font_path (str, optional): Path to a TTF font file. If None, default font will be used.
        
    Returns:
        PIL.Image: The augmented text image
    """
    # Randomly select text styling parameters
    font_size = random.randint(20, 40)
    bg_color = (
        random.randint(240, 255),  # Light background
        random.randint(240, 255),
        random.randint(240, 255)
    )
    text_color = (
        random.randint(0, 50),  # Dark text
        random.randint(0, 50),
        random.randint(0, 50)
    )
    
    # Randomly decide on text effects
    add_shadow = random.random() < 0.3
    add_outline = random.random() < 0.2
    add_texture = random.random() < 0.2
    add_gradient = random.random() < 0.2
    add_border = random.random() < 0.2
    
    # Randomly select text alignment
    text_alignment = random.choice(['left', 'center', 'right'])
    
    # Create the base text image
    img, _ = create_text_image(
        text=text,
        words_per_line=random.randint(5, 10),
        font_path=font_path,
        font_size=font_size,
        bg_color=bg_color,
        text_color=text_color,
        padding=random.randint(15, 30),
        line_spacing=random.uniform(1.1, 1.4),
        add_shadow=add_shadow,
        add_outline=add_outline,
        add_texture=add_texture,
        add_gradient=add_gradient,
        add_border=add_border,
        text_alignment=text_alignment
    )
    
    # Apply random augmentations to the image
    augmented_img = random_augment(
        image=img,
        augmentation_prob=0.8,  # High probability of applying augmentations
        max_augmentations=random.randint(1, 4),
        stretch_range=(1.05, 1.2),
        compress_range=(0.8, 0.95),
        rotation_range=(-15, 15),
        color_range=(0.1, 0.3),
        blur_range=(0, 0.5),
        noise_range=(0, 5)
    )
    
    return augmented_img

def save_augmented_text_image(text, output_path, font_path=None):
    """
    Generate an augmented text image and save it to the specified path.
    
    Args:
        text (str): The text to generate an image for
        output_path (str): Path where the image should be saved
        font_path (str, optional): Path to a TTF font file. If None, default font will be used.
        
    Returns:
        str: Path to the saved image
    """
    # Create the augmented image
    img = generate_augmented_text_image(text, font_path)
    
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save the image
    img.save(output_path)
    
    return output_path

# Example usage
if __name__ == "__main__":
    sample_text = "This is a sample text that will be converted to an image with random augmentations."
    output_path = "output/augmented_text.png"
    
    # You can specify a font path if you have one
    # font_path = "path/to/your/font.ttf"
    font_path = None
    
    saved_path = save_augmented_text_image(sample_text, output_path, font_path)
    print(f"Augmented text image saved to: {saved_path}") 