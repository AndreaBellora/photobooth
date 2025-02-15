from kivy.uix.screenmanager import Screen, NoTransition
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.graphics import Rectangle
from kivy.logger import Logger
from kivy.utils import get_color_from_hex
from kivy.app import App

from components.interfaces import TEST_PICTURE_PATH


import os
from shutil import copy2

from components.rounded_button import RoundedButton

class OfferPrintScreen(Screen):
    def __init__(self, counts=10, **kwargs):
        super(OfferPrintScreen, self).__init__(**kwargs)
        config = App.get_running_app().config

        self.base_font_size = 50
        self.big_font_size = 200

        self.layout = FloatLayout(size_hint=(1, 1))

        # Use the canvas to draw the tiled background
        with self.canvas.before:
            self.bg_texture = Rectangle(source='components/img/002-Watercolor-Paper.png', size=self.size, pos=self.pos)
        
        # Bind size and position changes to update the tiling
        self.bind(size=self.update_bg, pos=self.update_bg)

        # Display the picture
        self.picture_texture = Image(
            source=TEST_PICTURE_PATH, 
            size_hint=(1, 0.7),
            pos_hint={'center_x': 0.5, 'top': 0.96},
            allow_stretch=True,
            keep_ratio=True
            )   

        self.label = Label(
            text='Vuoi stampare la foto?',
            font_size=self.base_font_size,
            font_name=config['regular_font'],
            color=get_color_from_hex('#515151'),
            size_hint=(None, None),
            pos_hint={'center_y': 0.5},
            halign='center',
            valign='middle'
        )
        # Make it so that the label is just big enough to fit the text
        self.label.bind(texture_size=self.label.setter('size'))
        # Wrap text within the label bounds
        self.label.bind(size=self.label.setter('text_size'))  

        # Print button
        self.print_button = RoundedButton(
            text='Sì',
            font_name=config['cursive_font'],
            size_hint=(None, None),
            font_size=self.base_font_size,
            radius = [25]
        )
        self.print_button.bind(on_press=self.go_forward)
        self.print_button.texture_update()
        self.print_button.size = (self.print_button.texture_size[0] + 50, self.print_button.texture_size[1] + 35)

        # Back button
        self.back_button = RoundedButton(
            text='No',
            font_name=config['cursive_font'],
            size_hint=(None, None),
            font_size=self.base_font_size,
            radius = [25]
        )
        self.back_button.bind(on_press=self.go_home)
        self.back_button.texture_update()
        self.back_button.size = (self.back_button.texture_size[0] + 50, self.back_button.texture_size[1] + 35)

        self.bind(size=self.set_text_pos)

        self.layout.add_widget(self.picture_texture)
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.print_button)
        self.layout.add_widget(self.back_button)

        self.add_widget(self.layout)

    def set_text_pos(self, *args):
        # Layout for the text
        text_center_y = (self.picture_texture.pos_hint['top'] - self.picture_texture.size_hint[1])/2
        spacing = 50
        label_width = self.label.size[0]
        print_button_width = self.print_button.size[0]
        back_button_width = self.back_button.size[0]
        screen_width = self.width
        content_width = label_width + print_button_width + back_button_width + 2*spacing
        label_x = (screen_width - content_width) / 2
        print_button_x = label_x + label_width + spacing
        back_button_x = print_button_x + print_button_width + spacing
        self.label.pos_hint = {'x': label_x / screen_width, 'center_y': text_center_y}
        self.print_button.pos_hint = {'x': print_button_x / screen_width, 'center_y': text_center_y}
        self.back_button.pos_hint = {'x': back_button_x / screen_width, 'center_y': text_center_y}

    def on_enter(self, *args):
        app = App.get_running_app()
        config = app.config

        # Get the picture that is being handled
        self.picture = app.current_picture
        Logger.debug(f'OfferPrintScreen: Picture is {self.picture}')

        # Display the new picture
        Logger.debug(f"OfferPrintScreen: Displaying picture {self.picture}")
        self.picture_texture.source = self.picture
        self.picture_texture.reload()

        # Get the paths to the directories
        self.pictures_dir_path = config['pictures_dir_path']
        self.save_dir_path = os.path.join(self.pictures_dir_path, 'all')
        self.printed_dir_path = os.path.join(self.pictures_dir_path, 'printed')

        # Rename the picture
        self.picture_extension = os.path.splitext(self.picture)[1]
        new_pic_name = config['picture_file_name']
        
        # Make the wmk string something that we can rely on
        if 'wmk' in self.picture:
            Logger.critical(f'OfferPrintScreen: Please remove the \'wmk\' string from the picture name')
            # Exit the app
            App.get_running_app().stop()

        # Get the number of pictures already taken 
        pic_number = len([f for f in os.listdir(self.save_dir_path) if (f.endswith(self.picture_extension)) and 'wmk' not in f])
        new_pic_name += '_' + str(pic_number) + self.picture_extension
        
        # Create a temporary copy of the picture
        try:
            copy2(self.picture, new_pic_name)
        except Exception as e:
            Logger.critical(f"Error copying picture to temporary directory: {e}\nPicture: {self.picture}")
            # Exit the app
            App.get_running_app().stop()
        Logger.info(f"OfferPrintScreen: Picture temporarily copied to {new_pic_name}")

        # Remove the old picture if it is not the test picture
        if self.picture != TEST_PICTURE_PATH:
            os.remove(self.picture)

        self.picture = new_pic_name

        # Copy the picture to the save directory
        try:
            copy2(self.picture, self.save_dir_path)
        except Exception as e:
            Logger.critical(f"Error copying picture to save directory: {e}\nPicture: {self.picture}")
            # Exit the app
            App.get_running_app().stop()
        Logger.info(f"OfferPrintScreen: Picture saved to {self.save_dir_path}/{self.picture}")

        # Apply the watermark if possible
        if hasattr(app, 'picture_editor'):
            try:
                app.picture_editor.load_image(self.picture)
                app.picture_editor.apply_watermark()
                Logger.info(f"OfferPrintScreen: Watermark applied to {self.picture}")
            except Exception as e:
                Logger.critical(f"OfferPrintScreen: Error applying watermark: {e}")
                # Exit the app
                App.get_running_app().stop()
                
            # Remove the temporary picture and update picture name by adding a _wmk suffix
            os.remove(self.picture)
            self.picture = os.path.splitext(self.picture)[0] + '_wmk' + self.picture_extension
            app.picture_editor.save_image(self.picture)

            # Save it in the all directory
            try:
                copy2(self.picture, self.save_dir_path)
            except Exception as e:
                Logger.critical(f"Error copying picture to save directory: {e}\nPicture: {self.picture}")
                # Exit the app
                App.get_running_app().stop()
            Logger.info(f"OfferPrintScreen: Watermarked picture saved to {self.save_dir_path}/{self.picture}")

        # Display the picture
        Logger.debug(f"OfferPrintScreen: Displaying picture {self.picture}")
        self.picture_texture.source = self.picture
        self.picture_texture.reload()

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
        Logger.info('OfferPrintScreen: will print this!')

        # Copy the picture to the printed directory
        try:
            copy2(self.picture, self.printed_dir_path)
        except Exception as e:
            Logger.critical(f"Error copying picture to save directory: {e}\nPicture: {self.picture}")
            # Exit the app
            App.get_running_app().stop()
        Logger.info(f"OfferPrintScreen: Picture saved to {self.printed_dir_path}/{self.picture}")

        app = App.get_running_app()
        app.current_picture = self.picture

        if 'nprints_default' in app.config.keys():
            app.nprints = app.config['nprints_default']
        else:
            app.nprints = 1

        self.manager.transition = NoTransition()
        self.manager.current = self.manager.next()

    def go_home(self, *args):
        self.manager.transition = NoTransition()
        if 'offer_pic' in self.manager.screen_names:
            self.manager.current = 'offer_pic'

