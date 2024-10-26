# config.py

class Config:
    # Data collection variables
    data = []                  # Stores collected data
    collecting_data = False    # Tracks if data collection is active
    session_folder = None      # Path to the session folder
    start_time = 0             # Start time for data collection
    
    # Arduino connection
    arduino = None             # Holds the Arduino connection object
    
    # GUI components (initialized to None, populated by GUI functions)
    connection_status = None   # Label to show Arduino connection status
    start_session_button = None  # Button to start the session
    flowrate_label = None      # Label to show the live flow rate
    start_button = None        # Button to start and stop data collection
    is_welcome_screen = True   # Tracks if the GUI is on the welcome screen
