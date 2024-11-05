# communication/sensor_manager.py

from communication.arduino_interface import ArduinoConnection
from data.data_processing import parse_sensor_data
from utils.exceptions import ConnectionLostError
from threading import Thread
import queue
import time

class SensorManager:
    def __init__(self, port):
        self.arduino = ArduinoConnection(port=port)
        self.display_queue = queue.Queue()  # For live data display
        self.data_queue = None  # Initialize as None
        self.receiving_data = False
        self.thread = None
        self.connected = False

    def connect(self):
        """Connects to the Arduino device."""
        self.arduino.connect()
        self.connected = True

    def start_receiving_only(self):
        """Begins receiving data from the Arduino for live display."""
        if not self.arduino.connected:
            raise ConnectionLostError("Arduino is not connected.")
        self.receiving_data = True
        self.thread = Thread(target=self.receive_data)
        self.thread.daemon = True
        self.thread.start()

    def start_data_acquisition(self):
        """Initializes data acquisition by creating a data queue and resetting cumulative flow on Arduino."""
        self.data_queue = queue.Queue()  # Initialize data_queue at session start
        self.reset_cumulative_flow()  # Reset cumulative flow counter on Arduino

    def reset_cumulative_flow(self):
        """Sends command to Arduino to reset the cumulative flow counter."""
        try:
            self.arduino.reset_cumulative_flow()
        except ConnectionLostError as e:
            self.connected = False
            raise ConnectionLostError("Failed to reset cumulative flow: Arduino connection lost.")

    def stop(self):
        """Stops receiving data and disconnects from Arduino."""
        if self.receiving_data:
            self.receiving_data = False
            if self.thread:
                self.thread.join()
        self.arduino.disconnect()
        self.connected = False

    def receive_data(self):
        """Continuously receives and processes data from Arduino while active."""
        while self.receiving_data:
            try:
                line = self.arduino.read_line()
                data = parse_sensor_data(line)
                if data:
                    self.display_queue.put(data)  # Place data in display queue for GUI
                    # Only put data into data_queue if data acquisition is active
                    if self.data_queue is not None:
                        self.data_queue.put(data)
            except ConnectionLostError as e:
                self.receiving_data = False
                self.connected = False
                break
            time.sleep(0.1)  # Small delay to prevent CPU overload
