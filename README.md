#  SentinelOne Industrial

### AI-Powered Factory Worker Safety Monitoring System

> **A real-time industrial safety system combining IoT sensors, computer vision, and intelligent safety logic to detect hazardous conditions and protect factory workers.** 

 



\

---

## 📌 Overview

**SentinelOne Industrial** is a real-time factory worker safety monitoring system designed to identify and respond to potentially dangerous workplace conditions.

The system combines:

* 🌫️ **Gas sensing** using MQ-series sensors
* 📏 **Proximity monitoring** using an HC-SR04 ultrasonic sensor
* 👷 **AI-based worker detection** using YOLO
* 🧠 **Intelligent safety classification**
* 📊 **Real-time safety dashboard**
* 🚨 **Danger-zone intrusion detection**
* 📝 **Automatic safety event logging**
* 📈 **Safety history and analytics**

The project demonstrates how **embedded systems, IoT, computer vision, and Python-based software** can work together to create an intelligent industrial safety solution.

---

## 🎯 Problem Statement

Industrial environments can expose workers to multiple hazards such as:

* Toxic or combustible gases
* Unsafe proximity to hazardous areas
* Unauthorized entry into danger zones
* Lack of continuous safety monitoring
* Delayed detection of hazardous situations

Traditional safety systems often rely heavily on manual monitoring.

**SentinelOne Industrial aims to provide an automated, continuous, and data-driven safety monitoring layer.**

---

## 💡 Solution

The system continuously collects information from physical sensors and a camera.

The data is processed by the Python safety engine, which evaluates:

**Gas Level + Distance + Worker Presence + Zone Status**

and determines the current safety condition:

### 🟢 SAFE

No significant hazard detected.

### 🟠 WARNING

A potentially unsafe condition has been detected.

### 🔴 DANGER.

A critical hazard or dangerous-zone intrusion has been detected.

The system also records safety events for later analysis.

---

# 🏗️ System Architecture

```text
                  ┌──────────────────────┐
                  │      Factory Area    │
                  └──────────┬───────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
        ┌──────────┐   ┌──────────┐   ┌──────────┐
        │ MQ Gas   │   │ HC-SR04  │   │ Webcam   │
        │ Sensor   │   │ Ultrasonic│   │          │
        └────┬─────┘   └────┬─────┘   └────┬─────┘
             │              │              │
             └──────────────┼──────────────┘
                            ▼
                    ┌───────────────┐
                    │ Arduino UNO   │
                    │ Sensor Layer  │
                    └───────┬───────┘
                            │
                       Serial USB
                            │
                            ▼
                 ┌────────────────────┐
                 │ Python Safety Engine│
                 └─────────┬──────────┘
                           │
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
        ┌─────────┐   ┌──────────┐  ┌──────────┐
        │  YOLO   │   │ Safety   │  │   Zone   │
        │ Worker  │   │  Logic   │  │ Analysis │
        │Detection│   │          │  │          │
        └────┬────┘   └────┬─────┘  └────┬─────┘
             └─────────────┼──────────────┘
                           ▼
                 ┌────────────────────┐
                 │ Real-Time Dashboard │
                 └─────────┬──────────┘
                           │
                  ┌────────┴────────┐
                  ▼                 ▼
             Safety Status      Event Logs
                                  │
                                  ▼
                           CSV / Analytics
```

---

# ⚙️ Hardware Components

| Component     | Purpose                                 |
| ------------- | --------------------------------------- |
| Arduino Uno   | Sensor acquisition and hardware control |
| MQ-2 / MQ-135 | Gas/environmental monitoring            |
| HC-SR04       | Distance and proximity measurement      |
| Laptop Webcam | Real-time worker detection              |
| USB Cable     | Arduino ↔ Python communication          |

---

# 💻 Software Stack

| Technology  | Role                                  |
| ----------- | ------------------------------------- |
| Python 3.12 | Main application and safety engine    |
| OpenCV      | Computer vision and camera processing |
| YOLO        | AI-based worker detection             |
| PySerial    | Arduino serial communication          |
| CSV         | Safety event storage                  |
| Arduino IDE | Microcontroller programming           |
| Matplotlib  | Safety analytics and visualization    |

---

# 🚨 Safety Monitoring Logic

The system evaluates multiple conditions simultaneously.

```text
             Sensor + Vision Data
                     │
                     ▼
            ┌─────────────────┐
            │ Safety Analysis │
            └────────┬────────┘
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
    Gas Level     Distance    Worker Count
        │            │            │
        └────────────┼────────────┘
                     ▼
              Zone Evaluation
                     │
                     ▼
             Safety Classification
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
        SAFE       WARNING     DANGER
```

A dangerous-zone intrusion can immediately escalate the system to **DANGER**, even when the gas level itself is below the critical threshold.

Example event:

```text
Gas: 45 | Distance: 114.70 cm | Workers: 1
Zone: INTRUSION | Status: DANGER
Reason: DANGER ZONE INTRUSION
```

---

# 🤖 AI Worker Detection

Earlier versions of the project used traditional computer-vision approaches for worker detection.

The system was upgraded to **YOLO-based object detection** to provide a more robust foundation for real-time worker monitoring.

YOLO allows the system to:

* Detect people in the camera frame
* Count detected workers
* Monitor worker presence
* Combine worker location with safety-zone logic
* Support future PPE and behavior monitoring

---

# 📊 Real-Time Safety Dashboard

The dashboard provides live visibility into the industrial environment.

It displays information such as:

* Current gas reading
* Distance measurement
* Number of detected workers
* Current safety zone
* Overall safety status
* Hazard reason
* Camera feed
* Safety events

Example:

```text
┌─────────────────────────────────────┐
│       SENTINELONE INDUSTRIAL        │
├─────────────────────────────────────┤
│ Gas Level      : 45                 │
│ Distance       : 114.70 cm          │
│ Workers        : 1                  │
│ Zone           : INTRUSION          │
│ Status         : DANGER             │
│ Reason         : DANGER ZONE        │
│                  INTRUSION          │
└─────────────────────────────────────┘
```

---

# 📝 Safety Event Logging

Safety events are automatically stored for analysis.

Example:

```text
Timestamp,Gas,Distance,Workers,Zone,Status,Reason
2026-08-15 01:18:32,45,114.70,1,INTRUSION,DANGER,DANGER ZONE INTRUSION
```

This enables:

* Historical safety analysis
* Incident investigation
* Hazard frequency tracking
* Future predictive analytics
* Safety performance reporting

---

# 📈 Analytics

The project includes safety history and analytics capabilities to transform raw safety events into useful information.

Potential metrics include:

* Total safety events
* SAFE/WARNING/DANGER distribution
* Gas-level trends
* Distance trends
* Worker activity
* Zone intrusion frequency
* Hazard occurrence over time

---

# 📂 Project Structure

```text
SentinelOne-Industrial/
│
├── Arduino/
│   └── sensor_monitor.ino
│
├── Python/
│   ├── sentinelone_main_yolo_zone_stage3.py
│   └── ...
│
├── logs/
│   └── safety_log.csv
│
├── requirements.txt
├── README.md
└── LICENSE
```

> File names may vary depending on the current development stage of the project.

---

# 🚀 Getting Started

## 1. Clone the Repository

```bash
git clone https://github.com/meghkademani/SentinelOne-Industrial.git
cd SentinelOne-Industrial
```

## 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If required packages are not already listed:

```bash
pip install opencv-python pyserial ultralytics numpy matplotlib
```

## 4. Connect the Hardware

Connect:

* MQ-2/MQ-135 → Arduino
* HC-SR04 → Arduino
* Arduino Uno → Computer via USB
* Webcam → Computer

Upload the Arduino firmware using **Arduino IDE**.

## 5. Select the Correct COM Port

Check the Arduino IDE under:

```text
Tools → Port
```

Then configure the corresponding COM port in the Python application.

## 6. Run SentinelOne Industrial

```powershell
python sentinelone_main_yolo_zone_stage3.py
```

---

# 🔧 Development Roadmap

### ✅ Completed

* [x] Arduino sensor integration
* [x] Arduino–Python serial communication
* [x] Gas monitoring
* [x] Ultrasonic distance monitoring
* [x] SAFE/WARNING/DANGER classification
* [x] Real-time dashboard
* [x] Safety event logging
* [x] Safety history and analytics
* [x] YOLO-based worker detection
* [x] Danger-zone intrusion detection

### 🔄 Future Enhancements

* [ ] Automatic buzzer and warning-light activation
* [ ] Multi-zone industrial mapping
* [ ] PPE detection
* [ ] Helmet and safety-vest detection
* [ ] Worker fall detection
* [ ] Emergency SOS mechanism
* [ ] Cloud-based monitoring
* [ ] Mobile notifications
* [ ] Web-based supervisor dashboard
* [ ] Edge deployment using Raspberry Pi
* [ ] Predictive hazard analysis
* [ ] Industrial-grade sensor integration

---

# 🌐 Potential Real-World Applications

SentinelOne Industrial can be adapted for:

* Manufacturing plants
* Chemical industries
* Warehouses
* Construction sites
* Oil & gas facilities
* Mining environments
* Automotive manufacturing
* Restricted industrial zones

---

# 🔐 Safety Disclaimer

This project is a **prototype and educational engineering system**.

It is not intended to replace certified industrial safety equipment, emergency systems, or legally required workplace safety procedures.

For real-world deployment, the system would require industrial-grade sensors, validated detection algorithms, fail-safe hardware, cybersecurity measures, environmental testing, and compliance with applicable safety standards.

---

# 👨‍💻 Author

### Megh Kademani

**Electronics & Communication Engineering | Embedded Systems | IoT | Computer Vision | Automotive Technology**

GitHub:
https://github.com/meghkademani

LinkedIn:
https://www.linkedin.com/in/meghkademani30

---

# ⭐ Project Vision

> **SentinelOne Industrial aims to bridge embedded systems and artificial intelligence to create safer, smarter, and more responsive industrial environments.**

If you find this project interesting, consider ⭐ **starring the repository** and following the development journey.

---

## 📄 License

This project is licensed under the **MIT License**.
