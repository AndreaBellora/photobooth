from components.offer_screen import OfferScreen
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from kivy.logger import Logger, LOG_LEVELS
from json import load

# Manual test to evaluate the OfferScreen
class MyApp(App):
    def build(self):
        self.config = load(open('config.json'))

        Window.size = (1024, 600)
        sm = ScreenManager()
        sm.add_widget(OfferScreen(name='offer'))

        return sm
    
if __name__ == '__main__':
    Logger.setLevel(LOG_LEVELS['debug'])
    MyApp().run()