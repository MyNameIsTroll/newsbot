import feedparser
from mastodon import Mastodon
import json
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

# Créez une nouvelle instance de l'API Mastodon dans /settings/applications et copiez vos identifiants.
mastodon = Mastodon(
    client_id='xxx',
    client_secret='xxx',
    access_token='xxx',
    api_base_url='https://xxx.tld'  # Remplacez par l'URL de votre instance
)

# Lire les flux RSS à partir d'un fichier texte
with open('/HOME/USER/PATH/rss_feeds.txt', 'r') as f: # Modifiez par votre chemin
    rss_feeds = f.readlines()

# Lire les liens déjà publiés à partir d'un fichier json
try:
    with open('/HOME/USER/PATH/published_links.json', 'r') as f: # Modifiez par votre chemin
        published_links = json.load(f)
except FileNotFoundError:
    published_links = []

# Lire la dernière fois que le cache a été vidé à partir d'un fichier
try:
    with open('/home/pi/mes_bots/rts_bot/last_cache_clear.txt', 'r') as f:
        last_cache_clear_str = f.read().strip()  # Supprime les espaces blancs au début et à la fin
        if last_cache_clear_str:  # Vérifie si la chaîne n'est pas vide
            last_cache_clear = datetime.strptime(last_cache_clear_str, "%Y-%m-%d %H:%M:%S.%f")
        else:
            last_cache_clear = datetime.now()
except FileNotFoundError:
    last_cache_clear = datetime.now()

post_limit = 3  # Limite du nombre de toots par exécution du script (défaut = 3)
time_limit = datetime.now() - timedelta(days=1)  # Limite de temps pour les articles du flux RSS, poste uniquement les nouvelles entrées datant de moins d'un jour.
post_count = 0  # Compteur du nombre de toots

for feed in rss_feeds:
    d = feedparser.parse(feed)
    for entry in d.entries:
        if post_count >= post_limit:
            break
        published_time = datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %Z")
        if entry.link not in published_links and published_time > time_limit:
            # Format du post
            soup = BeautifulSoup(entry.summary, "html.parser")
            clean_summary = soup.get_text()
            post = f"{entry.title}\n{entry.link}\n{clean_summary}"
            if len(post) > 500:
                post = post[:497] + "..."
            mastodon.status_post(post)
            published_links.append(entry.link)
            post_count += 1

# Enregistrer les liens déjà publiés dans un fichier json
with open('/home/pi/mes_bots/rts_bot/published_links.json', 'w') as f:
    json.dump(published_links, f)

# Vider le cache chaque semaine
if datetime.now() - last_cache_clear > timedelta(weeks=1):
    published_links = []
    last_cache_clear = datetime.now()
    # Enregistrer la dernière fois que le cache a été vidé dans un fichier
    with open('/home/pi/mes_bots/rts_bot/last_cache_clear.txt', 'w') as f:
        f.write(last_cache_clear.strftime("%Y-%m-%d %H:%M:%S.%f"))
