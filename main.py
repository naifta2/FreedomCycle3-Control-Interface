from PythonSupport.gui_interface import initialize_interface
from PythonSupport.config import Config, Widget
import tkinter as tk

def main():
    # Initialize main Tkinter window
    window = Widget.create(None, tk.Tk)
    window.title("FreedomCycle3 Control Interface")

    # Set window size and center it on the screen
    window.geometry("400x300")
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")
    
    # Initialize the interface with the persistent frame and welcome screen
    initialize_interface(window)

    # Run the Tkinter main loop
    window.mainloop()

if __name__ == "__main__":
    main()
