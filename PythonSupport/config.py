# config.py

import os
import tkinter as tk

class Config:
    # Data collection variables
    data = []                  # Stores collected data
    collecting_data = False    # Tracks if data collection is active
    session_folder = None      # Path to the session folder
    start_time = 0             # Start time for data collection
    
    # Arduino connection
    arduino = None             # Holds the Arduino connection object
    
    # GUI components
    connection_status = None   # Label to show Arduino connection status
    start_session_button = None  # Button to start the session
    flowrate_label = None      # Label to show the live flow rate
    start_button = None        # Button to start and stop data collection
    is_welcome_screen = True   # Tracks if the GUI is on the welcome screen
    after_id = None            # Global variable to store the after() ID for flowrate updates

    # Path to the cloned FreedomCycle3-Logged-Data repository
    REPO_PATH = os.path.join(os.getcwd(), "FreedomCycle3-Logged-Data")

class Widget:
    def create(parent, widget_type, **options):
        return widget_type(parent, **options)