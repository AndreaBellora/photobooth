import os
import pytest
import logging
from components.interfaces import CameraInterface

@pytest.mark.parametrize("camera_type", ["Fake camera", "Nikon DSC D3000"])
def test_camera_interface(camera_type):

    # Setup logging for test
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()
    logger.info(f"Testing camera interface with {camera_type}")

    try:
        camera = CameraInterface(camera_type)
    except Exception as e:
        pytest.skip(f"Skipping test for {camera_type} due to exception: {e}")

    # Setup the camera
    assert camera.setup() == True, f"Failed to setup {camera_type}"
    
    # Capture a picture
    picture_path = camera.capture()
    assert picture_path is not None, f"Failed to capture picture for {camera_type}"
    assert os.path.exists(picture_path), f"Picture not found for {camera_type}"
    
    # Display the picture for 5 seconds
    camera.display(picture_path, duration=5)
    
    # Clean up
    if camera_type != "Fake camera":
        os.remove(picture_path)
        assert not os.path.exists(picture_path), f"Failed to delete picture for {camera_type} ({picture_path})"