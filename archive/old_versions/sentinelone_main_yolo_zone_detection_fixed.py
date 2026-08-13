import cv2
import serial
import time
import re
import csv
import os
from datetime import datetime
from ultralytics import YOLO


# =========================================================
# SENTINELONE INDUSTRIAL
# FACTORY WORKER SAFETY MONITOR
# =========================================================

ARDUINO_PORT = "COM3"
BAUD_RATE = 9600

# =========================================================
# SAFETY THRESHOLDS
# =========================================================

GAS_WARNING = 70
GAS_DANGER = 150

DISTANCE_WARNING = 20
DISTANCE_DANGER = 10


# =========================================================
# COLORS - OpenCV uses BGR
# =========================================================

BLACK = (15, 15, 15)
DARK = (25, 25, 30)
WHITE = (255, 255, 255)

GREEN = (50, 220, 50)
ORANGE = (0, 165, 255)
RED = (50, 50, 230)

CYAN = (255, 220, 0)
PURPLE = (200, 80, 200)
YELLOW = (0, 220, 255)


# =========================================================
# CSV LOGGING
# =========================================================

LOG_FILE = "safety_log.csv"


def create_log_file():

    if not os.path.exists(LOG_FILE):

        with open(
            LOG_FILE,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                "Timestamp",
                "Gas Level",
                "Distance (cm)",
                "Workers",
                "Safety Status"
            ])


def log_event(gas, distance, workers, status):

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    with open(
        LOG_FILE,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            timestamp,
            gas,
            f"{distance:.2f}",
            workers,
            status
        ])

    print(
        f"[LOGGED] {timestamp} | "
        f"Gas: {gas} | "
        f"Distance: {distance:.2f} cm | "
        f"Workers: {workers} | "
        f"Status: {status}"
    )


create_log_file()


# =========================================================
# SAFETY ENGINE
# =========================================================

def calculate_safety(gas, distance):

    if gas > GAS_DANGER or distance <= DISTANCE_DANGER:
        return "DANGER"

    elif gas > GAS_WARNING or distance <= DISTANCE_WARNING:
        return "WARNING"

    else:
        return "SAFE"


# =========================================================
# CONNECT ARDUINO
# =========================================================

print("Connecting to Arduino...")

try:

    arduino = serial.Serial(
        ARDUINO_PORT,
        BAUD_RATE,
        timeout=0.1
    )

    time.sleep(2)

    print("Arduino connected successfully!")

except serial.SerialException:

    print("ERROR: Could not connect to Arduino.")
    print("Make sure Arduino is connected to COM3.")
    exit()


# =========================================================
# START CAMERA
# =========================================================

print("Starting webcam...")

# DirectShow is generally more stable for webcams on Windows.
camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Request a predictable working resolution.
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)

if not camera.isOpened():

    print("ERROR: Could not open webcam.")

    arduino.close()

    exit()


print("Webcam started successfully!")


# =========================================================
# YOLO WORKER DETECTOR
# =========================================================

print("Loading YOLO worker detection model...")

worker_model = YOLO("yolo11n.pt")

print("YOLO worker detection model loaded successfully.")


# =========================================================
# INITIAL VALUES
# =========================================================

gas_value = 0
distance = 0.0
worker_count = 0
zone_intrusion = False
zone_worker_count = 0

previous_status = None

# =========================================================
# YOLO STABILITY SETTINGS
# =========================================================
# Run YOLO every N frames and keep the latest valid detections
# between inference frames. This reduces CPU/GPU load and
# makes the dashboard smoother on laptops.
YOLO_EVERY_N_FRAMES = 2
frame_counter = 0
last_faces = []

# =========================================================
# DANGER ZONE SETTINGS - STAGE 1
# =========================================================
# Percentages of the camera frame. Easy to adjust later.
# Default zone is a smaller lower-middle floor area so the label
# stays visible beside the dashboard cards.
DANGER_ZONE_X1 = 0.25
DANGER_ZONE_Y1 = 0.45
DANGER_ZONE_X2 = 0.80
DANGER_ZONE_Y2 = 0.96

# Small tolerance for YOLO box jitter at the zone boundary.
ZONE_DETECTION_MARGIN = 12


# =========================================================
# START MESSAGE
# =========================================================

print()
print("=" * 60)
print("             SENTINELONE INDUSTRIAL")
print("        FACTORY WORKER SAFETY MONITOR")
print("=" * 60)
print("Monitoring active...")
print("Safety events saved to safety_log.csv")
print("Press Q to quit.")
print()


# =========================================================
# MAIN LOOP
# =========================================================

try:
    while True:

        # =====================================================
        # READ ARDUINO
        # =====================================================

        line = arduino.readline().decode(
            "utf-8",
            errors="ignore"
        ).strip()

        if line:

            match = re.search(
                r"Gas:\s*(\d+)\s*\|\s*Distance:\s*([\d.]+)",
                line
            )

            if match:

                gas_value = int(match.group(1))

                distance = float(
                    match.group(2)
                )


        # =====================================================
        # READ CAMERA
        # =====================================================

        success, frame = camera.read()

        if not success:

            print("ERROR: Could not read webcam.")

            break


        # =====================================================
        # GET FRAME SIZE
        # =====================================================

        height, width = frame.shape[:2]

        # =====================================================
        # DANGER ZONE - FRAME-SCALED COORDINATES
        # =====================================================
        zone_x1 = max(0, min(int(width * DANGER_ZONE_X1), width - 1))
        zone_y1 = max(0, min(int(height * DANGER_ZONE_Y1), height - 1))
        zone_x2 = max(zone_x1 + 1, min(int(width * DANGER_ZONE_X2), width - 1))
        zone_y2 = max(zone_y1 + 1, min(int(height * DANGER_ZONE_Y2), height - 1))


        # =====================================================
        # YOLO WORKER DETECTION
        # =====================================================

        frame_counter += 1

        # Keep the latest detections on frames where YOLO is not run.
        # This makes the UI smoother while preserving worker tracking.
        if frame_counter % YOLO_EVERY_N_FRAMES == 0:

            results = worker_model(
                frame,
                conf=0.45,
                imgsz=640,
                verbose=False
            )

            detected_faces = []

            for result in results:

                for box in result.boxes:

                    class_id = int(box.cls[0])
                    confidence = float(box.conf[0])

                    # COCO class 0 = person
                    if class_id != 0:
                        continue

                    # Ignore extremely weak detections even if the
                    # model/configuration is changed later.
                    if confidence < 0.45:
                        continue

                    x1, y1, x2, y2 = map(
                        int,
                        box.xyxy[0]
                    )

                    # Keep coordinates inside the current frame.
                    x1 = max(0, min(x1, width - 1))
                    y1 = max(0, min(y1, height - 1))
                    x2 = max(0, min(x2, width - 1))
                    y2 = max(0, min(y2, height - 1))

                    box_width = max(1, x2 - x1)
                    box_height = max(1, y2 - y1)

                    detected_faces.append(
                        (x1, y1, box_width, box_height)
                    )

            last_faces = detected_faces

        faces = last_faces
        worker_count = len(faces)

        # =====================================================
        # DANGER ZONE WORKER DETECTION - STAGE 1
        # =====================================================
        # Bottom-center of the YOLO box is used as the worker's
        # standing/foot point.
        zone_intrusion = False
        zone_worker_count = 0

        for (x, y, w, h) in faces:
            foot_x = x + (w // 2)
            foot_y = y + h

            # Expand the logical detection area slightly. This prevents
            # normal YOLO bounding-box jitter from flipping a worker
            # between CLEAR and INTRUSION at the boundary.
            detect_x1 = max(0, zone_x1 - ZONE_DETECTION_MARGIN)
            detect_y1 = max(0, zone_y1 - ZONE_DETECTION_MARGIN)
            detect_x2 = min(width - 1, zone_x2 + ZONE_DETECTION_MARGIN)
            detect_y2 = min(height - 1, zone_y2 + ZONE_DETECTION_MARGIN)

            if (
                detect_x1 <= foot_x <= detect_x2
                and detect_y1 <= foot_y <= detect_y2
            ):
                zone_intrusion = True
                zone_worker_count += 1


        # =====================================================
        # SAFETY STATUS
        # =====================================================

        status = calculate_safety(
            gas_value,
            distance
        )


        # =====================================================
        # LOG WHEN STATUS CHANGES
        # =====================================================

        if previous_status is None:

            log_event(
                gas_value,
                distance,
                worker_count,
                status
            )

            previous_status = status

        elif status != previous_status:

            log_event(
                gas_value,
                distance,
                worker_count,
                status
            )

            previous_status = status


        # =====================================================
        # STATUS COLOR
        # =====================================================

        if status == "SAFE":

            status_color = GREEN

        elif status == "WARNING":

            status_color = ORANGE

        else:

            status_color = RED


        # =====================================================
        # DANGER ZONE OVERLAY - STAGE 1
        # =====================================================

        zone_color = RED if zone_intrusion else GREEN

        if zone_intrusion:
            zone_label = f"DANGER ZONE - {zone_worker_count} WORKER"
            if zone_worker_count != 1:
                zone_label += "S"
        else:
            zone_label = "DANGER ZONE - CLEAR"

        # Light transparent fill.
        overlay = frame.copy()
        cv2.rectangle(
            overlay,
            (zone_x1, zone_y1),
            (zone_x2, zone_y2),
            zone_color,
            -1
        )
        frame = cv2.addWeighted(overlay, 0.10, frame, 0.90, 0)

        # Zone boundary.
        cv2.rectangle(
            frame,
            (zone_x1, zone_y1),
            (zone_x2, zone_y2),
            zone_color,
            3
        )

        # Put the label inside the zone toward the right side.
        # This avoids the large dashboard information cards on the left.
        (label_width, label_height), _ = cv2.getTextSize(
            zone_label,
            cv2.FONT_HERSHEY_SIMPLEX,
            0.50,
            2
        )

        zone_label_x = max(
            zone_x1 + 8,
            zone_x2 - label_width - 10
        )

        zone_label_y = zone_y1 + label_height + 10

        cv2.putText(
            frame,
            zone_label,
            (zone_label_x, zone_label_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.50,
            zone_color,
            2
        )


        # =====================================================
        # YOLO WORKER DETECTION BOX
        # =====================================================

        for (x, y, w, h) in faces:

            foot_x = x + (w // 2)
            foot_y = y + h

            detect_x1 = max(0, zone_x1 - ZONE_DETECTION_MARGIN)
            detect_y1 = max(0, zone_y1 - ZONE_DETECTION_MARGIN)
            detect_x2 = min(width - 1, zone_x2 + ZONE_DETECTION_MARGIN)
            detect_y2 = min(height - 1, zone_y2 + ZONE_DETECTION_MARGIN)

            worker_in_zone = (
                detect_x1 <= foot_x <= detect_x2
                and detect_y1 <= foot_y <= detect_y2
            )

            worker_box_color = RED if worker_in_zone else GREEN
            worker_label = (
                "WORKER IN DANGER ZONE"
                if worker_in_zone
                else "WORKER DETECTED"
            )

            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                worker_box_color,
                3
            )

            # Label background

            label_y1 = max(0, y - 32)

            cv2.rectangle(
                frame,
                (x, label_y1),
                (x + w, y),
                worker_box_color,
                -1
            )

            cv2.putText(
                frame,
                worker_label,
                (x + 5, y - 9),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.48,
                BLACK,
                2
            )


        # =====================================================
        # HEADER
        # =====================================================

        cv2.rectangle(
            frame,
            (0, 0),
            (width, 58),
            DARK,
            -1
        )

        cv2.putText(
            frame,
            "SENTINELONE INDUSTRIAL",
            (22, 39),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.82,
            CYAN,
            2
        )


        # =====================================================
        # PANEL SETTINGS
        # =====================================================

        panel_x1 = 18
        panel_x2 = 305

        panel_height = 62

        gas_y1 = 70
        distance_y1 = 140
        worker_y1 = 210
        safety_y1 = 280


        # =====================================================
        # GAS PANEL
        # =====================================================

        cv2.rectangle(
            frame,
            (panel_x1, gas_y1),
            (panel_x2, gas_y1 + panel_height),
            DARK,
            -1
        )

        cv2.rectangle(
            frame,
            (panel_x1, gas_y1),
            (panel_x2, gas_y1 + panel_height),
            CYAN,
            2
        )

        cv2.putText(
            frame,
            "GAS LEVEL",
            (35, gas_y1 + 25),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            CYAN,
            2
        )

        cv2.putText(
            frame,
            str(gas_value),
            (35, gas_y1 + 52),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.72,
            WHITE,
            2
        )


        # =====================================================
        # DISTANCE PANEL
        # =====================================================

        cv2.rectangle(
            frame,
            (panel_x1, distance_y1),
            (panel_x2, distance_y1 + panel_height),
            DARK,
            -1
        )

        cv2.rectangle(
            frame,
            (panel_x1, distance_y1),
            (panel_x2, distance_y1 + panel_height),
            PURPLE,
            2
        )

        cv2.putText(
            frame,
            "DISTANCE",
            (35, distance_y1 + 25),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            PURPLE,
            2
        )

        cv2.putText(
            frame,
            f"{distance:.2f} cm",
            (35, distance_y1 + 52),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.72,
            WHITE,
            2
        )


        # =====================================================
        # WORKER PANEL
        # =====================================================

        cv2.rectangle(
            frame,
            (panel_x1, worker_y1),
            (panel_x2, worker_y1 + panel_height),
            DARK,
            -1
        )

        cv2.rectangle(
            frame,
            (panel_x1, worker_y1),
            (panel_x2, worker_y1 + panel_height),
            YELLOW,
            2
        )

        cv2.putText(
            frame,
            "WORKERS DETECTED",
            (35, worker_y1 + 25),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.52,
            YELLOW,
            2
        )

        cv2.putText(
            frame,
            str(worker_count),
            (35, worker_y1 + 52),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.72,
            WHITE,
            2
        )


        # =====================================================
        # SAFETY STATUS PANEL
        # =====================================================

        cv2.rectangle(
            frame,
            (panel_x1, safety_y1),
            (panel_x2, safety_y1 + panel_height),
            DARK,
            -1
        )

        cv2.rectangle(
            frame,
            (panel_x1, safety_y1),
            (panel_x2, safety_y1 + panel_height),
            status_color,
            3
        )

        cv2.putText(
            frame,
            "SAFETY STATUS",
            (35, safety_y1 + 25),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.52,
            status_color,
            2
        )

        cv2.putText(
            frame,
            status,
            (35, safety_y1 + 53),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.72,
            status_color,
            2
        )


        # =====================================================
        # BOTTOM STATUS BAR
        # =====================================================

        bottom_height = 38

        bottom_y = height - bottom_height

        cv2.rectangle(
            frame,
            (0, bottom_y),
            (width, height),
            DARK,
            -1
        )

        cv2.putText(
            frame,
            "SYSTEM: OPERATIONAL",
            (18, height - 13),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.45,
            GREEN,
            2
        )

        cv2.putText(
            frame,
            "MONITORING ACTIVE",
            (230, height - 13),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.45,
            CYAN,
            2
        )

        cv2.putText(
            frame,
            "Q = EXIT",
            (width - 85, height - 13),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.45,
            WHITE,
            2
        )


        # =====================================================
        # SHOW DASHBOARD
        # =====================================================

        cv2.imshow(
            "SentinelOne Industrial",
            frame
        )


        # =====================================================
        # TERMINAL OUTPUT
        # =====================================================

        print(
            f"Gas: {gas_value:3d} | "
            f"Distance: {distance:6.2f} cm | "
            f"Workers: {worker_count} | "
            f"Status: {status}"
        )


        # =====================================================
        # QUIT
        # =====================================================

        if cv2.waitKey(1) & 0xFF == ord("q"):

            break

# =========================================================
# CLEANUP
# =========================================================

finally:
    camera.release()
    arduino.close()

    cv2.destroyAllWindows()

    print()
    print("SentinelOne Industrial stopped.")
    print(f"Safety log saved to: {LOG_FILE}")