import threading

from kivy.app import App
from kivy.graphics import Color, Rectangle, Line
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen, NoTransition
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
from kivy.logger import Logger

class PhotoCaptureScreen(Screen):
    def __init__(self,camera_interface,**kwargs):
        super(PhotoCaptureScreen, self).__init__(**kwargs)
        app = App.get_running_app()
        config = app.config

        self.camera_interface = camera_interface        
        self.layout = FloatLayout(size_hint=(1, 1))

        # Use the canvas to draw the tiled background
        with self.canvas.before:
            self.bg_texture = Rectangle(source='components/img/002-Watercolor-Paper.png', size=self.size, pos=self.pos)

        # Bind size and position changes to update the tiling
        self.bind(size=self.update_bg, pos=self.update_bg)

        # Create the animated spinny_thing
        with self.canvas.after:
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
        # Animate the spinny_thing
        Clock.schedule_interval(self.animate_spinny_thing, 0.05)

        Logger.debug(f'PhotoCaptureScreen: Taking picture')
        # Run asyncronously the take_picture method
        threading.Thread(target=self.take_picture).start()

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

    def take_picture(self):
        Logger.debug('PhotoCaptureScreen: Taking picture')
        app = App.get_running_app()
        try:
            app.current_picture = self.camera_interface.capture()
        except Exception as e:
            Logger.critical(f'PhotoCaptureScreen: Error taking picture: {e}')
            # Exit the app
            app.stop()
        Clock.schedule_once(self.picture_taken)

    def picture_taken(self, dt):
        Logger.debug('PhotoCaptureScreen: Picture taken')

        Clock.unschedule(self.animate_spinny_thing)

        self.manager.transition = NoTransition()
        self.manager.current = self.manager.next()

    def go_back(self, *args):
        self.manager.transition = NoTransition()
        self.manager.current = self.manager.previous()

    def go_home(self, *args):
        self.manager.transition = NoTransition()
        self.manager.current = self.manager.screen_names[0]

    def go_forward(self, *args):
        self.manager.transition = NoTransition()
        self.manager.current = self.manager.next()