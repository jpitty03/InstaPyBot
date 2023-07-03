import builtins
import json
import csv

'''
To use this script, you need to download your data from Instagram.
To do this, go to your Instagram profile, click the gear icon, and click "Privacy and Security".
Scroll down to "Data Download" and click "Request Download".

Once you've downloaded the data, unzip the file and copy the 
following.json and followers_1.json files into the same directory as this script.
'''

# Load the following.json file
with builtins.open('follower_following_utils\\following.json', 'r') as following_file:
    following_data = json.load(following_file)

# Load the followers_1.json file
with builtins.open('follower_following_utils\\followers_1.json', 'r') as followers_file:
    followers_data = json.load(followers_file)

# Extract the usernames from following_data
following_usernames = set(entry['string_list_data'][0]['value'] for entry in following_data['relationships_following'])

# Extract the usernames from followers_data
followers_usernames = set(entry['string_list_data'][0]['value'] for entry in followers_data)

# Find the users you are following but who are not following you back
not_following_back = following_usernames - followers_usernames

# Write the results to a CSV file
with open('follower_following_utils\\not_following_back.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Username'])
    writer.writerows([[username] for username in not_following_back])

print("Results written to not_following_back.csv")
