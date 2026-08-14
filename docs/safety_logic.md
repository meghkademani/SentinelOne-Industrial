# SentinelOne Industrial — Safety Logic

## Overview

SentinelOne Industrial combines camera-based worker detection, camera danger-zone monitoring, ultrasonic proximity sensing, and gas monitoring to determine the current safety state.

The system reports:

- SAFE
- WARNING
- DANGER

Camera-zone intrusion and ultrasonic proximity are treated as separate safety conditions.

## 1. Worker Detection

YOLO is used to detect workers/persons in the camera view.

A detected worker does **not** automatically cause a DANGER state.

The worker's position is evaluated against the configured camera danger zone.

### Worker outside danger zone

```text
Worker detected
      |
      v
Zone = CLEAR
      |
      v
No camera intrusion