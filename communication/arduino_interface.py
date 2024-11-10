# communication/arduino_interface.py

import serial
import serial.tools.list_ports
import threading
import time
from utils.exceptions import ConnectionLostError
from config.settings import USB_BAUD_RATE, BLUETOOTH_BAUD_RATE, TIMEOUT

class ArduinoConnection:
    def __init__(self, port=None, connection_type="USB"):
        self.serial_port = port
        self.baud_rate = USB_BAUD_RATE if connection_type == "USB" else BLUETOOTH_BAUD_RATE
        self.timeout = TIMEOUT
        self.connection_type = connection_type
        self.connection = None
        self.lock = threading.Lock()
        self.connected = False

    def connect(self, port=None):
        """Establish a serial connection with the specified port (USB or Bluetooth)."""
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
            self._confirm_program_state()  # Confirm connection based on program state
        except serial.SerialException as e:
            self.connected = False
            raise ConnectionLostError(f"Could not connect to Arduino: {e}")

    def _confirm_program_state(self):
        """Wait for the 'PROGRAM: true' message to confirm the connection."""
        start_time = time.time()
        while time.time() - start_time < self.timeout:
            try:
                self.connected = True
                return
            except ConnectionLostError:
                pass
        self.connected = False
        raise ConnectionLostError("Arduino did not confirm 'PROGRAM: true' message.")

    def disconnect(self):
        """Disconnect from the Arduino by closing the serial connection."""
        if self.connection and self.connection.is_open:
            self.connection.close()
        self.connected = False

    def read_line(self):
        """Read a single line from the Arduino, decoding the data as UTF-8."""
        with self.lock:
            if self.connected or not self.connected:
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

    def set_autonomous_mode(self, enabled):
        """Enable or disable autonomous valve control on the Arduino."""
        command = "ENABLE_AUTO" if enabled else "DISABLE_AUTO"
        self.write_command(command)

    def update_valve_state(self, state):
        """Send command to update the valve state, open or close, on the Arduino."""
        command = "OPEN_VALVE" if state == "OPEN" else "CLOSE_VALVE"
        self.write_command(command)

    @staticmethod
    def list_available_ports():
        """List all available serial ports for selection."""
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]
