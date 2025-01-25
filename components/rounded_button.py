from kivy.uix.button import Button
from kivy.graphics import RoundedRectangle, Color, Line
from kivy.utils import get_color_from_hex

class RoundedButton(Button):
    def __init__(self,
                 bkg_color=get_color_from_hex('#AE8EC3'),
                 bkg_color_down=get_color_from_hex('#C9A0DC'),
                 border_color=get_color_from_hex('#000000'),
                 border_color_down=get_color_from_hex('#FFFFFF'),
                 border_width=1,
                 radius=[25],
                 **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self.update_canvas, size=self.update_canvas)
        self.bkg_color = bkg_color
        self.bkg_color_down = bkg_color_down
        self.border_color = border_color
        self.border_color_down = border_color_down
        self.radius = radius
        self.border_width = border_width

        self.background_color = (0, 0, 0, 0)  # Make the default background transparent
        self.background_normal = ""  # Remove default Kivy button background

        with self.canvas.before:
            self.bg_color = Color(*self.bkg_color)
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=self.radius)

        with self.canvas.after:
            self.bd_color = Color(*self.border_color)
            self.rect_border = Line(rounded_rectangle=(self.x,self.y,self.width,self.height,*self.radius), 
                               width=self.border_width)

        self.bind(pos=self.update_canvas, 
                  size=self.update_canvas, 
                  state=self.on_state_change)

    def update_canvas(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos
        self.rect_border.rounded_rectangle = (self.x,self.y,self.width,self.height,*self.radius)
    
    def on_state_change(self, *args):
        """Change color based on the button state."""
        if self.state == 'down':
            self.bg_color.rgba = self.bkg_color_down
            self.bd_color.rgba = self.border_color_down
        else:
            self.bg_color.rgba = self.bkg_color
            self.bd_color.rgba = self.border_color