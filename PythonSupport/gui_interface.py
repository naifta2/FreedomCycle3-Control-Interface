import time
import tkinter as tk
from PythonSupport.config import Config, Widget
from PythonSupport.arduino_interface import connect_arduino, disconnect_arduino, read_arduino
from PythonSupport.data_acquisition import initialize_session, start_collection, stop_collection, collect_data, save_data

def initialize_interface(window):
    """Initializes the interface layout, including the persistent widgets."""
    
    # Persistent frame for widgets that stay across screens (e.g., connection status)
    Config.persistent_frame = tk.Frame(window)
    Config.persistent_frame.pack(side="top", fill="x")

    # Persistent widget: Arduino connection status label
    Config.connection_status = tk.Label(Config.persistent_frame, text="Checking Arduino...", bg="yellow", font=("Helvetica", 12))
    Config.connection_status.pack(side="left", padx=20, pady=5)

    # Main content frame for screen-specific content
    Config.main_content_frame = tk.Frame(window)
    Config.main_content_frame.pack(expand=True, fill="both")

    # Start with the welcome screen
    setup_welcome_screen(window)

def setup_welcome_screen(window):
    """Sets up the welcome screen content in the main content frame."""
    # Clear the main content frame
    for widget in Config.main_content_frame.winfo_children():
        widget.destroy()

    Config.is_welcome_screen = True

    # Welcome screen content
    welcome_label = Widget.create(Config.main_content_frame, tk.Label, text="Welcome to FreedomCycle3 Interface", font=("Helvetica", 16))
    welcome_label.pack(anchor="center", pady=20)

    Config.start_session_button = Widget.create(Config.main_content_frame, tk.Button, text="Start Work Session", font=("Helvetica", 14), command=lambda: start_work_session(window))
    Config.start_session_button.pack(anchor="center", pady=10)
    Config.start_session_button.config(state="disabled")

    close_button = Widget.create(Config.main_content_frame, tk.Button, text="Close Program", font=("Helvetica", 14), command=window.destroy)
    close_button.pack(anchor="center", pady=10)

    continuous_check_arduino_connection(window)

def continuous_check_arduino_connection(window):
    """Checks Arduino connection and updates the persistent connection status label."""
    if Config.is_welcome_screen:
        if Config.arduino or connect_arduino():
            Config.connection_status.config(bg="green", text="Arduino Connected")
            Config.start_session_button.config(state="normal")
            print("GUI: Arduino connected")
        else:
            Config.connection_status.config(bg="red", text="No Arduino Connected")
            Config.start_session_button.config(state="disabled")
            print("GUI: No Arduino Connected")
    Config.connection_status.after(1000, lambda: continuous_check_arduino_connection(window))

def start_work_session(window):
    """Starts a new work session and sets up the session screen."""
    Config.is_welcome_screen = False
    initialize_session()
    show_session_screen(window)

def show_session_screen(window):
    """Sets up the session screen content in the main content frame."""
    # Clear the main content frame
    for widget in Config.main_content_frame.winfo_children():
        widget.destroy()

    # Session screen content
    Config.flowrate_label = tk.Label(Config.main_content_frame, text="Current Flow Rate: --- L/min", font=("Helvetica", 14))
    Config.flowrate_label.pack(anchor="center", pady=10)

    Config.start_button = tk.Button(Config.main_content_frame, text="Start Collection", font=("Helvetica", 14), command=start_collection_handler)
    Config.start_button.pack(anchor="center", pady=10)

    stop_button = tk.Button(Config.main_content_frame, text="Stop Session", font=("Helvetica", 14), command=lambda: stop_work_session(window))
    stop_button.pack(anchor="center", pady=10)

    update_flowrate(window)  # Start the flow rate update loop

def start_collection_handler():
    """Handles start/stop collection toggling."""
    if Config.collecting_data:
        stop_collection()
        save_data()
        Config.start_button.config(text="Start Collection")
    else:
        start_collection()
        Config.start_button.config(text="Stop Collection")

def update_flowrate(window):
    """Updates the flow rate label with data from Arduino."""
    flowrate = read_arduino()
    timestamp = time.time()  # Precise timestamp for each reading

    if Config.flowrate_label:  
        Config.flowrate_label.config(text=f"Current Flow Rate: {flowrate} L/min")
        if Config.collecting_data:
            # Log each data point with the precise timestamp
            collect_data(flowrate, timestamp)

    # Schedule the next update sooner to improve responsiveness
    Config.after_id = window.after(250, lambda: update_flowrate(window))

def stop_work_session(window):
    """Ends the work session and returns to the welcome screen."""
    if Config.collecting_data:
        stop_collection()
        save_data()
    if Config.after_id is not None:
        window.after_cancel(Config.after_id)
    show_welcome_screen(window)

def show_welcome_screen(window):
    """Returns to the welcome screen content in the main content frame."""
    Config.is_welcome_screen = True
    if Config.after_id is not None:
        window.after_cancel(Config.after_id)
    setup_welcome_screen(window)
