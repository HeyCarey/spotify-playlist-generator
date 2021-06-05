
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

WEB_FILE = "website.html"


# reading website.html file which I used copy(document.querySelector('html').outerHTML) to
# copy the html from the Billboard Top 100 because it's written with React
def read_web_file():
    try:
        open(WEB_FILE)
    except FileNotFoundError:
        print(f"You need to save the rendered HTML to {WEB_FILE}")
        exit()
    finally:
        # Read the web page from file
        with open(WEB_FILE, mode="r", encoding="utf-8") as fp:
            content = fp.read()
        return BeautifulSoup(content, "html.parser")


# here I'm pulling out the titles and writing them as a list to titles.txt

titles = open("titles.txt", "w")

soup = read_web_file()
for item in soup.findAll('span', attrs={'class': "chart-element__information__song text--truncate color--primary"}):
    titles.write('\n%s' % item.string)

# using spotipy https://pypi.org/project/spotipy/ to authenticate  with Spotify
# with my unique Client ID/ Client Secret
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id="client_Id",
        client_secret="client_secret",
        redirect_uri="http://example.com",
        scope="playlist-modify-private",
        show_dialog=True,
        cache_path="token.txt"))

user_id = sp.current_user()["id"]

#read song titles in txt file and then create list
list_of_songs = open("titles.txt", "r")
song_names = [line.rstrip("\n") for line in list_of_songs]

#get uri's of songs from spotify
song_uris = []
year = 1972
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

#create playlist
playlist = sp.user_playlist_create(user=user_id, name=year, public=False)
print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)