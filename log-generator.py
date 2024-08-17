import time
import json
from datetime import datetime
import random

# List of sample log types 
log_types = ["INFO", "WARNING", "ERROR", "DEBUG"]

# List of sample log messages
log_messages = [
    "User logged in",
    "Failed login attempt",
    "Database connection error",
    "API request received",
    "Data processing completed"
]

#Creates a dummy log entry 
def generate_log_entry():
    timestamp = datetime.now().isoformat() # returns in the format of 'YYYY-MM-DD HH:MM:SS.
    log_type = random.choice(log_types)
    message = random.choice(log_messages)
    
    log = {
        "timestamp": timestamp,
        "type": log_type,
        "message": message
    }

    return log


def write_log_to_file(log_entry, filename="app.log"):
    """Write a log entry to the specified file"""
    with open(filename, "a") as log_file:
        log_file.write(json.dumps(log_entry) + "\n")

def main():
    while True:
        log_entry = generate_log_entry()
        write_log_to_file(log_entry)
        print(f"Log entry written: {log_entry}")
        time.sleep(3)  # Wait for 10 seconds before generating the next log

if __name__ == "__main__":
    main()