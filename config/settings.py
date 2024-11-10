# config/settings.py

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Serial communication settings
USB_BAUD_RATE = 115200
BLUETOOTH_BAUD_RATE = 9600
TIMEOUT = 1


# Bluetooth settings (optional, if using a default port for Bluetooth connection)
DEFAULT_BLUETOOTH_PORT = None  # You can set to a specific port if applicable, e.g., '/dev/rfcomm0'

# Data collection settings
DATA_SAVE_INTERVAL = 60  # Save data every 60 seconds
EXPECTED_RANGES = {
    'FLOW1': (0, 100),
    'CUMULATIVE_FLOW': (0, 1000),  # Adjusted based on expected cumulative flow range
    'PRESSURE1': (0, 200),
    'PRESSURE2': (0, 200),
    'PRESSURE3': (0, 200),
    'VALVE_STATE': (0, 1),
}

# Autonomous session
AUTO = False

# Paths
DATA_DIR = os.path.join(BASE_DIR, 'data_sessions')
LOG_DIR = os.path.join(BASE_DIR, 'logs')
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')

# GitHub repository settings
# REPO_PATH = os.path.join(BASE_DIR, 'FreedomCycle3-Logged-Data')
BACK_UP = True      # Back up logged data to GitHub repository.

# GUI settings
WINDOW_TITLE = "FreedomCycle3 Control Interface"
WINDOW_SIZE = "800x600"
THEME = 'default'  # Options: 'clam', 'alt', 'default', 'classic'

# Other settings
AUTOSAVE_ENABLED = True
