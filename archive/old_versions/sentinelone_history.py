import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# ============================================================
# SENTINELONE INDUSTRIAL - SAFETY HISTORY & ANALYTICS
# ============================================================

LOG_FILE = Path("safety_log.csv")


# ============================================================
# LOAD CSV
# ============================================================

def load_safety_log():

    if not LOG_FILE.exists():
        print("\nERROR: safety_log.csv not found!")
        return None

    try:
        df = pd.read_csv(LOG_FILE)

        if df.empty:
            print("\nSafety log is empty.")
            return None

        return df

    except Exception as e:
        print(f"\nERROR reading safety_log.csv: {e}")
        return None


# ============================================================
# DISPLAY STATISTICS
# ============================================================

def display_statistics(df):

    print("\n")
    print("=" * 60)
    print("       SENTINELONE INDUSTRIAL")
    print("       SAFETY HISTORY & ANALYTICS")
    print("=" * 60)

    # Safety event counts
    total_events = len(df)

    safe_events = (df["Safety Status"] == "SAFE").sum()
    warning_events = (df["Safety Status"] == "WARNING").sum()
    danger_events = (df["Safety Status"] == "DANGER").sum()

    print("\nSAFETY EVENTS")
    print("-" * 60)

    print(f"Total Events   : {total_events}")
    print(f"SAFE Events    : {safe_events}")
    print(f"WARNING Events : {warning_events}")
    print(f"DANGER Events  : {danger_events}")

    # Gas statistics
    print("\nGAS SENSOR")
    print("-" * 60)

    print(f"Maximum Gas    : {df['Gas Level'].max():.2f}")
    print(f"Minimum Gas    : {df['Gas Level'].min():.2f}")
    print(f"Average Gas    : {df['Gas Level'].mean():.2f}")

    # Distance statistics
    print("\nULTRASONIC SENSOR")
    print("-" * 60)

    print(f"Maximum Distance : {df['Distance (cm)'].max():.2f} cm")
    print(f"Minimum Distance : {df['Distance (cm)'].min():.2f} cm")
    print(f"Average Distance : {df['Distance (cm)'].mean():.2f} cm")

    # Worker statistics
    print("\nWORKER DETECTION")
    print("-" * 60)

    print(f"Maximum Workers : {df['Workers'].max()}")
    print(f"Average Workers : {df['Workers'].mean():.2f}")

    print("\n" + "=" * 60)


# ============================================================
# SAFETY EVENT GRAPH
# ============================================================

def plot_safety_events(df):

    statuses = ["SAFE", "WARNING", "DANGER"]

    counts = [
        (df["Safety Status"] == "SAFE").sum(),
        (df["Safety Status"] == "WARNING").sum(),
        (df["Safety Status"] == "DANGER").sum()
    ]

    plt.figure(figsize=(8, 5))

    plt.bar(statuses, counts)

    plt.title("SentinelOne Safety Event Distribution")
    plt.xlabel("Safety Status")
    plt.ylabel("Number of Events")

    plt.grid(axis="y", linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.show()


# ============================================================
# GAS LEVEL HISTORY
# ============================================================

def plot_gas_history(df):

    plt.figure(figsize=(10, 5))

    plt.plot(
        range(len(df)),
        df["Gas Level"],
        marker="o",
        label="Gas Level"
    )

    # Warning threshold
    plt.axhline(
        y=70,
        linestyle="--",
        label="Warning Threshold (70)"
    )

    # Danger threshold
    plt.axhline(
        y=150,
        linestyle="--",
        label="Danger Threshold (150)"
    )

    plt.title("Gas Level History")
    plt.xlabel("Logged Event")
    plt.ylabel("Gas Level")

    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()


# ============================================================
# DISTANCE HISTORY
# ============================================================

def plot_distance_history(df):

    plt.figure(figsize=(10, 5))

    plt.plot(
        range(len(df)),
        df["Distance (cm)"],
        marker="o",
        label="Distance"
    )

    # Warning threshold
    plt.axhline(
        y=20,
        linestyle="--",
        label="Warning Threshold (20 cm)"
    )

    # Danger threshold
    plt.axhline(
        y=10,
        linestyle="--",
        label="Danger Threshold (10 cm)"
    )

    plt.title("Distance History")
    plt.xlabel("Logged Event")
    plt.ylabel("Distance (cm)")

    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()


# ============================================================
# MAIN
# ============================================================

def main():

    print("\nLoading SentinelOne safety history...")

    df = load_safety_log()

    if df is None:
        return

    display_statistics(df)

    print("\nOpening Safety Event graph...")
    plot_safety_events(df)

    print("Opening Gas Level graph...")
    plot_gas_history(df)

    print("Opening Distance graph...")
    plot_distance_history(df)

    print("\nAnalytics completed successfully.")


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":
    main()