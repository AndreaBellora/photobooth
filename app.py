from screeninfo import get_monitors
from json import load
import os

from kivy.core.window import Window
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.logger import Logger, LOG_LEVELS

from components.interfaces import CameraInterface,PrinterInterface
from components.picture_editor import PictureEditor
from components.offer_pic_screen import OfferPicScreen
from components.countdown_screen import CountdownScreen
from components.photo_capture_screen import PhotoCaptureScreen
from components.offer_print_screen import OfferPrintScreen
from components.nprints_screen import NPrintsScreen
from components.photo_print_screen import PhotoPrintScreen

class MyApp(App):

    def build(self):
        self.config = load(open('config.json'))

        # Could use this to populate the settings screen
        # keeping it easy for now

        self.title = self.config['app_title']

        # Set up the camera
        try:
            self.camera = CameraInterface(self.config['camera_type'])
        except Exception as e:
            Logger.fatal(f"Error setting up camera: {e}")
            self.stop()
            return
        
        # Set up printer
        try:
            self.printer = PrinterInterface(self.config['printer_type'])
        except Exception as e:
            Logger.fatal(f"Error setting up printer: {e}")
            self.stop()
            return
        
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
        
        # Detect screens and print their details
        monitors = get_monitors()
        for i, monitor in enumerate(monitors):
            Logger.debug(f"Monitor {i}: {monitor}")
        
        # Example: Use the second monitor if available
        if len(monitors) > 1:
            target_monitor = monitors[1]  # Choose the second monitor
            Window.left = target_monitor.x
            Window.top = target_monitor.y
            Window.size = (target_monitor.width, target_monitor.height)
        else:
            target_monitor = monitors[0]
            Window.size = (1024, 600)
        Logger.info(f"Using monitor {target_monitor}")        

        # Prepare output folders
        pictures_dir_path = self.config['pictures_dir_path']
        try:
            os.makedirs(pictures_dir_path, exist_ok=True)
            os.makedirs(os.path.join(pictures_dir_path, 'all'), exist_ok=True)
            os.makedirs(os.path.join(pictures_dir_path, 'printed'), exist_ok=True)
        except Exception as e:
            Logger.critical(f"Error creating output folders: {e}")
            self.stop()
        Logger.info(f"Output folder: {pictures_dir_path}")

        # Your app's UI
        sm = ScreenManager()

        # Add all screens here
        sm.add_widget(OfferPicScreen(name='offer_pic'))
        sm.add_widget(CountdownScreen(name='countdown',counts=5))
        sm.add_widget(PhotoCaptureScreen(camera_interface=self.camera, name='loading'))
        sm.add_widget(OfferPrintScreen(name='offer_print'))
        sm.add_widget(NPrintsScreen(name='nprints'))
        sm.add_widget(PhotoPrintScreen(printer_interface=self.printer, name='print-loading'))

        return sm

if __name__ == '__main__':
    # Logger.setLevel(LOG_LEVELS['debug'])
    MyApp().run()