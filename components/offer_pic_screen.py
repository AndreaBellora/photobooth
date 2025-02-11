from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Rectangle
from kivy.utils import get_color_from_hex
from kivy.app import App

from components.rounded_button import RoundedButton

class OfferPicScreen(Screen):
    def __init__(self, counts=10, **kwargs):
        super(OfferPicScreen, self).__init__(**kwargs)
        config = App.get_running_app().config

        self.base_font_size = 50
        self.big_font_size = 200

        self.layout = FloatLayout(size_hint=(1, 1))

        # Use the canvas to draw the tiled background
        with self.canvas.before:
            self.bg_texture = Rectangle(source='components/img/002-Watercolor-Paper.png', size=self.size, pos=self.pos)
        
        # Bind size and position changes to update the tiling
        self.bind(size=self.update_bg, pos=self.update_bg)

        self.label = Label(
            text='Vuoi fare una foto?',
            font_size=self.base_font_size,
            font_name=config['regular_font'],
            color=get_color_from_hex('#515151'),
            size_hint=(None, None),
            pos_hint={'center_x': 0.5, 'center_y': 0.7},
            halign='center',
            valign='middle'
        )
        # Make it so that the label is just big enough to fit the text
        self.label.bind(texture_size=self.label.setter('size'))
        # Wrap text within the label bounds
        self.label.bind(size=self.label.setter('text_size'))  

        # Start button
        self.forward_button = RoundedButton(
            text='Via!',
            font_name=config['cursive_font'],
            size_hint=(None, None),
            font_size=self.base_font_size,
            radius = [25]
        )
        self.forward_button.pos_hint = {'center_x': 0.5, 'center_y': 0.3}
        self.forward_button.bind(on_press=self.go_forward)
        self.forward_button.texture_update()
        self.forward_button.size = (self.forward_button.texture_size[0] + 50, self.forward_button.texture_size[1] + 35)

        self.layout.add_widget(self.label)        
        self.layout.add_widget(self.forward_button)

        self.add_widget(self.layout)

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

    def go_forward(self, *args):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = self.manager.next()
