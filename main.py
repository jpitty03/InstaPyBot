import csv
import random
import time
import numpy as np
import pyperclip
import constants
from utils.user_utils import FollowTracker, comment_on_post, convert_image_to_bytes, find_posts_icon_location, follow_user, get_followers_following, is_account_not_private_or_no_posts, save_first_three_posts, save_image_section
from utils.search_utils import find_comment_button, go_to_user_profile
from utils.login_utils import is_logged_in
from utils.log_utils import log_action
from clarifai_utils.image_processor import send_image_to_clarifai, get_label_matches
import cv2
import pyautogui

# Load the captured image from variable
pyautogui.sleep(2)

# Initialize the follow tracker
follow_tracker = FollowTracker()

# Set current time
follow_tracker.set_start_time()
print(follow_tracker.get_start_time())
pyautogui.sleep(2)
print(follow_tracker.calculate_time_difference())

# Read the CSV file
profileUrls = []
with open(constants.CSV_FILE, 'r', newline='', encoding='latin-1') as csvfile:
    # Read the CSV file
    reader = csv.DictReader(csvfile)
    for row in reader:
        profileUrl = row['profileUrl']
        profileUrls.append(profileUrl)






x = 0
# x = len(usernames)
# print (x)
while x < 500:
    # Refresh the page
    if follow_tracker.is_following_too_many() == True:
        print("Followed too many users, sleeping for 15 minutes")
        time.sleep(900)
        follow_tracker.reset_follow_count()
        print("Follow count reset")
    print()
    print("###########################################################")
    print("Starting new user loop")
    pyautogui.hotkey('ctrl', 'r')
    time.sleep(random.uniform(6.0, 8.0))
    log_action("Checking for login state")
    if is_logged_in() == True:
        log_action("Logged in")
    else:
        log_action("Not logged in, exiting program")
        print("Not logged in, exiting program")
        break
    
    # Meat and potatoes

    username = go_to_user_profile(profileUrls[x])
    if username == constants.ACCOUNT_NAME:
        log_action("Found" + constants.ACCOUNT_NAME +", skipping")
        x += 1

    print("Searching for " + username)
    pyautogui.sleep(2)
    time.sleep(random.uniform(constants.LOAD_TIME_MIN, constants.LOAD_TIME_MAX))

    # Get user data and skip if requirements not met
    print("Getting followers and following count")
    counts = get_followers_following()
    if counts is None:
        print("User got a jacked up profile, skipping")
        x += 1
        continue

    posts_count, follower_count, following_count = counts

    if ((int(follower_count) / int(following_count) > 2) or 
        (int(following_count) < 100) or 
        (int(posts_count) < 15) or 
        (int(following_count) / int(follower_count) > 4)):
        print("Follower count more than double following count, or low following/posts, skipping")
        x += 1
        continue
    print("Follower count less than double following count, or high following/posts, continuing")


    # Follow user
    did_we_follow = follow_user(username)
    print("Did we follow? " + str(did_we_follow))
    if did_we_follow == True:
        follow_tracker.increment_followed_count()
        print("Followed count:", follow_tracker.get_followed_count())
        print("Followed count: " + str(follow_tracker.get_followed_count()))
        print("Refreshing page")
        pyautogui.hotkey('ctrl', 'r')
        time.sleep(random.uniform(3.0, 5.0))
    
    # Should we start commenting?
    if (is_account_not_private_or_no_posts() == True) and (did_we_follow == True):
        # Grabbing posts icon location
        posts_icon_location = find_posts_icon_location()

        #Check image section for food first
        print("Checking image section for food")
        save_image_section(posts_icon_location)
        if get_label_matches(send_image_to_clarifai(convert_image_to_bytes(constants.IMAGE_SECTION_PATH))) == True:
            print("Found food in image section, commenting")

            # Check images for food
            print("Checking images for food")
            image_one_center, image_two_center, image_three_center = save_first_three_posts(posts_icon_location)

            # If matches, comment
            if get_label_matches(send_image_to_clarifai(convert_image_to_bytes(constants.POST_ONE_PATH))) == True:
                print("Matches found on first image, commenting")
                pyautogui.moveTo(image_one_center[0], image_one_center[1] - 100, 
                                duration=random.uniform(0.5, 1.0), 
                                tween=pyautogui.easeOutQuad)
                time.sleep(random.uniform(0.7, 1.5))
                pyautogui.click()
                time.sleep(random.uniform(constants.LOAD_TIME_MIN, constants.LOAD_TIME_MAX))
                find_comment_button()
                comment_on_post()

            elif get_label_matches(send_image_to_clarifai(convert_image_to_bytes(constants.POST_TWO_PATH))) == True:
                print("Matches found on second image, commenting")
                pyautogui.moveTo(image_two_center[0], image_two_center[1] - 100,
                                duration=random.uniform(0.5, 1.0),
                                tween=pyautogui.easeOutQuad)
                time.sleep(random.uniform(0.7, 1.5))
                pyautogui.click()
                time.sleep(random.uniform(constants.LOAD_TIME_MIN, constants.LOAD_TIME_MAX))
                find_comment_button()
                comment_on_post()

            elif get_label_matches(send_image_to_clarifai(convert_image_to_bytes(constants.POST_THREE_PATH))) == True:
                print("Matches found on third image, commenting")
                pyautogui.moveTo(image_three_center[0], image_three_center[1] - 100,
                                duration=random.uniform(0.5, 1.0),
                                tween=pyautogui.easeOutQuad)
                time.sleep(random.uniform(0.7, 1.5))
                pyautogui.click()
                time.sleep(random.uniform(constants.LOAD_TIME_MIN, constants.LOAD_TIME_MAX))
                find_comment_button()
                comment_on_post()


        #End of loop
    x += 1

