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
        self.arduino.connect()
        self.connected = True

    def start_receiving_only(self):
        if not self.arduino.connected:
            raise ConnectionLostError("Arduino is not connected.")
        self.receiving_data = True
        self.thread = Thread(target=self.receive_data)
        self.thread.daemon = True
        self.thread.start()

    def start_data_acquisition(self):
        # Initialize data_queue when session starts
        self.data_queue = queue.Queue()

    def stop(self):
        if self.receiving_data:
            self.receiving_data = False
            if self.thread:
                self.thread.join()
        self.arduino.disconnect()
        self.connected = False

    def receive_data(self):
        while self.receiving_data:
            try:
                line = self.arduino.read_line()
                data = parse_sensor_data(line)
                if data:
                    self.display_queue.put(data)
                    # Only put data into data_queue if data acquisition is active
                    if self.data_queue is not None:
                        self.data_queue.put(data)
            except ConnectionLostError as e:
                self.receiving_data = False
                self.connected = False
                break
            time.sleep(0.1)