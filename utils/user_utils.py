import csv
import os
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
from utils.log_utils import log_action


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


class FollowTracker:
    def __init__(self):
        self.followed_count = 0
        self.unfollowed_count = 0
        self.total_followed_count = 0
        self.max_followed_count_daily = 0
        self.max_followed_count_hourly = 0
        self.max_unfollowed_count_hourly = 0

    
    def increment_total_followed_count(self):
        self.total_followed_count += 1

    def get_total_followed_count(self):
        return self.total_followed_count
    
    def set_randomize_max_follow_count_daily(self, min, max):
        self.max_followed_count_daily = random.randint(min, max)

    def get_max_followed_count_daily(self):
        return self.max_followed_count_daily
    
    def reset_total_followed_count(self):
        self.total_followed_count = 0

    def get_max_followed_count_hourly(self):
        return self.max_followed_count_hourly

    def increment_followed_count(self):
        self.followed_count += 1
    
    def set_randomize_max_follow_count_hourly(self, min, max):
        self.max_followed_count_hourly = random.randint(min, max)

    def set_randomize_max_unfollow_count_hourly(self, min, max):
        self.max_unfollowed_count_hourly = random.randint(min, max)

    def get_max_unfollowed_count_hourly(self):
        return self.max_unfollowed_count_hourly

    def set_unfollow_profileUrls(self, profileUrls):
        self.unfollow_profileUrls = profileUrls

    def get_unfollow_profileUrls(self, x):
        return self.unfollow_profileUrls[x]
    
    def increment_unfollowed_count(self):
        self.unfollowed_count += 1

    def get_unfollowed_count(self):
        return self.unfollowed_count
    
    def reset_unfollow_count(self):
        self.unfollowed_count = 0

    def get_followed_count(self):
        return self.followed_count
    
    def reset_follow_count(self):
        self.followed_count = 0

    def is_following_too_many_hourly(self):
        if (self.followed_count >= self.max_followed_count_hourly) and (self.calculate_time_difference() < 3600):
            log_action("Followed too many people this hour")
            log_action("Hourly Followed count: ", str(self.followed_count) + "/" + str(self.max_followed_count_hourly))
            log_action("Time difference: ", str(self.calculate_time_difference()))
            return True
        else:
            return False
        
    def is_following_too_many_daily(self):
        if (self.total_followed_count >= self.max_followed_count_daily) and (self.calculate_time_difference() < 86400):
            log_action("Followed too many people today")
            log_action("Faily Followed count: " + str(self.total_followed_count) + "/" + str(self.max_followed_count_daily))
            log_action("Time difference: ", str(self.calculate_time_difference()))
            return True
        else:
            return False
        
    def is_unfollowing_too_many_hourly(self):
        if (self.unfollowed_count >= self.max_unfollowed_count_hourly) and (self.calculate_time_difference() < 3600):
            log_action("Unfollowed too many people this hour")
            log_action("Hourly Unfollowed count: " +  str(self.unfollowed_count) + "/" + str(self.max_unfollowed_count_hourly))
            log_action("Time difference: ", str(self.calculate_time_difference()))
            return True
        else:
            return False

    def set_start_time(self):
        self.start_time = time.time()

    def get_start_time(self):
        return self.start_time
    
    def calculate_time_difference(self):
        if self.start_time is None:
            raise ValueError("Start time has not been set.")

        current_time = time.time()
        time_difference = current_time - self.start_time
        return time_difference
    

def unfollow_users(unfollow_username):
    # Start unfollowing
    log_action("Starting unfollow method")
    remove_user_from_csv(unfollow_username, constants.UNFOLLOW_CSV_PATH + constants.UNFOLLOW_CSV_NAME, constants.UNFOLLOW_HEADERS)

    # Send ctrl l
    pyautogui.hotkey('ctrl', 'l')
    time.sleep(random.uniform(1.0, 2.0))
    # Go to user profile
    log_action("Going to user profile " + unfollow_username)
    pyperclip.copy('https://www.instagram.com/' + unfollow_username)
    time.sleep(random.uniform(1.0, 2.0))
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(random.uniform(1.0, 2.0))
    pyautogui.press('enter')
    time.sleep(random.uniform(constants.LOAD_TIME_MIN, constants.LOAD_TIME_MAX))

    following_button_location = pyautogui.locateOnScreen("./assets/following_button.png", 
                                                      confidence=constants.CONFIDENCE_LEVEL,
                                                      region=constants.FOLLOW_BUTTON_REGION)
    if following_button_location is None:
        following_button_location = pyautogui.locateOnScreen("./assets/following_button_2.png", 
                                                      confidence=constants.CONFIDENCE_LEVEL,
                                                      region=constants.FOLLOW_BUTTON_REGION)
    
    if following_button_location is not None:
        following_button_center = pyautogui.center(following_button_location)
        pyautogui.moveTo(following_button_center[0], following_button_center[1], 
                                    duration=random.uniform(0.5, 1.0), 
                                    tween=pyautogui.easeOutQuad)
        pyautogui.click()
        pyautogui.sleep(random.uniform(1.0, 2.0))
        unfollow_button_location = pyautogui.locateOnScreen("./assets/unfollow_button.png", 
                                                      confidence=constants.CONFIDENCE_LEVEL,
                                                      region=constants.UNFOLLOW_BUTTON_REGION)
        
        if unfollow_button_location is not None:
            unfollow_button_center = pyautogui.center(unfollow_button_location)
            pyautogui.moveTo(unfollow_button_center[0], unfollow_button_center[1], 
                                    duration=random.uniform(0.5, 1.0), 
                                    tween=pyautogui.easeOutQuad)
            pyautogui.click()
            pyautogui.sleep(random.uniform(1.0, 2.0))
            log_action("Sleeping for 2 seconds")
            pyautogui.press('f5')
            pyautogui.sleep(random.uniform(constants.LOAD_TIME_MIN, constants.LOAD_TIME_MAX))
            log_action("Removing " + unfollow_username + " from " + constants.UNFOLLOW_CSV_NAME)
            return True

        else:
            log_action("Unfollow button not found")
            log_action("Sleeping for 2 seconds")
            time.sleep(2)
            return False
    else:
        log_action("Following button not found")
        log_action("Sleeping for 2 seconds")
        time.sleep(2)
        return False


def remove_user_from_csv(username, csv_file_path, headers):
    headers_lowercase = [header.lower() for header in headers]
    username_index = headers_lowercase.index('username')

    with open(csv_file_path, 'r', encoding='utf-8') as readFile:
        reader = csv.reader(readFile)
        next(reader, None)  # skip the headers
        lines_before = list(reader)

    lines_after = [line for line in lines_before if line[username_index] != username]

    with open(csv_file_path, 'w', newline='', encoding='utf-8') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerow(headers)  # write the header
        writer.writerows(lines_after)

    if len(lines_before) == len(lines_after):
        log_action(f"User '{username}' was not found in '{csv_file_path}'.")
    else:
        log_action(f"User '{username}' was successfully removed in '{csv_file_path}'.")


def follow_user(user):
    log_action("Following user: " + user)

    # Click the follow button
    follow_button_location = pyautogui.locateOnScreen("./assets/follow_button.png", 
                                                      confidence=constants.CONFIDENCE_LEVEL,
                                                      region=constants.FOLLOW_BUTTON_REGION)
    following_button_location = pyautogui.locateOnScreen("./assets/following_button.png", 
                                                      confidence=constants.CONFIDENCE_LEVEL,
                                                      region=constants.FOLLOW_BUTTON_REGION)
    if following_button_location is None:
        following_button_location = pyautogui.locateOnScreen("./assets/following_button_2.png", 
                                                      confidence=constants.CONFIDENCE_LEVEL,
                                                      region=constants.FOLLOW_BUTTON_REGION)
        
    log_action("Follow button location: ", follow_button_location)
    if (follow_button_location is not None) and (is_account_not_private_or_no_posts() is True):
        log_action("Follow button found")
        follow_button_center = pyautogui.center(follow_button_location)

        log_action("Moving mouse to follow button")
        pyautogui.moveTo(follow_button_center, duration=random.uniform(0.5, 1.0), 
                         tween=pyautogui.easeOutQuad)
        time.sleep(random.uniform(0.2, 0.5))
        log_action("Clicking on follow button")
        pyautogui.click()
        time.sleep(random.uniform(2, 3.5))

        # Verify that the user was followed
        following_button_location = pyautogui.locateOnScreen("./assets/following_button.png", 
                                                      confidence=constants.CONFIDENCE_LEVEL,
                                                      region=constants.FOLLOW_BUTTON_REGION)
        if following_button_location is None:
            following_button_location = pyautogui.locateOnScreen("./assets/following_button_2.png", 
                                                        confidence=constants.CONFIDENCE_LEVEL,
                                                        region=constants.FOLLOW_BUTTON_REGION)
        
        if following_button_location is not None:
            log_action("User followed successfully")
            return True
        else:
            log_action("User not followed something happened")
            return False
    if following_button_location is not None:
        log_action("Already following " + user + " or profile is private")
        return False

    
def is_account_not_private_or_no_posts():
    # Find Posts icon
    pyautogui.sleep(3)
    posts_icon_location = find_posts_icon_location()
    if posts_icon_location is not None:
        log_action("Posts icon found")
        return True
    else:
        log_action("Posts icon not found, account is private or has no posts")
        return False


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
    log_action("Copying comment")
    pyperclip.copy(random.choice(constants.FOOD_COMMENTS))
    time.sleep(random.uniform(0.2, 0.5))

    log_action("Pasting comment")
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(random.uniform(0.2, 0.5))
    pyautogui.press('enter')
    time.sleep(random.uniform(2, 3))