# data/data_acquisition.py

import os
import threading
import time
import csv
import subprocess
from datetime import datetime
from data.logger import setup_logging
import logging
import queue  # Import queue module
from tkinter import messagebox
from config.settings import DATA_DIR, DATA_SAVE_INTERVAL, AUTOSAVE_ENABLED, BACK_UP

class DataAcquisition:
    def __init__(self):
        self.data_queue = None
        self.data = []
        self.collecting_data = False
        self.session_folder = None
        self.save_thread = None
        self.collect_thread = None
        self.logger = logging.getLogger(__name__)
        self.data_lock = threading.Lock()
        self.session_start_time = None  # Initialize session start time

    def start_session(self, data_queue):
        self.data_queue = data_queue
        self.collecting_data = True
        self.session_start_time = datetime.now()  # Record session start time
        self.session_folder = os.path.join(DATA_DIR, self.session_start_time.strftime("%Y%m%d_%H%M%S"))
        os.makedirs(self.session_folder, exist_ok=True)
        setup_logging(self.session_folder)
        self.logger.info("Session started.")

        # Clear any old data in data_queue
        while not self.data_queue.empty():
            self.data_queue.get()

        # Start data collection thread
        self.collect_thread = threading.Thread(target=self.collect_data)
        self.collect_thread.daemon = True
        self.collect_thread.start()

        # Start autosave thread
        if AUTOSAVE_ENABLED:
            self.save_thread = threading.Thread(target=self.autosave_data)
            self.save_thread.daemon = True
            self.save_thread.start()

    def stop_session(self):
        if not self.collecting_data:
            self.logger.info("No active session to stop.")
            return
        self.collecting_data = False
        if self.collect_thread:
            self.collect_thread.join()
        if self.save_thread:
            self.save_thread.join()
        self.save_data()

        self.logger.info("Session stopped.")

        if BACK_UP:
            self.push_to_repository("data_sessions/" + self.session_start_time.strftime("%Y%m%d_%H%M%S"))


    def collect_data(self):
        while self.collecting_data:
            if self.data_queue is not None:
                try:
                    data_point = self.data_queue.get(timeout=1)
                    # Calculate elapsed time since session started
                    elapsed_time = (datetime.now() - self.session_start_time).total_seconds()
                    data_point['elapsed_time'] = elapsed_time  # Add elapsed time to data point
                    with self.data_lock:
                        self.data.append(data_point)
                except queue.Empty:
                    pass

    def autosave_data(self):
        while self.collecting_data:
            time.sleep(DATA_SAVE_INTERVAL)
            self.save_data()

    def save_data(self):
        with self.data_lock:
            if not self.data:
                self.logger.info("No data to save.")
                return
            filename = os.path.join(self.session_folder, 'data.csv')
            try:
                # Add 'elapsed_time' to fieldnames
                fieldnames = ['timestamp', 'elapsed_time', 'FLOW1', 'FLOW2', 'PRESSURE']
                file_exists = os.path.isfile(filename)
                with open(filename, 'a', newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    if not file_exists:
                        writer.writeheader()
                    for data_point in self.data:
                        # Ensure data_point has all required keys
                        row = {field: data_point.get(field, '') for field in fieldnames}
                        writer.writerow(row)
                self.logger.info(f"Data saved to {filename}.")
                self.data.clear()
            except Exception as e:
                self.logger.error(f"Failed to save data: {e}")

    def push_to_repository(self, session_folder_name):
        """Commits and pushes the session folder to the GitHub submodule repository."""
        try:
            # Stage, commit, and push the changes
            subprocess.run(["git", "add", session_folder_name], check=True)
            subprocess.run(["git", "commit", "-m", f"Add session data for {session_folder_name}"], check=True)
            subprocess.run(["git", "push"], check=True)

        except subprocess.CalledProcessError as e:
            messagebox.showerror(f"Error pushing session data to GitHub: {e}")
