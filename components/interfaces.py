import subprocess
import os
import time
from kivy.logger import Logger
from pydub import AudioSegment
from pydub.playback import play

TEST_PICTURE_PATH = 'tests/test_pic.JPG'
TEST_PICTURE_SOUND = 'tests/camera-shutter-199580.mp3'

class CameraInterface:

    def get_camera_name(self):
        # Detect camera name using gphoto2
        try:
            result = subprocess.run(
                ['gphoto2', '--auto-detect'],
                text=True,
                capture_output=True,
                check=True
            )
            if len(result.stdout.splitlines()) < 3:
                Logger.warning('CameraInterface: No camera detected.')
                return None
            camera_name = result.stdout.splitlines()[2]
            return camera_name
        except subprocess.CalledProcessError as e:
            Logger.fatal(f"CameraInterface: Error detecting camera: {e}")
            return None

    def __init__(self, camera_model):
        self.camera_model = camera_model
        self.camera_name = self.get_camera_name()
        Logger.info(f'CameraInterface: Setting up camera {self.camera_model}')
        if self.camera_model == 'Fake camera':
            return
        if self.camera_name is None:
            raise Exception('No camera found')
        Logger.debug(f'CameraInterface: Found camera named: {self.camera_name}')
        if (camera_model not in self.camera_name) and (camera_model != 'Fake camera'):
            raise Exception(f'Tried setting up {camera_model}, but camera not detected.')

    def setup_nikon_dsc_d3000(self):
        if 'Nikon DSC D3000' in self.camera_name:
            Logger.debug('CameraInterface: Nikon DSC D3000 detected.')
            # Execute the command to setup the right capture mode 
            # gphoto2 --set-config /main/capturesettings/capturemode=3
            try:
                subprocess.run(
                    ['gphoto2', '--set-config', '/main/capturesettings/capturemode=3'],
                    check=True
                )
                Logger.info('CameraInterface: Nikon DSC D3000 setup complete.')
            except subprocess.CalledProcessError as e:
                Logger.fatal(f"CameraInterface: Error setting up Nikon DSC D3000: {e}")
        else:
            raise Exception('Tried setting up Nikon DSC D3000, but camera not detected.')
        
    def setup(self):
        if self.camera_model == 'Nikon DSC D3000':
            self.setup_nikon_dsc_d3000()
            return True
        elif self.camera_model == 'Fake camera':
            return True
        else:
            Logger.error(f'CameraInterface: Camera model {self.camera_model} not supported.')
            return False

    def display(self,picture_path, duration=5):
        """Display picture for 5 seconds"""
        try:
            subprocess.run(['xdg-open', picture_path], check=True)
            time.sleep(duration)
            subprocess.run(['pkill', '-f', picture_path], check=True)
        except subprocess.CalledProcessError as e:
            Logger.error(f"CameraInterface: Error displaying picture: {e}")

    def capture(self,timeout=30):
        # Handle the fake camera case
        if self.camera_model == 'Fake camera':
            if not os.path.exists(TEST_PICTURE_PATH):
                Logger.fatal(f'CameraInterface: Fake picture path not found: {TEST_PICTURE_PATH}')
                return None
            if not os.path.exists(TEST_PICTURE_SOUND):
                Logger.fatal(f'CameraInterface: Fake sound path not found: {TEST_PICTURE_SOUND}')
                return None
            # Play sound
            sound = AudioSegment.from_file(TEST_PICTURE_SOUND)
            play(sound)

            time.sleep(15)
            return TEST_PICTURE_PATH
        
        # Take picture using 'gphoto2 --capture-image-and-download'
        # and return the path to the picture taken
        try:
            result = subprocess.run(
                ['gphoto2', '--capture-image-and-download'],
                text=True,
                capture_output=True,
                check=True,
                timeout=timeout
            )
            for line in result.stdout.splitlines():
                if 'Saving file as' in line:
                    picture_path = line.split(' ')[-1]
                    # Find the cwd path
                    cwd = os.getcwd()
                    picture_path = os.path.join(cwd, picture_path)
                    return picture_path
        except:
            Logger.error('CameraInterface: Error taking picture')


class PrinterInterface:
    # To be implemented
    pass