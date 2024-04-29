# Artist Network Application - README

## Overview
The Artist Network Application visualizes connections between musical artists using data from the Spotify API. It provides an interactive way to explore collaborations and shared playlists, presenting a network graph where nodes are artists and edges represent these connections.

## Features
- **Authentication**: Secure login with Spotify credentials is required to access the API data.
- **Interactive Graph**: Visualize connections between artists based on shared playlists and collaborations within chosen music categories.
- **Artist Profiles**: View detailed information about artists, including genres, popularity, and associated playlists.
- **Search Functionality**: Users can search for artists to explore their profiles and understand their influence within the network graph.
- **Popularity Insights**: The application highlights popular artists by analyzing the network's connections.
- **Extended Network Exploration**: Beyond direct collaborations, users can discover broader connection patterns among artists.

## Interactions and Responses
- Users are prompted to log in with Spotify credentials upon initiating the application.
- After logging in, the user selects a music category to visualize the artist network graph.
- Clicking on an artist node presents detailed information about that artist in a dedicated info panel.
- Searching for an artist will return their profile, and the graph will adjust to highlight their connections.
- The application responds to user queries by fetching and rendering the requested data, updating the UI accordingly.

## Installation and Configuration

### Prerequisites
- Python 3.6+
- Pip (Python package manager)
- Spotify Developer Account for API keys

### Setup Instructions
1. **Obtain API Credentials**:
   - Register an application on the [Spotify Developer Dashboard](https://developer.spotify.com/documentation/web-api).
   - Note the Client ID and Client Secret.
   - Set the redirect URI to `http://127.0.0.1:5000/callback`.

2. **Environment Setup**:
   - Store the Spotify credentials as environment variables or in a `.env` file:
     ```bash
     export SPOTIFY_CLIENT_ID='your_client_id'
     export SPOTIFY_CLIENT_SECRET='your_client_secret'
     ```

3. **Activate the Setup Script**:
   - Make the script executable and initialize the environment:
     ```bash
     chmod +x si507.sh
     ./si507.sh myenv
     ```

4. **Run the Application**:
   - Launch the Flask application:
     ```bash
     flask run
     ```
   - Access the app at `http://127.0.0.1:5000`.

## Caching and API Limitations
The application implements selective caching due to API rate limits and the extensive data size. It stores a subset of music playlist graph files, optimizing the balance between data visualization quality and API usage constraints.

## Dependencies
This application requires the following Python packages:
- Flask: To serve the web application.
- Requests: To make HTTP requests to the Spotify API.
- Networkx: To create and manipulate the network graph.
- Bleach: To sanitize user inputs and prevent XSS attacks.

These dependencies are listed in `requirements.txt` and are installed during the setup process.

## Data Structure and Access
- **Network Graph**: Nodes are artists; edges represent shared playlists.
- **Data Source**: [Spotify API](https://developer.spotify.com/documentation/web-api) (Data in JSON format).
- **Access Method**: Data is fetched through authenticated HTTP requests. Full caching is not implemented to stay within API request limits.
- **Data Summary**: The data includes artist names, genres, popularity scores, and the number of shared playlists.

## Support and Contributions
For detailed API usage and limitations, consult the [Spotify API documentation](https://developer.spotify.com/documentation/web-api). The source code and [Flask documentation](https://flask.palletsprojects.com/en/2.0.x/) provide additional development and troubleshooting guidance.
