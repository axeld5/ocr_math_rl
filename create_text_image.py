import random
import os
import numpy as np
from PIL import ImageFont, Image, ImageDraw, ImageFilter, ImageEnhance, ImageOps

def create_text_image(
        text, 
        words_per_line=3, 
        font_path=None, 
        font_size=24, 
        bg_color=(255, 255, 255), 
        text_color=(0, 0, 0), 
        padding=20, 
        line_spacing=1.2,
        style_probabilities=None,
        add_shadow=False,
        add_outline=False,
        outline_width=1,
        outline_color=(0, 0, 0),
        outline_opacity=1.0,
        shadow_offset=(2, 2),
        shadow_color=(100, 100, 100),
        shadow_blur=2,
        add_texture=False,
        texture_intensity=0.1,
        text_alignment='center',
        max_width=None,
        max_height=None,
        add_border=False,
        border_width=5,
        border_color=(0, 0, 0),
        add_watermark=False,
        watermark_text="",
        watermark_font_size=12,
        watermark_color=(200, 200, 200),
        watermark_opacity=0.3,
        watermark_position='bottom-right',
        add_gradient=False,
        gradient_start_color=(255, 255, 255),
        gradient_end_color=(240, 240, 240),
        gradient_direction='vertical'
    ):
    """
    Create an image with styled text.
    
    Args:
        text (str): The text to place in the image
        words_per_line (int): Number of words per line
        font_path (str): Path to TTF font (or None for default)
        font_size (int): Font size for the image
        bg_color (tuple): Background color in RGB
        text_color (tuple): Text color in RGB
        padding (int): Padding around the text
        line_spacing (float): Line spacing multiplier
        style_probabilities (dict): Probabilities for different text styles
        add_shadow (bool): Whether to add a shadow to the text
        add_outline (bool): Whether to add an outline to the text
        outline_width (int): Width of the text outline
        outline_color (tuple): Color of the text outline in RGB
        outline_opacity (float): Opacity of the text outline (0-1)
        shadow_offset (tuple): Offset of the shadow (x, y)
        shadow_color (tuple): Color of the shadow in RGB
        shadow_blur (int): Blur radius for the shadow
        add_texture (bool): Whether to add texture to the background
        texture_intensity (float): Intensity of the texture (0-1)
        text_alignment (str): Text alignment ('left', 'center', 'right')
        max_width (int): Maximum width of the image (None for auto)
        max_height (int): Maximum height of the image (None for auto)
        add_border (bool): Whether to add a border around the image
        border_width (int): Width of the border
        border_color (tuple): Color of the border in RGB
        add_watermark (bool): Whether to add a watermark
        watermark_text (str): Text for the watermark
        watermark_font_size (int): Font size for the watermark
        watermark_color (tuple): Color of the watermark in RGB
        watermark_opacity (float): Opacity of the watermark (0-1)
        watermark_position (str): Position of the watermark ('top-left', 'top-right', 'bottom-left', 'bottom-right', 'center')
        add_gradient (bool): Whether to add a gradient background
        gradient_start_color (tuple): Start color of the gradient in RGB
        gradient_end_color (tuple): End color of the gradient in RGB
        gradient_direction (str): Direction of the gradient ('horizontal', 'vertical')
    
    Returns:
        PIL.Image: Image with the styled text
        dict: Information about the text positioning
    """
    # Default style probabilities if not provided
    if style_probabilities is None:
        style_probabilities = {
            'normal': 0.92,
            'bold': 0.02,
            'strikethrough': 0,
            'uppercase': 0.03,
            'italic': 0.02
        }
    
    # Validate text alignment
    if text_alignment not in ['left', 'center', 'right']:
        text_alignment = 'center'
    
    # Load fonts
    try:
        if font_path and os.path.exists(font_path):
            regular_font = ImageFont.truetype(font_path, font_size, encoding="latin-1")
            bold_font = ImageFont.truetype(font_path, font_size, encoding="latin-1")
            italic_font = ImageFont.truetype(font_path, font_size, encoding="latin-1")
        else:
            regular_font = ImageFont.load_default()
            bold_font = regular_font
            italic_font = regular_font
    except Exception as e:
        print(f"Font loading error: {e}, using default font")
        regular_font = ImageFont.load_default()
        bold_font = regular_font
        italic_font = regular_font
    
    # Split text into words and group them
    words = text.split()
    word_groups = [words[i:i + words_per_line] for i in range(0, len(words), words_per_line)]
    
    # Apply styles to words
    styled_word_groups = []
    for group in word_groups:
        styled_words = []
        for word in group:
            # Choose style based on probabilities
            style_choice = random.random()
            cumulative_prob = 0
            chosen_style = 'normal'
            
            for style, prob in style_probabilities.items():
                cumulative_prob += prob
                if style_choice <= cumulative_prob:
                    chosen_style = style
                    break
            
            # Apply the chosen style
            if chosen_style == 'strikethrough':
                styled_words.append((word, 'strikethrough'))
            elif chosen_style == 'bold':
                styled_words.append((word, 'bold'))
            elif chosen_style == 'uppercase':
                styled_words.append((word.upper(), 'normal'))
            elif chosen_style == 'italic':
                styled_words.append((word, 'italic'))
            else:
                styled_words.append((word, 'normal'))
                
        styled_word_groups.append(styled_words)
    
    # Calculate text dimensions
    temp_img = Image.new('RGB', (1, 1), bg_color)
    temp_draw = ImageDraw.Draw(temp_img)
    
    def get_text_dimensions(text, font):
        bbox = temp_draw.textbbox((0, 0), text, font=font)
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        return width, height
    
    # Calculate line widths
    line_widths = []
    for styled_words in styled_word_groups:
        line_width = 0
        for word, style in styled_words:
            if style == 'bold':
                font = bold_font
            elif style == 'italic':
                font = italic_font
            else:
                font = regular_font
                
            word_width, _ = get_text_dimensions(word + ' ', font)
            line_width += word_width
        if line_width > 0:
            space_width, _ = get_text_dimensions(' ', regular_font)
            line_width -= space_width
        line_widths.append(line_width)
    
    # Calculate image dimensions
    img_width = max(line_widths) + (padding * 2) if line_widths else padding * 2
    line_height = int(font_size * line_spacing)
    img_height = (len(styled_word_groups) * line_height) + (padding * 2)
    
    # Apply max width/height constraints if provided
    if max_width is not None and img_width > max_width:
        scale_factor = max_width / img_width
        img_width = max_width
        img_height = int(img_height * scale_factor)
        font_size = int(font_size * scale_factor)
        padding = int(padding * scale_factor)
        line_height = int(line_height * scale_factor)
        
        # Reload fonts with new size
        try:
            if font_path and os.path.exists(font_path):
                regular_font = ImageFont.truetype(font_path, font_size, encoding="latin-1")
                bold_font = ImageFont.truetype(font_path, font_size, encoding="latin-1")
                italic_font = ImageFont.truetype(font_path, font_size, encoding="latin-1")
            else:
                regular_font = ImageFont.load_default()
                bold_font = regular_font
                italic_font = regular_font
        except Exception as e:
            print(f"Font reloading error: {e}, using default font")
            regular_font = ImageFont.load_default()
            bold_font = regular_font
            italic_font = regular_font
    
    if max_height is not None and img_height > max_height:
        scale_factor = max_height / img_height
        img_height = max_height
        img_width = int(img_width * scale_factor)
        font_size = int(font_size * scale_factor)
        padding = int(padding * scale_factor)
        line_height = int(line_height * scale_factor)
        
        # Reload fonts with new size
        try:
            if font_path and os.path.exists(font_path):
                regular_font = ImageFont.truetype(font_path, font_size, encoding="latin-1")
                bold_font = ImageFont.truetype(font_path, font_size, encoding="latin-1")
                italic_font = ImageFont.truetype(font_path, font_size, encoding="latin-1")
            else:
                regular_font = ImageFont.load_default()
                bold_font = regular_font
                italic_font = regular_font
        except Exception as e:
            print(f"Font reloading error: {e}, using default font")
            regular_font = ImageFont.load_default()
            bold_font = regular_font
            italic_font = regular_font
    
    # Create base image
    img = Image.new('RGB', (img_width, img_height), bg_color)
    
    # Add gradient background if requested
    if add_gradient:
        gradient_img = create_gradient(img_width, img_height, gradient_start_color, gradient_end_color, gradient_direction)
        # Use a moderate blend factor that preserves readability while still showing the gradient
        img = Image.blend(img, gradient_img, 0.7)
    
    # Add texture to background if requested
    if add_texture:
        texture = create_texture(img_width, img_height, texture_intensity)
        # Use the actual texture_intensity directly but scale it for readability
        # This ensures the intensity parameter is meaningful while still keeping text readable
        blend_factor = texture_intensity * 0.7  # Scale down slightly for readability
        img = Image.blend(img, texture, blend_factor)
    
    draw = ImageDraw.Draw(img)
    
    # Draw text with effects
    lines_info = []
    for i, (styled_words, line_width) in enumerate(zip(styled_word_groups, line_widths)):
        # Calculate x position based on alignment
        if text_alignment == 'left':
            x_pos = padding
        elif text_alignment == 'right':
            x_pos = img_width - padding - line_width
        else:  # center
            x_pos = padding + (img_width - 2 * padding - line_width) // 2
            
        y_pos = padding + (i * line_height)
        current_x = x_pos
        word_positions = []
        rendered_text = ''
        
        for word, style in styled_words:
            if style == 'bold':
                font = bold_font
            elif style == 'italic':
                font = italic_font
            else:
                font = regular_font
                
            word_width, word_height = get_text_dimensions(word, font)
            
            # Draw outline if requested
            if add_outline:
                # Draw outline using a more selective approach to avoid overwhelming the text
                # Just draw at the major compass points and diagonals for a cleaner look
                outline_positions = [
                    (-outline_width, 0), (outline_width, 0),  # Left and right
                    (0, -outline_width), (0, outline_width),  # Top and bottom
                ]
                
                # Add diagonal positions only for wider outlines
                if outline_width > 1:
                    outline_positions.extend([
                        (-outline_width, -outline_width), (outline_width, outline_width),  # Diagonals
                        (-outline_width, outline_width), (outline_width, -outline_width)
                    ])
                
                # Adjust outline color based on opacity (blend with background color)
                if outline_opacity < 1.0:
                    adjusted_outline_color = (
                        int(outline_color[0] * outline_opacity + bg_color[0] * (1 - outline_opacity)),
                        int(outline_color[1] * outline_opacity + bg_color[1] * (1 - outline_opacity)),
                        int(outline_color[2] * outline_opacity + bg_color[2] * (1 - outline_opacity))
                    )
                else:
                    adjusted_outline_color = outline_color
                
                # Draw the outline
                for offset_x, offset_y in outline_positions:
                    draw.text((current_x + offset_x, y_pos + offset_y), 
                            word, fill=adjusted_outline_color, font=font)
            
            # Draw shadow if requested
            if add_shadow:
                shadow_img = Image.new('RGBA', (word_width + shadow_blur*2, word_height + shadow_blur*2), (0,0,0,0))
                shadow_draw = ImageDraw.Draw(shadow_img)
                shadow_draw.text((shadow_blur, shadow_blur), word, fill=shadow_color, font=font)
                shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(radius=shadow_blur))
                img.paste(shadow_img, 
                         (int(current_x + shadow_offset[0] - shadow_blur), 
                          int(y_pos + shadow_offset[1] - shadow_blur)), 
                         shadow_img)
            
            # Draw main text
            draw.text((current_x, y_pos), word, fill=text_color, font=font)
            
            # Draw strikethrough if requested
            if style == 'strikethrough':
                strike_y = y_pos + (word_height // 2)
                draw.line([(current_x, strike_y), (current_x + word_width, strike_y)], 
                          fill=text_color, width=max(1, font_size // 15))
            
            word_positions.append({
                'word': word,
                'x': current_x,
                'y': y_pos,
                'width': word_width,
                'height': word_height,
                'style': style
            })
            
            space_width, _ = get_text_dimensions(' ', font)
            current_x += word_width + space_width
            rendered_text += word + ' '
            
        if rendered_text:
            rendered_text = rendered_text[:-1]
            
        lines_info.append({
            'text': rendered_text,
            'x_pos': x_pos,
            'y_pos': y_pos,
            'width': line_width,
            'height': line_height,
            'words': word_positions
        })
    
    # Add border if requested
    if add_border:
        img = ImageOps.expand(img, border=border_width, fill=border_color)
        # Update image dimensions and info
        img_width, img_height = img.size
        for line in lines_info:
            line['x_pos'] += border_width
            line['y_pos'] += border_width
            for word in line['words']:
                word['x'] += border_width
                word['y'] += border_width
    
    # Add watermark if requested
    if add_watermark and watermark_text:
        watermark_img = add_watermark_to_image(
            img, watermark_text, watermark_font_size, watermark_color, 
            watermark_opacity, watermark_position, font_path
        )
        img = watermark_img
    
    return img, {
        'lines': lines_info,
        'image_width': img_width,
        'image_height': img_height,
        'centroid_x': img_width // 2,
        'centroid_y': img_height // 2
    }

def create_texture(width, height, intensity):
    """
    Create a textured background.
    
    Args:
        width (int): Width of the texture
        height (int): Height of the texture
        intensity (float): Intensity of the texture (0-1)
        
    Returns:
        PIL.Image: Textured background
    """
    # Create noise pattern
    noise = np.random.randint(0, 255, (height, width), dtype=np.uint8)
    noise_img = Image.fromarray(noise)
    
    # Apply Gaussian blur to smooth the noise - intensity affects blur amount
    # Less intense = more blur (smoother texture)
    blur_radius = max(1, int(3 * (1 - intensity)))
    noise_img = noise_img.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    
    # Adjust contrast based on intensity
    # Higher intensity = higher contrast
    contrast_factor = 1.0 + intensity  # ranges from 1.0 to 2.0
    enhancer = ImageEnhance.Contrast(noise_img)
    noise_img = enhancer.enhance(contrast_factor)
    
    # Convert to RGB mode to match the main image
    noise_img = noise_img.convert('RGB')
    
    return noise_img

def create_gradient(width, height, start_color, end_color, direction='vertical'):
    """
    Create a gradient background.
    
    Args:
        width (int): Width of the gradient
        height (int): Height of the gradient
        start_color (tuple): Start color of the gradient in RGB
        end_color (tuple): End color of the gradient in RGB
        direction (str): Direction of the gradient ('horizontal', 'vertical')
        
    Returns:
        PIL.Image: Gradient background
    """
    gradient = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(gradient)
    
    if direction == 'horizontal':
        for x in range(width):
            # Calculate color at this position
            r = int(start_color[0] + (end_color[0] - start_color[0]) * x / width)
            g = int(start_color[1] + (end_color[1] - start_color[1]) * x / width)
            b = int(start_color[2] + (end_color[2] - start_color[2]) * x / width)
            draw.line([(x, 0), (x, height)], fill=(r, g, b))
    else:  # vertical
        for y in range(height):
            # Calculate color at this position
            r = int(start_color[0] + (end_color[0] - start_color[0]) * y / height)
            g = int(start_color[1] + (end_color[1] - start_color[1]) * y / height)
            b = int(start_color[2] + (end_color[2] - start_color[2]) * y / height)
            draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    return gradient

def add_watermark_to_image(image, watermark_text, font_size, color, opacity, position, font_path=None):
    """
    Add a watermark to an image.
    
    Args:
        image (PIL.Image): The image to add the watermark to
        watermark_text (str): The text for the watermark
        font_size (int): Font size for the watermark
        color (tuple): Color of the watermark in RGB
        opacity (float): Opacity of the watermark (0-1)
        position (str): Position of the watermark
        font_path (str): Path to TTF font (or None for default)
        
    Returns:
        PIL.Image: Image with watermark
    """
    # Create a copy of the image
    img = image.copy()
    
    # Load font
    try:
        if font_path and os.path.exists(font_path):
            font = ImageFont.truetype(font_path, font_size, encoding="latin-1")
        else:
            font = ImageFont.load_default()
    except Exception as e:
        print(f"Watermark font loading error: {e}, using default font")
        font = ImageFont.load_default()
    
    # Create a new image for the watermark
    watermark = Image.new('RGBA', img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(watermark)
    
    # Get text dimensions
    bbox = draw.textbbox((0, 0), watermark_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Calculate position
    if position == 'top-left':
        pos = (10, 10)
    elif position == 'top-right':
        pos = (img.width - text_width - 10, 10)
    elif position == 'bottom-left':
        pos = (10, img.height - text_height - 10)
    elif position == 'bottom-right':
        pos = (img.width - text_width - 10, img.height - text_height - 10)
    else:  # center
        pos = ((img.width - text_width) // 2, (img.height - text_height) // 2)
    
    # Draw watermark text
    draw.text(pos, watermark_text, font=font, fill=(*color, int(255 * opacity)))
    
    # Composite the watermark onto the image
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    return Image.alpha_composite(img, watermark)
