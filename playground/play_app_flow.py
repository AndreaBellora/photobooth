import kivy
kivy.require('2.3.0') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition


class FirstScreen(Screen):
    def __init__(self, **kwargs):
        super(FirstScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        label = Label(text='This is the first screen')
        button = Button(text='Go to second screen')
        button.bind(on_press=self.switch_to_second)
        layout.add_widget(label)
        layout.add_widget(button)
        self.add_widget(layout)

    def switch_to_second(self, *args):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'second'

class SecondScreen(Screen):
    def __init__(self, **kwargs):
        super(SecondScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        label = Label(text='This is the second screen')
        button = Button(text='Go to first screen')
        button.bind(on_press=self.switch_to_first)
        layout.add_widget(label)
        layout.add_widget(button)
        self.add_widget(layout)
    def switch_to_first(self, *args):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'first'


class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(FirstScreen(name='first'))
        sm.add_widget(SecondScreen(name='second'))
        return sm

if __name__ == '__main__':
    MyApp().run()