import os
from text_image_generator import generate_augmented_text_image, save_augmented_text_image

def main():
    """
    Example script demonstrating how to use the text image generator.
    """
    # Create output directory if it doesn't exist
    os.makedirs("output", exist_ok=True)
    
    # Example 1: Basic usage
    text1 = "This is a simple example of text to image conversion with augmentations."
    save_augmented_text_image(text1, "output/example1.png")
    print(f"Example 1 saved to: output/example1.png")
    
    # Example 2: Mathematical expression
    text2 = "E = mc^2"
    save_augmented_text_image(text2, "output/example2.png")
    print(f"Example 2 saved to: output/example2.png")
    
    # Example 3: Multiple lines
    text3 = "This is a multi-line text.\nIt has several lines.\nEach line will be rendered separately."
    save_augmented_text_image(text3, "output/example3.png")
    print(f"Example 3 saved to: output/example3.png")
    
    # Example 4: Generate multiple variations of the same text
    text4 = "Generate multiple variations of the same text"
    for i in range(3):
        output_path = f"output/example4_variation{i+1}.png"
        save_augmented_text_image(text4, output_path)
        print(f"Example 4 variation {i+1} saved to: {output_path}")
    
    print("\nAll examples have been generated successfully!")

if __name__ == "__main__":
    main() 