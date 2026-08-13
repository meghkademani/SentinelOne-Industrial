# SentinelOne Industrial

## Factory Worker Safety Monitoring System

SentinelOne Industrial is a real-time industrial safety monitoring system that combines Arduino-based environmental sensing with computer vision to monitor factory-worker safety conditions.

The system integrates gas-level monitoring, ultrasonic distance measurement, YOLO-based worker detection, danger-zone detection, real-time safety classification, event logging, and safety analytics.

---

## 🚨 Key Features

- Real-time gas monitoring using MQ-2 / MQ-135
- Ultrasonic proximity monitoring using HC-SR04
- Real-time worker detection using YOLO
- Danger-zone intrusion detection
- SAFE / WARNING / DANGER classification
- Live safety monitoring dashboard
- CSV-based safety event logging
- Safety history and analytics
- Statistical analysis and graphs
- Arduino-to-Python serial communication
- Webcam-based computer vision

---

## 🏗️ System Architecture

```text
                    ┌────────────────────┐
                    │     Arduino UNO    │
                    └─────────┬──────────┘
                              │
                     Serial Communication
                              │
              ┌───────────────┴───────────────┐
              │                               │
        MQ-2 / MQ-135                       HC-SR04
        Gas Sensor                         Distance
              │                               │
              └───────────────┬───────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │ Python Safety   │
                    │    Engine       │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
           OpenCV          YOLO         Sensor Data
          Webcam        Worker Detection
              │              │
              │              ▼
              │        Danger Zone
              │         Detection
              │              │
              └──────────────┼──────────────┘
                             ▼
                   SAFE / WARNING / DANGER
                             │
                  ┌──────────┴──────────┐
                  │                     │
                  ▼                     ▼
             Live Dashboard        CSV Logging
                                        │
                                        ▼
                              History & AnalyticsPerfect. 🔥

Your project structure is now ready for documentation.

### Step 2 — Create `README.md`

We're going to make this the **professional front page of your GitHub repository**.

Run:

```powershell
New-Item -ItemType File -Name README.md -Force
```

Then open it in VS Code:

```powershell
code .\README.md
```

It will open a blank `README.md`.

### Paste this into it

````markdown
# SentinelOne Industrial

## Factory Worker Safety Monitoring System

SentinelOne Industrial is a real-time industrial safety monitoring system that combines Arduino-based environmental sensing with computer vision to monitor factory-worker safety conditions.

The system integrates gas-level monitoring, ultrasonic distance measurement, YOLO-based worker detection, danger-zone detection, real-time safety classification, event logging, and safety analytics.

---

## 🚨 Key Features

- Real-time gas monitoring using MQ-2 / MQ-135
- Ultrasonic proximity monitoring using HC-SR04
- Real-time worker detection using YOLO
- Danger-zone intrusion detection
- SAFE / WARNING / DANGER classification
- Live safety monitoring dashboard
- CSV-based safety event logging
- Safety history and analytics
- Statistical analysis and graphs
- Arduino-to-Python serial communication
- Webcam-based computer vision

---

## 🏗️ System Architecture

```text
                    ┌────────────────────┐
                    │     Arduino UNO    │
                    └─────────┬──────────┘
                              │
                     Serial Communication
                              │
              ┌───────────────┴───────────────┐
              │                               │
        MQ-2 / MQ-135                       HC-SR04
        Gas Sensor                         Distance
              │                               │
              └───────────────┬───────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │ Python Safety   │
                    │    Engine       │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
           OpenCV          YOLO         Sensor Data
          Webcam        Worker Detection
              │              │
              │              ▼
              │        Danger Zone
              │         Detection
              │              │
              └──────────────┼──────────────┘
                             ▼
                   SAFE / WARNING / DANGER
                             │
                  ┌──────────┴──────────┐
                  │                     │
                  ▼                     ▼
             Live Dashboard        CSV Logging
                                        │
                                        ▼
                              History & Analytics
````

---

## 🔧 Hardware

* Arduino Uno
* MQ-2 / MQ-135 gas sensor
* HC-SR04 ultrasonic sensor
* Laptop / USB connection
* Webcam

---

## 💻 Software

* Python 3.12
* OpenCV
* PySerial
* Ultralytics YOLO
* Pandas
* Matplotlib
* Tkinter
* CSV logging

---

## 🤖 Computer Vision

The system uses a YOLO model to detect workers in the webcam feed.

Worker detection is integrated with the safety monitoring system so that the presence of a worker inside a configured danger zone can contribute to the overall safety status.

---

## 🛡️ Safety Logic

The system evaluates multiple safety conditions simultaneously.

### SAFE

Normal operating conditions.

### WARNING

A monitored parameter has crossed its warning threshold.

### DANGER

A critical condition is detected, such as:

* Gas level exceeding the danger threshold
* Distance entering the danger range
* Worker detected inside the configured danger zone

---

## 📊 Monitoring & Analytics

Safety events are recorded in CSV format.

The history/analytics system provides:

* Total events
* SAFE events
* WARNING events
* DANGER events
* Average gas level
* Average distance
* Average workers detected
* Gas history
* Distance history
* Worker detection history
* Safety event distribution

---

## 📁 Project Structure

```text
SentinelOne-Industrial/
│
├── README.md
├── sentinelone_main_yolo_zone_stage3.py
├── sentinelone_serial.py
├── worker_detection.py
├── worker_detection_yolo.py
├── yolo11n.pt
│
├── archive/
│
├── data/
│
├── docs/
│
├── models/
│
└── src/
```

---

## ⚙️ Current Implementation

The current working implementation includes:

* Arduino-Python serial communication
* Real-time sensor monitoring
* YOLO worker detection
* Danger-zone detection
* SAFE / WARNING / DANGER classification
* Live monitoring dashboard
* CSV event logging
* Safety history and analytics

---

## 🎯 Project Goal

The goal of SentinelOne Industrial is to demonstrate how embedded sensors and computer vision can be combined into a unified industrial safety monitoring system capable of detecting environmental hazards, worker presence, and dangerous-zone intrusion in real time.

---

## ⚠️ Disclaimer

This project is an educational/prototype safety-monitoring system and should not be treated as a certified industrial safety system or as a replacement for professionally certified safety equipment and procedures.

---

## 👤 Project

**SentinelOne Industrial**

Factory Worker Safety Monitor

````

### After pasting

Save it:

**Ctrl + S**

Then come back to PowerShell and run:

```powershell
Get-Content .\README.md -TotalCount 10
````

You should see:

```text
# SentinelOne Industrial

## Factory Worker Safety Monitoring System
```

**Don't create the other documentation files yet.**

Once the README is saved, tell me **`README done`** and we'll do **Step 3: create `.gitignore` and `requirements.txt`**, then prepare the repository for GitHub.
