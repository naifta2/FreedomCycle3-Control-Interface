import os
import subprocess
import serial
import serial.tools.list_ports
from PythonSupport.config import Config

def find_arduino_port():
    """Detects the Arduino port automatically."""
    ports = list(serial.tools.list_ports.comports())
    print(f"Available ports: {[port.device for port in ports]}")
    for port in ports:
        if "Arduino" in port.description or "usbmodem" in port.device:
            print(f"Detected Arduino on port: {port.device}")
            return port.device
    print("No Arduino port detected.")
    return None

def release_busy_port(port):
    """Check and release the busy port if another process is using it."""
    try:
        # Run `lsof` command to find processes using the port
        result = subprocess.run(["lsof", port], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Check if any process is listed in the output
        if result.stdout:
            print(f"Port {port} is busy. Attempting to release it.")
            # Parse the output to get the process ID (PID)
            lines = result.stdout.strip().split("\n")
            for line in lines[1:]:  # Skip the header line
                pid = int(line.split()[1])
                print(f"Killing process {pid} using port {port}")
                os.kill(pid, 9)  # Forcefully kill the process
            print(f"Port {port} has been released.")
        else:
            print(f"No processes found using {port}.")
    except Exception as e:
        print(f"Error releasing port {port}: {e}")

def connect_arduino():
    """Attempts to connect to the Arduino, releasing the port if necessary."""
    port = find_arduino_port()
    if port:
        try:
            if Config.arduino is None or not Config.arduino.is_open:
                Config.arduino = serial.Serial(port, 9600, timeout=1)
                print("Successfully connected to Arduino.")
            return True
        except serial.SerialException as e:
            if "Resource busy" in str(e):
                print(f"Port {port} is busy.")
                release_busy_port(port)
                # Retry connection after releasing the port
                try:
                    Config.arduino = serial.Serial(port, 9600, timeout=1)
                    print("Successfully connected to Arduino after releasing the port.")
                    return True
                except Exception as retry_exception:
                    print(f"Failed to connect after releasing port: {retry_exception}")
            else:
                print(f"Failed to connect to Arduino: {e}")
    else:
        print("Arduino port not found.")
    return False

def disconnect_arduino():
    """Disconnects the Arduino if connected."""
    if Config.arduino and Config.arduino.is_open:
        Config.arduino.close()
        print("Arduino disconnected.")
    Config.arduino = None

def read_arduino():
    """Reads float data from the Arduino if connected."""
    if Config.arduino and Config.arduino.is_open:
        try:
            print("in try")
            # Read a line from Arduino
            if Config.arduino.in_waiting > 0:
                line = Config.arduino.readline().decode('utf-8').strip()
                # Convert the line to a float value
                data = float(line)
                print(f"Data read from Arduino: Flow Rate = {data} L/min")
                return data
        except ValueError as ve:
            print(f"ValueError: Unable to convert '{line}' to float: {ve}")
        except serial.SerialException as se:
            print(f"SerialException: {se}")
            disconnect_arduino()
    return None