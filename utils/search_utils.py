import pyautogui
import time
import random

import pyperclip
from utils.log_utils import log_action
import constants
from utils.user_utils import comment_on_post

def go_to_user_profile(profileUrl):
    # Press CTRL + L to focus on the URL bar
    pyautogui.hotkey('ctrl', 'l')
    time.sleep(random.uniform(0.2, 0.5))
    pyperclip.copy(profileUrl)
    time.sleep(random.uniform(0.2, 0.5))
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(random.uniform(0.2, 0.5))
    pyautogui.press('enter')
    time.sleep(random.uniform(constants.LOAD_TIME_MIN, constants.LOAD_TIME_MAX))
    username = profileUrl.split('/')[-1]
    print("Navigated to user profile: " + username)

    return username


    

def find_and_click_search_bar():
    # Find the search bar image on the screen
    log_action("Finding search bar image")
    search_bar_location = pyautogui.locateOnScreen("./assets/search_bar.png", 
                                                   confidence=constants.CONFIDENCE_LEVEL)

    # Check if the search bar image is found
    if search_bar_location is not None:
        log_action("Search bar image found")
        # Get the center coordinates of the search bar
        search_bar_center = pyautogui.center(search_bar_location)

        # Add a short delay before moving the mouse
        time.sleep(random.uniform(0.5, 1.0))

        # Move the mouse cursor to the search bar
        pyautogui.moveTo(search_bar_center, duration=random.uniform(0.5, 1.0), tween=pyautogui.easeOutQuad)

        # Add another short delay before clicking
        time.sleep(random.uniform(0.2, 0.5))

        # Perform a single click on the search bar
        pyautogui.click()

        # Add another short delay before clicking
        time.sleep(random.uniform(0.2, 0.5))

        # Log the action using the log_action function from log_utils module
        log_action("Clicked on the search bar")
    else:
        log_action("Search bar image not found.")
        print("Search bar image not found.")

def find_comment_button():
    # Find the comment button image on the screen
    print("Finding comment button image")
    comment_icon_location = pyautogui.locateOnScreen(constants.COMMENT_ICON_PATH, 
                             confidence=constants.CONFIDENCE_LEVEL,
                             region=constants.COMMENT_SEARCH_REGION)
    
    if comment_icon_location is not None:
        print("Found comment icon, moving mouse to it")
        comment_icon_center = pyautogui.center(comment_icon_location)
        pyautogui.moveTo(x = (comment_icon_center[0] + 45), y = comment_icon_center[1],
                         duration=random.uniform(0.5, 1.0),
                         tween=pyautogui.easeOutQuad)
        time.sleep(random.uniform(0.2, 0.5))
        print("Clicking on comment icon")
        pyautogui.click()
        time.sleep(random.uniform(0.2, 0.5))

    else:
        print("Comment icon not found")
    
    

        