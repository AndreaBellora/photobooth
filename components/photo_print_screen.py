import threading

from kivy.app import App
from kivy.graphics import Color, Rectangle, Line
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen, NoTransition
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
from kivy.logger import Logger

class PhotoPrintScreen(Screen):
    def __init__(self,printer_interface,**kwargs):
        super(PhotoPrintScreen, self).__init__(**kwargs)
        app = App.get_running_app()
        config = app.config

        self.printer_interface = printer_interface      
        self.layout = FloatLayout(size_hint=(1, 1))

        # Use the canvas to draw the tiled background
        with self.canvas.before:
            self.bg_texture = Rectangle(source='components/img/002-Watercolor-Paper.png', size=self.size, pos=self.pos)

        # Create the animated spinny_thing
        with self.canvas:
            self.spinny_thing_angle_1 = 0
            self.spinny_thing_angle_2 = 270
            self.st_step_1 = 20
            self.st_step_2 = 15
            self.spinny_thing_color = Color(*get_color_from_hex('#AE8EC3'))
            self.spinny_thing = Line(circle=(self.center_x,
                                             self.center_y,
                                             40,
                                             self.spinny_thing_angle_1,
                                             self.spinny_thing_angle_2),
                                     width=5)
        self.bind(pos=self._update_spinny_thing, size=self._update_spinny_thing)

        # Animate the spinny_thing
        Clock.schedule_interval(self.animate_spinny_thing, 0.05)

        # Bind size and position changes to update the tiling
        self.bind(size=self.update_bg, pos=self.update_bg)

        self.add_widget(self.layout)


    def _update_background(self, *args):
        # Ensure the rectangle matches the label's size and position
        self.label.rect.size = self.label.size
        self.label.rect.pos = self.label.pos

    def _update_spinny_thing(self, *args):
        self.spinny_thing.circle = (self.center_x, self.center_y, 50, self.spinny_thing_angle_1, self.spinny_thing_angle_2)

    def animate_spinny_thing(self, dt):
        # Make it oscillate while rotating
        if self.spinny_thing_angle_2 - self.spinny_thing_angle_1 <= 15:
            self.st_step_1 = self.st_step_2 - 5
        elif self.spinny_thing_angle_2 - self.spinny_thing_angle_1 >= 270:
            self.st_step_1 = self.st_step_2 + 5

        # Make it rotate
        self.spinny_thing_angle_1 += self.st_step_1
        self.spinny_thing_angle_2 += self.st_step_2


        if self.spinny_thing_angle_1 >= 360 and self.spinny_thing_angle_2 >= 360:
            self.spinny_thing_angle_1 -= 360
            self.spinny_thing_angle_2 -= 360

        self._update_spinny_thing()

    def on_enter(self, *args):
        Logger.debug(f'PhotoPrintScreen: Entering print loading screen')
        # Run asyncronously the print_photos method
        threading.Thread(target=self.print_photos).start()

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

    def print_photos(self):
        app = App.get_running_app()
        nprints=app.nprints            
        picture = app.current_picture
        Logger.debug(f'PhotoPrintScreen: Printing {nprints} copies of picture {picture}'.format(nprints=nprints, picture=picture))

        self.printer_interface.print(
            picture_path=picture,
            n_copies=nprints
        )
                
        Clock.schedule_once(self.photos_printed)

    def photos_printed(self, dt):
        Logger.debug('PhotoPrintScreen: Picture(s) printed')

        self.manager.transition = NoTransition()
        self.manager.current = self.manager.screen_names[0]