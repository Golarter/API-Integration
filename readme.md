# API Integration Challenge

This is a Flask application that allows users to search for movies, view their details (title, release date, genres, and poster), and check the weather on the movie's release date in Bogotá.

## Features
- Search movies using The Movie Database (TMDB) API.
- Display movie details including poster.
- Fetch weather data for Bogotá using Open-Meteo API.

## Requirements
- Python 3.x
- Flask
- Requests

## How to Run the Project

###If your operating system is Windows**
1. . You can download the executable version of the application from the following link: [Download the executable](https://github.com/Golarter/API-Integration/blob/main/dist/app.exe)
    - After clicking the link, you will be redirected to the file's page.
    - Click on the three dots located at the top right of the file section.
    - From the dropdown menu, select "Download" to start downloading the file.
3. Run the program: Once downloaded, simply double-click on the app.exe file to start the application.
   
### Alternative: Run from the source code
1. Clone this repository. git clone
   ```
      https://github.com/Golarter/API-Integration/tree/main
   ```
3. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the application:
   ```
   python app.py
   ```
5. Open your browser and go to `http://127.0.0.1:5000` in case your browser does not open automatically.

## Run the application:
Once the application is running, open your browser and go to http://127.0.0.1:5000.

1. Search for a movie:
    - You will see a simple interface like the one shown in the first image. ![IMAGE 1](https://github.com/Golarter/API-Integration/blob/282809c6fef90019f8476c2c00f66c4f4bd0e693/Templates/IMG%201.jpg)
    - Enter the name of a movie (e.g., "Red One") in the input field labeled "Movie Title."
    - Press Enter or click the Search button to retrieve the results.
2. View the results:
    - The application will display details about the movie and the weather conditions on its release date, as shown in the second image. ![IMAGE 2](https://github.com/Golarter/API-Integration/blob/282809c6fef90019f8476c2c00f66c4f4bd0e693/Templates/IMG%202.jpg)
        - The details include:
        - The city (e.g., Bogotá).
        - The movie title.
        - The release date.
        - The genres of the movie.
        - The minimum and maximum temperatures on the release date.
3. Send the results to the webhook:
    - The application will automatically send the retrieved data to the webhook after fetching the results.
