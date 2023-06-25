import time

def log_action(*args):
    # Open the log file in append mode
    with open("./logs/log.txt", "a") as log_file:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} - {' '.join(str(arg) for arg in args)}\n"
        log_file.write(log_entry)
