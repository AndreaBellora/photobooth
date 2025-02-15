from kivy.uix.screenmanager import Screen, NoTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.graphics import Rectangle
from kivy.utils import get_color_from_hex
from kivy.app import App
from kivy.logger import Logger

from components.rounded_button import RoundedButton

class NPrintsScreen(Screen):
    def __init__(self, **kwargs):
        super(NPrintsScreen, self).__init__(**kwargs)
        app = App.get_running_app()
        config = app.config

        self.layout = FloatLayout(size_hint=(1, 1))

        # Use the canvas to draw the tiled background
        with self.canvas.before:
            self.bg_texture = Rectangle(source='components/img/002-Watercolor-Paper.png', size=self.size, pos=self.pos)

        # Bind size and position changes to update the tiling
        self.bind(size=self.update_bg, pos=self.update_bg)


        self.label_question = Label(
            text='Quante copie vuoi stampare?',
            font_size=50,
            font_name=config['regular_font'],
            color=get_color_from_hex('#515151'),
            size_hint=(None, None),
            pos_hint={
                'center_x': 0.5,
                'center_y': 0.8
            },
        )
        # Make it so that the label_question is just big enough to fit the text
        self.label_question.bind(texture_size=self.label_question.setter('size'))
        # Wrap text within the label_question bounds
        self.label_question.bind(size=self.label_question.setter('text_size'))  
        self.layout.add_widget(self.label_question)

        self.label_n = Label(
            text=str(config['nprints_default']),
            font_size=100,
            font_name=config['regular_font'],
            color=get_color_from_hex('#515151'),
            size_hint=(None, None),
            pos_hint={   
                'center_y': 0.5
            },
            halign='center',
            valign='middle'
        )
        # Make it so that the label_n is just big enough to fit the text
        self.label_n.bind(texture_size=self.label_n.setter('size'))
        # Wrap text within the label_n bounds
        self.label_n.bind(size=self.label_n.setter('text_size'))  

        self.down_button = RoundedButton(
            text='\u2212', # minus sign
            font_name=config['regular_font'],
            size_hint=(None, None),
            font_size=100,
            radius = [25]
        )
        self.down_button.bind(on_press=self.down_print)
        self.down_button.texture_update()

        self.up_button = RoundedButton(
            text='\u002b', # plus sign
            font_name=config['regular_font'],
            size_hint=(None, None),
            font_size=100,
            radius = [25]
        )
        self.up_button.bind(on_press=self.up_print)
        self.up_button.texture_update()

        self.bind(size=self.set_text_pos)

        self.print_button = RoundedButton(
            text='Stampa', 
            font_name=config['regular_font'],
            pos_hint={'center_x': 0.5, 'center_y': 0.2},
            size_hint=(None, None),
            font_size=50,
            radius = [25]
        )
        self.print_button.bind(on_press=self.go_forward)
        self.print_button.texture_update()
        self.print_button.size = (self.print_button.texture_size[0] + 50, self.print_button.texture_size[1] + 35)

        self.layout.add_widget(self.label_n)
        self.layout.add_widget(self.down_button)
        self.layout.add_widget(self.up_button)
        self.layout.add_widget(self.print_button)

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

    def set_text_pos(self, *args):
        # Layout for the text
        text_center_y = 0.5
        spacing = 50
        label_n_width = self.label_n.size[0]
        down_button_width = self.down_button.size[0]
        up_button_width = self.up_button.size[0]
        screen_width = self.width
        content_width = label_n_width + down_button_width + up_button_width + 2*spacing
        down_button_x = (screen_width - content_width) / 2
        label_n_x = down_button_x + down_button_width + spacing
        up_button_x = label_n_x + label_n_width + spacing

        self.down_button.pos_hint = {'x': down_button_x / screen_width, 'center_y': text_center_y}
        self.label_n.pos_hint = {'x': label_n_x / screen_width, 'center_y': text_center_y}
        self.up_button.pos_hint = {'x': up_button_x / screen_width, 'center_y': text_center_y}

    def down_print(self, *args):
        app = App.get_running_app()
        if not hasattr(app, 'nprints'):
            app.nprints = app.config['nprints_default']
        if app.nprints > 1:
            app.nprints -= 1
            self.label_n.text = str(app.nprints)

    def up_print(self, *args):
        app = App.get_running_app()
        if not hasattr(app, 'nprints'):
            app.nprints = app.config['nprints_default']
        app.nprints += 1
        self.label_n.text = str(app.nprints)

    def go_forward(self, *args):
        app = App.get_running_app()
        Logger.info('NPrintsScreen: Printing {} copies'.format(app.nprints))
        self.manager.transition = NoTransition()
        self.manager.current = self.manager.next()

    def on_enter(self, *args):
        app = App.get_running_app()
        if hasattr(app, 'nprints'):
            self.label_n.text = str(app.nprints)
        else:
            app.nprints = app.config['nprints_default']
            self.label_n.text = str(app.nprints)