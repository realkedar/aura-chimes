from flask import Flask, session, redirect, request, jsonify
from spotify import create_spotify_oauth, get_spotify_auth_token, get_user_top_genres, create_personalized_playlist
import spotipy

app = Flask(__name__)
