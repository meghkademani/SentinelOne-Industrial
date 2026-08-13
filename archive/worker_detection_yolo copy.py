import cv2
from ultralytics import YOLO


# ============================================================
# SENTINELONE INDUSTRIAL
# YOLO WORKER DETECTION TEST
# ============================================================

print("Loading YOLO model...")

model = YOLO("yolo11n.pt")

print("YOLO model loaded successfully.")


# ============================================================
# CAMERA
# ============================================================

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("ERROR: Could not open webcam.")
    exit()


# ============================================================
# PERSON CLASS
# COCO CLASS 0 = PERSON
# ============================================================

PERSON_CLASS = 0


print("Starting worker detection...")
print("Press Q to exit.")


# ============================================================
# MAIN LOOP
# ============================================================

while True:

    ret, frame = cap.read()

    if not ret:
        print("ERROR: Could not read webcam frame.")
        break


    # --------------------------------------------------------
    # YOLO DETECTION
    # --------------------------------------------------------

    results = model(
        frame,
        conf=0.45,
        verbose=False
    )


    worker_count = 0


    # --------------------------------------------------------
    # PROCESS DETECTIONS
    # --------------------------------------------------------

    for result in results:

        boxes = result.boxes

        for box in boxes:

            class_id = int(
                box.cls[0]
            )

            confidence = float(
                box.conf[0]
            )


            # Only detect PERSON
            if class_id != PERSON_CLASS:
                continue


            worker_count += 1


            # Bounding box
            x1, y1, x2, y2 = map(
                int,
                box.xyxy[0]
            )


            # Draw bounding box
            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )


            # Label
            label = (
                f"WORKER "
                f"{confidence * 100:.0f}%"
            )


            cv2.putText(
                frame,
                label,
                (x1, max(y1 - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )


    # ========================================================
    # WORKER COUNT
    # ========================================================

    cv2.rectangle(
        frame,
        (15, 15),
        (300, 65),
        (20, 20, 20),
        -1
    )


    cv2.putText(
        frame,
        f"WORKERS DETECTED: {worker_count}",
        (25, 48),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 255),
        2
    )


    # ========================================================
    # DISPLAY
    # ========================================================

    cv2.imshow(
        "SentinelOne - YOLO Worker Detection",
        frame
    )


    # ========================================================
    # EXIT
    # ========================================================

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break


# ============================================================
# CLEANUP
# ============================================================

cap.release()

cv2.destroyAllWindows()

print("YOLO worker detection stopped.")