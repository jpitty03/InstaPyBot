import requests
import time

def download_file(url, destination):
    with requests.get(url, stream=True) as response:
        response.raise_for_status()  # Raise an exception if there's an error

        with open(destination, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

def get_file_lines(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            yield line

# Specify the URL of the file
file_url = SPECIFY_PATH
file_path = "remote_logs.txt"

# Download the file initially
download_file(file_url, file_path)
last_line_count = sum(1 for _ in get_file_lines(file_path))

# Continuously compare and print the new content
while True:
    time.sleep(10)  # Pause for 10 second before checking for updates
    download_file(file_url, file_path)
    current_line_count = sum(1 for _ in get_file_lines(file_path))

    if current_line_count > last_line_count:
        for line in get_file_lines(file_path):
            if last_line_count > 0:
                last_line_count -= 1
            else:
                print(line.strip())
        last_line_count = current_line_count