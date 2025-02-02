from screeninfo import get_monitors
from json import load

from kivy.core.window import Window
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.logger import Logger, LOG_LEVELS

from components.interfaces import CameraInterface
from components.offer_pic_screen import OfferPicScreen
from components.countdown_screen import CountdownScreen
from components.pic_loading_screen import PicLoadingScreen

class MyApp(App):

    def build(self):
        self.config = load(open('config.json'))

        # Could use this to populate the settings screen
        # keeping it easy for now

        self.title = self.config['app_title']

        try:
            self.camera = CameraInterface(self.config['camera_type'])
        except Exception as e:
            Logger.fatal(f"Error setting up camera: {e}")
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


        # Your app's UI
        sm = ScreenManager()

        # Add all screens here
        sm.add_widget(OfferPicScreen(name='offer'))
        sm.add_widget(CountdownScreen(name='countdown',counts=5))
        sm.add_widget(PicLoadingScreen(camera_interface=self.camera, name='loading'))

        return sm

if __name__ == '__main__':
    Logger.setLevel(LOG_LEVELS['debug'])
    MyApp().run()