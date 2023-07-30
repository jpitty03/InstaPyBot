import builtins
import json
import csv

'''
To use this script, you need to download your data from Instagram.
To do this, go to your Instagram profile, click the gear icon, and click "Privacy and Security".
Scroll down to "Data Download" and click "Request Download".

Once you've downloaded the data, unzip the file and copy the 
following.json and followers_1.json files into the same directory as this script.
The script will place the order from earliest to latest in a CSV file called not_following_back.csv.
'''

# Load the following.json file
with builtins.open('follower_following_utils\\following.json', 'r') as following_file:
    following_data = json.load(following_file)

# Load the followers_1.json file
with builtins.open('follower_following_utils\\followers_1.json', 'r') as followers_file:
    followers_data = json.load(followers_file)

# Extract the usernames and timestamps from following_data
following_info = [(entry['string_list_data'][0]['value'], entry['string_list_data'][0]['timestamp']) for entry in following_data['relationships_following']]

# Extract the usernames from followers_data
followers_usernames = set(entry['string_list_data'][0]['value'] for entry in followers_data)

# Find the users you are following but who are not following you back
not_following_back_info = [(username, timestamp) for username, timestamp in following_info if username not in followers_usernames]

# Sort the not_following_back_info list based on the timestamp (earliest to latest)
not_following_back_info.sort(key=lambda x: x[1])

# Write the results to a CSV file in order from earliest to latest
with open('follower_following_utils\\not_following_back.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Username'])
    writer.writerows(not_following_back_info)

print("Results written to not_following_back.csv")

unfollow_profile_usernames = []
with open('follower_following_utils\\not_following_back.csv', 'r', newline='', encoding='latin-1') as csvfile:
    # Read the CSV file
    reader = csv.DictReader(csvfile)
    for row in reader:
        username = row['Username']
        unfollow_profile_usernames.append(username)

print(unfollow_profile_usernames)
