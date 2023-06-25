import os
import requests
import time
from dotenv import load_dotenv


# If you're running this program on a remote machine,
# you can use this function to download the logs file 
# from the remote machine to your local machine
# Add the file to a google drive folder and share the folder

def download_file(url, destination, start_byte):
    headers = {'Range': f'bytes={start_byte}-'}
    response = requests.get(url, headers=headers, stream=True)
    with open(destination, 'ab') as file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)

def print_latest_content(file_path):
    with open(file_path, 'r') as file:
        file.seek(0, 2)  # Move the file pointer to the end
        while True:
            line = file.readline()
            if not line:
                time.sleep(0.1)  # Sleep for a short interval if no new content is available
                continue
            print(line.strip())

# Specify the URL to download the file from
download_url = os.getenv("LOG_FILE_URL")
print(download_url)
# Specify the path where the file will be saved
file_path = "remote_logs.txt"

# Download the file initially
download_file(download_url, file_path, 0)

# Continuously download and print the latest content
while True:
    print_latest_content(file_path)
    file_size = os.path.getsize(file_path)
    download_file(download_url, file_path, file_size)


