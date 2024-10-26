# PythonSupport Directory

The **PythonSupport** directory contains the core modules for the FreedomCycle3-Control-Interface project. These modules handle configuration, GUI setup, Arduino communication, data acquisition, and logging, providing the foundation for real-time monitoring and control.

## Directory Contents

### `config.py`
- **Purpose**: Stores global variables and configuration settings shared across modules, allowing consistent access to key project parameters.
- **Key Variables**:
  - `data`: List that stores collected data for each session.
  - `collecting_data`: Boolean indicating if data collection is active.
  - `session_folder`: Directory path for saving session data.
  - `arduino`: Serial object for Arduino communication.
  - `connection_status`, `flowrate_label`, etc.: Tkinter widgets used in the GUI.
- **Usage**: `config.py` simplifies global variable access, improving code readability and organization.

### `gui_interface.py`
- **Purpose**: Defines the Tkinter GUI layout and functions, including the welcome screen, live flow rate display, and control buttons.
- **Key Functions**:
  - `setup_welcome_screen(root)`: Initializes the welcome screen and manages session start functionality.
  - `continuous_check_arduino_connection(root)`: Continuously monitors and updates Arduino connection status.
  - `update_flowrate(root)`: Periodically updates the live flow rate display in the GUI.
  - `start_work_session(root)` and `stop_work_session(root)`: Handle GUI transitions and session lifecycle.
- **Usage**: `gui_interface.py` provides a user-friendly interface for managing and viewing data in real-time.

### `arduino_interface.py`
- **Purpose**: Manages the connection with the Arduino and handles serial communication to read flow rate data.
- **Key Functions**:
  - `find_arduino_port()`: Detects and returns the Arduino’s serial port.
  - `connect_arduino()`: Establishes and maintains the Arduino connection.
  - `read_arduino()`: Reads data from the Arduino if connected.
  - `release_busy_port(port)`: Forcefully releases a busy serial port if occupied by another process.
- **Usage**: `arduino_interface.py` allows the main interface to interact with Arduino hardware for accurate flow rate measurement.

### `data_acquisition.py`
- **Purpose**: Handles data collection, timestamping, and saving session data for analysis.
- **Key Functions**:
  - `initialize_session()`: Creates a new session folder and prepares logging.
  - `start_collection()`: Begins data collection by setting initial conditions.
  - `collect_data(flowrate, timestamp)`: Collects flow rate data and logs it with precise timestamps.
  - `save_data()`: Saves collected data to a CSV file within the session folder.
- **Usage**: `data_acquisition.py` structures and saves data efficiently, enabling later analysis of flow rates and session metrics.

### `logger.py`
- **Purpose**: Provides file-based logging to track actions and events during each session.
- **Key Functions**:
  - `start_logging(session_folder)`: Initializes a `log.txt` file within the session folder.
  - `log(message)`: Writes timestamped log entries to track session actions.
- **Usage**: `logger.py` records session events, offering a detailed trace for debugging and validation.

## How These Modules Work Together

1. **GUI Initialization**: The `gui_interface.py` module initializes the Tkinter GUI and starts the application interface.
2. **Arduino Connection**: `arduino_interface.py` detects and connects the Arduino device, allowing data to flow into the system.
3. **Data Collection**: When a session starts, `data_acquisition.py` collects flow rate data and logs each reading with precise timestamps.
4. **File-Based Logging**: `logger.py` tracks session events, including connection status, data collection start and stop, and any errors.

Together, these modules form a robust, interactive system for real-time data monitoring and control in the FreedomCycle3-Control-Interface project.
