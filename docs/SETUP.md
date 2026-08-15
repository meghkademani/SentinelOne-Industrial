# SentinelOne Industrial – Setup Guide

This guide explains how to set up and run the **SentinelOne Industrial** factory worker safety monitoring prototype.

SentinelOne Industrial combines **Arduino-based environmental sensing, ultrasonic distance measurement, computer vision, YOLO11n worker detection, danger-zone monitoring, and safety-event logging** into a unified monitoring system.

> **Project status:** Functional engineering prototype.

---

## 1. Prerequisites

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
* Internet connection for installing Python dependencies

---

## 2. Clone the Repository

Clone the project from GitHub:

```bash
git clone https://github.com/meghkademani/SentinelOne-Industrial.git
cd SentinelOne-Industrial
```

---

## 3. Create the Python Virtual Environment

A virtual environment keeps project dependencies isolated from the rest of the system.

Create the environment:

```powershell
python -m venv .venv
```

Activate it in Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

After activation, the terminal should display:

```text
(.venv)
```

### PowerShell execution-policy error

If PowerShell prevents activation, run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate the environment again:

```powershell
.\.venv\Scripts\Activate.ps1
```

---

## 4. Install Python Dependencies

Make sure `.venv` is active before installing packages.

```powershell
pip install -r requirements.txt
```

Verify Python:

```powershell
python --version
```

Verify pip:

```powershell
pip --version
```

Verify PyTorch:

```powershell
python -c "import torch; print('PyTorch:', torch.__version__)"
```

Verify Ultralytics:

```powershell
python -c "import ultralytics; print('Ultralytics: OK')"
```

If both verification commands succeed, the computer-vision environment is ready.

---

## 5. Arduino and Sensor Setup

Connect the hardware before starting the Python monitoring application.

### Arduino

1. Connect the Arduino Uno to the computer using USB.
2. Connect the MQ-series gas sensor.
3. Connect the HC-SR04 ultrasonic sensor.
4. Open the Arduino sketch located in:

```text
sketch_aug13a/
```

5. Upload the sensor-reading firmware using the Arduino IDE.
6. Open **Windows Device Manager**.
7. Locate the Arduino under **Ports (COM & LPT)**.
8. Note the assigned COM port.

The development configuration currently uses:

```text
COM3
```

The actual COM port may be different on another computer.

### Webcam

Connect the webcam and verify that Windows recognizes it.

Close applications such as other camera software, video-conferencing applications, or other Python programs that may already be using the webcam.

---

## 6. Serial Communication

The Python application receives sensor data from the Arduino through a serial connection.

Current development configuration:

```text
Serial Port : COM3
Baud Rate   : 9600
```

The Arduino sends sensor information containing values such as gas level and distance.

Example:

```text
Gas: 82 | Distance: 17.50
```

If Windows assigns the Arduino a different COM port, update the corresponding serial configuration in the active Python implementation before running the system.

> The COM port is currently configured in the Python implementation rather than through a dedicated external configuration file.

---

## 7. YOLO Model

The project uses **YOLO11n** for real-time person/worker detection.

The model file included with the project is:

```text
yolo11n.pt
```

Make sure the model file remains available in the project directory expected by the application.

The YOLO model is used to:

* Detect people in webcam frames.
* Count detected workers.
* Determine worker positions.
* Evaluate whether a worker has entered the configured danger zone.

The system performs YOLO inference at a controlled frame interval to reduce unnecessary computational load.

---

## 8. Run the Monitoring System

Before starting the application, verify:

* `.venv` is activated.
* Arduino is connected.
* Arduino sensor firmware is running.
* Correct COM port is configured.
* Webcam is available.
* YOLO model is present.
* Python dependencies are installed.

### Start the current Stage 5 application

Run:

```powershell
python sentinelone_stage5.py
```

The application will initialize the monitoring pipeline:

```text
Arduino
   ↓
Serial Sensor Data
   ↓
Python Safety Engine
   +
Webcam
   ↓
YOLO11n Detection
   ↓
Worker / Danger-Zone Evaluation
   ↓
Safety Classification
   ↓
Dashboard + Event Logging
```

During operation, the terminal reports information such as:

```text
Gas: 31 | Distance: 233.96 cm | Workers: 1
Zone: INTRUSION
Status: DANGER
Reason: DANGER ZONE INTRUSION
```

Press:

```text
Q
```

to stop monitoring.

The application then releases the webcam, closes the serial connection, and saves the safety log.

---

## 9. Safety Classification

The safety engine evaluates sensor conditions and worker-zone conditions.

### SAFE

The monitored environment is operating within the configured safe limits.

### WARNING

A monitored condition has crossed its warning threshold but has not reached the configured danger condition.

### DANGER

A critical safety condition has been detected.

Examples include:

* Worker entering the configured danger zone.
* Gas level exceeding the danger threshold.
* Distance reaching the danger threshold.

Danger conditions take priority over normal operation.

---

## 10. Current Safety Thresholds

The current prototype uses the following software thresholds.

### Gas

| Condition | Threshold |
| --------- | --------: |
| WARNING   |    `> 70` |
| DANGER    |   `> 150` |

### Distance

| Condition | Threshold |
| --------- | --------: |
| WARNING   | `≤ 20 cm` |
| DANGER    | `≤ 10 cm` |

These values are **prototype software thresholds** and are not certified occupational exposure limits or industrial safety standards.

---

## 11. Danger-Zone Monitoring

The camera frame contains a configurable rectangular danger zone.

The current implementation uses normalized coordinates rather than fixed pixel coordinates, allowing the zone to adapt to the active camera resolution.

Current configuration:

```python
DANGER_ZONE_X1 = 0.25
DANGER_ZONE_Y1 = 0.45
DANGER_ZONE_X2 = 0.80
DANGER_ZONE_Y2 = 1.00
```

The system evaluates the lower portion of a detected person's bounding box as an approximation of their standing/foot position.

When a detected worker enters the configured danger zone, the system reports:

```text
Zone: INTRUSION
Status: DANGER
Reason: DANGER ZONE INTRUSION
```

---

## 12. Safety Event Logging

Safety events are recorded in:

```text
safety_log.csv
```

The log contains information such as:

```text
Timestamp
Gas
Distance
Workers
Status
Reason
```

Example:

```text
2026-08-16 01:10:10 | Gas: 31 | Distance: 233.96 cm | Workers: 1 | Status: DANGER | Reason: DANGER ZONE INTRUSION
```

The CSV log can later be used by the project's analytics and history components.

---

## 13. Project Structure

The important project components are organized approximately as follows:

```text
SentinelOne-Industrial/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── sentinelone_stage5.py
├── sentinelone_serial.py
├── sentinelone_analytics.py
├── sentinelone_history.py
├── worker_detection.py
├── worker_detection_yolo.py
│
├── yolo11n.pt
├── safety_log.csv
│
├── sketch_aug13a/
│   └── Arduino sensor firmware
│
├── src/
│   └── Supporting source components
│
├── models/
│   └── Model-related resources
│
├── docs/
│   ├── SETUP.md
│   ├── safety_logic.md
│   └── testing.md
│
└── archive/
    └── Previous development versions
```

### Main application

```text
sentinelone_stage5.py
```

The current Stage 5 monitoring application and primary runtime entry point.

### Serial communication

```text
sentinelone_serial.py
```

Contains serial communication functionality used to exchange information with the Arduino.

### Worker detection

```text
worker_detection.py
worker_detection_yolo.py
```

Supporting worker/person detection functionality.

### Analytics

```text
sentinelone_analytics.py
sentinelone_history.py
```

Components used for safety-event history and analysis.

### Arduino firmware

```text
sketch_aug13a/
```

Contains the Arduino-side sensor firmware.

### YOLO model

```text
yolo11n.pt
```

YOLO11n model weights used for person detection.

### Documentation

```text
docs/
```

Contains setup, safety-logic, and testing documentation.

### Archive

```text
archive/
```

Contains previous development versions that are kept separate from the active implementation.

---

## 14. Basic Startup Checklist

Before starting the system:

* [ ] Arduino Uno is connected.
* [ ] MQ-series gas sensor is connected.
* [ ] HC-SR04 sensor is connected.
* [ ] Arduino firmware has been uploaded.
* [ ] Correct Arduino COM port is known.
* [ ] Webcam is connected and available.
* [ ] `.venv` is activated.
* [ ] Python dependencies are installed.
* [ ] `yolo11n.pt` is available.
* [ ] `sentinelone_stage5.py` is present.

Then run:

```powershell
python sentinelone_stage5.py
```

---

## 15. Troubleshooting

### Arduino connection fails

Check:

1. Arduino USB connection.
2. COM port in Windows Device Manager.
3. Python serial-port configuration.
4. Arduino firmware.
5. Whether another program is using the serial port.

If necessary, disconnect and reconnect the Arduino and restart the application.

---

### Webcam does not start

Check:

* Webcam connection.
* Windows camera permissions.
* Whether another application is using the camera.
* Camera availability in OpenCV.

Close other camera applications and restart the monitoring program.

---

### `ModuleNotFoundError`

Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Then reinstall dependencies:

```powershell
pip install -r requirements.txt
```

---

### YOLO model fails to load

Verify that:

```text
yolo11n.pt
```

is available and that Ultralytics is installed:

```powershell
python -c "import ultralytics; print('Ultralytics: OK')"
```

Also verify PyTorch:

```powershell
python -c "import torch; print('PyTorch:', torch.__version__)"
```

---

### Serial data shows unexpected values

Check:

* Arduino sensor wiring.
* Arduino firmware.
* Sensor power supply.
* Serial baud rate.
* Serial output format.
* Sensor calibration.

The current prototype values should not be interpreted as certified industrial measurements.

---

### Application stops unexpectedly

Check the terminal output for the Python exception.

Common causes include:

* Arduino disconnect.
* Serial-port errors.
* Webcam failure.
* Missing dependency.
* Missing YOLO model.
* Incorrect configuration.
* Hardware communication problems.

The terminal output should be checked first because it usually identifies the failing component.

---

## 16. Quick Start

For an already configured development environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Then:

```powershell
python sentinelone_stage5.py
```

Make sure the Arduino and webcam are connected before starting the application.

Press `Q` to stop monitoring.

---

## 17. Important Notes

SentinelOne Industrial is currently an **engineering and educational prototype**.

The gas, distance, and computer-vision measurements depend on the connected hardware, calibration, camera position, environmental conditions, and software configuration.

The configured thresholds are project-specific prototype values.

This system must **not** be treated as a certified industrial safety controller or as a replacement for professional safety equipment, industrial controls, risk assessments, emergency systems, or trained safety personnel.

For architecture and decision-making details, see:

```text
docs/safety_logic.md
```

For validation and test procedures, see:

```text
docs/testing.md
```

---

**SentinelOne Industrial**

*Industrial Worker Safety Monitoring using Sensors + Computer Vision*
