from components.picture_editor import PictureEditor
from components.interfaces import TEST_PICTURE_PATH
import json

from kivy.logger import Logger

TEST_OUTPUT_PATH = 'test_output.jpg'


if __name__ == '__main__':
    with open('config.json') as f:
        config = json.load(f)
    
    try:
        watermark_color_map = {}
        if 'watermark_color_map' in config:
            for k, v in config['watermark_color_map'].items():
                key = tuple([int(x) for x in k.split(',')])
                watermark_color_map[key] = tuple(v)
        picture_desired_ar = config['picture_desired_ar']
        picture_desired_ar = float(picture_desired_ar[0]) / picture_desired_ar[1]
        picture_editor = PictureEditor(
            watermark_path=config['watermark_path'],
            watermark_color_map=watermark_color_map,
            picture_desired_ar=picture_desired_ar,
            )
    except Exception as e:
        Logger.critical(f"Error setting up picture editor: {e}")
        raise e
    
    picture_editor.load_image(TEST_PICTURE_PATH)
    picture_editor.apply_watermark()
    picture_editor.save_image(TEST_OUTPUT_PATH)
    Logger.info(f'Output saved to {TEST_OUTPUT_PATH}')

    # Show the saved image
    picture_editor.load_image(TEST_OUTPUT_PATH)
    picture_editor.show_image()