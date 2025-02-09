from components.offer_print_screen import OfferPrintScreen
from components.picture_editor import PictureEditor
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from kivy.logger import Logger, LOG_LEVELS
from json import load

from components.interfaces import TEST_PICTURE_PATH

# Manual test to evaluate the OfferScreen
class MyApp(App):
    def build(self):
        self.config = load(open('config.json'))

        self.current_picture = TEST_PICTURE_PATH

        # Set up the picture editor
        try:
            watermark_color_map = {}
            if 'watermark_color_map' in self.config:
                for k, v in self.config['watermark_color_map'].items():
                    key = tuple([int(x) for x in k.split(',')])
                    watermark_color_map[key] = tuple(v)
            picture_desired_ar = self.config['picture_desired_ar']
            picture_desired_ar = float(picture_desired_ar[0]) / picture_desired_ar[1]
            self.picture_editor = PictureEditor(
                watermark_path=self.config['watermark_path'],
                watermark_color_map=watermark_color_map,
                picture_desired_ar=picture_desired_ar,
                )
        except Exception as e:
            Logger.fatal(f"Error setting up picture editor: {e}")
            self.stop()
            return
        
        Window.size = (1024, 600)
        sm = ScreenManager()
        sm.add_widget(OfferPrintScreen(name='offer'))

        return sm
    
if __name__ == '__main__':
    Logger.setLevel(LOG_LEVELS['debug'])
    MyApp().run()