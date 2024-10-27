# gui/widgets.py

import tkinter as tk
from tkinter import ttk

class LabeledValue(ttk.Frame):
    """A custom widget to display a label and a value."""

    def __init__(self, parent, label_text, value_var, unit="", *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.label = ttk.Label(self, text=label_text)
        self.value_label = ttk.Label(self, textvariable=value_var)
        self.unit_label = ttk.Label(self, text=unit)
        self._layout_widgets()

    def _layout_widgets(self):
        self.label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.value_label.grid(row=0, column=1, padx=5, pady=5, sticky='e')
        self.unit_label.grid(row=0, column=2, padx=5, pady=5, sticky='w')

class StatusBar(ttk.Frame):
    """A custom status bar widget."""

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, relief=tk.SUNKEN, *args, **kwargs)
        self.label = ttk.Label(self, text="Ready", anchor='w')
        self.label.pack(fill=tk.X)

    def set_status(self, message):
        self.label.config(text=message)