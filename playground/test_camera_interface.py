import subprocess
import sys
import os


# Detect camera name using gphoto2
def get_camera_name():
    try:
        result = subprocess.run(
            ['gphoto2', '--auto-detect'],
            text=True,
            capture_output=True,
            check=True
        )
        camera_name = result.stdout.splitlines()[2]
        return camera_name
    except subprocess.CalledProcessError as e:
        print(f"Error detecting camera: {e}")
        return None

# Test for Nikon camera
def setup_nikon_dsc_d3000():
    camera_name = get_camera_name()
    if 'Nikon DSC D3000' in camera_name:
        print('Nikon DSC D3000 detected.')
        # Execute the command to setup the right capture mode 
        # gphoto2 --set-config /main/capturesettings/capturemode=3
        try:
            subprocess.run(
                ['gphoto2', '--set-config', '/main/capturesettings/capturemode=3'],
                check=True
            )
            print('Nikon DSC D3000 setup complete.')
        except subprocess.CalledProcessError as e:
            print(f"Error setting up Nikon DSC D3000: {e}")
    else:
        raise Exception('Tried setting up Nikon DSC D3000, but camera not detected.')
    
def capture():
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
        print('Error taking picture')
    
if __name__ == '__main__':
    # Test setup Nikon camera
    try:
        setup_nikon_dsc_d3000()
    except Exception as e:
        print(e)
        sys.exit(1)

    # Test take picture
    picture_path = capture()
    print(f'Picture path: {picture_path}')

    # Display picture
    if picture_path:
        try:
            subprocess.run(['xdg-open', picture_path])
        except subprocess.CalledProcessError as e:
            print(f"Error opening picture: {e}")
    else:
        print('No picture path found.')
        sys.exit(1)