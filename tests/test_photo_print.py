from json import load

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from kivy.logger import Logger, LOG_LEVELS

from components.photo_print_screen import PhotoPrintScreen
from components.interfaces import PrinterInterface
from components.interfaces import TEST_PICTURE_PATH

# Manual test to evaluate the PhotoCaptureScreen
class MyApp(App):
    def build(self):
        self.config = load(open('config.json'))

        Window.size = (1024, 600)
        sm = ScreenManager()
        sm.add_widget(PhotoPrintScreen(name='print-loading',
                                       printer_interface=PrinterInterface('Fake printer')))

        self.nprints = 1
        self.current_picture = TEST_PICTURE_PATH


        return sm
    
if __name__ == '__main__':
    Logger.setLevel(LOG_LEVELS['debug'])
    MyApp().run()