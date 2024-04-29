## Overview

This application leverages the Spotify Web API to explore and visualize relationships between musical artists based on shared playlists. The project utilizes the Flask web application framework, D3.js for visualization, and a network graph to display connections between artists.

## Installation and Setup

### Prerequisites

- Python 3.x
- Flask
- NetworkX
- Requests
- D3.js (via HTML CDN)
- Optional: Flask-Caching for enhanced performance

### Configuration

1. **Clone the Repository**:
   - Ensure git is installed on your system.
   - Clone this repository to your local machine using `git clone <repository-url>`.

2. **Install Required Python Libraries**:
   - Run `pip install flask networkx requests` in your command line.
   - Optionally, install `flask-caching` if you plan to use caching features.

3. **Environment Setup**:
   - Set environment variables as needed, especially for `FLASK_APP` and `FLASK_ENV`.

### Spotify API Configuration

- Obtain a Client ID and Client Secret from the Spotify Developer Dashboard.
- Create an application on the Spotify Developer Dashboard.
- Configure the Redirect URI in your Spotify app settings to match the callback URI in the Flask app.

#### Detailed Steps
1. Visit the [Spotify Developer Dashboard](https://developer.spotify.com/documentation/web-api).
2. Log in and follow the instructions to create an application.
3. Once created, note down your Client ID and Client Secret.
4. Set up the Redirect URI, such as `http://127.0.0.1:5000/callback`, ensuring it matches the one configured in your Flask application.

## Running the Application

1. **Start the Flask Server**:
   - Navigate to the root directory of your cloned repository.
   - Run `flask run` to start the application.
   - Visit `http://localhost:5000/` in your web browser to interact with the application.

2. **Using the Application**:
   - Log in using your Spotify credentials.
   - Explore various categories and visualize the artist network.
   - Search for specific artists, check out popular artists, and their influence within the network.

## Project Structure

### Backend (`*.py` Files)

- **`DataStructure.py`**:
  - Manages the artist graph with functionalities to add artists, connections, and serialize/deserialize the graph.

- **`Spotify_api.py`**:
  - Handles authentication and communication with the Spotify Web API to fetch artist and playlist data.

- **`Views.py`**:
  - Flask routes for the web application, handling user interactions, session management, and rendering templates.

### Frontend (`*.html` Files)

- **HTML and JavaScript**:
  - Uses D3.js to visualize the artist network graph.
  - Interactive elements allow users to search for artists, view artist details, and explore artist connections.

### Network Graph

- **Nodes**: Represent individual artists.
- **Edges**: Represent connections between artists, quantified by the number of shared playlists.

## Data Sources

- **Spotify Web API**:
  - **URL**: [Spotify Web API Documentation](https://developer.spotify.com/documentation/web-api)
  - **Data Format**: JSON
  - **Access Method**: Using the `requests` library for API requests.

## Additional Information

- Ensure all interactions with the Spotify API comply with the terms of service, especially regarding data usage and API call limits.
- The application is configured for development environments. For production environments, ensure settings like HTTPS and secure token and session management.
