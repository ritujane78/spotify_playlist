import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri="http://example.com",
                                               scope="playlist-modify-private",
                                               show_dialog=True,
                                               cache_path="token.txt",
                                               username= 12163618671))
user_id = sp.current_user()["id"]
print(user_id)

date = input("which year do you want to travel to? Type the date in this format: YYYY-MM-DD:")

header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"}

response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}", headers=header)
billboard_page = response.text

soup=BeautifulSoup(billboard_page, 'html.parser')
# print(soup)
title_songs = soup.find_all("li", class_="o-chart-results-list__item")
artists = soup.find_all(name="span", class_="c-label")
# print(artists)
song_names= []
artists_100 = []

for song in title_songs:
    title = song.find("h3")

    if title:
        song_names.append(title.getText().strip())
        artists_100.append(song.find("span").getText().strip())

# print(song_names)
# print(artists_100)


song_uris = []
year = date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    # print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")


# print(song_uris)

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
# print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
print("Playlist Created!!")
