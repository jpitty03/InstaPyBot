import random
import re
import time
import cv2
import numpy as np
import pyautogui
import pyperclip
from clarifai_utils.image_processor import get_label_matches, send_image_to_clarifai
from utils.log_utils import log_action
import constants
from PIL import Image
import pytesseract


def get_followers_following():
    pyautogui.screenshot('./assets/follower_following.png', region=(constants.FOLLOWER_FOLLOWING_REGION))

    img = cv2.imread("./assets/follower_following.png")
    img = cv2.bitwise_not(img)
    _, binary = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)

    # increase size of image
    scale_percent = 200
    width = int(binary.shape[1] * scale_percent / 100)
    height = int(binary.shape[0] * scale_percent / 100)
    dim = (width, height)
    binary = cv2.resize(binary, dim, interpolation=cv2.INTER_AREA)

    txt = pytesseract.image_to_string(binary, config="--oem 3 --psm 4")
    print(txt)
    

    s = txt.replace(',', '') # remove commas if any

    pattern = r"([\d.]+[KkMm]?)"
    numbers = re.findall(pattern, s)

    if len(numbers) >= 3:
        posts = convert_str(numbers[0])
        followers = convert_str(numbers[1])
        following = convert_str(numbers[2])
        return posts, followers, following
    else:
        return None

def convert_str(s):
    multiplier = 1

    if 'k' in s or 'K' in s:
        multiplier = 1_000
        s = s.replace('k', '').replace('K', '')

    elif 'm' in s or 'M' in s:
        multiplier = 1_000_000
        s = s.replace('m', '').replace('M', '')

    try:
        return round(float(s) * multiplier)
    except ValueError:
        return s


print(get_followers_following())

class FollowTracker:
    def __init__(self):
        self.followed_count = 0

    def increment_followed_count(self):
        self.followed_count += 1

    def get_followed_count(self):
        return self.followed_count
    
    def reset_follow_count(self):
        self.followed_count = 0

    def is_following_too_many(self):
        if self.followed_count >= constants.MAX_FOLLOWS_PER_HOUR:
            return True
        else:
            return False


def follow_user(user):
    print("Following user: " + user)

    # Click the follow button
    follow_button_location = pyautogui.locateOnScreen("./assets/follow_button.png", 
                                                      confidence=constants.CONFIDENCE_LEVEL,
                                                      region=constants.FOLLOW_BUTTON_REGION)
    following_button_location = pyautogui.locateOnScreen("./assets/following_button.png", 
                                                      confidence=constants.CONFIDENCE_LEVEL,
                                                      region=constants.FOLLOW_BUTTON_REGION)
    print("Follow button location: ", follow_button_location)
    if (follow_button_location is not None) and (is_account_not_private_or_no_posts() is True):
        print("Follow button found")
        log_action("Follow button found")
        follow_button_center = pyautogui.center(follow_button_location)

        print("Moving mouse to follow button")
        pyautogui.moveTo(follow_button_center, duration=random.uniform(0.5, 1.0), 
                         tween=pyautogui.easeOutQuad)
        time.sleep(random.uniform(0.2, 0.5))
        print("Clicking on follow button")
        pyautogui.click()
        time.sleep(random.uniform(2, 3.5))

        # Verify that the user was followed
        following_button_location = pyautogui.locateOnScreen("./assets/following_button.png", 
                                                      confidence=constants.CONFIDENCE_LEVEL,
                                                      region=constants.FOLLOW_BUTTON_REGION)
        if following_button_location is not None:
            print("User followed successfully")
            return True
        else:
            print("User not followed something happened")
            return False
    if following_button_location is not None:
        print("Already following " + user + " or profile is private")
        return False

    
def is_account_not_private_or_no_posts():
    # Find Posts icon
    pyautogui.sleep(3)
    posts_icon_location = find_posts_icon_location()
    if posts_icon_location is not None:
        print("Posts icon found")
        return True
    else:
        print("Posts icon not found, account is private or has no posts")
        return False
    
    # center of posts icon: 980, 396
    # top of image section: 980, 422
    # pixels from posts to top of image: 26

def find_posts_icon_location():
    posts_icon_location = pyautogui.locateOnScreen("./assets/posts_icon.png",
                                                    region=constants.POSTS_SEARCH_REGION,
                                                    confidence=constants.CONFIDENCE_LEVEL)
    return posts_icon_location
    


def convert_image_to_bytes(image_path):
    with open(image_path, 'rb') as f:
        image_bytes = f.read()
    f.close()
    return image_bytes

def save_image_section(posts_icon_location):
    pyautogui.screenshot(constants.IMAGE_SECTION_PATH, region=(651, posts_icon_location[1] + 34, 936, 308))


def save_first_three_posts(posts_icon_location):
    # Calculate location of image section
    image_section_left = 651
    image_section_top = posts_icon_location[1] + 34
    image_section_width = 936
    image_section_height = 308

    # Calculate location of each of the three images from image section
    image_one_left = image_section_left
    image_one_top = image_section_top
    image_one_width = image_section_width / 3
    image_one_height = image_section_height

    pyautogui.screenshot(constants.POST_ONE_PATH, region=(image_one_left, 
                                                            image_one_top, 
                                                            image_one_width, 
                                                            image_one_height))
    image_one_center = pyautogui.center((image_one_left,
                                         image_one_top,
                                         image_one_width,
                                         image_one_height))
    
    image_two_left = image_section_left + image_one_width
    image_two_top = image_section_top
    image_two_width = image_section_width / 3
    image_two_height = image_section_height

    pyautogui.screenshot(constants.POST_TWO_PATH, region=(image_two_left, 
                                                            image_two_top,
                                                            image_two_width,
                                                            image_two_height))
    image_two_center = pyautogui.center((image_two_left, 
                                         image_two_top,
                                         image_two_width,
                                         image_two_height))
    
    image_three_left = image_section_left + (image_one_width * 2)
    image_three_top = image_section_top
    image_three_width = image_section_width / 3
    image_three_height = image_section_height

    pyautogui.screenshot(constants.POST_THREE_PATH, region=(image_three_left, 
                                                                image_three_top,
                                                                image_three_width,
                                                                image_three_height))
    image_three_center = pyautogui.center((image_three_left, 
                                           image_three_top, 
                                           image_three_width, 
                                           image_three_height))
    
    return image_one_center, image_two_center, image_three_center

def comment_on_post():
    # Find/Click on comment button

    # Copy/paste random comment from FOOD_COMMENTS list
    print("Copying comment")
    pyperclip.copy(random.choice(constants.FOOD_COMMENTS))
    time.sleep(random.uniform(0.2, 0.5))

    print("Pasting comment")
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(random.uniform(0.2, 0.5))
    pyautogui.press('enter')
    time.sleep(random.uniform(0.2, 0.5))