import random

ACCOUNT_NAME = 'bbqsprinkles'
CSV_FILE = 'assets\\accountData\\happymanbbq.csv'
IMG_PROC = './assets/image_processing/'
IMAGE_PATH = "food_or_nah.png"
COMMENT_ICON_PATH = './assets/comment_icon.png'
IMAGE_SECTION_PATH = './assets/image_processing/image_section.png'
CONFIDENCE_LEVEL = 0.8
MAX_FOLLOWS_PER_HOUR = 25
MAX_UNFOLLOWS_PER_HOUR = 25
MAX_LIKES_PER_HOUR = 50
MAX_COMMENTS_PER_HOUR = 25
MAX_MSSG_PER_HOUR = 25
CLARIFAI_API_KEY = '580f314b8c9640af9c462b31396f9553'
CLARIFAI_TOKEN = '85d0e66beb94408285b55dbb13be4edf'
POST_ONE_PATH = './assets/image_processing/image_one.png'
POST_TWO_PATH = './assets/image_processing/image_two.png'
POST_THREE_PATH = './assets/image_processing/image_three.png'
FOOD_COMMENTS = [
    "Are you freaking kidding me?!? 😍🔥🍖",
    "Now that's looking tasty! 🍽️🔥",
    "Mouthwatering to say the least. What's the recipe? 🤤",
    "Great pic! Wish I could taste it through the screen! 😂🍗",
    "Damn, that looks so delicious! 👏🍔",
    "Your food game is strong! 💪🔥",
    "Nice! Would love to join in the BBQ fun next time! 🥳🍖",
    "Can almost smell it from here. 👃💨",
    "This plate is a food lover's dream! ❤️",
    "Looks incredibly juicy. Great job! 🥩👌",
    "This picture alone has me drooling. 😋",
    "Can't wait to try this at our next cookout! Thanks for the inspiration! 🌟",
    "It's eatin' time somewhere, right? 🌎🔥",
    "Meats and good times. Nothing beats that combo! 🎉",
    "Wish I could reach in and grab a bite! 😆",
    "You are the grill master! 🔥🍴",
    "Fantastic spread! Need an extra guest at your next cookout? 😉",
    "Is there anything better than food cooked over a flame? I think not! 🍔🔥",
    "Smoky, savory, and scrumptious! 🍖💯",
    "Needs more BBQ Sprinkles! 🍖💯",
    "Good food, good friends, and good times. This captures it all. ❤️",
    "That looks amazing! Care to share the recipe? 😏",
    "Delicious! I can almost hear the sizzle from here. 🔥",
    "Cooked to perfection! Bravo! 👏👏",
    "Foodie goals right there! 🏆🔥",
    "Is there room for one more at this feast? 😍",
    "Now this is my kind of comfort food. 🥰🍖",
    "That's a picture-perfect meal! 📸",
    "The smokiness from BBQ...there's just nothing like it! 🍖🔥",
    "Those sides look as good as the BBQ! 🥗🍖",
    "The golden brown color on that chicken! Perfection! 🍗✨",
    "This is food art at its finest! 🖼️🍖",
    "Now that's a sight for sore eyes! 😍🍔",
    "👌🔥",
    "BBQ done right. Looks delicious! 🌟",
    "Food bliss right there! 😇",
    "Getting serious BBQ envy right now! 😅",
    "What kind of hardware you cookin with? ",
    "Check us out if you want, if not, no worries, you're killin it! 💪🔥"
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
FOLLOWER_FOLLOWING_REGION = (965, 196, 407, 40)
COMMENT_SEARCH_REGION = (28, 967, 1867, 54)

# Image coordinates for 1080p monitor with Highlights
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
