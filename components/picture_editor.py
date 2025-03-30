from PIL import Image

from kivy.logger import Logger

class PictureEditor():
    def __init__(self, 
                 watermark_path, 
                 watermark_color_map,
                 picture_desired_ar,
                 ):
        self.watermark_path = watermark_path
        self.watermark_color_map = watermark_color_map
        self.picture_desired_ar = picture_desired_ar

        self.watermark = Image.open(watermark_path).convert('RGBA')

        # Apply color map to watermark
        pixels = self.watermark.load()  # Direct access to pixel data (memory-efficient)
        width, height = self.watermark.size
        for y in range(height):
            for x in range(width):
                pixel = pixels[x, y]
                if pixel in watermark_color_map:
                    pixels[x, y] = watermark_color_map[pixel]  # Modify pixel in-place
                    
        # Update image
        Logger.info('PictureEditor: Watermark loaded and color map applied')
        
    def load_image(self, image_path):
        self.current_image = Image.open(image_path).convert('RGBA')

    def show_image(self):
        if self.current_image is None:
            Logger.error('PictureEditor: No image loaded')
            return None

        self.current_image.show()

    def crop_to_aspect_ratio(self, desired_ar = None):
        # Calculate current aspect ratio
        if desired_ar is None:
            desired_ar = self.picture_desired_ar

        if self.current_image is None:
            Logger.error('PictureEditor: No image loaded')
            return None

        width, height = self.current_image.size
        aspect_ratio = width / height
        Logger.debug(f"Original Aspect Ratio: {aspect_ratio:.4f} (width/height)")

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
        self.current_image = self.current_image.crop((left, upper, right, lower))

    def apply_watermark(self):
        
        if self.current_image is None:
            Logger.error('PictureEditor: No image loaded')
            return None
        
        self.crop_to_aspect_ratio()
        
        image_size = self.current_image.size
        watermark_size = self.watermark.size
        
        if watermark_size != image_size:
            Logger.info(f'PictureEditor: Watermark and image sizes do not match (wmk: {watermark_size}, img: {image_size}). Resizing watermark to match image size')
            self.watermark = self.watermark.resize(image_size, Image.LANCZOS)
    
        # Apply watermark
        self.current_image.paste(self.watermark, (0, 0), self.watermark)

    def save_image(self, output_path):
        if self.current_image is None:
            Logger.error('PictureEditor: No image loaded')
            return None

        try:
            if '.jpeg' in output_path.lower() or '.jpg' in output_path.lower():
                self.current_image.convert('RGB').save(output_path, format='JPEG')
            else:
                self.current_image.save(output_path)
            Logger.info(f'PictureEditor: Image saved to {output_path}')
        except Exception as e:
            Logger.error(f'PictureEditor: Error saving image: {e}')
            return None    
