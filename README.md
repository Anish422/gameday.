# gameday.

[![Watch the video](https://img.youtube.com/vi/A5HN5pMBneY/maxresdefault.jpg)](https://www.youtube.com/watch?v=A5HN5pMBneY)

gameday. is an interactive web application designed for NFL enthusiasts, analysts, and casual viewers alike. It provides a comprehensive breakdown of matchups between any two NFL teams, offering real-time statistics, key player performance, and a detailed history of previous encounters.

## Features
- Select two NFL teams to compare their current statistics.
- View historical matchups between the two teams over the last five years.
- Visual presentation of key players and team stats for each matchup.

## Tech Stack
- **Python**: Backend powered by Flask.
- **HTML/CSS**: Frontend UI with a modern design using styled HTML and custom CSS.
- **JavaScript**: Handles fetching and displaying data dynamically.
- **NFL API**: Data is retrieved using the NFL API from RapidAPI.

## Try it Yourself

Flask deployment not currently active. To test the app locally, follow these steps:

1) Clone the Repository
2) Substitute the API key in app.py with your own key from [Rapid API - NFL](https://rapidapi.com/Creativesdev/api/nfl-api-data/playground/apiendpoint_de643883-47b6-44c2-b8b8-fd39f4f9170a)
3) pip install Flask requests
4) Open your browser and navigate to http://127.0.0.1:5000/
5) Play around with gameday.
