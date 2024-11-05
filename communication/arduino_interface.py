# communication/arduino_interface.py

import serial
import serial.tools.list_ports
import threading
import time
from utils.exceptions import ConnectionLostError
from config.settings import BAUD_RATE, TIMEOUT

class ArduinoConnection:
    def __init__(self, port=None):
        self.serial_port = port
        self.baud_rate = BAUD_RATE
        self.timeout = TIMEOUT
        self.connection = None
        self.lock = threading.Lock()
        self.connected = False

    def connect(self, port=None):
        if port:
            self.serial_port = port
        if not self.serial_port:
            raise ConnectionLostError("Serial port not specified.")
        try:
            self.connection = serial.Serial(
                self.serial_port,
                self.baud_rate,
                timeout=self.timeout
            )
            self.connected = True
        except serial.SerialException as e:
            self.connected = False
            raise ConnectionLostError(f"Could not connect to Arduino: {e}")

    def disconnect(self):
        if self.connection and self.connection.is_open:
            self.connection.close()
        self.connected = False

    def read_line(self):
        """Read a single line from the Arduino, decoding the data as UTF-8."""
        with self.lock:
            if self.connected:
                try:
                    line = self.connection.readline().decode('utf-8', errors='replace').strip()
                    return line
                except serial.SerialException as e:
                    self.connected = False
                    raise ConnectionLostError(f"Connection lost: {e}")
            else:
                raise ConnectionLostError("Arduino is not connected.")

    def write_command(self, command):
        """Send a command to the Arduino."""
        with self.lock:
            if self.connected:
                try:
                    self.connection.write(f"{command}\n".encode('utf-8'))
                except serial.SerialException as e:
                    self.connected = False
                    raise ConnectionLostError(f"Failed to send command: {e}")
            else:
                raise ConnectionLostError("Arduino is not connected.")

    def reset_cumulative_flow(self):
        """Send the command to reset cumulative flow on the Arduino."""
        self.write_command("RESET_CUMULATIVE_FLOW")

    @staticmethod
    def list_available_ports():
        """List all available serial ports."""
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]
