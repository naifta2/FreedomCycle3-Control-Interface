import tkinter as tk
from PythonSupport.gui_interface import setup_welcome_screen  # Only import setup_welcome_screen

# Initialize main Tkinter window
root = tk.Tk()
root.title("Flowmeter Interface")

# Set up the welcome screen, which includes continuous Arduino checking
setup_welcome_screen(root)

# Run the GUI event loop
root.mainloop()