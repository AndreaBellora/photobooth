import os
import pytest
from components.camera_interface import CameraInterface

@pytest.mark.parametrize("camera_type", ["Fake camera", "Nikon DSC D3000"])
def test_camera_interface(camera_type):
    camera = CameraInterface(camera_type)
    
    # Setup the camera
    assert camera.setup() == True, f"Failed to setup {camera_type}"
    
    # Capture a picture
    picture_path = camera.capture()
    assert os.path.exists(picture_path), f"Picture not found for {camera_type}"
    
    # Display the picture for 5 seconds
    camera.display(picture_path, duration=5)
    
    # Clean up
    if camera_type != "Fake camera":
        os.remove(picture_path)
        assert not os.path.exists(picture_path), f"Failed to delete picture for {camera_type}"
        