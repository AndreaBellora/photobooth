from json import load

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from kivy.logger import Logger, LOG_LEVELS

from components.countdown_screen import CountdownScreen
# Manual test to evaluate the OfferScreen
class MyApp(App):
    def build(self):
        self.config = load(open('config.json'))

        Window.size = (1024, 600)
        sm = ScreenManager()
        sm.add_widget(CountdownScreen(name='countdown'))

        return sm
    
if __name__ == '__main__':
    Logger.setLevel(LOG_LEVELS['debug'])
    MyApp().run()