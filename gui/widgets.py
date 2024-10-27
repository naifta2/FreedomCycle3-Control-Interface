# gui/widgets.py

import tkinter as tk

class LabeledValue(tk.Frame):
    """A custom widget to display a label and a value."""

    def __init__(self, parent, label_text, value_var, unit='', **kwargs):
        bg_color = kwargs.pop('bg', parent['bg'])
        super().__init__(parent, bg=bg_color, **kwargs)

        label = tk.Label(self, text=label_text, font=('Arial', 12), bg=bg_color)
        label.pack(side='left', padx=5)

        value_label = tk.Label(self, textvariable=value_var, font=('Arial', 12, 'bold'), bg=bg_color)
        value_label.pack(side='left', padx=5)

        unit_label = tk.Label(self, text=unit, font=('Arial', 12), bg=bg_color)
        unit_label.pack(side='left', padx=5)

    def _layout_widgets(self):
        self.label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.value_label.grid(row=0, column=1, padx=5, pady=5, sticky='e')
        self.unit_label.grid(row=0, column=2, padx=5, pady=5, sticky='w')

class StatusBar(tk.Frame):
    def __init__(self, parent, **kwargs):
        bg_color = kwargs.pop('bg', parent['bg'])
        super().__init__(parent, bg=bg_color, **kwargs)
        self.label = tk.Label(self, text="", anchor='w', bg=bg_color)
        self.label.pack(fill='x')

    def set_status(self, message):
        self.label.config(text=message)