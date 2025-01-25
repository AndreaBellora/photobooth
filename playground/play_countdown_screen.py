import kivy
kivy.require('2.3.0') # replace with your current kivy version !

from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.clock import Clock
from functools import partial

class FirstScreen(Screen):
    def __init__(self, **kwargs):
        super(FirstScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        label = Label(text='This is the first screen')
        button = Button(text='Go to countdown screen')
        button.bind(on_press=self.switch_to_second)
        layout.add_widget(label)
        layout.add_widget(button)
        self.add_widget(layout)

    def switch_to_second(self, *args):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = self.manager.next()

class CountdownScreen(Screen):
    def __init__(self, counts=10, **kwargs):
        super(CountdownScreen, self).__init__(**kwargs)
        self.base_font_size = 50
        self.big_font_size = 200
        self.animation_duration = 0.6
        self.animation_steps = 10
        self.tick_time = 1.5
        self.counts = counts

        self.layout = FloatLayout(size_hint=(1, 1))

        # Countdown label
        self.label = Label(
            text='This is the countdown screen',
            font_size=self.base_font_size,
            size_hint=(None, None),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            halign='center',
            valign='middle'
        )

        # Make it so that the label is just big enough to fit the text
        self.label.bind(texture_size=self.label.setter('size'))

        # self.label.bind(size=self.label.setter('text_size'))  # Wrap text within the label bounds
        with self.label.canvas.before:
            Color(0,1,0,1)
            self.label.rect = Rectangle(size=self.label.size, pos=self.label.pos)
        self.label.bind(size=self._update_background, pos=self._update_background, texture_size=self._update_background)    

        self.layout.add_widget(self.label)        

        # Start button
        self.start_button = Button(
            text='Start countdown',
            size_hint=(None, None),
            font_size=self.base_font_size
        )
        self.start_button.pos_hint = {'center_x': 0.5, 'center_y': 0.2}
        self.start_button.bind(on_press=self.start_countdown)
        self.start_button.bind(texture_size=self.start_button.setter('size'))  # Make the button text size responsive

        self.layout.add_widget(self.start_button)

        self.add_widget(self.layout)

    def _update_background(self, *args):
        # Ensure the rectangle matches the label's size and position
        self.label.rect.size = self.label.size
        self.label.rect.pos = self.label.pos


    def start_countdown(self, *args):
        if self.start_button in self.layout.children:
            self.layout.remove_widget(self.start_button)
        # Remove the button from the layout
        # if self.start_button in self.box_layout.children:
        #     self.box_layout.remove_widget(self.start_button)  # Explicitly remove the button

        self.label.font_size = self.big_font_size
        self.label.text = str(self.counts)
        # Start updating the label text almost every second
        Clock.schedule_interval(self.update_label, self.tick_time - self.animation_duration)

    def update_label(self, time_dt):
        def grow_font_size(step, dt, grow_frac=0.5):
            step_frac = step/(self.animation_steps/2)
            self.label.font_size = int(self.big_font_size + (grow_frac*self.big_font_size) * step_frac)
        def shrink_font_size(step, dt, grow_frac=0.5):
            step_frac = step / (self.animation_steps/2)
            self.label.font_size = int((1 + grow_frac)*self.big_font_size - (grow_frac*self.big_font_size) * step_frac)
        def change_text(dt):
            if self.counts == 0: 
                self.label.text = "Smile!"
            else:
                self.label.text = str(self.counts)

        
        self.counts -= 1

        if self.counts >= 0:
            # Update the label text and animate the font size
            for i in range(int(self.animation_steps)):
                if i+1 <= self.animation_steps/2:
                    Clock.schedule_once(partial(grow_font_size,i+1), (i+1)*self.animation_duration / self.animation_steps)
                else:
                    Clock.schedule_once(partial(shrink_font_size,i+1-self.animation_steps/2), (i+1)*self.animation_duration / self.animation_steps)

            Clock.schedule_once(change_text, self.animation_duration / 2)


        else:
            # Stop the countdown and show the "Go back" button
            Clock.unschedule(self.update_label)
            self.label.font_size = self.base_font_size
            self.label.text = "Done!"
            go_back_button = Button(text='Go back')
            go_back_button.bind(on_press=self.go_back)
            self.layout.add_widget(go_back_button)

    def go_back(self, *args):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = self.manager.previous()

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        # sm.add_widget(FirstScreen(name='first'))
        sm.add_widget(CountdownScreen(name='countdown'))
        return sm

if __name__ == '__main__':
    MyApp().run()