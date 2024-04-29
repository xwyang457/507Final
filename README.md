# Artist Network Application - README

## Overview
The Artist Network Application is a Flask-powered tool that creates a visual network of musical artists. It harnesses data from the Spotify API, illustrating connections between artists based on shared playlists and collaborations.

## Features
- **Authentication**: Secure login with Spotify credentials.
- **Interactive Graph**: Visual representation of artist connections within selected music categories.
- **Artist Profiles**: Access to detailed artist information, including genres, popularity, and associated playlists.
- **Search Functionality**: Locate specific artists and view their influence within the network.
- **Popularity Insights**: Discover popular artists based on network connections.
- **Extended Network Exploration**: Investigate broader artist connections beyond direct collaborations.

## Installation and Configuration

### Prerequisites
- Python 3.6+
- Pip (Python package manager)
- Spotify Developer Account (for API keys)

### Setup Instructions

1. **Obtain API Credentials**:
   - Register an application on the [Spotify Developer Dashboard](https://developer.spotify.com/documentation/web-api).
   - Note down the Client ID and Client Secret.
   - Set `http://127.0.0.1:5000/callback` as the redirect URI.

2. **Environment Setup**:
   - Export the Spotify credentials as environment variables:
     ```bash
     export SPOTIFY_CLIENT_ID='your_client_id'
     export SPOTIFY_CLIENT_SECRET='your_client_secret'
     ```
   - Alternatively, use a `.env` file to store these variables.

3. **Activate the Script**:
   - Make the setup script executable and run it:
     ```bash
     chmod +x si507.sh
     ./si507.sh myenv
     ```
   - Replace `myenv` with your desired environment name. This will create and activate a virtual environment, and install the necessary dependencies.

4. **Run the Application**:
   - Start the Flask application using:
     ```bash
     flask run
     ```
   - Access the app in a web browser at `http://127.0.0.1:5000`.

## Usage

Navigate the application through the web interface. Authenticate with Spotify, select a category to view the artist graph, and use search features to explore artist details.

## Caching and API Limitations

Due to Spotify API's rate limits and the extensive size of data, the application does not cache all data. Currently, it stores a subset of music playlist graph files. This selective caching strategy aims to balance between providing valuable data visualizations and staying within the API usage constraints.

## Dependencies

The application requires the following Python packages:
- Flask
- Requests
- Networkx
- Bleach

All dependencies are listed in `requirements.txt` and are installed during the setup process.

## Data Structure and Access

- **Network Graph**: Nodes represent artists; edges reflect shared playlists.
- **Data Source**: Spotify API (JSON format).
- **Access**: Data is retrieved using authenticated HTTP requests. Due to API limits, not all data is cached.
- **Data Summary**: The application processes numerous variables, including artist names, genres, and popularity, with a focus on visual clarity and network representation.

## Support and Contributions

Refer to the Spotify API documentation for detailed usage and limitations. The source code and Flask documentation offer additional guidance for custom development or troubleshooting.
