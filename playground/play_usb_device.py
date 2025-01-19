import serial.tools.list_ports

def list_usb_devices():
    ports = serial.tools.list_ports.comports()
    if not ports:
        print("No devices connected.")
        return

    print("Connected USB Devices:")
    for port in ports:
        print(f"Port: {port.device}")
        print(f"Description: {port.description}")
        print(f"Hardware ID: {port.hwid}")
        print("-" * 40)

if __name__ == "__main__":
    list_usb_devices()
