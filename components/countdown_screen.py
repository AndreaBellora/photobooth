from functools import partial
from datetime import datetime

from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
from kivy.logger import Logger

class CountdownScreen(Screen):
    def __init__(self,counts=5,**kwargs):
        super(CountdownScreen, self).__init__(**kwargs)
        app = App.get_running_app()
        config = app.config

        self.base_font_size = 50
        self.big_font_size = 200
        self.animation_duration = 0.6
        self.animation_steps = 10
        self.tick_time = 2
        self.counts = counts

        self.layout = FloatLayout(size_hint=(1, 1))

        # Use the canvas to draw the tiled background
        with self.canvas.before:
            self.bg_texture = Rectangle(source='components/img/002-Watercolor-Paper.png', size=self.size, pos=self.pos)

        # Bind size and position changes to update the tiling
        self.bind(size=self.update_bg, pos=self.update_bg)


        # Countdown label
        self.label = Label(
            text='This is the countdown screen',
            font_size=self.base_font_size,
            font_name=config['regular_font'],
            color=get_color_from_hex('#515151'),
            size_hint=(None, None),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            halign='center',
            valign='middle'
        )

        # Make it so that the label is just big enough to fit the text
        self.label.bind(texture_size=self.label.setter('size'))
        # Wrap text within the label bounds
        # self.label.bind(size=self.label.setter('text_size'))  

        with self.label.canvas.before:
            Color(0,0,0,0)
            self.label.rect = Rectangle(size=self.label.size, pos=self.label.pos)
        self.label.bind(size=self._update_background, pos=self._update_background, texture_size=self._update_background)    

        self.layout.add_widget(self.label)        

        self.add_widget(self.layout)


        Logger.debug(f'CountdownScreen: Starting countdown: {datetime.now()}')
        Clock.schedule_once(self.start_countdown, 1)
        
    def _update_background(self, *args):
        # Ensure the rectangle matches the label's size and position
        self.label.rect.size = self.label.size
        self.label.rect.pos = self.label.pos

    def start_countdown(self, *args):
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
            self.label.text = "Smile!"
            self.go_forward()
            
    def update_bg(self, *args):
        """
        Updates the background to make it repeat along x and y.
        """
        texture = self.bg_texture.texture
        texture.wrap = 'repeat'
        texture.uvsize = (
            self.width / texture.width,
            self.height / texture.height
        )
        self.bg_texture.size = self.size
        self.bg_texture.pos = self.pos

    def go_back(self, *args):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = self.manager.previous()

    def go_home(self, *args):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = self.manager.first()

    def go_forward(self, *args):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = self.manager.next()