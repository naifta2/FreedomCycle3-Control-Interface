# gui/themes.py

import tkinter as tk
from tkinter import ttk

def apply_theme(style):
    """Applies custom styles to the GUI."""
    # Configure styles for ttk widgets
    style.theme_use('clam')  # Use base theme as 'clam'

    # Customize styles
    style.configure('TButton', font=('Helvetica', 12), padding=5)
    style.configure('TLabel', font=('Helvetica', 12))
    style.configure('TFrame', background='#f0f0f0')
    style.configure('StatusBar.TLabel', font=('Helvetica', 10), foreground='gray')

    # Additional custom styles can be added here
