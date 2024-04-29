import requests
from flask import session, request, redirect, url_for
import time

def init_spotify_auth(client_id, client_secret, redirect_uri):
    """
    Initializes the Spotify OAuth authentication credentials and stores them in the session.

    Parameters:
        client_id (str): The Spotify Client ID.
        client_secret (str): The Spotify Client Secret.
        redirect_uri (str): The URI to which Spotify will redirect the user after authorization is complete.
    """
    session['client_id'] = client_id
    session['client_secret'] = client_secret
    session['redirect_uri'] = redirect_uri

def spotify_login():
    """
    Constructs the Spotify login URL and redirects the user to Spotify's authorization page.

    Returns:
        werkzeug.wrappers.Response: A response object that redirects the user to Spotify's authorization URL.
    """
    auth_url = "https://accounts.spotify.com/authorize"
    response_type = "code"
    scope = "playlist-read-private"
    redirect_uri = session['redirect_uri']
    client_id = session['client_id']
    
    return redirect(f"{auth_url}?response_type={response_type}&client_id={client_id}&scope={scope}&redirect_uri={redirect_uri}")

def spotify_callback():
    """
    Handles the callback from Spotify after user authentication. Retrieves the access token and stores it in the session.

    Returns:
        werkzeug.wrappers.Response: A redirect response to the main index page of the application, 
        either with the user logged in if the token was retrieved successfully, or with an error message otherwise.
    """
    code = request.args.get('code')
    token_url = "https://accounts.spotify.com/api/token"
    redirect_uri = session['redirect_uri']
    client_id = session['client_id']
    client_secret = session['client_secret']

    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.post(token_url, headers=headers, data=payload, auth=(client_id, client_secret))
    token_info = response.json()
    
    if 'access_token' in token_info:
        session['access_token'] = token_info['access_token']
        return redirect(url_for('main.index'))
    else:
        print("Error retrieving access token:", token_info)
        return redirect(url_for('main.index'))
    
def make_spotify_request(url, method='GET', data=None):
    """Make a request to the Spotify API handling authentication and rate limits."""
    headers = {
        'Authorization': f"Bearer {session.get('access_token')}",
        'Content-Type': 'application/json'
    }
    for attempt in range(5):
        if method == 'POST':
            response = requests.post(url, headers=headers, json=data)
        else:
            response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            retry_after = int(response.headers.get('Retry-After', 1))
            print(f"Rate limit exceeded. Retrying after {retry_after} seconds...")
            time.sleep(retry_after)
        else:
            response.raise_for_status()
    raise Exception("Max retry attempts exceeded")

def get_artist_details(artist_id):
    """
    Fetch basic details for a given artist from Spotify, limiting to just the name, genre, and popularity.

    Parameters:
        artist_id (str): The unique Spotify ID for the artist.
    
    Returns:
        dict: A dictionary containing the artist's name, genres, and popularity.
    """
    url = f'https://api.spotify.com/v1/artists/{artist_id}'
    try:
        artist_data = make_spotify_request(url)
        return {
            'name': artist_data['name'],
            'genres': artist_data['genres'],
            'popularity': artist_data['popularity']
        }
    except requests.HTTPError as e:
        print(f"HTTP Error: {e}")
        return None

def get_playlist_artists(playlist_id):
    """
    Fetches the artists and their details from the given Spotify playlist.
    
    Parameters:
        playlist_id (str): The Spotify ID for the playlist.
    
    Returns:
        dict: A dictionary where each key is an artist name and each value is artist details.
    """
    url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
    artist_details = {}
    while url:
        response = make_spotify_request(url)
        for item in response.get('items', []):
            track = item.get('track')
            if track is None:
                continue   
            for artist in track.get('artists', []):
                artist_id = artist['id']
                artist_name = artist['name']
                if artist_id not in artist_details:
                    details = get_artist_details(artist_id)
                    if details:
                        artist_details[artist_name] = details
        url = response.get('next')

    return artist_details

def get_categories():
    """
    Fetches a list of music categories available on Spotify.

    Returns:
        dict: A dictionary containing category details. The expected key in the dictionary is
              'categories', which will hold details including unique identifiers and names for each category.
              
    Raises:
        HTTPError: An error from requests if the HTTP request failed.
    """
    url = 'https://api.spotify.com/v1/browse/categories'
    return make_spotify_request(url)

def get_category_playlists(category_id):
    """
    Fetches playlists for a specified category from Spotify.

    Parameters:
        category_id (str): The Spotify category identifier for which playlists are to be fetched.

    Returns:
        list: A list of dictionaries where each dictionary contains details about a playlist
              within the specified category.

    Raises:
        HTTPError: An error from requests if the HTTP request failed, providing the reason for the failure.
    """
    url = f"https://api.spotify.com/v1/browse/categories/{category_id}/playlists?limit=5"
    return make_spotify_request(url)['playlists']['items']