import csv
import random
import time
import numpy as np
import pyperclip
import constants
from utils.user_utils import *
from utils.search_utils import find_comment_button, go_to_user_profile
from utils.login_utils import is_logged_in
from utils.log_utils import log_action
from clarifai_utils.image_processor import send_image_to_clarifai, get_label_matches
import pyautogui
import threading
import keyboard
from dotenv import load_dotenv
import datetime

MINIMUM_POST_COUNT = 15
MINIMUM_FOLLOWER_COUNT = 100
MINIMUM_FOLLOWING_COUNT = 100
FOLLOWER_FOLLOWING_RATIO_MAX = 2
FOLLOWER_FOLLOWING_RATIO_MAX = 4

load_dotenv()

# Initialize the follow tracker
follow_tracker = FollowTracker()

# Set current time
follow_tracker.set_start_time()
log_action(follow_tracker.get_start_time())
pyautogui.sleep(2)
follow_tracker.set_randomize_max_follow_count_hourly(constants.MAX_FOLLOWS_PER_HOUR_MIN, constants.MAX_FOLLOWS_PER_HOUR_MAX)
follow_tracker.set_randomize_max_follow_count_daily(constants.MAX_FOLLOWS_PER_DAY_MIN, constants.MAX_FOLLOWS_PER_DAY_MAX)
follow_tracker.set_randomize_max_unfollow_count_hourly(constants.MAX_UNFOLLOWS_PER_HOUR_MIN, constants.MAX_UNFOLLOWS_PER_HOUR_MAX)

log_action(follow_tracker.get_max_followed_count_daily())
log_action(follow_tracker.get_max_followed_count_hourly())

# Read the CSV file
follow_usernames = []
with open(constants.CSV_FILE_PATH + constants.CSV_FILE_NAME, 'r', newline='', encoding='latin-1') as csvfile:
    # Read the CSV file
    reader = csv.DictReader(csvfile)
    for row in reader:
        username = row['username']
        follow_usernames.append(username)

unfollow_profile_usernames = []
if constants.UNFOLLOW_TOGGLE == True:
    with open('follower_following_utils\\not_following_back.csv', 'r', newline='', encoding='latin-1') as csvfile:
        # Read the CSV file
        reader = csv.DictReader(csvfile)
        for row in reader:
            username = row['Username']
            unfollow_profile_usernames.append( username)
follow_tracker.set_unfollow_profileUrls(unfollow_profile_usernames)


x = 0
while x <= len(follow_usernames):
    print("Starting program")
    # Refresh the page
    if follow_tracker.is_following_too_many_hourly() == True:
        log_action("Followed too many users, sleeping for 1 hour")
        log_action("Time elapsed: " + str(follow_tracker.calculate_time_difference()) + " seconds")

        # Sleep for 1 hour, log time to restart
        time_to_start = follow_tracker.get_start_time() + constants.SLEEP_TIME_HOURLY
        log_action('Starting again at: ' + str(datetime.datetime.fromtimestamp(time_to_start).strftime('%m/%d %H:%M:%S')))
        time.sleep(constants.SLEEP_TIME_HOURLY)
        follow_tracker.reset_follow_count()
        follow_tracker.reset_unfollow_count()
        follow_tracker.set_randomize_max_follow_count_hourly(constants.MAX_FOLLOWS_PER_HOUR_MIN, constants.MAX_FOLLOWS_PER_HOUR_MAX)
        log_action("Follow count reset")
        follow_tracker.set_randomize_max_unfollow_count_hourly(constants.MAX_UNFOLLOWS_PER_HOUR_MIN, constants.MAX_UNFOLLOWS_PER_HOUR_MAX)
        log_action("Unfollow count reset")
        follow_tracker.set_start_time()
    else:
        log_action("Current follow within 1 hour: " + str(follow_tracker.get_followed_count()))
        log_action("Time elapsed: " + str(follow_tracker.calculate_time_difference()) + " seconds")

    if follow_tracker.is_following_too_many_daily() == True:
        log_action("Daily follow limit reached, sleeping for 24 hours")

        # Sleep for 1 hour, log time to restart
        time_to_start = follow_tracker.get_start_time() + constants.SLEEP_TIME_DAILY
        log_action('Starting again at: ' + str(datetime.datetime.fromtimestamp(time_to_start).strftime('%m/%d %H:%M:%S')))

        time.sleep(constants.SLEEP_TIME_DAILY)
        follow_tracker.reset_follow_count()
        follow_tracker.reset_unfollow_count()
        follow_tracker.reset_total_followed_count()
        follow_tracker.set_randomize_max_follow_count_hourly(constants.MAX_FOLLOWS_PER_HOUR_MIN, constants.MAX_FOLLOWS_PER_HOUR_MAX)
        log_action("Follow count reset")
        follow_tracker.set_randomize_max_unfollow_count_hourly(constants.MAX_UNFOLLOWS_PER_HOUR_MIN, constants.MAX_UNFOLLOWS_PER_HOUR_MAX)
        log_action("Unfollow count reset")
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

    '''
    To use the unfollow method, set the UNFOLLOW_TOGGLE to True in constants.py
    Run /follower_following_utils/compare_follower_following.py to get a list of users to unfollow
    This exports a csv file with the users to unfollow
    '''
    if constants.UNFOLLOW_TOGGLE == True:
        print("Starting unfollow method")
        # check if we should unfollow
        try:
            if follow_tracker.is_unfollowing_too_many_hourly() == False:
                did_we_unfollow = unfollow_users(follow_tracker.get_unfollow_profileUrls(x))
                if did_we_unfollow == True:
                    follow_tracker.increment_unfollowed_count()
                    log_action("Unfollowed user: " + follow_tracker.get_unfollow_profileUrls(x))
                    log_action("Unfollowed count: " + str(follow_tracker.get_unfollowed_count()) + "/" + str(follow_tracker.get_max_unfollowed_count_hourly()))
        except IndexError:
            log_action("No more users to unfollow")
            
    username = go_to_user_profile(follow_usernames[x])
    if username == constants.ACCOUNT_NAME:
        log_action("Found" + constants.ACCOUNT_NAME +", skipping")
        x += 1

    log_action("Searching for " + username)
    remove_user_from_csv(username, constants.CSV_FILE_PATH + constants.CSV_FILE_NAME, constants.FOLLOW_HEADERS)
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

    if (int(following_count) == 0) or (int(follower_count) == 0):
        log_action("Cannot divide by zero, skipping")
        x += 1
        continue


    if ((int(follower_count) / int(following_count) > FOLLOWER_FOLLOWING_RATIO_MAX) or 
        (int(following_count) < MINIMUM_FOLLOWING_COUNT) or 
        (int(posts_count) < MINIMUM_POST_COUNT) or 
        (int(following_count) / int(follower_count) > FOLLOWER_FOLLOWING_RATIO_MAX)):
        log_action("Follower count more than double following count, or low following/posts, skipping")
        x += 1
        continue
    log_action("Criteria matches, continuing to follow")


    # Follow user
    did_we_follow = follow_user(username)
    log_action("Did we follow? " + str(did_we_follow))
    if did_we_follow == True:
        follow_tracker.increment_followed_count()
        follow_tracker.increment_total_followed_count()
        log_action("Total followed count: " + str(follow_tracker.get_total_followed_count()) + "/" + str(follow_tracker.get_max_followed_count_daily()))
        log_action("Followed count:" + str(follow_tracker.get_followed_count()) + "/" + str(follow_tracker.get_max_followed_count_hourly()))
        log_action("Refreshing page")
        pyautogui.hotkey('ctrl', 'r')
        time.sleep(random.uniform(3.0, 5.0))
    
    # Should we start commenting?
    if (constants.COMMENT_TOGGLE == True):
        # Grabbing posts icon location
        posts_icon_location = find_posts_icon_location()
        if (is_account_followable() == True) and (did_we_follow == True) and (posts_icon_location is not None):

            image_one_center, image_two_center, image_three_center = save_first_three_posts(posts_icon_location)
            
            #Check image section for food first
            log_action("Checking image section for food and liking first image")
            save_image_section(posts_icon_location)

            # Liking first image if we followed the user and profile is not private
            pyautogui.moveTo(image_one_center[0], image_one_center[1], -100,
                            duration=random.uniform(0.5, 1.0),
                            tween=pyautogui.easeOutQuad)
            time.sleep(random.uniform(0.7, 1.5))
            pyautogui.click()
            # Find and click heart button
            pyautogui.sleep(random.uniform(1, 2))
            like_heart_location = pyautogui.locateOnScreen("./assets/like_heart.png",
                                                                region=constants.HEART_LIKE_LOCATION,
                                                                confidence=0.8)
            if like_heart_location is not None:
                log_action("Found heart, liking first image")
                pyautogui.moveTo(pyautogui.center(like_heart_location), 
                                duration=random.uniform(0.5, 1.0),
                                tween=pyautogui.easeOutQuad)
                pyautogui.sleep(random.uniform(1, 2))
                pyautogui.click()
            
            # Press escape button to exit of image
            pyautogui.press('esc')
            pyautogui.sleep(random.uniform(1, 2))



            if get_label_matches(send_image_to_clarifai(convert_image_to_bytes(constants.IMAGE_SECTION_PATH))) == True:
                log_action("Found food in image section, commenting")

                # Check images for food
                log_action("Checking images for food")

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
        else:
            log_action("Not following user, or no posts to comment on, skipping")


        #End of loop
    x += 1

log_action("Finished")
print("Finished")

