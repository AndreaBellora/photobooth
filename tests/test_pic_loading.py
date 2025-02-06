from json import load

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from kivy.logger import Logger, LOG_LEVELS

from components.photo_capture_screen import PhotoCaptureScreen
from components.interfaces import CameraInterface

# Manual test to evaluate the PhotoCaptureScreen
class MyApp(App):
    def build(self):
        self.config = load(open('config.json'))

        Window.size = (1024, 600)
        sm = ScreenManager()
        sm.add_widget(PhotoCaptureScreen(name='pic-loading',
                                       camera_interface=CameraInterface('Fake camera')))

        return sm
    
if __name__ == '__main__':
    Logger.setLevel(LOG_LEVELS['debug'])
    MyApp().run()