import csv
import random
import time
import numpy as np
import constants
from utils.user_utils import FollowTracker, comment_on_post, convert_image_to_bytes, find_posts_icon_location, follow_user, get_followers_following, is_account_not_private_or_no_posts, save_first_three_posts, save_image_section
from utils.search_utils import find_comment_button, go_to_user_profile
from utils.login_utils import is_logged_in
from utils.log_utils import log_action
from clarifai_utils.image_processor import send_image_to_clarifai, get_label_matches
import pyautogui
import threading
import keyboard

run_program = True

def exit_program():
    global run_program
    while True:
        if keyboard.is_pressed('q'):  # if key 'q' is pressed
            run_program = False
            break  # finish the loop
        else:
            pass
        time.sleep(0.5)  # delay to reduce CPU usage

exit_thread = threading.Thread(target=exit_program)
exit_thread.start()

# Initialize the follow tracker
follow_tracker = FollowTracker()

# Set current time
follow_tracker.set_start_time()
log_action(follow_tracker.get_start_time())
pyautogui.sleep(2)
follow_tracker.set_randomize_max_follow_count_hourly(constants.MAX_FOLLOWS_PER_HOUR_MIN, constants.MAX_FOLLOWS_PER_HOUR_MAX)
follow_tracker.set_randomize_max_follow_count_daily(constants.MAX_FOLLOWS_PER_DAY_MIN, constants.MAX_FOLLOWS_PER_DAY_MAX)
log_action(follow_tracker.get_max_followed_count_daily())
log_action(follow_tracker.get_max_followed_count_hourly())

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
# log_action (x)
while x < 500 and run_program == True:
    # Refresh the page
    if follow_tracker.is_following_too_many_hourly() == True:
        log_action("Followed too many users, sleeping for 1 hour")
        time.sleep(constants.SLEEP_TIME_HOURLY)
        follow_tracker.reset_follow_count()
        follow_tracker.set_randomize_max_follow_count_hourly(constants.MAX_FOLLOWS_PER_HOUR_MIN, constants.MAX_FOLLOWS_PER_HOUR_MAX)
        log_action("Follow count reset")
        log_action("Time elapsed: " + str(follow_tracker.calculate_time_difference()) + " seconds")
        follow_tracker.set_start_time()
    else:
        log_action("Current follow within 1 hour: " + str(follow_tracker.get_followed_count()))
        log_action("Time elapsed: " + str(follow_tracker.calculate_time_difference()) + " seconds")

    if follow_tracker.is_following_too_many_daily() == True:
        log_action("Daily follow limit reached, sleeping for 24 hours")
        time.sleep(constants.SLEEP_TIME_DAILY)
        follow_tracker.reset_follow_count()
        follow_tracker.reset_total_followed_count()
        follow_tracker.set_randomize_max_follow_count_hourly(constants.MAX_FOLLOWS_PER_HOUR_MIN, constants.MAX_FOLLOWS_PER_HOUR_MAX)
        log_action("Follow count reset")
        follow_tracker.set_start_time()
    else:
        log_action("Current follow within 24 hours: " + str(follow_tracker.get_total_followed_count()))
    log_action("")
    log_action("###########################################################")
    log_action(follow_tracker.get_start_time())
    log_action("Starting new user loop")
    pyautogui.hotkey('ctrl', 'r')
    time.sleep(random.uniform(6.0, 8.0))
    log_action("Checking for login state")
    if is_logged_in() == True:
        log_action("Logged in")
    else:
        log_action("Not logged in, exiting program")
        break


    # Meat and potatoes
    username = go_to_user_profile(profileUrls[x])
    if username == constants.ACCOUNT_NAME:
        log_action("Found" + constants.ACCOUNT_NAME +", skipping")
        x += 1

    log_action("Searching for " + username)
    pyautogui.sleep(2)
    time.sleep(random.uniform(constants.LOAD_TIME_MIN, constants.LOAD_TIME_MAX))

    # Get user data and skip if requirements not met
    log_action("Getting followers and following count")
    counts = get_followers_following()
    if counts is None:
        log_action("User got a jacked up profile, skipping")
        x += 1
        continue

    posts_count, follower_count, following_count = counts

    if ((int(follower_count) / int(following_count) > 2) or 
        (int(following_count) < 100) or 
        (int(posts_count) < 15) or 
        (int(following_count) / int(follower_count) > 4)):
        log_action("Follower count more than double following count, or low following/posts, skipping")
        x += 1
        continue
    log_action("Follower count less than double following count, or high following/posts, continuing")


    # Follow user
    did_we_follow = follow_user(username)
    log_action("Did we follow? " + str(did_we_follow))
    if did_we_follow == True:
        follow_tracker.increment_followed_count()
        follow_tracker.increment_total_followed_count()
        log_action("Total followed count:", follow_tracker.get_total_followed_count())
        log_action("Followed count:", follow_tracker.get_followed_count())
        log_action("Refreshing page")
        pyautogui.hotkey('ctrl', 'r')
        time.sleep(random.uniform(3.0, 5.0))
    
    # Should we start commenting?
    if (constants.COMMENT_TOGGLE == True):
        if (is_account_not_private_or_no_posts() == True) and (did_we_follow == True):
            # Grabbing posts icon location
            posts_icon_location = find_posts_icon_location()

            #Check image section for food first
            log_action("Checking image section for food")
            save_image_section(posts_icon_location)
            if get_label_matches(send_image_to_clarifai(convert_image_to_bytes(constants.IMAGE_SECTION_PATH))) == True:
                log_action("Found food in image section, commenting")

                # Check images for food
                log_action("Checking images for food")
                image_one_center, image_two_center, image_three_center = save_first_three_posts(posts_icon_location)

                # If matches, comment
                if get_label_matches(send_image_to_clarifai(convert_image_to_bytes(constants.POST_ONE_PATH))) == True:
                    log_action("Matches found on first image, commenting")
                    pyautogui.moveTo(image_one_center[0], image_one_center[1] - 100, 
                                    duration=random.uniform(0.5, 1.0), 
                                    tween=pyautogui.easeOutQuad)
                    time.sleep(random.uniform(0.7, 1.5))
                    pyautogui.click()
                    time.sleep(random.uniform(constants.LOAD_TIME_MIN, constants.LOAD_TIME_MAX))
                    find_comment_button()
                    comment_on_post()

                elif get_label_matches(send_image_to_clarifai(convert_image_to_bytes(constants.POST_TWO_PATH))) == True:
                    log_action("Matches found on second image, commenting")
                    pyautogui.moveTo(image_two_center[0], image_two_center[1] - 100,
                                    duration=random.uniform(0.5, 1.0),
                                    tween=pyautogui.easeOutQuad)
                    time.sleep(random.uniform(0.7, 1.5))
                    pyautogui.click()
                    time.sleep(random.uniform(constants.LOAD_TIME_MIN, constants.LOAD_TIME_MAX))
                    find_comment_button()
                    comment_on_post()

                elif get_label_matches(send_image_to_clarifai(convert_image_to_bytes(constants.POST_THREE_PATH))) == True:
                    log_action("Matches found on third image, commenting")
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

log_action("Finished")

