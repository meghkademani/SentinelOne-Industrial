import tkinter as tk
from tkinter import messagebox, ttk
from pathlib import Path

import pandas as pd

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# ============================================================
# SENTINELONE INDUSTRIAL
# SAFETY HISTORY & ANALYTICS DASHBOARD
# ============================================================

LOG_FILE = Path("safety_log.csv")


# ============================================================
# COLORS
# ============================================================

BG_COLOR = "#111111"
PANEL_COLOR = "#1c1c1c"

CYAN = "#00e5ff"
GREEN = "#00ff33"
YELLOW = "#ffd900"
RED = "#ff3030"
MAGENTA = "#d946ef"

WHITE = "#ffffff"
GRAY = "#aaaaaa"


# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()

root.title(
    "SentinelOne Industrial - Safety Analytics"
)

root.geometry("1150x750")

root.minsize(1000, 650)

root.configure(
    bg=BG_COLOR
)


# ============================================================
# TITLE
# ============================================================

title = tk.Label(
    root,
    text="SENTINELONE INDUSTRIAL",
    font=("Consolas", 22, "bold"),
    fg=CYAN,
    bg=BG_COLOR
)

title.pack(
    pady=(10, 0)
)


subtitle = tk.Label(
    root,
    text="SAFETY HISTORY & ANALYTICS",
    font=("Consolas", 11),
    fg=WHITE,
    bg=BG_COLOR
)

subtitle.pack(
    pady=(0, 5)
)


# ============================================================
# STATISTICS FRAME
# ============================================================

stats_frame = tk.Frame(
    root,
    bg=BG_COLOR
)

stats_frame.pack(
    fill="x",
    padx=15,
    pady=4
)


# ============================================================
# STATISTIC CARD FUNCTION
# ============================================================

def create_card(parent, title_text, color):

    card = tk.Frame(
        parent,
        bg=PANEL_COLOR,
        highlightbackground=color,
        highlightthickness=2
    )

    card.pack(
        side="left",
        expand=True,
        fill="both",
        padx=4
    )

    title_label = tk.Label(
        card,
        text=title_text,
        font=("Consolas", 9, "bold"),
        fg=color,
        bg=PANEL_COLOR
    )

    title_label.pack(
        pady=(6, 1)
    )

    value_label = tk.Label(
        card,
        text="0",
        font=("Consolas", 17, "bold"),
        fg=WHITE,
        bg=PANEL_COLOR
    )

    value_label.pack(
        pady=(0, 6)
    )

    return value_label


# ============================================================
# CREATE CARDS
# ============================================================

total_label = create_card(
    stats_frame,
    "TOTAL EVENTS",
    CYAN
)

safe_label = create_card(
    stats_frame,
    "SAFE",
    GREEN
)

warning_label = create_card(
    stats_frame,
    "WARNING",
    YELLOW
)

danger_label = create_card(
    stats_frame,
    "DANGER",
    RED
)

avg_gas_label = create_card(
    stats_frame,
    "AVG GAS",
    CYAN
)

avg_distance_label = create_card(
    stats_frame,
    "AVG DISTANCE",
    CYAN
)

avg_workers_label = create_card(
    stats_frame,
    "AVG WORKERS",
    CYAN
)


# ============================================================
# MATPLOTLIB FIGURE
# ============================================================

figure = Figure(
    figsize=(10, 5.5),
    dpi=90,
    facecolor=BG_COLOR
)


ax_gas = figure.add_subplot(2, 2, 1)

ax_distance = figure.add_subplot(2, 2, 2)

ax_events = figure.add_subplot(2, 2, 3)

ax_workers = figure.add_subplot(2, 2, 4)


# ============================================================
# GRAPH CANVAS
# ============================================================

canvas = FigureCanvasTkAgg(
    figure,
    master=root
)

canvas.get_tk_widget().pack(
    fill="both",
    expand=True,
    padx=15,
    pady=5
)


# ============================================================
# EVENT HISTORY FRAME
# ============================================================

history_frame = tk.Frame(
    root,
    bg=BG_COLOR
)

history_frame.pack(
    fill="x",
    padx=15,
    pady=4
)


history_title = tk.Label(
    history_frame,
    text="RECENT SAFETY EVENTS",
    font=("Consolas", 10, "bold"),
    fg=CYAN,
    bg=BG_COLOR
)

history_title.pack(
    anchor="w",
    pady=(0, 3)
)


# ============================================================
# TABLE CONTAINER
# ============================================================

table_container = tk.Frame(
    history_frame,
    bg=PANEL_COLOR
)

table_container.pack(
    fill="x"
)


# ============================================================
# TABLE STYLE
# ============================================================

style = ttk.Style()

style.theme_use("clam")

style.configure(
    "Treeview",
    background=PANEL_COLOR,
    foreground=WHITE,
    fieldbackground=PANEL_COLOR,
    rowheight=22,
    font=("Consolas", 8)
)

style.configure(
    "Treeview.Heading",
    background="#252525",
    foreground=CYAN,
    font=("Consolas", 8, "bold")
)

style.map(
    "Treeview",
    background=[
        ("selected", "#333333")
    ],
    foreground=[
        ("selected", WHITE)
    ]
)


# ============================================================
# TABLE
# ============================================================

columns = (
    "Timestamp",
    "Gas Level",
    "Distance",
    "Workers",
    "Safety Status"
)

tree = ttk.Treeview(
    table_container,
    columns=columns,
    show="headings",
    height=4
)


# ============================================================
# TABLE HEADINGS
# ============================================================

tree.heading(
    "Timestamp",
    text="TIMESTAMP"
)

tree.heading(
    "Gas Level",
    text="GAS LEVEL"
)

tree.heading(
    "Distance",
    text="DISTANCE"
)

tree.heading(
    "Workers",
    text="WORKERS"
)

tree.heading(
    "Safety Status",
    text="SAFETY STATUS"
)


# ============================================================
# COLUMN WIDTHS
# ============================================================

tree.column(
    "Timestamp",
    width=220,
    anchor="center"
)

tree.column(
    "Gas Level",
    width=130,
    anchor="center"
)

tree.column(
    "Distance",
    width=150,
    anchor="center"
)

tree.column(
    "Workers",
    width=120,
    anchor="center"
)

tree.column(
    "Safety Status",
    width=180,
    anchor="center"
)


# ============================================================
# SCROLLBAR
# ============================================================

scrollbar = ttk.Scrollbar(
    table_container,
    orient="vertical",
    command=tree.yview
)

tree.configure(
    yscrollcommand=scrollbar.set
)


tree.pack(
    side="left",
    fill="x",
    expand=True
)

scrollbar.pack(
    side="right",
    fill="y"
)


# ============================================================
# LOAD DATA
# ============================================================

def load_data():

    if not LOG_FILE.exists():

        messagebox.showerror(
            "SentinelOne Error",
            "safety_log.csv was not found."
        )

        return None

    try:

        df = pd.read_csv(LOG_FILE)

        if df.empty:

            messagebox.showwarning(
                "SentinelOne",
                "The safety log is empty."
            )

            return None

        return df

    except Exception as error:

        messagebox.showerror(
            "CSV Error",
            f"Unable to read safety_log.csv\n\n{error}"
        )

        return None


# ============================================================
# UPDATE HISTORY TABLE
# ============================================================

def update_history_table(df):

    # Remove old rows
    for item in tree.get_children():

        tree.delete(item)


    # Show newest events first
    recent_df = df.tail(50).iloc[::-1]


    for _, row in recent_df.iterrows():

        status = str(
            row["Safety Status"]
        )

        item = tree.insert(
            "",
            "end",
            values=(
                row["Timestamp"],
                row["Gas Level"],
                f"{row['Distance (cm)']:.2f} cm",
                row["Workers"],
                status
            )
        )


# ============================================================
# UPDATE DASHBOARD
# ============================================================

def update_dashboard():

    df = load_data()

    if df is None:
        return


    # ========================================================
    # STATISTICS
    # ========================================================

    total_events = len(df)

    safe_events = (
        df["Safety Status"] == "SAFE"
    ).sum()

    warning_events = (
        df["Safety Status"] == "WARNING"
    ).sum()

    danger_events = (
        df["Safety Status"] == "DANGER"
    ).sum()

    average_gas = df["Gas Level"].mean()

    average_distance = df["Distance (cm)"].mean()

    average_workers = df["Workers"].mean()


    # ========================================================
    # UPDATE CARDS
    # ========================================================

    total_label.config(
        text=str(total_events)
    )

    safe_label.config(
        text=str(safe_events)
    )

    warning_label.config(
        text=str(warning_events)
    )

    danger_label.config(
        text=str(danger_events)
    )

    avg_gas_label.config(
        text=f"{average_gas:.1f}"
    )

    avg_distance_label.config(
        text=f"{average_distance:.1f} cm"
    )

    avg_workers_label.config(
        text=f"{average_workers:.1f}"
    )


    # ========================================================
    # UPDATE TABLE
    # ========================================================

    update_history_table(df)


    # ========================================================
    # CLEAR GRAPHS
    # ========================================================

    ax_gas.clear()

    ax_distance.clear()

    ax_events.clear()

    ax_workers.clear()


    # ========================================================
    # GAS GRAPH
    # ========================================================

    ax_gas.set_facecolor(
        PANEL_COLOR
    )

    ax_gas.plot(
        range(len(df)),
        df["Gas Level"],
        marker="o",
        linewidth=1.8,
        color=CYAN,
        label="Gas Level"
    )

    ax_gas.axhline(
        70,
        linestyle="--",
        color=YELLOW,
        linewidth=1,
        label="Warning 70"
    )

    ax_gas.axhline(
        150,
        linestyle="--",
        color=RED,
        linewidth=1,
        label="Danger 150"
    )

    ax_gas.set_title(
        "Gas Level History",
        color=WHITE,
        fontsize=10
    )

    ax_gas.set_xlabel(
        "Logged Event",
        color=GRAY,
        fontsize=8
    )

    ax_gas.set_ylabel(
        "Gas Level",
        color=GRAY,
        fontsize=8
    )

    ax_gas.tick_params(
        colors=GRAY,
        labelsize=7
    )

    ax_gas.grid(
        True,
        linestyle="--",
        alpha=0.25
    )

    ax_gas.legend(
        fontsize=7
    )


    # ========================================================
    # DISTANCE GRAPH
    # ========================================================

    ax_distance.set_facecolor(
        PANEL_COLOR
    )

    ax_distance.plot(
        range(len(df)),
        df["Distance (cm)"],
        marker="o",
        linewidth=1.8,
        color=MAGENTA,
        label="Distance"
    )

    ax_distance.axhline(
        20,
        linestyle="--",
        color=YELLOW,
        linewidth=1,
        label="Warning 20 cm"
    )

    ax_distance.axhline(
        10,
        linestyle="--",
        color=RED,
        linewidth=1,
        label="Danger 10 cm"
    )

    ax_distance.set_title(
        "Distance History",
        color=WHITE,
        fontsize=10
    )

    ax_distance.set_xlabel(
        "Logged Event",
        color=GRAY,
        fontsize=8
    )

    ax_distance.set_ylabel(
        "Distance (cm)",
        color=GRAY,
        fontsize=8
    )

    ax_distance.tick_params(
        colors=GRAY,
        labelsize=7
    )

    ax_distance.grid(
        True,
        linestyle="--",
        alpha=0.25
    )

    ax_distance.legend(
        fontsize=7
    )


    # ========================================================
    # SAFETY EVENTS
    # ========================================================

    ax_events.set_facecolor(
        PANEL_COLOR
    )

    statuses = [
        "SAFE",
        "WARNING",
        "DANGER"
    ]

    counts = [
        safe_events,
        warning_events,
        danger_events
    ]

    bars = ax_events.bar(
        statuses,
        counts,
        color=[
            GREEN,
            YELLOW,
            RED
        ]
    )

    ax_events.set_title(
        "Safety Event Distribution",
        color=WHITE,
        fontsize=10
    )

    ax_events.set_xlabel(
        "Safety Status",
        color=GRAY,
        fontsize=8
    )

    ax_events.set_ylabel(
        "Events",
        color=GRAY,
        fontsize=8
    )

    ax_events.tick_params(
        colors=GRAY,
        labelsize=7
    )

    ax_events.grid(
        axis="y",
        linestyle="--",
        alpha=0.25
    )


    for bar, value in zip(
        bars,
        counts
    ):

        ax_events.text(
            bar.get_x() +
            bar.get_width() / 2,

            bar.get_height() + 0.1,

            str(value),

            ha="center",

            color=WHITE,

            fontsize=9,

            fontweight="bold"
        )


    # ========================================================
    # WORKER GRAPH
    # ========================================================

    ax_workers.set_facecolor(
        PANEL_COLOR
    )

    ax_workers.plot(
        range(len(df)),
        df["Workers"],
        marker="o",
        linewidth=1.8,
        color=YELLOW,
        label="Workers"
    )

    ax_workers.set_title(
        "Workers Detected",
        color=WHITE,
        fontsize=10
    )

    ax_workers.set_xlabel(
        "Logged Event",
        color=GRAY,
        fontsize=8
    )

    ax_workers.set_ylabel(
        "Workers",
        color=GRAY,
        fontsize=8
    )

    ax_workers.tick_params(
        colors=GRAY,
        labelsize=7
    )

    ax_workers.grid(
        True,
        linestyle="--",
        alpha=0.25
    )

    ax_workers.legend(
        fontsize=7
    )


    # ========================================================
    # REDRAW
    # ========================================================

    figure.tight_layout(
        pad=2
    )

    canvas.draw()


    # ========================================================
    # STATUS
    # ========================================================

    status_label.config(
        text="DATA UPDATED SUCCESSFULLY",
        fg=GREEN
    )

    root.after(
        2500,
        lambda: status_label.config(
            text="READY",
            fg=CYAN
        )
    )


# ============================================================
# CONTROL PANEL
# ============================================================

control_frame = tk.Frame(
    root,
    bg=BG_COLOR
)

control_frame.pack(
    fill="x",
    padx=15,
    pady=3
)


# ============================================================
# REFRESH BUTTON
# ============================================================

refresh_button = tk.Button(
    control_frame,
    text="REFRESH DATA",
    command=update_dashboard,
    font=("Consolas", 10, "bold"),
    fg=BG_COLOR,
    bg=CYAN,
    activeforeground=BG_COLOR,
    activebackground=WHITE,
    padx=18,
    pady=5,
    relief="flat",
    cursor="hand2"
)

refresh_button.pack(
    side="left"
)


# ============================================================
# STATUS LABEL
# ============================================================

status_label = tk.Label(
    control_frame,
    text="READY",
    font=("Consolas", 9, "bold"),
    fg=CYAN,
    bg=BG_COLOR
)

status_label.pack(
    side="left",
    padx=15
)


# ============================================================
# FOOTER
# ============================================================

footer = tk.Label(
    root,
    text="SENTINELONE INDUSTRIAL  |  ANALYTICS MODE  |  safety_log.csv",
    font=("Consolas", 8, "bold"),
    fg=GREEN,
    bg=BG_COLOR
)

footer.pack(
    pady=(2, 5)
)


# ============================================================
# INITIAL LOAD
# ============================================================

update_dashboard()


# ============================================================
# START
# ============================================================

root.mainloop()