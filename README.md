# Artist Network Application - README

## Overview
The Artist Network Application is a Flask-powered tool that creates a visual network of musical artists using the Spotify API, showcasing connections based on shared playlists and collaborations.

## Features
- **Authentication**: Users log in with their Spotify credentials.
- **Interactive Graph**: Users can view an interactive graph depicting artist connections.
- **Artist Profiles**: Detailed information about each artist, such as genres and popularity.
- **Search Functionality**: Ability to search for and view specific artists' influence and profiles.
- **Popularity Insights**: Insights into the most popular artists based on network connections.
- **Influence Metrics**: Analysis of artists' influence within the network using centrality measures.
- **Extended Network Exploration**: Users can explore broader artist connections.
  
## Data Source and Interaction

### Origin and Documentation Formats
Data is sourced from the Spotify Web API at various endpoints, returned in JSON format. Detailed endpoint URLs include:
- Artist Details: `https://api.spotify.com/v1/artists/{artist_id}`
- Playlist Artists: `https://api.spotify.com/v1/playlists/{playlist_id}/tracks`
- Music Categories: `https://api.spotify.com/v1/browse/categories`
- Category Playlists: `https://api.spotify.com/v1/browse/categories/{category_id}/playlists`

### Access and Caching
Authenticated HTTP requests are used to access the data. Due to API rate limits, not all data is cached; only a subset is stored, primarily involving some music playlist graph files for efficient data retrieval and visualization.

### Network Graph Organization
The network graph is structured with:
- **Nodes**: Each representing an artist.
- **Edges**: Existing between artists who appear together on two or more playlists. Artists featured together on only one playlist are not linked by an edge.

## Installation and Configuration

### Prerequisites
- Python 3.6+
- Pip
- Spotify Developer Account for API keys

### Setup Instructions
1. **Obtain API Credentials**:
   - Register on the [Spotify Developer Dashboard](https://developer.spotify.com/documentation/web-api).
   - Note your Client ID and Client Secret.
   - Set your redirect URI to `http://127.0.0.1:5000/callback`.

2. **Environment Setup**:
   - Export your Spotify credentials or use a `.env` file:
     ```
     export SPOTIFY_CLIENT_ID='your_client_id'
     export SPOTIFY_CLIENT_SECRET='your_client_secret'
     ```

3. **Activate the Script**:
   - Make the script executable and run it:
     ```
     chmod +x si507.sh
     ./si507.sh <env_name>
     ```

4. **Run the Application**:
   - Launch the Flask app:
     ```
     flask run
     ```

## Dependencies
The application requires several third-party Python packages:
- `Flask`: To create and manage the web server.
- `Requests`: For making HTTP requests to the Spotify API.
- `Networkx`: To manage the graph structure representing artist relationships.
- `Bleach`: For sanitizing inputs to prevent cross-site scripting attacks.

Install these packages using:
```
pip install -r requirements.txt
```

## Usage
After installation, access the application at `http://127.0.0.1:5000` in your web browser, log in with your Spotify credentials, and navigate the features through the web interface.

## Support and Contributions
Consult the Spotify API documentation for usage details and limitations. For custom development or troubleshooting, refer to the source code documentation and the Flask framework guidelines.
