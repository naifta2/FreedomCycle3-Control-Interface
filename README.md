
# FreedomCycle3-Control-Interface

**FreedomCycle3-Control-Interface** is a Python-based control and monitoring interface developed as part of the Freedom Cycle3 project, a senior design initiative aimed at enhancing power plant efficiency through a steam-driven water hammer mechanism for energy recycling. This interface integrates high-speed sensors and microcontrollers for real-time monitoring and data logging, helping to validate the Freedom Cycle’s potential for improved thermal efficiency.

## Project Overview

The Freedom Cycle3 project focuses on developing a prototype that achieves 100 psig pressure using a steam-driven water hammer mechanism, with key specifications including a 5 ms injector response time, a durable chassis, and robust control systems. This Python interface provides critical tools for data monitoring, flow rate control, and logging, enabling the team to capture precise data for Technology Readiness Level 3 (TRL3) validation.

## Features

- **Real-Time Flow Rate Monitoring**: Displays current flow rates in the GUI with high responsiveness.
- **Data Logging**: Logs flow rate data, timestamps, and other critical metrics for each session.
- **Arduino Integration**: Controls and collects data from Arduino-based hardware with seamless serial communication.
- **Session-Based Logging**: Each test session generates a separate data log, stored in a structured folder for easy access.

## Requirements

- Python 3.9 or later
- Arduino device (configured with necessary sensors)
- Required Python libraries (Tkinter, PySerial)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/naifta2/FreedomCycle3-Control-Interface.git
   cd FreedomCycle3-Control-Interface
   ```

2. Install required libraries:
   ```bash
   pip install pyserial
   ```

## Usage

1. Connect your Arduino device to your computer.
2. Run the main interface:
   ```bash
   python main.py
   ```
3. Use the GUI to start a work session, monitor live flow rates, and log data as needed. Each session’s data is saved in a dedicated folder for easy access.

## Project Structure

```plaintext
FreedomCycle3-Control-Interface
│
├── main.py                          # Entry point for the interface
│
└── PythonSupport                    # Support files and modules for the project
    ├── config.py                    # Global variables and configuration settings
    ├── gui_interface.py             # Tkinter-based GUI and interface functions
    ├── arduino_interface.py         # Arduino connection and data handling
    ├── data_acquisition.py          # Data collection and logging functions
    └── logger.py                    # Logger for file-based session logs
```

## Module Details

- **main.py**: Launches the GUI interface and initializes the project.
- **config.py**: Stores global variables and shared configurations for easy access across modules.
- **gui_interface.py**: Defines the Tkinter-based GUI, including the welcome screen, live flow rate display, and control buttons.
- **arduino_interface.py**: Manages Arduino connection, handles serial data reading, and attempts reconnection if the device disconnects.
- **data_acquisition.py**: Handles data collection, including timestamp logging and saving data to CSV files for each test session.
- **logger.py**: Logs session events to a `log.txt` file, providing a record of each action and reading for debugging and validation.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for suggestions or improvements.

## License

This project is licensed under the MIT License.
