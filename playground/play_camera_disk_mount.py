import subprocess

def list_devices():
    """Lists devices recognized by the GNOME virtual file system."""
    try:
        result = subprocess.run(
            ["gio", "mount", "-l"],
            text=True,
            capture_output=True,
            check=True
        )
        devices = result.stdout.splitlines()
        print("Devices detected:")
        for line in devices:
            print(line)
        return devices
    except subprocess.CalledProcessError as e:
        print(f"Error listing devices: {e}")
        return []

def mount_device_by_name(name):
    """Mounts a device by name using gio."""
    try:
        devices = list_devices()
        for device in devices:
            if name in device:
                uri = device.split(": ")[-1].strip()
                print(f"Mounting device '{name}' with URI: {uri}")
                subprocess.run(["gio", "mount", uri], check=True)
                print(f"Device '{name}' mounted successfully.")
                return True
        print(f"Device '{name}' not found.")
        return False
    except subprocess.CalledProcessError as e:
        print(f"Error mounting device: {e}")
        return False

def main():
    # Replace 'Camera Name' with the name of your camera as it appears in `gio mount -l`.
    camera_name = "NIKON DSC D3000"
    mounted = mount_device_by_name(camera_name)
    if mounted:
        print("Camera mounted successfully.")
    else:
        print("Camera could not be mounted.")

if __name__ == "__main__":
    main()
