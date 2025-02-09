from PIL import Image

def fit_to_aspect_ratio(image, desired_ar):
    # Calculate current aspect ratio
    width, height = image.size
    aspect_ratio = width / height
    print(f"Original Aspect Ratio: {aspect_ratio:.4f} (width/height)")

    # Determine cropping dimensions to match the desired aspect ratio
    if aspect_ratio > desired_ar:
        # Image is too wide -> Crop width
        new_width = int(height * desired_ar)
        new_height = height
        left = (width - new_width) // 2
        upper = 0
        right = left + new_width
        lower = new_height
    else:
        # Image is too tall -> Crop height
        new_width = width
        new_height = int(width / desired_ar)
        left = 0
        upper = (height - new_height) // 2
        right = new_width
        lower = upper + new_height

    # Crop symmetrically
    return image.crop((left, upper, right, lower)), new_width, new_height

def apply_color_map(image, color_map):
    # Apply color mapping
    pixels = list(image.getdata())  # Get pixel data
    new_pixels = [color_map.get(p, p) for p in pixels]  # Replace colors

    # Update image
    image.putdata(new_pixels)
    return image

# Paths
picture_path = 'tests/test_pic.JPG'
picture_desired_ar = 148 / 100  # Desired aspect ratio (width / height)
watermark_path = 'components/img/Watermark2.png'
watermark_desired_size = (None, None)
watermark_color_map = {
    (255,255,255,255): (255, 255, 255, 180),
}



# Open the first image
picture = Image.open(picture_path).convert('RGBA')

# Crop symmetrically
picture_cropped, new_width, new_height = fit_to_aspect_ratio(picture, picture_desired_ar)
print(f"Cropped Size: {picture_cropped.size}")

# Open watermark
watermark = Image.open(watermark_path).convert('RGBA')
print(f"Watermark Size: {watermark.size}")

# Resize watermark
if watermark_desired_size[0] is None:
    watermark_desired_size = (new_width, new_height)
watermark_resized = watermark.resize(watermark_desired_size, Image.LANCZOS)
print(f"Resized Watermark Size: {watermark_resized.size}")

# Change watermark color
watermark_colored = apply_color_map(watermark_resized, watermark_color_map)

# Compute new size for positioning
picture_width, picture_height = picture_cropped.size
watermark_width, watermark_height = watermark_colored.size

# Position watermark (horizontally centered, 100 pixels from the bottom)
position = (0, 0)

# Paste watermark onto the cropped picture
picture_cropped.paste(watermark_colored, position, watermark_colored)

# Show the final image
picture_cropped.show()
# Convert to RGB before saving
picture_cropped.convert("RGB").save("/home/andrea/DownloadsWindows/test.jpeg", format="JPEG")