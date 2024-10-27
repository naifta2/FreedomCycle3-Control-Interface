
# FreedomCycle3 Control Interface

**FreedomCycle3 Control Interface** is a Python-based application designed to control and monitor the Freedom Cycle3 project,
which aims to enhance power plant efficiency through a steam-driven water hammer mechanism for energy recycling.
The interface provides real-time data visualization, control over hardware components, and robust data logging for analysis and validation.

## **Project Overview**

The Freedom Cycle3 project focuses on developing a prototype that achieves 100 psig pressure using a steam-driven water hammer mechanism.
Key specifications include:

- **Fast Injector Response Time**: 5 ms injector response time.
- **Durable Chassis**: Robust physical structure for operational stability.
- **Advanced Control Systems**: Integration of multiple sensors and actuators.

This Python interface is essential for data monitoring, control, and logging, enabling the team to capture precise data for
Technology Readiness Level 3 (TRL3) validation.

## **Features**

- **Real-Time Data Visualization**: Displays live readings from multiple sensors, including flow rates and pressure.
- **Data Logging**: Logs sensor data with precise timestamps, saved in structured session folders.
- **Hardware Control**: Provides control over hardware components like injection valves directly from the GUI.
- **Robust Error Handling**: Detects and handles disconnections or errors gracefully, ensuring data integrity.
- **Modular Design**: Easily expandable to include additional sensors or controls in the future.
- **User-Friendly Interface**: Intuitive GUI with modern design elements, including logos and branding.

## **Requirements**

- Python 3.8 or later
- Arduino device (configured with necessary sensors and firmware)
- Required Python libraries (listed in `requirements.txt`)
- Git (for data repository synchronization)

## **Installation**

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/naifta2/FreedomCycle3-Control-Interface.git
   cd FreedomCycle3-Control-Interface
   ```

2. **Set Up Virtual Environment (Optional but Recommended)**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use venv\Scripts\activate
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Settings**:

   Update `config/settings.py` with the appropriate serial port and other configurations.

5. **Upload Arduino Firmware**:

   - Navigate to `Arduino/FreedomCycle3_Firmware/` and open `FreedomCycle3_Firmware.ino` in the Arduino IDE.
   - Adjust sensor pins and calibration constants as per your hardware setup.
   - Upload the firmware to your Arduino device.

## **Usage**

1. **Run the Application**:

   ```bash
   python main.py
   ```

2. **Using the GUI**:

   - **Start Session**: Click on "Start Session" to begin data collection.
   - **Monitor Sensors**: View real-time sensor data updates in the GUI.
   - **Control Hardware**: Use the provided buttons to control hardware components like injection valves.
   - **Stop Session**: Click on "Stop Session" to end data collection and save data.

3. **Data Storage**:

   - Data is saved in the `data_sessions/` directory with timestamped folders.
   - Logs are stored in the `logs/` directory for each session.

## **Project Structure**

```plaintext
FreedomCycle3-Control-Interface/
├── main.py               # Entry point of the application
├── config/               # Contains configuration settings
├── gui/                  # Manages the graphical user interface
├── communication/        # Handles communication with the Arduino and sensors
├── data/                 # Manages data acquisition, processing, and logging
├── utils/                # Contains utility functions and custom exceptions
├── assets/               # Stores logos and other static assets
└── Arduino/              # Contains the Arduino firmware code
```

## **Modules Overview**

- `main.py`: Entry point of the application.
- `config/`: Contains configuration settings.
- `gui/`: Manages the graphical user interface.
- `communication/`: Handles communication with the Arduino and sensors.
- `data/`: Manages data acquisition, processing, and logging.
- `utils/`: Contains utility functions and custom exceptions.
- `assets/`: Stores logos and other static assets.
- `Arduino/`: Contains the Arduino firmware code.

## **Contributing**

Contributions are welcome! Please open an issue or submit a pull request for suggestions or improvements.

## **License**

This project is licensed under the MIT License. See the LICENSE file for details.

## **Acknowledgments**

- **University Name**: University of Illinois at Urbana-Champaign
- **Faculty Advisor**: Prof. Jiajun He
- **Sponsor**: Constellation Energy
- **Sponsor Contact**: John Freeman
- **Project Manager**: Fatemeh Cheraghi Pouria
- **Team Members**: Naif Alotaibi, Kevin Cantieri, Vaani Chimnani, Anna Kovarik, & Colin Zimmers

## **Contact**

For questions or support, please contact <ImprovedFreedomCyclePatent3@office365.illinois.edu>.
