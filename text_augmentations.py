import random
from PIL import Image, ImageEnhance, ImageFilter

def random_augment(image, augmentation_prob=0.5, max_augmentations=3, 
                  stretch_range=(1.1, 1.3), compress_range=(0.7, 0.9),
                  rotation_range=(-25, 25), color_range=(0.3, 0.8),
                  blur_range=(0, 1), noise_range=(0, 10)):
    """
    Randomly apply augmentations to an image with configurable probability.
    
    Args:
        image: A PIL Image object
        augmentation_prob: Probability of applying any augmentation (default: 0.5)
        max_augmentations: Maximum number of augmentations to apply (default: 3)
        stretch_range: Range for stretch factors (default: (1.1, 1.3))
        compress_range: Range for compression factors (default: (0.7, 0.9))
        rotation_range: Range for rotation angles in degrees (default: (-25, 25))
        color_range: Range for color degradation factors (default: (0.3, 0.8))
        blur_range: Range for Gaussian blur radius (default: (0, 1))
        noise_range: Range for noise intensity (default: (0, 10))
        
    Returns:
        The augmented PIL Image object
    """
    if random.random() < augmentation_prob:
        return image
        
    img = image.copy()
    
    # Define all possible augmentations with their functions
    augmentations = {
        'stretch_horizontal': lambda img: img.resize(
            (int(img.width * random.uniform(*stretch_range)), img.height), 
            Image.LANCZOS
        ),
        'stretch_vertical': lambda img: img.resize(
            (img.width, int(img.height * random.uniform(*stretch_range))), 
            Image.LANCZOS
        ),
        'compress_horizontal': lambda img: img.resize(
            (int(img.width * random.uniform(*compress_range)), img.height), 
            Image.LANCZOS
        ),
        'compress_vertical': lambda img: img.resize(
            (img.width, int(img.height * random.uniform(*compress_range))), 
            Image.LANCZOS
        ),
        'color_degradation': lambda img: ImageEnhance.Color(img).enhance(
            random.uniform(*color_range)
        ),
        'brightness': lambda img: ImageEnhance.Brightness(img).enhance(
            random.uniform(0.8, 1.2)
        ),
        'contrast': lambda img: ImageEnhance.Contrast(img).enhance(
            random.uniform(0.8, 1.2)
        ),
        'sharpness': lambda img: ImageEnhance.Sharpness(img).enhance(
            random.uniform(0.8, 1.2)
        ),
        'rotation': lambda img: img.rotate(
            random.uniform(*rotation_range), 
            resample=Image.BICUBIC, 
            expand=True
        ),
        'gaussian_blur': lambda img: img.filter(
            ImageFilter.GaussianBlur(radius=random.uniform(*blur_range))
        ),
        'noise': lambda img: add_noise(img, random.uniform(*noise_range))
    }
    
    # Select random augmentations
    num_augmentations = random.randint(1, max_augmentations)
    selected_augmentations = random.sample(list(augmentations.keys()), num_augmentations)
    
    # Apply selected augmentations
    for aug_name in selected_augmentations:
        img = augmentations[aug_name](img)
        
    return img

def add_noise(image, intensity):
    """
    Add random noise to an image.
    
    Args:
        image: A PIL Image object
        intensity: Intensity of the noise (0-255)
        
    Returns:
        PIL Image with added noise
    """
    # Convert to numpy array for faster processing
    import numpy as np
    img_array = np.array(image)
    
    # Generate random noise
    noise = np.random.normal(0, intensity, img_array.shape).astype(np.uint8)
    
    # Add noise to image
    noisy_img = np.clip(img_array + noise, 0, 255).astype(np.uint8)
    
    # Convert back to PIL Image
    return Image.fromarray(noisy_img)