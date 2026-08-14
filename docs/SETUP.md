# SentinelOne Industrial – Setup Guide

This guide explains how to set up and run the SentinelOne Industrial factory worker safety monitoring prototype.

SentinelOne Industrial combines Arduino-based environmental sensing with computer vision to monitor worker safety conditions and classify the environment into `SAFE`, `WARNING`, and `DANGER` states.

---

## 1. Prerequisites

Before running the system, make sure you have:

### Hardware

* Arduino Uno
* MQ-series gas sensor
* HC-SR04 ultrasonic distance sensor
* USB cable for Arduino
* Webcam
* Windows computer

### Software

* Python 3.x
* Git
* Arduino IDE
* A working internet connection for installing Python dependencies

---

## 2. Clone the Repository

Clone the repository using Git:

```bash
git clone https://github.com/meghkademani/SentinelOne-Industrial.git
cd SentinelOne-Industrial
```

---

## 3. Create a Python Virtual Environment

Using a virtual environment keeps the project's Python dependencies isolated from other projects.

Create the virtual environment:

```bash
python -m venv .venv
```

Activate the environment on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

After activation, the terminal should show:

```text
(.venv)
```

If PowerShell blocks the activation script, run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate the environment again:

```powershell
.\.venv\Scripts\Activate.ps1
```

---

## 4. Install Python Dependencies

Make sure the virtual environment is activated before installing dependencies.

Install the required packages:

```bash
pip install -r requirements.txt
```

The project uses Python libraries for computer vision, YOLO-based detection, serial communication, analytics, and data processing.

To verify the Python environment:

```bash
python --version
pip --version
```

To verify PyTorch:

```bash
python -c "import torch; print('PyTorch:', torch.__version__)"
```

To verify Ultralytics:

```bash
python -c "import ultralytics; print('Ultralytics: OK')"
```

---

## 5. Hardware Setup

Connect the hardware before starting the monitoring application.

### Arduino

1. Connect the Arduino Uno to the computer using USB.
2. Connect the MQ-series gas sensor to the Arduino.
3. Connect the HC-SR04 ultrasonic distance sensor to the Arduino.
4. Upload the Arduino sensor-reading firmware using the Arduino IDE.
5. Open Windows Device Manager and identify the Arduino's COM port.
6. Make sure the Arduino is available for serial communication.

### Webcam

Connect the webcam to the computer and make sure Windows recognizes it.

Close other applications that may already be using the webcam.

---

## 6. Serial Communication

The Python application communicates with the Arduino through a serial connection.

The current prototype uses a serial connection with a baud rate of:

```text
9600
```

The COM port may vary depending on the computer.

For example:

```text
COM3
```

may be used on the development machine.

If your Arduino appears on a different COM port, the current implementation may require the serial-port setting in the Python code to be updated accordingly.

> Centralized configuration for the COM port and safety thresholds is planned as a future improvement.

---

## 7. Run the Monitoring System

Before starting the application, make sure:

* The `.venv` environment is activated.
* The Arduino is connected through USB.
* The Arduino sensor-reading firmware is running.
* The webcam is connected and available.
* The required Python dependencies are installed.

Start the main SentinelOne Industrial monitoring application:

```bash
python sentinelone_main_yolo_zone_stage3.py
```

The main application uses the supporting modules in the repository to perform monitoring and detection.

During execution, the system can:

1. Connect to the Arduino.
2. Read sensor data.
3. Start the webcam.
4. Load the YOLO worker-detection model.
5. Detect workers in the camera feed.
6. Monitor the configured danger zone.
7. Evaluate sensor and worker-detection conditions.
8. Determine the current safety state.
9. Display the monitoring information.
10. Generate analytics and safety-related information.

Press `Q` to stop the monitoring application.

---

## 8. Safety States

SentinelOne Industrial classifies the current environment into three safety states.

### SAFE

The monitored conditions are within the configured safe limits.

### WARNING

One or more monitored conditions require attention, but the situation has not reached the danger threshold.

### DANGER

A dangerous condition has been detected, such as a worker entering a monitored danger zone or a sensor value exceeding its configured threshold.

The exact thresholds depend on the current implementation and may be adjusted as the project evolves.

---

## 9. Troubleshooting

### 9.1 Arduino connection fails

If the application cannot connect to the Arduino:

* Make sure the Arduino is connected through USB.
* Check the Arduino's COM port in Windows Device Manager.
* Make sure the correct COM port is configured in the Python application.
* Make sure no other application is using the Arduino's serial port.
* Confirm that the Arduino firmware is running.
* Disconnect and reconnect the Arduino if necessary.
* Restart the monitoring application.

### 9.2 Webcam is not detected

If the webcam does not start:

* Make sure the webcam is connected.
* Check Windows camera permissions.
* Close other applications that may be using the camera.
* Reconnect the webcam.
* Restart the monitoring application.

### 9.3 Python module is missing

If Python reports an error such as:

```text
ModuleNotFoundError
```

make sure the virtual environment is activated:

```powershell
.\.venv\Scripts\Activate.ps1
```

Then reinstall the project dependencies:

```bash
pip install -r requirements.txt
```

### 9.4 PyTorch or Ultralytics verification fails

Verify that the packages are installed inside the active virtual environment:

```bash
python -c "import torch; print('PyTorch:', torch.__version__)"
```

```bash
python -c "import ultralytics; print('Ultralytics: OK')"
```

If either command fails, reinstall the project dependencies:

```bash
pip install -r requirements.txt
```

### 9.5 YOLO model fails to load

If the YOLO model cannot be loaded:

* Make sure the required model file is present in the expected project location.
* Make sure Ultralytics is installed.
* Make sure PyTorch is installed correctly.
* Check the terminal output for the specific model-loading error.

Verify Ultralytics:

```bash
python -c "import ultralytics; print('Ultralytics: OK')"
```

### 9.6 The application immediately closes or stops

Check the terminal for the Python error message.

Common causes include:

* Incorrect COM port
* Arduino not connected
* Webcam unavailable
* Missing Python dependency
* Missing YOLO model
* Incorrect project path
* Virtual environment not activated

---

## 10. Project Structure

The current project contains the following important Python modules:

```text
SentinelOne-Industrial/
│
├── sentinelone_main_yolo_zone_stage3.py
├── sentinelone_serial.py
├── worker_detection.py
├── worker_detection_yolo.py
├── requirements.txt
├── README.md
│
└── docs/
    └── SETUP.md
```

### Main application

`sentinelone_main_yolo_zone_stage3.py`

This is the main entry point used to start the SentinelOne Industrial monitoring system.

### Serial communication

`sentinelone_serial.py`

Handles communication between the Python application and the Arduino.

### Worker detection

`worker_detection.py`

Contains worker-detection functionality used by the project.

### YOLO worker detection

`worker_detection_yolo.py`

Contains YOLO-based worker detection functionality.

### Dependencies

`requirements.txt`

Contains the Python packages required to run the project.

### Documentation

`docs/`

Contains project documentation and setup instructions.

---

## 11. Basic Startup Checklist

Before running SentinelOne Industrial, verify the following:

* [ ] Arduino Uno is connected.
* [ ] Arduino sensor firmware is running.
* [ ] MQ-series gas sensor is connected.
* [ ] HC-SR04 sensor is connected.
* [ ] Webcam is connected.
* [ ] Correct Arduino COM port is known.
* [ ] Python virtual environment is activated.
* [ ] Python dependencies are installed.
* [ ] YOLO model is available.
* [ ] Main application file is present.

Start the system with:

```bash
python sentinelone_main_yolo_zone_stage3.py
```

---

## 12. Current Limitations

The current version is a working prototype and has some limitations.

These include:

* Serial-port configuration is not yet centralized.
* Safety thresholds are not yet managed through a dedicated configuration file.
* Error handling can be improved.
* Automated unit testing is still being developed.
* Continuous integration is not yet implemented.
* The analytics and event-logging system can be expanded.

These limitations are part of the project's planned engineering roadmap.

---

## 13. Future Improvements

Planned improvements include:

1. Robust Arduino and serial-connection error handling.
2. Centralized configuration for COM ports, thresholds, camera settings, and danger zones.
3. Improved safety-event logging and analytics.
4. Unit tests for `SAFE`, `WARNING`, and `DANGER` decision logic.
5. Detailed architecture documentation.
6. GitHub Actions and continuous integration.
7. Additional reliability and production-oriented improvements.

The goal is to evolve SentinelOne Industrial from a working prototype into a stronger, maintainable, and portfolio-level industrial safety monitoring system.

---

## 14. Support and Troubleshooting

If you encounter a problem:

1. Check the terminal error message.
2. Verify that the virtual environment is active.
3. Verify that all dependencies are installed.
4. Check the Arduino USB and COM-port connection.
5. Check that the webcam is available.
6. Verify that the required YOLO model is present.
7. Review the project documentation and source code for configuration details.

When reporting an issue, include the relevant terminal error message and the steps that caused the problem.

---

## 15. Quick Start

For an already configured development environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Then:

```bash
python sentinelone_main_yolo_zone_stage3.py
```

Make sure the Arduino and webcam are connected before starting the application.

---

**SentinelOne Industrial**
*Industrial Worker Safety Monitoring using Sensors + Computer Vision*
