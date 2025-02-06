from components.offer_print_screen import OfferPrintScreen
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

        Window.size = (1024, 600)
        sm = ScreenManager()
        sm.add_widget(OfferPrintScreen(name='offer'))

        return sm
    
if __name__ == '__main__':
    Logger.setLevel(LOG_LEVELS['debug'])
    MyApp().run()