import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

# Load environment variables
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")

# Scopes: Reading user data & creating/modifying playlists
SCOPES = "user-top-read user-library-read playlist-modify-public playlist-modify-private"

def create_spotify_oauth():
    """Set up Spotify OAuth authentication"""
    return SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope=SCOPES
    )

def get_spotify_auth_token(code):
    """Exchange authorization code for access token"""
    sp_oauth = create_spotify_oauth()
    return sp_oauth.get_access_token(code)

def get_user_top_genres(access_token):
    """Retrieve user's top artists to infer genre preferences"""
    sp = spotipy.Spotify(auth=access_token)
    
    # Get top artists
    top_artists = sp.current_user_top_artists(limit=10)["items"]
    
    genres = set()
    for artist in top_artists:
        genres.update(artist["genres"])  # Each artist may have multiple genres

    return list(genres)  # Return list of unique genres

def search_song(title, access_token):
    """Search for a song by title and return its Spotify URI"""
    sp = spotipy.Spotify(auth=access_token)
    results = sp.search(q=title, limit=1, type="track")

    tracks = results.get("tracks", {}).get("items", [])
    return tracks[0]["uri"] if tracks else None  # Return track URI if found

def create_personalized_playlist(user_id, weather, song_titles, access_token):
    """Create a playlist based on weather and add suggested songs"""
    sp = spotipy.Spotify(auth=access_token)

    # Create a new playlist
    playlist = sp.user_playlist_create(user=user_id, name=f"Weather Vibes: {weather}", public=True)
    playlist_id = playlist["id"]

    # Search for song URIs
    track_uris = [search_song(title, access_token) for title in song_titles if search_song(title, access_token)]

    if track_uris:
        sp.playlist_add_items(playlist_id, track_uris)

    return playlist["external_urls"]["spotify"]  # Return the Spotify playlist link
