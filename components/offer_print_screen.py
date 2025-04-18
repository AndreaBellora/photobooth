from kivy.uix.screenmanager import Screen, NoTransition
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import AsyncImage
from kivy.graphics import Rectangle
from kivy.logger import Logger
from kivy.utils import get_color_from_hex
from kivy.graphics import Color
from kivy.app import App

from kivy.clock import Clock

from kivy.graphics.opengl import glGetIntegerv, GL_MAX_TEXTURE_SIZE
from components.interfaces import TEST_PICTURE_PATH
from PIL import Image as PILImage


import os
from shutil import copy2

from components.rounded_button import RoundedButton

class OfferPrintScreen(Screen):
    def get_max_texture_size(self):
        max_size = (glGetIntegerv(GL_MAX_TEXTURE_SIZE))[0]
        Logger.debug(f"OpenGL Max Texture Size: {max_size}")
        return max_size
    
    def resize_image_if_needed(self, image_path):
        image = PILImage.open(image_path)
        test_image_width, test_image_height = image.size
        image.close()
        if test_image_width > self.max_texture_size or test_image_height > self.max_texture_size:       
            # Calculate the new size
            if test_image_width > test_image_height:
                scale = self.max_texture_size / test_image_width
            else:
                scale = self.max_texture_size / test_image_height
            new_width = int(test_image_width * scale)
            new_height = int(test_image_height * scale)

            # Resize the image
            image = PILImage.open(image_path)
            image = image.resize((new_width, new_height), PILImage.LANCZOS)
            resized_image_path = os.path.splitext(image_path)[0] + '_resized' + os.path.splitext(image_path)[1]
            image.save(resized_image_path)
            Logger.debug(f"OfferPrintScreen: Resized image to {resized_image_path}")
            image.close()
            return resized_image_path
        else:
            return image_path           
         
    def __init__(self, counts=10, **kwargs):
        super(OfferPrintScreen, self).__init__(**kwargs)
        config = App.get_running_app().config

        self.base_font_size = 50
        self.big_font_size = 200

        self.max_texture_size = self.get_max_texture_size()

        self.files_to_clean = []
        self.layout = FloatLayout(size_hint=(1, 1))

        # Use the canvas to draw the tiled background
        with self.canvas.before:
            Color(1,1,1,1)
            self.bg_texture = Rectangle(source='components/img/002-Watercolor-Paper.png', size=self.size, pos=self.pos)
        
        # Bind size and position changes to update the tiling
        self.bind(size=self.update_bg, pos=self.update_bg)

        # test_display_image = self.resize_image_if_needed(TEST_PICTURE_PATH)
        # if test_display_image != TEST_PICTURE_PATH:
            # self.files_to_clean.append(test_display_image)

        # Display the picture
        self.picture_texture = AsyncImage(
            source='components/img/transparent.png', 
            size_hint=(0.7, 0.7),
            pos_hint={'center_x': 0.5, 'top': 0.96},
            # allow_stretch=True,
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
        # display_image = self.resize_image_if_needed(self.picture)
        # if display_image != self.picture:
        #     Logger.info(f"OfferPrintScreen: Resized image to {display_image}")
        #     self.files_to_clean.append(display_image)
        #     self.picture_texture.source = display_image
        # else:
        #     self.picture_texture.source = self.picture
        # Logger.debug(f"OfferPrintScreen: Displaying picture {self.picture_texture.source}")
        # self.picture_texture.reload()

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
        Logger.debug(f"OfferPrintScreen: Picture temporarily copied to {new_pic_name}")

        # Remove the original picture file, named by the camera
        if self.picture != TEST_PICTURE_PATH:
            Logger.debug(f"OfferPrintScreen: Removing file from camera: {self.picture}")
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
        display_image = self.resize_image_if_needed(self.picture)
        if display_image != self.picture:
            Logger.info(f"OfferPrintScreen: Resized image to {display_image}")
            self.files_to_clean.append(display_image)
            self.files_to_clean.append(self.picture)
            self.picture_texture.source = display_image
        else:
            self.files_to_clean.append(self.picture)
            self.picture_texture.source = self.picture
        Logger.debug(f"OfferPrintScreen: Displaying picture {self.picture_texture.source}")
        self.picture_texture.reload()

    def on_leave(self, *args):
        # Remove all temporary files
        Logger.debug(f"OfferPrintScreen: Removing temporary files: {self.files_to_clean}")
        for file in set(self.files_to_clean):
            try:
                if os.path.isfile(file):
                    os.remove(file)
                    Logger.debug(f"OfferPrintScreen: Removed temporary file {file}")
                    self.files_to_clean.remove(file)
            except Exception as e:
                Logger.error(f"Error removing temporary file: {e}\nFile: {file}")
        
        self.picture_texture.source = 'components/img/transparent.png'
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

        # Remove the the temporary picture file
        if self.picture != TEST_PICTURE_PATH:
            Logger.debug(f"OfferPrintScreen: Removing temporary picture {self.picture}")
            os.remove(self.picture)
            app.current_picture = self.printed_dir_path + '/' + self.picture

        self.manager.transition = NoTransition()
        self.manager.current = self.manager.next()

    def go_home(self, *args):
        self.manager.transition = NoTransition()
        if 'offer_pic' in self.manager.screen_names:
            self.manager.current = 'offer_pic'

