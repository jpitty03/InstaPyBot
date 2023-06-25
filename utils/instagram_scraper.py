import requests
from bs4 import BeautifulSoup
import re

# Deprecated

class InstagramProfileScraper:
    def __init__(self, username):
        self.username = username
        self.url = f"https://www.instagram.com/{username}/"

    def scrape_counts(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the description meta tag
        description_meta = soup.find('meta', attrs={'name': 'description'})

        # Extract the content attribute of the description meta tag
        description = description_meta.get('content')

        # Extract the follower count and following count using regular expressions
        follower_count = re.search(r'([\d,]+) Followers', description).group(1)
        following_count = re.search(r'([\d,]+) Following', description).group(1)

        # Remove commas from the counts and convert them to integers
        follower_count = int(follower_count.replace(',', ''))
        following_count = int(following_count.replace(',', ''))

        return follower_count, following_count
