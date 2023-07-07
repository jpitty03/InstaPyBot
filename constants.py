import random
import os
from dotenv import load_dotenv

ACCOUNT_NAME = os.getenv("ACCOUNT_NAME")
COMMENT_TOGGLE = True
UNFOLLOW_TOGGLE = True
MAX_UNFOLLOWS_PER_HOUR_MIN = 6
MAX_UNFOLLOWS_PER_HOUR_MAX = 9
FOLLOW_HEADERS = ['profileUrl', 'username', 'fullName', 'imgUrl', 'id', 'isPrivate', 'isVerified', 'query', 'timestamp']
CSV_FILE_PATH = 'assets/accountData/'
CSV_FILE_NAME = 'happymanbbq.csv'
UNFOLLOW_HEADERS = ['Username']
UNFOLLOW_CSV_PATH = './follower_following_utils/'
UNFOLLOW_CSV_NAME = 'not_following_back.csv'
IMG_PROC = './assets/image_processing/'
IMAGE_PATH = "food_or_nah.png"
COMMENT_ICON_PATH = './assets/comment_icon.png'
IMAGE_SECTION_PATH = './assets/image_processing/image_section.png'
CONFIDENCE_LEVEL = 0.8
MAX_FOLLOWS_PER_HOUR_MIN = 6
MAX_FOLLOWS_PER_HOUR_MAX = 9

MAX_FOLLOWS_PER_DAY_MIN = 65
MAX_FOLLOWS_PER_DAY_MAX = 85

MAX_UNFOLLOWS_PER_HOUR = 25
MAX_LIKES_PER_HOUR = 50
MAX_COMMENTS_PER_HOUR = random.randint(15, 25)
MAX_COMMENTS_PER_HOUR_MIN = 6
MAX_COMMENTS_PER_HOUR_MAX = 9
MAX_MSSG_PER_HOUR = 25
SLEEP_TIME_HOURLY = random.randint(3600, 4000)
SLEEP_TIME_DAILY = random.randint(86000, 90000)
CLARIFAI_API_KEY = os.getenv("CLARIFAI_API_KEY")
CLARIFAI_TOKEN = os.getenv("CLARIFAI_TOKEN")
POST_ONE_PATH = './assets/image_processing/image_one.png'
POST_TWO_PATH = './assets/image_processing/image_two.png'
POST_THREE_PATH = './assets/image_processing/image_three.png'
FOOD_COMMENTS = [
    "TEST COMMENT 1😍🔥🍖",
    "TEST COMMENT 2🍽️🔥"
]
FOOD_LABELS = [
    'food',
    'meat',
    'burger',
    'chicken',
    'beef',
    'pork',
    'seafood',
    'beefsteak',
    'steak',
    'sirloin',
    'ribeye',
    'ribs',
    'pork ribs'
]
FOOD_LABEL_THRESHOLD = 0.9

POSTS_SEARCH_REGION = (611, 116, 988, 925)
POSTS_SEARCH_REGION_HL = (661, 571, 1590 - 661, 606 - 571)
FOLLOW_BUTTON_REGION = (660, 118, 842, 78)
UNFOLLOW_BUTTON_REGION = (752, 672, 1147, 723)
FOLLOWER_FOLLOWING_REGION = (965, 196, 407, 40)
COMMENT_SEARCH_REGION = (28, 967, 1867, 54)


#########################################################
# Image coordinates for 1080p monitor with Highlights
# Deprecated, using a better method to find posts
ONE_LEFT = 652
ONE_TOP = 625
ONE_WIDTH = 959 - ONE_LEFT
ONE_HEIGHT = 932 - ONE_TOP

TWO_LEFT = 966
TWO_TOP = 625
TWO_WIDTH = 1271 - TWO_LEFT
TWO_HEIGHT = 932 - TWO_TOP

THREE_LEFT = 1286
THREE_TOP = 634
THREE_WIDTH = 1592 - THREE_LEFT
THREE_HEIGHT = 939 - THREE_TOP

NON_HL_ARRAY = [
    ONE_LEFT, ONE_TOP, ONE_WIDTH, ONE_HEIGHT,
    TWO_LEFT, TWO_TOP, TWO_WIDTH, TWO_HEIGHT,
    THREE_LEFT, THREE_TOP, THREE_WIDTH, THREE_HEIGHT
]

# Image coordinates for 1080p monitor without Highlights
# Deprecated, using a better method to find posts
ONE_LEFT_NOHL = 653
ONE_TOP_NOHL = 441
ONE_WIDTH_NOHL = 967 - ONE_LEFT_NOHL
ONE_HEIGHT_NOHL = 748 - ONE_TOP_NOHL

TWO_LEFT_NOHL = 974
TWO_TOP_NOHL = 441
TWO_WIDTH_NOHL = 1280 - TWO_LEFT_NOHL
TWO_HEIGHT_NOHL = 748 - TWO_TOP_NOHL

THREE_LEFT_NOHL = 1286
THREE_TOP_NOHL = 441
THREE_WIDTH_NOHL = 1592 - THREE_LEFT_NOHL
THREE_HEIGHT_NOHL = 748 - THREE_TOP_NOHL

HL_ARRAY = [
    ONE_LEFT_NOHL, ONE_TOP_NOHL, ONE_WIDTH_NOHL, ONE_HEIGHT_NOHL,
    TWO_LEFT_NOHL, TWO_TOP_NOHL, TWO_WIDTH_NOHL, TWO_HEIGHT_NOHL,
    THREE_LEFT_NOHL, THREE_TOP_NOHL, THREE_WIDTH_NOHL, THREE_HEIGHT_NOHL
]
#########################################################

SEARCH_X = random.randint(161, 400) # I know, random in a CONSTANT file,
SEARCH_Y = 309                      # but it's a constant for the duration 
                                    # of the program

LOAD_TIME_MIN = 5
LOAD_TIME_MAX = 8
