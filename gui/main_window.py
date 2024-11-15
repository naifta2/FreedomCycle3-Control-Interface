# gui/main_window.py

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import logging
from communication.sensor_manager import SensorManager
from communication.arduino_interface import ArduinoConnection
from data.data_acquisition import DataAcquisition
from config.settings import WINDOW_TITLE, WINDOW_SIZE, ASSETS_DIR, AUTO
from gui.widgets import LabeledValue, StatusBar
from gui.themes import apply_theme
from utils.helpers import resource_path

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(WINDOW_TITLE)
        self.geometry(WINDOW_SIZE)
        self.configure(bg='white')
        self.style = ttk.Style(self)
        apply_theme(self.style)
        self.logger = logging.getLogger(__name__)
        self.selected_port = tk.StringVar()
        self.arduino_connected = tk.BooleanVar(value=False)
        self.data_receiving = tk.BooleanVar(value=False)
        self.sensor_manager = None
        self.data_acquisition = None
        self.auto = False
        self.auto_mode_enabled = tk.BooleanVar(value=False)  # Indicator for autonomous mode
        self.create_widgets()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        # Load logos
        university_logo_path = resource_path(os.path.join(ASSETS_DIR, 'university_logo.png'))
        sponsor_logo_path = resource_path(os.path.join(ASSETS_DIR, 'sponsor_logo.png'))

        # Resize logos
        logo_max_width = 150
        logo_max_height = 100

        university_logo_image = Image.open(university_logo_path).convert("RGBA")
        university_logo_image.thumbnail((logo_max_width, logo_max_height), Image.LANCZOS)
        self.university_logo = ImageTk.PhotoImage(university_logo_image)

        sponsor_logo_image = Image.open(sponsor_logo_path).convert("RGBA")
        sponsor_logo_image.thumbnail((logo_max_width, logo_max_height), Image.LANCZOS)
        self.sponsor_logo = ImageTk.PhotoImage(sponsor_logo_image)

        # Display logos
        logo_frame = tk.Frame(self, bg='white')
        logo_frame.pack(side="top", pady=10)

        uni_logo_label = tk.Label(logo_frame, image=self.university_logo, bg='white')
        uni_logo_label.pack(side="left", padx=10)

        sponsor_logo_label = tk.Label(logo_frame, image=self.sponsor_logo, bg='white')
        sponsor_logo_label.pack(side="right", padx=10)

        # Serial Port Selection
        port_frame = tk.Frame(self, bg='white')
        port_frame.pack(pady=10)

        tk.Label(port_frame, text="Select Serial Port:", bg='white').pack(side="left", padx=5)
        self.port_combo = ttk.Combobox(port_frame, textvariable=self.selected_port, width=30)
        self.port_combo.pack(side="left", padx=5)
        self.port_combo.bind("<<ComboboxSelected>>", self.port_selected)

        refresh_button = ttk.Button(port_frame, text="Refresh Ports", command=self.refresh_ports)
        refresh_button.pack(side="left", padx=5)

        # Autonomous Mode Light Bulb Indicator
        self.auto_mode_indicator = tk.Label(self, text="Auto Mode OFF", fg="grey", bg="black", font=("Arial", 12))
        self.auto_mode_indicator.pack(pady=5)

        # Analog Pressure Gauges
        self.pressure_gauge_1 = ttk.Progressbar(self, orient="horizontal", length=200, mode="determinate", maximum=200)
        self.pressure_gauge_1.pack(pady=10)
        self.pressure_gauge_label_1 = tk.Label(self, text="Pressure 1", bg="black")
        self.pressure_gauge_label_1.pack()

        self.pressure_gauge_2 = ttk.Progressbar(self, orient="horizontal", length=200, mode="determinate", maximum=200)
        self.pressure_gauge_2.pack(pady=10)
        self.pressure_gauge_label_2 = tk.Label(self, text="Pressure 2", bg="black")
        self.pressure_gauge_label_2.pack()

        # Control Buttons
        control_frame = tk.Frame(self, bg='white')
        control_frame.pack(pady=10)

        self.start_auto_button = ttk.Button(control_frame, text="Start Auto Mode", command=self.enable_autonomous_mode, state='disabled')
        self.start_auto_button.pack(side="left", padx=10)

        self.stop_auto_button = ttk.Button(control_frame, text="Stop Auto Mode", command=self.disable_autonomous_mode, state='disabled')
        self.stop_auto_button.pack(side="left", padx=10)
        
        self.start_button = ttk.Button(control_frame, text="Start Session", command=self.start_session, state='disabled')
        self.start_button.pack(side="left", padx=10)

        self.stop_button = ttk.Button(control_frame, text="Stop Session", command=self.stop_session, state='disabled')
        self.stop_button.pack(side="left", padx=10)

        self.open_valve_button = ttk.Button(control_frame, text="Open Valve", command=self.open_valve, state='disabled')
        self.open_valve_button.pack(side="left", padx=10)

        self.close_valve_button = ttk.Button(control_frame, text="Close Valve", command=self.close_valve, state='disabled')
        self.close_valve_button.pack(side="left", padx=10)

        # Arduino Connection Indicators
        indicator_frame = tk.Frame(self, bg='white')
        indicator_frame.pack(pady=10)

        self.connection_indicator = tk.Label(indicator_frame, text="Arduino Disconnected", fg="red", bg='white')
        self.connection_indicator.pack(side="left", padx=10)

        self.data_indicator = tk.Label(indicator_frame, text="No Data", fg="red", bg='white')
        self.data_indicator.pack(side="left", padx=10)

        # Sensor Data Display
        data_frame = tk.Frame(self, bg="grey")
        data_frame.pack(pady=20)

        self.flow1_var = tk.DoubleVar(value=0.00)
        self.flow2_var = tk.DoubleVar(value=0.00)
        self.pressure1_var = tk.DoubleVar(value=0.00)
        self.pressure2_var = tk.DoubleVar(value=0.00)
        self.pressure3_var = tk.DoubleVar(value=0.00)

        flow1_widget = LabeledValue(data_frame, "Flow Rate 1", self.flow1_var, unit="L/min")
        flow1_widget.pack(pady=5)

        flow2_widget = LabeledValue(data_frame, "Cumulative Flow", self.flow2_var, unit="L")
        flow2_widget.pack(pady=5)

        pressure1_widget = LabeledValue(data_frame, "Pressure 1", self.pressure1_var, unit="psi")
        pressure1_widget.pack(pady=5)

        pressure2_widget = LabeledValue(data_frame, "Pressure 2", self.pressure2_var, unit="psi")
        pressure2_widget.pack(pady=5)

        pressure3_widget = LabeledValue(data_frame, "Pressure 3", self.pressure3_var, unit="psi")
        pressure3_widget.pack(pady=5)

        # Status Bar
        self.status_bar = StatusBar(self, bg="grey")
        self.status_bar.pack(side="bottom", fill="x")

        # Adjust window size to fit content
        self.update_idletasks()
        self.minsize(self.winfo_width(), self.winfo_height())

        # Refresh ports after widgets are created
        self.refresh_ports()

    def refresh_ports(self):
        ports = ArduinoConnection.list_available_ports()
        self.port_combo['values'] = ports
        if ports:
            self.port_combo.current(0)
            self.selected_port.set(ports[0])
            self.start_button.config(state='normal')
            self.start_auto_button.config(state='normal')
            self.connect_to_arduino()
        else:
            self.selected_port.set('')
            self.start_button.config(state='disabled')
            self.start_auto_button.config(state='disabled')
            self.disconnect_from_arduino()

    def port_selected(self, event):
        selected_port = self.selected_port.get()
        self.logger.info(f"Selected port: {selected_port}")
        self.connect_to_arduino()

    def connect_to_arduino(self):
        # Disconnect existing connection if any
        if self.sensor_manager:
            self.sensor_manager.stop()
            self.sensor_manager = None
        selected_port = self.selected_port.get()
        if not selected_port:
            self.connection_indicator.config(text="Arduino Disconnected", foreground="red")
            return
        try:
            self.sensor_manager = SensorManager(port=selected_port)
            self.sensor_manager.connect()
            self.sensor_manager.start_receiving_only()
            self.update_gui()
            self.connection_indicator.config(text="Arduino Connected", foreground="green")
            self.open_valve_button.config(state='normal')
            self.close_valve_button.config(state='normal')
        except Exception as e:
            self.connection_indicator.config(text="Arduino Disconnected", foreground="red")
            messagebox.showerror("Error", f"Failed to connect to Arduino: {e}")

    def disconnect_from_arduino(self):
        if self.sensor_manager:
            self.sensor_manager.stop()
            self.sensor_manager = None
        self.connection_indicator.config(text="Arduino Disconnected", foreground="red")
        self.open_valve_button.config(state='disabled')
        self.close_valve_button.config(state='disabled')
        self.flow1_var.set(0.0)
        self.flow2_var.set(0.0)
        self.pressure1_var.set(0.0)
        self.pressure2_var.set(0.0)
        self.pressure3_var.set(0.0)
        self.data_indicator.config(text="No Data", foreground="red")

    def start_session(self):
        try:
            if not self.sensor_manager or not self.sensor_manager.connected:
                messagebox.showerror("Error", "Arduino is not connected.")
                return
            # Start data acquisition in sensor manager and reset cumulative flow on Arduino
            self.sensor_manager.arduino.write_command("RESET_CUMULATIVE_FLOW")  # Send reset command
            self.sensor_manager.start_data_acquisition()
            self.data_acquisition = DataAcquisition()
            self.data_acquisition.start_session(self.sensor_manager.data_queue)
            self.start_button.config(state='disabled')
            self.stop_button.config(state='normal')
            self.status_bar.set_status("Session Started")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start session: {e}")
            self.status_bar.set_status("Error starting session")
    
    def enable_autonomous_mode(self, enabled=True):
        """Enable autonomous valve control on the Arduino."""
        try:
            if self.sensor_manager and self.sensor_manager.connected:
                start_button_state = "disabled" if enabled else "normal"
                stop_button_state = "normal" if enabled else "disabled"
                self.start_auto_button.config(state=start_button_state)
                self.stop_auto_button.config(state=stop_button_state)

                command = "ENABLE_AUTO" if enabled else "DISABLE_AUTO"
                self.sensor_manager.arduino.write_command(command)

                mode_status = "Auto Mode Enabled" if enabled else "Auto Mode Disabled"
                self.status_bar.set_status(mode_status)

                self.auto = enabled
                self.auto_mode_enabled.set(enabled)
                self.auto_mode_indicator.config(text="Auto Mode ON" if enabled else "Auto Mode OFF", fg="green" if enabled else "grey")
            else:
                messagebox.showerror("Error", "Arduino is not connected.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open valve: {e}")

            self.status_bar.set_status("Error Enabling Auto Mode")

    def disable_autonomous_mode(self, enabled=False):
        """Disable autonomous valve control on the Arduino."""
        try:
            if self.sensor_manager and self.sensor_manager.connected:
                start_button_state = "disabled" if enabled else "normal"
                stop_button_state = "normal" if enabled else "disabled"
                self.start_auto_button.config(state=start_button_state)
                self.stop_auto_button.config(state=stop_button_state)

                command = "ENABLE_AUTO" if enabled else "DISABLE_AUTO"
                self.sensor_manager.arduino.write_command(command)

                mode_status = "Auto Mode Enabled" if enabled else "Auto Mode Disabled"
                self.status_bar.set_status(mode_status)

                self.auto = enabled
                self.auto_mode_enabled.set(enabled)
                self.auto_mode_indicator.config(text="Auto Mode ON" if enabled else "Auto Mode OFF", fg="green" if enabled else "grey")
            else:
                messagebox.showerror("Error", "Arduino is not connected.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open valve: {e}")
            self.status_bar.set_status("Error Disabling Auto Mode")

    def stop_session(self):
        try:
            if self.data_acquisition:
                self.data_acquisition.stop_session()
                self.data_acquisition = None
            if self.auto:
                self.set_autonomous_mode(False)
            self.start_button.config(state='normal')
            self.stop_button.config(state='disabled')
            self.status_bar.set_status("Session Stopped")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop session: {e}")
            self.status_bar.set_status("Error stopping session")

    def update_gui(self):
        if self.sensor_manager and self.sensor_manager.receiving_data:
            data_received = False
            while not self.sensor_manager.display_queue.empty():
                data = self.sensor_manager.display_queue.get()
                if 'CUMULATIVE_FLOW' in data:
                    self.flow2_var.set(data['CUMULATIVE_FLOW'])
                if 'PRESSURE1' in data:
                    self.pressure1_var.set(data['PRESSURE1'])
                    self.pressure_gauge_1['value'] = data['PRESSURE1']
                if 'PRESSURE2' in data:
                    self.pressure2_var.set(data['PRESSURE2'])
                    self.pressure_gauge_2['value'] = data['PRESSURE2']
                if 'PRESSURE3' in data:
                    self.pressure3_var.set(data['PRESSURE3'])
                if 'AUTO_MODE' in data:
                    self.auto = bool(data['AUTO_MODE'])
                    self.auto_mode_indicator.config(text="Auto Mode ON" if bool(data['AUTO_MODE']) else "Auto Mode OFF", fg="green" if bool(data['AUTO_MODE']) else "grey")
                data_received = True
            if data_received:
                self.data_indicator.config(text="Receiving Data", foreground="green")
            self.after(100, self.update_gui)
        else:
            self.data_indicator.config(text="No Data", foreground="red")

    def open_valve(self):
        try:
            if self.sensor_manager and self.sensor_manager.connected:
                self.sensor_manager.arduino.write_command("OPEN_VALVE")
                self.status_bar.set_status("Valve Opened")
            else:
                messagebox.showerror("Error", "Arduino is not connected.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open valve: {e}")
            self.status_bar.set_status("Error opening valve")

    def close_valve(self):
        try:
            if self.sensor_manager and self.sensor_manager.connected:
                if self.auto:
                    self.set_autonomous_mode(False)
                self.sensor_manager.arduino.write_command("CLOSE_VALVE")
                self.status_bar.set_status("Valve Closed")
            else:
                messagebox.showerror("Error", "Arduino is not connected.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to close valve: {e}")
            self.status_bar.set_status("Error closing valve")

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            try:
                if self.sensor_manager:
                    self.sensor_manager.stop()
                if self.data_acquisition:
                    self.data_acquisition.stop_session()
            except Exception as e:
                self.logger.error(f"Error during closing: {e}")
            self.destroy()
