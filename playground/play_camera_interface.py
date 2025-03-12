import logging
import sys
import os
import subprocess

from components.interfaces import CameraInterface

if __name__ == '__main__':
    # Setup logging
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    
    model = 'Nikon DSC D3000'

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
