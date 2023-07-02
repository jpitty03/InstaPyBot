import requests
import time

def download_file(url, destination):
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception if there's an error

    with open(destination, 'wb') as file:
        file.write(response.content)

def get_file_lines(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return len(lines)

# Specify the URL of the file
file_url = "https://drive.google.com/uc?id=1ktU9FF9TCxGlmraZCh1vDv74LskosBBk&export=download"
file_path = "remote_logs.txt"

# Download the file initially
download_file(file_url, file_path)
last_line_count = get_file_lines(file_path)

# Continuously compare and print the new content
while True:
    time.sleep(10)  # Pause for 10 second before checking for updates
    download_file(file_url, file_path)
    current_line_count = get_file_lines(file_path)

    if current_line_count > last_line_count:
        with open(file_path, 'r') as file:
            new_lines = file.readlines()[last_line_count:]
            for line in new_lines:
                print(line.strip())
        last_line_count = current_line_count
