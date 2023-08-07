# InstaPyBot

:warning: **Active development in process. Some features/settings may not work properly.**

Please report any issues getting started. I'm not the greatest at instructions, so if you run into a problem feel free to open an issue!

## Description
InstaPyBot is an Instagram bot that follows users based on a CSV file and comments on pictures. It utilizes OCR to capture data on the screen, Pyautogui to mimic realistic movement, and Tesseract to capture screenshots and use AI to determine what to comment.

## Dependencies
- [Python](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)
- [Tesseract](https://github.com/UB-Mannheim/tesseract/wiki)

## Getting Started
1. Download and install Python from the [Python website](https://www.python.org/downloads/).
2. Download and install Git from the [Git website](https://git-scm.com/downloads).
3. Download and install Tesseract from the [Tesseract GitHub repository](https://github.com/UB-Mannheim/tesseract/wiki).

## Setup
1. Create a Python environment using the command: `python -m venv env`.
2. Activate the environment by running: `env\Scripts\activate`.
3. Install the required dependencies by running: `python -m pip install -r requirements.txt`.
4. Fill in the .env file, if commenting based on post content grab a Clarifai token/api key.
5. Use Phantombuster to scrape a user profile for followers. (Use a dummy account for scraping)
6. I'm using Instagram on Dark mode, and since it's looking for the images, it will only work on Dark mode.

## Usage
1. Navigate to the InstaPyBot directory: `cd InstaPyBot`.
2. Activate the Python environment: `env\Scripts\activate`.
3. Run the program using: `python main.py`

## Contributing
Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request.

## License
[MIT License](LICENSE)
