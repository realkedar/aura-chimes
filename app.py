from ai import ai_rec
from weather import get_weather
from flask import Flask, session, redirect, request, jsonify, render_template
from spotify import create_spotify_oauth, get_spotify_auth_token, get_user_top_genres, create_personalized_playlist
import spotipy

app = Flask(__name__)
app.secret_key = "meow123"


@app.route("/")
@app.route("/login")
def login():
    auth_url = create_spotify_oauth().get_authorize_url()
    return redirect(auth_url)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    token_info = get_spotify_auth_token(code)
    session["token_info"] = token_info
    return render_template('create.html')

@app.route("/home")
def home():
    token_info = session.get("token_info")
    if not token_info:
        return redirect("/login")

    access_token = token_info["access_token"]
    sp = spotipy.Spotify(auth=access_token)

    user_profile = sp.current_user()
    user_id = user_profile['id']

    # Fetch user’s favorite genres and weather
    genres = get_user_top_genres(access_token)
    weather = get_weather()
    
    # Use weather from weather.py and pass it into ai_rec from ai.py to generate a list of song titles
    titles = ai_rec(weather, genres)
    
    # Create a new playlist
    playlist = sp.user_playlist_create(
        user=user_id,
        name=f"Aura Chimes - Playlist for {weather}",
        public=True,
        description="A playlist generated based on the current weather."
    )
    playlist_id = playlist["id"]

    track_ids = []
    for title in titles:
        results = sp.search(q=title, type="track", limit=1)
        if results["tracks"]["items"]:
            track_ids.append(results["tracks"]["items"][0]["id"])

    # Add tracks to the playlist
    if track_ids:
        sp.playlist_add_items(playlist_id, track_ids)

    playlist_url = playlist["external_urls"]["spotify"]
    
    return render_template('playlist.html', playlist_url=playlist_url)

