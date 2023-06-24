import pyautogui
import constants
from utils.log_utils import log_action


def is_logged_in():
    # Perform image processing or template matching to locate elements on the screen
    # that indicate whether you are logged in or not.
    # You can use pyautogui's image recognition features for template matching.

    # Example: Check if the user profile picture is present
    # Assuming you have an image of the user profile picture saved as "profile_picture.png"
    profile_picture = pyautogui.locateOnScreen("./assets/profile_picture.png", confidence=constants.CONFIDENCE_LEVEL)
    login_button = pyautogui.locateOnScreen("./assets/login_button.png", confidence=constants.CONFIDENCE_LEVEL)
    search_button = pyautogui.locateOnScreen("./assets/search_bar.png", confidence=constants.CONFIDENCE_LEVEL)
    create_button = pyautogui.locateOnScreen("./assets/create_button.png", confidence=constants.CONFIDENCE_LEVEL)
    is_logged_in = False
    if (profile_picture is not None):
        is_logged_in = True
    if (search_button is not None):
        is_logged_in = True
    if (create_button is not None):
        is_logged_in = True
    if (login_button is not None):
        is_logged_in = False
    log_action(is_logged_in)
    log_action(profile_picture)
    log_action(search_button)
    log_action(login_button)
    
    # Log the login status
    log_action(f"Logged in: {is_logged_in}")

    # Return True if logged in, False otherwise
    return is_logged_in
