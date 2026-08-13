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

camera = cv2.VideoCapture(0)

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

previous_status = None


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
    # YOLO WORKER DETECTION
    # =====================================================

    # YOLO tracking makes the worker boxes and count much more stable
    # than running independent detection on every frame.
    results = worker_model.track(
        frame,
        persist=True,
        conf=0.50,
        classes=[0],
        verbose=False
    )

    # Keep the existing (x, y, w, h) format so the rest of the
    # dashboard code does not need to be rewritten.
    faces = []

    for result in results:

        if result.boxes is None:
            continue

        for box in result.boxes:

            class_id = int(box.cls[0])
            confidence = float(box.conf[0])

            # COCO class 0 = person
            if class_id != 0 or confidence < 0.50:
                continue

            x1, y1, x2, y2 = map(
                int,
                box.xyxy[0]
            )

            box_width = x2 - x1
            box_height = y2 - y1

            # Ignore extremely small detections that usually cause
            # flickering false worker counts.
            if box_width < 45 or box_height < 80:
                continue

            faces.append(
                (x1, y1, box_width, box_height)
            )

    worker_count = len(faces)


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
    # YOLO WORKER DETECTION BOX
    # =====================================================

    for (x, y, w, h) in faces:

        # Green detection box

        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            GREEN,
            3
        )

        # Compact fixed-size label so it does not stretch across
        # the entire worker bounding box.
        label_width = 170
        label_height = 30
        label_y1 = max(0, y - label_height)
        label_x2 = min(width, x + label_width)

        cv2.rectangle(
            frame,
            (x, label_y1),
            (label_x2, y),
            GREEN,
            -1
        )

        cv2.putText(
            frame,
            "WORKER",
            (x + 8, y - 9),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.50,
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

camera.release()
arduino.close()

cv2.destroyAllWindows()

print()
print("SentinelOne Industrial stopped.")
print(f"Safety log saved to: {LOG_FILE}")