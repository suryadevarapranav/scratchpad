# -*- coding: utf-8 -*-
"""Spotify Recommendation System"""

import json
import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/recommend": {"origins": "http://localhost:3000"}})

# Initialize Spotipy client
client_credentials_manager = SpotifyClientCredentials(client_id='d491d8d1fb704aecbfacf6df5d0b193e', client_secret='2a4a064cce9b4295982e3dfbdad3c89e')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Define excluded fields
excluded_fields = ['type', 'id', 'uri', 'track_href', 'analysis_url', 'duration_ms', 'time_signature']

# Function to load song data from JSON file
def load_song_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Function to get Spotify ID from song name
def get_spotify_id(song_name):
    results = sp.search(q=song_name, type='track', limit=1)
    if results['tracks']['items']:
        return results['tracks']['items'][0]['id']
    else:
        return None

# Function to get the audio features of a song based on the song ID
def get_audio_features(song_id):
    try:
        audio_features = sp.audio_features(tracks=[song_id])
        if audio_features and all(key in audio_features[0] for key in ['id', 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']):
            return audio_features[0]
        else:
            print("Error: Invalid audio features.")
            return None
    except Exception as e:
        print("Error:", e)
        return None

# Function to get the song name based on the song ID
def get_song_name(song_id):
    try:
        track_info = sp.track(song_id)
        song_name = track_info['name']
        return song_name
    except Exception as e:
        print("Error:", e)
        return None

# Function to calculate Euclidean distance between two songs based on specified fields
def euclidean_distance(song1, song2, fields):
    distance = np.linalg.norm([float(song1[field]) - float(song2[field]) for field in fields])
    return distance

# Function to recommend similar songs based on specified fields or genre-specific fields
def recommend_similar_songs(input_audio_features, data, num_recommendations=30):
    distances = {}

    fields = [field for field in input_audio_features.keys() if field not in excluded_fields]

    # Calculate distances between input song and all other songs based on specified fields
    for song_id, song_data in data.items():
        if song_id != input_audio_features['id']:
            distance = euclidean_distance(input_audio_features, song_data, fields)
            distances[song_id] = distance

    # Sort distances and get top recommendations
    sorted_distances = sorted(distances.items(), key=lambda x: x[1])
    recommendations = sorted_distances[:num_recommendations]

    return [rec[0] for rec in recommendations]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    file_path = "data/audio_features.json"  # Path to your JSON file
    data = load_song_data(file_path)

    input_data = request.get_json()
    song_name = input_data['song_name']

    input_song_id = get_spotify_id(song_name)

    if input_song_id is None:
        message = "Song not found. Please try again."
        return render_template('index.html', message=message)

    input_audio_features = get_audio_features(input_song_id)

    if input_audio_features:
        print(f"\nAudio Features of the Input Song '{song_name}':")
        for field, value in input_audio_features.items():
            if field not in excluded_fields:
                print(f"{field}: {value}")
    else:
        message = "Failed to retrieve audio features of the input song."
        return render_template('index.html', message=message)

    num_recommendations = int(15)

    recommendations = recommend_similar_songs(input_audio_features, data, num_recommendations)
    recommended_songs = []

    print(f"\nTop {num_recommendations} Recommended Songs:")
    for rec_id in recommendations:
        song_name = get_song_name(rec_id)
        song_audio_features = get_audio_features(rec_id)
        if song_audio_features:
            print(f"\nRecommended Song: {song_name}")
            for field, value in song_audio_features.items():
                if field not in excluded_fields:
                    print(f"{field}: {value}")
        else:
            print(f"\nRecommended Song: {song_name}")
            print("Failed to retrieve audio features for this song.")
        recommended_songs.append(song_name)

    if not recommendations:
        return jsonify({'error': 'No recommendations found'}), 404

    return jsonify({'recommended_songs': recommended_songs})

if __name__ == "__main__":
    app.run(debug=True)