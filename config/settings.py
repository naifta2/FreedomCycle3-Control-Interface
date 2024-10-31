# config/settings.py

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Serial communication settings
BAUD_RATE = 115200
TIMEOUT = 1

# Data collection settings
DATA_SAVE_INTERVAL = 60  # Save data every 60 seconds
EXPECTED_RANGES = {
    'FLOW1': (0, 100),
    'FLOW2': (0, 100),
    'PRESSURE1': (0, 200),
    'PRESSURE2': (0, 200),
    'PRESSURE3': (0, 200),
}

# Paths
DATA_DIR = os.path.join(BASE_DIR, 'data_sessions')
LOG_DIR = os.path.join(BASE_DIR, 'logs')
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')

# GitHub repository settings
# REPO_PATH = os.path.join(BASE_DIR, 'FreedomCycle3-Logged-Data')
BACK_UP = True      # Back up logged data to github repository.

# GUI settings
WINDOW_TITLE = "FreedomCycle3 Control Interface"
WINDOW_SIZE = "800x600"
THEME = 'default'  # Options: 'clam', 'alt', 'default', 'classic'

# Other settings
AUTOSAVE_ENABLED = True
