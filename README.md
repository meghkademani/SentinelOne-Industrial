# SentinelOne Industrial

## Factory Worker Safety Monitoring System

**SentinelOne Industrial** is a real-time industrial safety monitoring prototype that combines **embedded sensors, Arduino, computer vision, YOLO-based worker detection, danger-zone monitoring, and safety-event analytics** into a unified monitoring system.

The system continuously combines environmental sensor data with visual information from a webcam to determine whether the monitored environment is **SAFE, WARNING, or DANGER**.

> **Project Status:** Functional prototype / development project

---

## 🚨 Overview

Industrial environments can contain multiple simultaneous hazards. SentinelOne Industrial is designed as a prototype system for monitoring several of these conditions in real time.

The system combines:

* 🌫️ Gas-level monitoring
* 📏 Ultrasonic distance monitoring
* 👷 YOLO-based worker detection
* 🚧 Configurable danger-zone detection
* 🟢 SAFE / 🟠 WARNING / 🔴 DANGER classification
* 🖥️ Real-time monitoring dashboard
* 📋 CSV safety-event logging
* 📊 Historical safety analytics
* 🔌 Arduino-to-Python serial communication
* 📷 Webcam-based computer vision

---

# 🏗️ System Architecture

```text
                         SENTINELONE INDUSTRIAL
                    FACTORY WORKER SAFETY MONITOR
                                  │
              ┌───────────────────┴───────────────────┐
              │                                       │
              ▼                                       ▼
       ┌───────────────┐                       ┌───────────────┐
       │  ARDUINO UNO  │                       │    WEBCAM     │
       └───────┬───────┘                       └───────┬───────┘
               │                                       │
       ┌───────┴────────┐                              │
       │                │                              │
       ▼                ▼                              ▼
 ┌───────────┐    ┌───────────┐              ┌────────────────┐
 │ Gas Sensor│    │  HC-SR04   │              │ YOLO11n Model  │
 │ MQ-2 /    │    │ Ultrasonic │              │ Worker/Person  │
 │ MQ-135    │    │  Distance  │              │   Detection    │
 └─────┬─────┘    └─────┬─────┘              └───────┬────────┘
       │                │                             │
       └────────────────┴──────────────┬──────────────┘
                                       │
                                       ▼
                            ┌─────────────────────┐
                            │   PYTHON SAFETY     │
                            │       ENGINE        │
                            └──────────┬──────────┘
                                       │
                         ┌─────────────┼─────────────┐
                         │             │             │
                         ▼             ▼             ▼
                  ┌────────────┐ ┌────────────┐ ┌─────────────┐
                  │ Gas Safety │ │ Distance  │ │ Danger Zone │
                  │ Evaluation │ │ Evaluation│ │  Detection  │
                  └─────┬──────┘ └─────┬──────┘ └──────┬──────┘
                        │              │               │
                        └──────────────┼───────────────┘
                                       │
                                       ▼
                            ┌─────────────────────┐
                            │   SAFETY ENGINE     │
                            │                     │
                            │ SAFE / WARNING /    │
                            │       DANGER        │
                            └──────────┬──────────┘
                                       │
                         ┌─────────────┴─────────────┐
                         │                           │
                         ▼                           ▼
                ┌────────────────┐          ┌─────────────────┐
                │ LIVE DASHBOARD │          │  EVENT LOGGER   │
                │                │          │                 │
                │ Sensor Data    │          │ safety_log.csv  │
                │ Workers        │          └────────┬────────┘
                │ Zone Status    │                   │
                │ Safety Status  │                   ▼
                └────────────────┘          ┌─────────────────┐
                                            │    ANALYTICS    │
                                            │                 │
                                            │ History         │
                                            │ Statistics      │
                                            │ Graphs          │
                                            └─────────────────┘
```

---

# ⚙️ How It Works

The monitoring pipeline operates continuously:

```text
1. Arduino reads environmental sensors
              ↓
2. Sensor data is transmitted through serial communication
              ↓
3. Python receives gas and distance readings
              ↓
4. Webcam captures the monitoring area
              ↓
5. YOLO11n detects people/workers
              ↓
6. Worker positions are evaluated against the danger zone
              ↓
7. Gas, distance and zone conditions are evaluated
              ↓
8. Safety engine determines system state
              ↓
9. Dashboard displays the current condition
              ↓
10. Safety events are recorded for later analysis
```

---

# 👷 Computer Vision & Worker Detection

SentinelOne Industrial uses **YOLO11n** through the Ultralytics framework for real-time person detection.

The current implementation:

* Processes webcam frames using OpenCV.
* Runs YOLO inference at a controlled frame interval to improve responsiveness.
* Uses a confidence threshold of **0.45**.
* Filters detections to the COCO `person` class.
* Tracks the number of detected workers.
* Uses worker position for danger-zone evaluation.

## The system also retains the latest valid detections between inference frames to improve dashboard smoothness on typical computers.

# 🚧 Danger-Zone Detection

A configurable rectangular danger zone is defined inside the camera frame.

```text
             CAMERA FRAME
┌──────────────────────────────────────────┐
│                                          │
│              SAFE AREA                   │
│                                          │
│                                          │
│       ┌──────────────────────────┐       │
│       │                            │       │
│       │      DANGER ZONE          │       │
│       │                            │       │
│       │       👷                  │       │
│       │                            │       │
│       └──────────────────────────┘       │
│                                          │
└──────────────────────────────────────────┘
```

The current implementation calculates the zone relative to the camera frame rather than using fixed pixel coordinates. This makes the zone adaptable to the active frame dimensions.

Worker position is evaluated using the lower portion of the detected bounding box as an approximation of the worker's standing/foot position.

A worker entering the configured danger zone is treated as an immediate **DANGER** condition.

---

# 🛡️ Safety Classification

The safety engine evaluates multiple conditions.

## SAFE

The monitored conditions remain within normal operating limits.

## WARNING

A monitored parameter has crossed its warning threshold but has not reached the configured danger condition.

## DANGER

A critical condition has been detected.

Examples include:

* Worker intrusion into the configured danger zone
* Gas level exceeding the danger threshold
* Distance reaching the configured danger range

The safety engine prioritizes danger-zone intrusion and critical sensor conditions over normal operation.

---

# 📏 Current Distance Thresholds

The current implementation uses:

| Condition  | Threshold |
| ---------- | --------: |
| 🟠 WARNING |   ≤ 20 cm |
| 🔴 DANGER  |   ≤ 10 cm |

These values are configurable in the Python safety engine.

---

# 🌫️ Gas Monitoring

The system is designed to receive gas-level readings from the Arduino-based sensing subsystem.

The gas reading is transmitted to Python through the serial interface and incorporated into the safety classification.

The configured software thresholds are:

| Condition  | Gas Level |
| ---------- | --------: |
| 🟠 WARNING |      > 70 |
| 🔴 DANGER  |     > 150 |

These are **prototype software thresholds**, not certified occupational exposure limits. The implementation defines these values as `GAS_WARNING = 70` and `GAS_DANGER = 150`.

---

# 🔌 Arduino Communication

The Arduino communicates with the Python application using serial communication.

Current configuration:

```text
Serial Port : COM3
Baud Rate   : 9600
```

The Python application parses sensor messages containing gas and distance values.

Example data format:

```text
Gas: 82 | Distance: 17.50
```

The Python application extracts these values and feeds them into the safety engine.

> **Note:** The COM port may need to be changed depending on the computer and Arduino connection.

---

# 🖥️ Real-Time Dashboard

The application provides a live OpenCV monitoring interface.

The dashboard can display:

* Current gas level
* Current distance
* Number of detected workers
* Danger-zone status
* Current safety status
* System operational state
* Monitoring state
* Exit instruction

## The Stage 3 implementation displays the current status directly on the monitoring frame and reports the same information in the terminal.

# 📋 Safety Event Logging

Safety events are stored in CSV format.

The log records:

| Field         | Description                |
| ------------- | -------------------------- |
| Timestamp     | Time of the recorded event |
| Gas Level     | Current gas reading        |
| Distance      | Ultrasonic distance in cm  |
| Workers       | Number of detected workers |
| Safety Status | SAFE / WARNING / DANGER    |

This provides a persistent history that can be used for later analysis.

---

# 📊 Analytics

The project includes safety-history and analytics components for analyzing recorded events.

Possible analysis includes:

* Total recorded events
* SAFE events
* WARNING events
* DANGER events
* Average gas level
* Average distance
* Worker detection statistics
* Gas history
* Distance history
* Safety-status distribution

---

# 🔧 Hardware

## Required / Prototype Hardware

* Arduino Uno
* MQ-series gas sensor
* HC-SR04 ultrasonic distance sensor
* USB connection
* Computer/laptop
* Webcam

### Hardware Flow

```text
MQ Gas Sensor ─────┐
                   │
                   ▼
              Arduino UNO
                   │
HC-SR04 ───────────┘
                   │
                   │ USB / Serial
                   ▼
             Python Application
                   │
                   ▼
             Safety Engine
```

---

# 💻 Software Stack

| Component            | Technology  |
| -------------------- | ----------- |
| Programming          | Python      |
| Embedded Controller  | Arduino Uno |
| Computer Vision      | OpenCV      |
| Object Detection     | YOLO11n     |
| YOLO Framework       | Ultralytics |
| Serial Communication | PySerial    |
| Data Processing      | Pandas      |
| Visualization        | Matplotlib  |
| Logging              | CSV         |
| Dashboard            | OpenCV      |

---

# 📁 Project Structure

```text
SentinelOne-Industrial/
│
├── README.md
├── .gitignore
├── requirements.txt
│
├── sentinelone_main_yolo_zone_stage3.py
├── sentinelone_serial.py
├── worker_detection.py
├── worker_detection_yolo.py
│
├── yolo11n.pt
│
├── safety_log.csv
│
├── sentinelone_analytics.py
├── sentinelone_history.py
│
├── archive/
│   └── old_versions/
│       └── Previous development versions
│
├── docs/
│
└── data/
```

> The `archive/` directory contains previous development versions and is kept separately from the active implementation.

---

# 🚀 Installation

## 1. Clone the Repository

```bash
git clone https://github.com/meghkademani/SentinelOne-Industrial.git
cd SentinelOne-Industrial
```

## 2. Create a Python Environment

Recommended:

```powershell
python -m venv .venv
```

Activate it on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

## 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

---

# 🔌 Hardware Setup

1. Connect the Arduino Uno to the computer.
2. Connect the gas sensor.
3. Connect the HC-SR04 ultrasonic sensor.
4. Connect the webcam.
5. Upload the Arduino sketch to the Arduino Uno.
6. Confirm the Arduino serial port.
7. Update the Python serial-port configuration if necessary.

The current Python implementation is configured for `COM3` at `9600` baud.

---

# ▶️ Running the System

Start the main monitoring application:

```powershell
python sentinelone_main_yolo_zone_stage3.py
```

The application will:

```text
Connect to Arduino
       ↓
Start webcam
       ↓
Load YOLO11n
       ↓
Read sensor data
       ↓
Detect workers
       ↓
Evaluate danger zone
       ↓
Calculate safety status
       ↓
Display live dashboard
       ↓
Log safety events
```

Press:

```text
Q
```

to stop the monitoring application.

The application releases the camera, closes the Arduino connection, and closes OpenCV windows during shutdown.

---

# ⚙️ Configuration

Important configuration values can be adjusted in the main Python application.

### Serial Communication

```python
ARDUINO_PORT = "COM3"
BAUD_RATE = 9600
```

### Safety Thresholds

```python
GAS_WARNING = 70
GAS_DANGER = 150

DISTANCE_WARNING = 20
DISTANCE_DANGER = 10
```

### YOLO

```python
YOLO_EVERY_N_FRAMES = 2
```

### Danger Zone

```python
DANGER_ZONE_X1 = 0.25
DANGER_ZONE_Y1 = 0.45
DANGER_ZONE_X2 = 0.80
DANGER_ZONE_Y2 = 1.00
```

The danger-zone coordinates are normalized relative to the camera frame and can therefore be adjusted without hard-coding a specific camera resolution.

---

# 🧠 Safety Decision Logic

The core decision process can be represented as:

```text
                   SENSOR + VISION DATA
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
       Gas Level        Distance       Worker Zone
          │                │                │
          └────────────────┼────────────────┘
                           │
                           ▼
                    SAFETY ENGINE
                           │
             ┌─────────────┼─────────────┐
             │             │             │
             ▼             ▼             ▼
           SAFE         WARNING        DANGER
```

Conceptually:

```text
IF worker enters danger zone
        → DANGER

ELSE IF gas > danger threshold
        → DANGER

ELSE IF distance <= danger threshold
        → DANGER

ELSE IF gas > warning threshold
        → WARNING

ELSE IF distance <= warning threshold
        → WARNING

ELSE
        → SAFE
```

---

# 📈 Data & Analytics Pipeline

```text
                    REAL-TIME MONITORING
                            │
                            ▼
                  ┌───────────────────┐
                  │   Safety Events   │
                  └─────────┬─────────┘
                            │
                            ▼
                     safety_log.csv
                            │
                            ▼
                  ┌───────────────────┐
                  │ History / Analysis│
                  └─────────┬─────────┘
                            │
                  ┌─────────┼─────────┐
                  │         │         │
                  ▼         ▼         ▼
               Statistics  Trends   Graphs
```

---

# 🔬 Technical Highlights

### Multi-Modal Monitoring

The system combines **sensor-based monitoring** and **computer vision** rather than relying on a single safety signal.

### Real-Time Processing

Sensor data and webcam frames are processed continuously while the system is running.

### Configurable Danger Zone

The danger zone is defined relative to the camera frame, allowing the monitored region to be adjusted for different setups.

### YOLO Inference Optimization

YOLO inference is intentionally performed every second frame while retaining the latest detections between inference frames. This reduces computational load and improves dashboard responsiveness.

### Event-Based Logging

Safety information is stored as structured CSV data, allowing the system to be analyzed after operation.

---

# 🧪 Development Roadmap

Future improvements may include:

* [ ] Multi-camera monitoring
* [ ] Web-based monitoring dashboard
* [ ] Email/SMS/notification alerts
* [ ] Improved worker tracking
* [ ] More advanced zone management
* [ ] Database-backed event storage
* [ ] Remote monitoring
* [ ] Hardware alarm integration
* [ ] Improved sensor calibration
* [ ] Model optimization for edge devices
* [ ] Automated report generation

---

# ⚠️ Limitations

This project is currently a **prototype**.

Important limitations include:

* Gas readings depend on the connected sensor and its calibration.
* Distance measurements depend on the HC-SR04 and installation conditions.
* YOLO detection performance depends on camera quality, lighting, positioning, and scene conditions.
* A camera-based danger zone is dependent on the camera viewpoint.
* The configured safety thresholds are project-specific prototype values.
* The system has not been certified for use as an industrial safety control system.

---

# 🛑 Safety Disclaimer

**SentinelOne Industrial is an educational and engineering prototype.**

It is **not a certified industrial safety system** and must not be used as a replacement for professionally certified safety equipment, emergency systems, industrial controls, risk assessments, or trained safety personnel.

The threshold values and detection logic demonstrated in this repository are intended for experimentation and development.

---

# 🎯 Project Goal

The goal of SentinelOne Industrial is to demonstrate how **embedded systems, environmental sensing, computer vision, and software analytics** can be combined into a unified industrial safety-monitoring platform.

The project explores:

```text
Embedded Sensing
       +
Computer Vision
       +
Real-Time Processing
       +
Safety Decision Logic
       +
Event Logging
       +
Analytics
       =
Integrated Safety Monitoring Prototype
```

---

# 👤 Project

**SentinelOne Industrial**

Factory Worker Safety Monitoring System

Developed as an engineering prototype exploring the integration of **Arduino, Python, computer vision, YOLO, sensor monitoring, and safety analytics**.

---

## ⭐ If You Find This Project Interesting

Consider starring the repository and following the development of the project.

**SentinelOne Industrial — From sensing to vision, from detection to decision.**
