import webbrowser
from flask import Flask, request, render_template
import requests
from datetime import datetime
import threading

# Initialize Flask application
app = Flask(__name__)

# API keys and URLs for external services
TMDB_API_KEY = "bcfc82367910e4c2f07a6e9991113c41"  # API key for The Movie Database (TMDB)
WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"  # Base URL for Open-Meteo API
WEBHOOK_URL = "https://eo9m0nh4z7lacho.m.pipedream.net"  # Webhook URL to send combined data

# Function to fetch all movie genres from TMDB
def get_genres():
    """
    Fetch the list of movie genres from TMDB API and map genre IDs to genre names.
    :return: A dictionary mapping genre IDs to their respective names.
    """
    url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={TMDB_API_KEY}"
    response = requests.get(url).json()
    return {genre["id"]: genre["name"] for genre in response["genres"]}

@app.route("/", methods=["GET", "POST"])
def index():
    """
    Main route to handle user input (movie search) and display movie and weather data.
    """
    if request.method == "POST":
        # Get the movie title input from the user
        movie_title = request.form["movie_title"]

        # Fetch movie data from TMDB API
        tmdb_url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movie_title}"
        movie_response = requests.get(tmdb_url).json()

        # Check if any movie results were returned
        if not movie_response["results"]:
            return render_template("index.html", error="Movie not found.")

        # Extract movie details from the first result
        movie = movie_response["results"][0]
        movie_title = movie["title"]
        release_date = movie["release_date"]
        genre_ids = movie.get("genre_ids", [])

        # Validate that the release date is within the supported range for weather data
        start_date_limit = datetime.strptime("2016-01-01", "%Y-%m-%d")  # Minimum date supported
        end_date_limit = datetime.strptime("2025-01-19", "%Y-%m-%d")    # Maximum date supported
        release_date_obj = datetime.strptime(release_date, "%Y-%m-%d")  # Convert release date to datetime

        if release_date_obj < start_date_limit or release_date_obj > end_date_limit:
            return render_template("index.html", error="Weather data is not available for the movie's release date.")

        # Map genre IDs to genre names using the get_genres function
        genres_map = get_genres()
        genres = ", ".join([genres_map.get(genre_id, "Unknown") for genre_id in genre_ids])

        # Prepare parameters for the weather API request
        weather_params = {
            "latitude": 4.711,  # Latitude of Bogotá
            "longitude": -74.072,  # Longitude of Bogotá
            "start_date": release_date,  # Movie's release date
            "end_date": release_date,    # Same as start_date for a single day's weather
            "daily": "temperature_2m_min,temperature_2m_max",  # Required weather data: min and max temperatures
        }
        weather_response = requests.get(WEATHER_API_URL, params=weather_params).json()

        # Debugging: Print weather API response
        print("Weather API Response:", weather_response)

        # Extract daily weather data
        weather = weather_response.get("daily", {})

        # Handle missing weather data
        if "temperature_2m_min" not in weather or "temperature_2m_max" not in weather:
            return render_template("index.html", error="Weather data not available for the given date.")

        # Safely extract weather data, handle potential errors
        try:
            min_temp = weather["temperature_2m_min"][0]  # Minimum temperature
            max_temp = weather["temperature_2m_max"][0]  # Maximum temperature
        except (KeyError, IndexError):
            return render_template("index.html", error="Weather data not available for the given date.")

        # Prepare data to send to the webhook
        data_to_send = {
            "city": "Bogotá",  # Hardcoded city name
            "movie_title": movie_title,  # Title of the movie
            "release_date": release_date,  # Release date of the movie
            "genres": genres,  # Genres of the movie
            "min_temperature": min_temp,  # Minimum temperature on the release date
            "max_temperature": max_temp,  # Maximum temperature on the release date
        }

        # Send the combined data to the webhook
        requests.post(WEBHOOK_URL, json=data_to_send)

        # Render the template with the retrieved data
        return render_template("index.html", data=data_to_send)

    # Render the initial template for GET requests
    return render_template("index.html")

# Run the application in debug mode for development
if __name__ == "__main__":
    # Open the application in the default web browser
    threading.Timer(1.0, lambda: webbrowser.open("http://127.0.0.1:5000")).start()
    app.run(debug=False) 