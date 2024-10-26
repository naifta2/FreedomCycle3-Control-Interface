import time
import tkinter as tk
from config import Config
from arduino_interface import connect_arduino, disconnect_arduino, read_arduino
from data_acquisition import initialize_session, start_collection, stop_collection, collect_data, save_data

# Global variable to store the after() ID for flowrate updates
after_id = None

def setup_welcome_screen(root):
    Config.is_welcome_screen = True

    Config.connection_status = tk.Label(root, text="Checking Arduino...", bg="yellow", font=("Helvetica", 12))
    Config.connection_status.pack(pady=10)

    Config.start_session_button = tk.Button(root, text="Start Work Session", font=("Helvetica", 14), command=lambda: start_work_session(root))
    Config.start_session_button.pack(pady=10)
    Config.start_session_button.config(state="disabled")

    close_button = tk.Button(root, text="Close Program", font=("Helvetica", 14), command=root.destroy)
    close_button.pack(pady=10)

    continuous_check_arduino_connection(root)

def continuous_check_arduino_connection(root):
    if Config.is_welcome_screen:
        if Config.arduino or connect_arduino():
            if Config.connection_status:
                Config.connection_status.config(bg="green", text="Arduino Connected")
            if Config.start_session_button:
                Config.start_session_button.config(state="normal")
            print("GUI: Arduino connected")
        else:
            if Config.connection_status:
                Config.connection_status.config(bg="red", text="No Arduino Connected")
            if Config.start_session_button:
                Config.start_session_button.config(state="disabled")
            print("GUI: No Arduino Connected")

    root.after(1000, lambda: continuous_check_arduino_connection(root))

def start_work_session(root):
    global after_id  
    Config.is_welcome_screen = False
    initialize_session()
    show_session_screen(root)

def show_session_screen(root):
    global after_id  
    if after_id is not None:
        root.after_cancel(after_id)
    for widget in root.winfo_children():
        widget.destroy()

    Config.flowrate_label = tk.Label(root, text="Current Flow Rate: --- L/min", font=("Helvetica", 14))
    Config.flowrate_label.pack(pady=10)

    Config.start_button = tk.Button(root, text="Start Collection", font=("Helvetica", 14), command=start_collection_handler)
    Config.start_button.pack(pady=10)

    stop_button = tk.Button(root, text="Stop Session", font=("Helvetica", 14), command=lambda: stop_work_session(root))
    stop_button.pack(pady=10)

    update_flowrate(root)  # Start the flow rate update loop

def start_collection_handler():
    if Config.collecting_data:
        stop_collection()
        save_data()
        Config.start_button.config(text="Start Collection")
    else:
        start_collection()
        Config.start_button.config(text="Stop Collection")

def update_flowrate(root):
    global after_id  
    flowrate = read_arduino()
    timestamp = time.time()  # Precise timestamp for each reading

    if Config.flowrate_label and flowrate:  
        Config.flowrate_label.config(text=f"Current Flow Rate: {flowrate} L/min")
        if Config.collecting_data:
            # Log each data point with the precise timestamp
            collect_data(flowrate, timestamp)

    # Schedule the next update sooner to improve responsiveness
    if Config.flowrate_label:
        after_id = root.after(250, lambda: update_flowrate(root))

def stop_work_session(root):
    global after_id  
    if Config.collecting_data:
        stop_collection()
        save_data()
    if after_id is not None:
        root.after_cancel(after_id)
    show_welcome_screen(root)

def show_welcome_screen(root):
    global after_id  
    Config.is_welcome_screen = True
    if after_id is not None:
        root.after_cancel(after_id)
    for widget in root.winfo_children():
        widget.destroy()
    setup_welcome_screen(root)
