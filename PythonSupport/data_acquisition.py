import os
import time
import csv
from datetime import datetime
from config import Config
from logger import Logger

def initialize_session():
    """Creates a session folder and initializes the logger."""
    session_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    Config.session_folder = os.path.join(os.getcwd(), session_timestamp)
    os.makedirs(Config.session_folder, exist_ok=True)
    Logger.start_logging(Config.session_folder)
    Logger.log("Session folder created")

def start_collection():
    """Starts data collection."""
    Config.collecting_data = True
    Config.start_time = time.time()
    Config.data.clear()
    Logger.log("Data collection started and data list cleared")

def stop_collection():
    """Stops data collection."""
    Config.collecting_data = False
    Logger.log("Data collection stopped")

def collect_data(flowrate, timestamp):
    """Collects data with precise timestamps."""
    elapsed_time = timestamp - Config.start_time  # Calculate elapsed time using precise timestamp
    formatted_timestamp = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
    Config.data.append([formatted_timestamp, elapsed_time, flowrate])
    Logger.log(f"Data appended: {Config.data[-1]}")

def save_data():
    """Saves collected data to a CSV file in the session folder."""
    filename = os.path.join(Config.session_folder, "data_collected.csv")
    if Config.data:
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "Elapsed Time (s)", "Flow Rate (L/min)"])
            writer.writerows(Config.data)
        Logger.log(f"Data saved to {filename} with {len(Config.data)} entries.")
        return filename
    else:
        Logger.log("No data to save.")
        return None
