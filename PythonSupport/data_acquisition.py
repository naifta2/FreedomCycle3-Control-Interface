import os
import time
import csv
import shutil
import subprocess
from datetime import datetime
from PythonSupport.config import Config
from PythonSupport.logger import Logger

def initialize_session():
    """Creates a work session folder only in the submodule repository."""
    session_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    Config.session_folder = os.path.join(Config.REPO_PATH, session_timestamp)  # Use submodule path only
    os.makedirs(Config.session_folder, exist_ok=True)
    Logger.start_logging(Config.session_folder)
    Logger.log("Session folder created in the submodule repository")

def start_collection():
    """Starts data collection."""
    Config.collecting_data = True
    Config.start_time = time.time()
    Config.data.clear()
    Logger.log("Data collection started and data list cleared")

def stop_collection():
    """Stops data collection, saves final data, closes log, and pushes all changes."""
    Config.collecting_data = False
    Logger.log("Data collection stopped")
    
    # Final save and push of all data
    save_data()  # Ensure all data is saved before pushing
    
    # Final push to ensure all changes are in the repository
    push_to_repository(os.path.basename(Config.session_folder))

    # Close logging for the session
    Logger.close_log()

def collect_data(flowrate, timestamp):
    """Collects data with precise timestamps."""
    elapsed_time = timestamp - Config.start_time  # Calculate elapsed time using precise timestamp
    formatted_timestamp = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
    Config.data.append([formatted_timestamp, elapsed_time, flowrate])
    Logger.log(f"Data appended: {Config.data[-1]}")

def save_data():
    """Saves collected data to the submodule repository and pushes updates to GitHub."""
    filename = "data_collected.csv"
    file_path = os.path.join(Config.session_folder, filename)
    
    if Config.data:
        # Write data to the submodule session folder
        with open(file_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "Elapsed Time (s)", "Flow Rate (L/min)"])
            writer.writerows(Config.data)
        Logger.log(f"Data saved in submodule repository at {file_path} with {len(Config.data)} entries.")

        # Commit and push changes to the GitHub submodule repository
        push_to_repository(os.path.basename(Config.session_folder))
        return file_path
    else:
        Logger.log("No data to save.")
        return None

def push_to_repository(session_folder_name):
    """Commits and pushes the session folder to the GitHub submodule repository."""
    try:
        # Change directory to the submodule repository path
        os.chdir(Config.REPO_PATH)

        # Stage, commit, and push the changes
        subprocess.run(["git", "add", session_folder_name], check=True)
        subprocess.run(["git", "commit", "-m", f"Add session data for {session_folder_name}"], check=True)
        subprocess.run(["git", "push"], check=True)

        Logger.log(f"Session data {session_folder_name} pushed to GitHub repository.")
    except subprocess.CalledProcessError as e:
        Logger.log(f"Error pushing session data to GitHub: {e}")
    finally:
        # Return to the original directory
        os.chdir(os.path.dirname(__file__))