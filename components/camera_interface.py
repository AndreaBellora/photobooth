import subprocess
import sys
import os
import logging
import time

TEST_PICTURE_PATH = 'tests/test_pic.JPG'

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
                logging.error('No camera detected.')
                return None
            camera_name = result.stdout.splitlines()[2]
            return camera_name
        except subprocess.CalledProcessError as e:
            logging.fatal(f"Error detecting camera: {e}")
            return None

    def __init__(self, camera_model):
        self.camera_model = camera_model
        self.camera_name = self.get_camera_name()
        logging.info(f'Found camera named: {self.camera_name}')
        if (camera_model not in self.camera_name) and (camera_model != 'Fake camera'):
            raise Exception(f'Tried setting up {camera_model}, but camera not detected.')

    def setup_nikon_dsc_d3000(self):
        if 'Nikon DSC D3000' in self.camera_name:
            logging.info('Nikon DSC D3000 detected.')
            # Execute the command to setup the right capture mode 
            # gphoto2 --set-config /main/capturesettings/capturemode=3
            try:
                subprocess.run(
                    ['gphoto2', '--set-config', '/main/capturesettings/capturemode=3'],
                    check=True
                )
                logging.info('Nikon DSC D3000 setup complete.')
            except subprocess.CalledProcessError as e:
                logging.fatal(f"Error setting up Nikon DSC D3000: {e}")
        else:
            raise Exception('Tried setting up Nikon DSC D3000, but camera not detected.')
        
    def setup(self):
        if self.camera_model == 'Nikon DSC D3000':
            self.setup_nikon_dsc_d3000()
            return True
        elif self.camera_model == 'Fake camera':
            return True
        else:
            logging.error(f'Camera model {self.camera_model} not supported.')
            return False

    def display(self,picture_path, duration=5):
        """Display picture for 5 seconds"""
        try:
            subprocess.run(['xdg-open', picture_path], check=True)
            time.sleep(duration)
            subprocess.run(['pkill', '-f', picture_path], check=True)
        except subprocess.CalledProcessError as e:
            logging.error(f"Error displaying picture: {e}")

    def capture(self):
        # Handle the fake camera case
        if self.camera_model == 'Fake camera':
            if not os.path.exists(TEST_PICTURE_PATH):
                logging.fatal(f'Fake picture path not found: {TEST_PICTURE_PATH}')
                return None
            return TEST_PICTURE_PATH
        
        # Take picture using 'gphoto2 --capture-image-and-download'
        # and return the path to the picture taken
        try:
            result = subprocess.run(
                ['gphoto2', '--capture-image-and-download'],
                text=True,
                capture_output=True,
                check=True
            )
            for line in result.stdout.splitlines():
                if 'Saving file as' in line:
                    picture_path = line.split(' ')[-1]
                    # Find the cwd path
                    cwd = os.getcwd()
                    picture_path = os.path.join(cwd, picture_path)
                    return picture_path
        except:
            logging.error('Error taking picture')
    
if __name__ == '__main__':
    # Setup logging
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    
    model = 'Fake camera'

    # Read the model from cmd line and change it, unless it's empty
    if len(sys.argv) > 1:
        model = sys.argv[1]

    cam_interface = CameraInterface(model)

    # Test camera setup
    try:
        cam_interface.setup()
    except Exception as e:
        print(e)
        sys.exit(1)

    # Test take picture
    picture_path = cam_interface.capture()
    logging.info(f'Picture path: {picture_path}')
    
    # Display picture
    if picture_path:
        try:
            cam_interface.display(picture_path)
        except subprocess.CalledProcessError as e:
            logging.error(f"Error opening picture: {e}")
        
        # Remove the picture, unless it's the fake camera
        if model != 'Fake camera':
            os.remove(picture_path)
    else:
        logging.error('No picture path found.')
        sys.exit(1)