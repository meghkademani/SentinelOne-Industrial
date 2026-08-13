import serial
import time
import re

# ==========================================
# SENTINELONE INDUSTRIAL
# Safety Monitoring System
# ==========================================

# Arduino settings
ARDUINO_PORT = "COM3"
BAUD_RATE = 9600

# ==========================================
# PROTOTYPE SAFETY THRESHOLDS
# ==========================================

# Gas sensor raw ADC values
GAS_WARNING = 70
GAS_DANGER = 150

# Distance in centimeters
DISTANCE_WARNING = 20
DISTANCE_DANGER = 10


# ==========================================
# CONNECT TO ARDUINO
# ==========================================

arduino = serial.Serial(
    ARDUINO_PORT,
    BAUD_RATE,
    timeout=1
)

time.sleep(2)

print("=" * 55)
print("             SENTINELONE INDUSTRIAL")
print("        FACTORY WORKER SAFETY MONITOR")
print("=" * 55)
print("Arduino connected successfully!")
print("Safety monitoring started...\n")


# ==========================================
# SAFETY ENGINE
# ==========================================

def calculate_safety(gas, distance):

    # Check gas conditions
    gas_danger = gas > GAS_DANGER
    gas_warning = gas > GAS_WARNING

    # Check distance conditions
    distance_danger = distance <= DISTANCE_DANGER
    distance_warning = distance <= DISTANCE_WARNING

    # -----------------------------
    # DANGER
    # -----------------------------
    if gas_danger or distance_danger:
        return "DANGER"

    # -----------------------------
    # WARNING
    # -----------------------------
    elif gas_warning or distance_warning:
        return "WARNING"

    # -----------------------------
    # SAFE
    # -----------------------------
    else:
        return "SAFE"


# ==========================================
# MAIN MONITORING LOOP
# ==========================================

while True:

    try:

        # Read Arduino data
        line = arduino.readline().decode("utf-8").strip()

        if line:

            # Expected Arduino format:
            # Gas: 65 | Distance: 30.42 cm

            match = re.search(
                r"Gas:\s*(\d+)\s*\|\s*Distance:\s*([\d.]+)",
                line
            )

            if match:

                # Convert received text into numbers
                gas_value = int(match.group(1))
                distance = float(match.group(2))

                # Calculate safety status
                status = calculate_safety(
                    gas_value,
                    distance
                )

                # ==================================
                # DISPLAY
                # ==================================

                print("-" * 55)

                print(f"Gas Level     : {gas_value}")
                print(f"Distance      : {distance:.2f} cm")
                print(f"Safety Status : {status}")

    except KeyboardInterrupt:

        print("\n")
        print("=" * 55)
        print("SentinelOne Industrial stopped.")
        print("=" * 55)

        arduino.close()

        break