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
        with self.lock:
            if self.connected:
                try:
                    self.connection.write(f"{command}\n".encode('utf-8'))
                except serial.SerialException as e:
                    self.connected = False
                    raise ConnectionLostError(f"Failed to send command: {e}")
            else:
                raise ConnectionLostError("Arduino is not connected.")

    @staticmethod
    def list_available_ports():
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]
