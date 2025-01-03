import serial
import time

# Replace 'COM3' with your Arduino's port, e.g., '/dev/ttyUSB0' on Linux/macOS
arduino_port = '/dev/ttyACM1'
baud_rate = 115200  # Ensure this matches your Arduino code

# Open the serial connection
ser = serial.Serial(arduino_port, baud_rate, timeout=1)
time.sleep(2)  # Wait for the connection to initialize

try:
    # Sending a command to Arduino
    command = "\n"  # Replace with your actual command
    ser.write(command.encode())  # Convert the string to bytes and send
    print(f"Sent: {command}")

finally:
    # Close the serial connection
    ser.close()
    print("Connection closed.")
