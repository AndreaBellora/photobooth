from screeninfo import get_monitors
from kivy.config import Config
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.label import Label

class MyApp(App):
    def build(self):
        self.title = 'Experiment #1'
        # Detect screens and print their details
        monitors = get_monitors()
        for i, monitor in enumerate(monitors):
            print(f"Monitor {i}: {monitor}")
        
        # Example: Use the second monitor if available
        if len(monitors) > 1:
            target_monitor = monitors[1]  # Choose the second monitor
            Window.left = target_monitor.x
            Window.top = target_monitor.y
            Window.size = (target_monitor.width, target_monitor.height)

        # Your app's UI
        return Label(text="Hello, Kivy!")

if __name__ == '__main__':
    MyApp().run()
