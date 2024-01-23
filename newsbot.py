import feedparser
from mastodon import Mastodon
import json
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

# Create a new instance of the Mastodon API in /settings/applications (+ new application) and copy your credentials.
mastodon = Mastodon(
    client_id='xxx',
    client_secret='xxx',
    access_token='xxx',
    api_base_url='https://xxx.tld'  # Replace with the URL of your instance
)

# Read RSS feeds from a text file
with open('/HOME/USER/PATH/rss_feeds.txt', 'r') as f: # Modify your path
    rss_feeds = f.readlines()

# Read links already published from a json file
try:
    with open('/HOME/USER/PATH/published_links.json', 'r') as f: # Modify your path
        published_links = json.load(f)
except FileNotFoundError:
    published_links = []

# Read the last time the cache was cleared from a file
try:
    with open('/HOME/USER/PATH/last_cache_clear.txt', 'r') as f: # Modify your path
        last_cache_clear_str = f.read().strip()  # Removes leading and trailing white space
        if last_cache_clear_str: # Checks if the string is not empty
            last_cache_clear = datetime.strptime(last_cache_clear_str, "%Y-%m-%d %H:%M:%S.%f")
        else:
            last_cache_clear = datetime.now()
except FileNotFoundError:
    last_cache_clear = datetime.now()

post_limit = 3  # Limit number of toots per script execution (default = 3)
time_limit = datetime.now() - timedelta(days=1)  # Time limit for RSS feed articles, post only new entries less than one day old.
post_count = 0  # Toots counter, do not modify

for feed in rss_feeds:
    d = feedparser.parse(feed)
    for entry in d.entries:
        if post_count >= post_limit:
            break
        published_time = datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %Z")
        if entry.link not in published_links and published_time > time_limit:
            # Publishing format
            soup = BeautifulSoup(entry.summary, "html.parser")
            clean_summary = soup.get_text()
            post = f"{entry.title}\n{entry.link}\n{clean_summary}"
            if len(post) > 500:
                post = post[:497] + "..."
            mastodon.status_post(post)
            published_links.append(entry.link)
            post_count += 1

# Save previously published links in a json file
with open('/HOME/USER/PATH/published_links.json', 'w') as f: # Modify your path
    json.dump(published_links, f)

# Empty cache weekly
if datetime.now() - last_cache_clear > timedelta(weeks=1):
    published_links = []
    last_cache_clear = datetime.now()
    # Save the last time the cache was cleared in a file
    with open('/HOME/USER/PATH/last_cache_clear.txt', 'w') as f:
        f.write(last_cache_clear.strftime("%Y-%m-%d %H:%M:%S.%f"))
