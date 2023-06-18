import time

def log_action(action):
    # Open the log file in append mode
    with open("log.txt", "a") as log_file:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} - {action}\n"
        log_file.write(log_entry)
