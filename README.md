**README for Spotify API Application**

## Overview

This Spotify API Application utilizes the Spotify Web API to visualize relationships between musical artists based on their shared playlists. By integrating with Spotify's extensive music database, this tool provides insights into artist connections and network dynamics within the music industry.

## Features

- **User Authentication:** Secure Spotify OAuth integration.
- **Dynamic Graph Visualization:** Using D3.js to represent artist networks.
- **Artist Search Functionality:** Search and analyze artist details.
- **Popularity Metrics:** View popular artists and their influence within the network.

## Prerequisites

- Python 3.x
- Flask
- NetworkX
- Requests
- D3.js (via HTML CDN)
- Flask-Caching (optional for improved performance)

## Installation

1. **Clone the Repository:**
   ```bash
   git clone <repository-url>
   ```

2. **Set Up Environment:**
   Ensure you have root privileges or use `sudo` to execute scripts and setup commands.

3. **Run Setup Script:**
   Use the provided `si507.sh` shell script to create and activate a virtual environment, install dependencies, and start the Flask application:
   ```bash
   sudo ./si507.sh <env_name>
   ```

### Script Details (`si507.sh`)

- **Creates** and activates a virtual environment named as per the user's input.
- **Installs** all dependencies listed in `requirements.txt`.
- **Configures** and runs the Flask application with environment variables for development.
- **Cleans up** by deactivating the virtual environment after running the application.

## Configuration

- **Spotify API Credentials:**
  - Obtain Client ID and Client Secret from the Spotify Developer Dashboard.
  - Set the Redirect URI in your Spotify application settings to `http://127.0.0.1:5000/callback`.

## Running the Application

After setting up the environment and dependencies using the `si507.sh` script, the Flask application will be accessible at:
```
http://localhost:5000/
```
Navigate to this URL in a web browser to start using the application.

## Data Handling

- **DataStructure.py:** Manages the artist graph using NetworkX.
- **Spotify_api.py:** Handles API requests to Spotify for fetching artist and playlist data.
- **Views.py:** Flask routes that render the application's web pages and handle API routing.

## Additional Notes

- Ensure to comply with Spotify's API terms of service, particularly regarding rate limits and data usage.
- Customize the `si507.sh` script as needed to match your Flask application file names or additional configurations.
