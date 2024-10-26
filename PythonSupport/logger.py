import os
from datetime import datetime

class Logger:
    log_file = None

    @staticmethod
    def start_logging(session_folder):
        """Initialize the log file in the session folder."""
        Logger.log_file = os.path.join(session_folder, "log.txt")
        with open(Logger.log_file, "w") as f:
            f.write(f"--- Session started at {datetime.now()} ---\n")

    @staticmethod
    def log(message):
        """Append a message to the log file with a timestamp."""
        if Logger.log_file:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(Logger.log_file, "a") as f:
                f.write(f"[{timestamp}] {message}\n")
