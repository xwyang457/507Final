from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
from .spotify_api import init_spotify_auth, spotify_login, spotify_callback, get_categories, get_category_playlists
from app.DataStructure import ArtistGraph
import networkx as nx
from bleach import clean
# from . import cache

main = Blueprint('main', __name__)

artist_graph = ArtistGraph()

@main.route('/')
def index():
    """Serve the main page of the application."""
    if 'access_token' not in session:
        return redirect(url_for('.login'))
    return render_template('index.html')

@main.route('/login')
def login():
    """Initiate Spotify authentication and redirect to Spotify login page."""
    # Daniel
    # init_spotify_auth(client_id='d9c140d61d4a4741bb16eb41c30dd808',
    #                   client_secret='96cd44a7f467455e9825c5e7d9cf89b8',
    #                   redirect_uri='http://127.0.0.1:5000/callback')

    # Zheng Yuan
    init_spotify_auth(client_id='05ab55ac16ae49db815cc23f3756e576',
                      client_secret='385ee47a7fc14496a6fcc57b60d5d6a3', 
                        redirect_uri='http://127.0.0.1:5000/callback')
    return spotify_login()

@main.route('/callback')
def callback():
    """Handle the callback from Spotify authentication."""
    spotify_callback()
    # session['logged_in'] = True
    return redirect(url_for('main.categories'))

@main.route('/spotify/categories', methods=['GET'])
def categories():
    """Retrieve and display Spotify categories to the user."""
    if 'access_token' not in session:
        return redirect(url_for('.login'))
    categories = get_categories()
    categories = categories.get('categories', {}).get('items', [])
    return render_template('index.html', categories=categories)

@main.route('/api/artist_network/category/<category_id>')
def artist_network_by_category(category_id):
    """
    Build and return a graph of artists based on the selected Spotify category.
    Extracts playlists for a category and uses them to build the graph.
    """
    playlists = get_category_playlists(category_id)
    #artist_graph.reset_graph()
    artist_graph.build_category_graph(playlists)
    data = nx.readwrite.json_graph.node_link_data(artist_graph.graph) 
    return jsonify(data)

##############################################################################################
# @cache.cached(timeout=86400)
@main.route('/api/search_artist/<path:artist_name>', methods=['GET'])
def get_artist(artist_name):
    """Return details about an artist, including their connections and influence metrics."""
    try:
        artist_name = clean(artist_name)
        artist_details = artist_graph.get_artist_details(artist_name)
        if artist_details:
            connections = artist_graph.get_connections(artist_name)
            degree = artist_graph.degree_centrality(artist_name)
            betweenness = artist_graph.betweenness_centrality(artist_name)

            artist_info = {
                'details': artist_details,
                'connections': connections,
                'influence': {
                    'degree_centrality': degree,
                    'betweenness_centrality': betweenness
                }
            }
            return jsonify(artist_info), 200
        else:
            return jsonify({'error': 'Artist not found'}), 404
    except KeyError:
        return jsonify({'error': 'Artist not found'}), 403
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# @cache.cached(timeout=86400)
@main.route('/api/artist_details/<path:artist_name>', methods=['GET'])
def artist_details(artist_name):
    """
    Retrieves detailed information about an artist, including their connections and genres.

    Parameters:
        artist_name (str): The name of the artist, URL-encoded if necessary.

    Returns:
        jsonify: A JSON response containing the artist's connections and genre details,
                 or an error message if the artist is not found.

    Raises:
        HTTP 404: If the specified artist cannot be found in the graph.
    """
    try:
        connections = artist_graph.get_connections(artist_name)
        genres = artist_graph.get_genres_for_artists(connections)
        
        details = {
            'connections': connections,
            'genres': genres
        }
        return jsonify(details), 200
    except KeyError:
        return jsonify({'error': 'Artist not found'}), 404

    
@main.route('/api/recommend/popular_artists', methods=['GET'])
def get_popular_artists():
    """
    Retrieves a list of the most popular artists based on the total weight of their connections.

    Returns:
        jsonify: A JSON response containing a list of the most popular artists,
                 or an error message if there is an issue calculating popularity.

    Raises:
        HTTP 500: If there is an internal server error while processing the request.
    """
    try:
        popular_artists = artist_graph.recommend_popular_artists()
        return jsonify(popular_artists), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@main.route('/api/recommend/<artist_name>/influence', methods=['GET'])
def artist_influence(artist_name):
    """Return influence metrics for the specified artist within the network."""
    try:
        degree = artist_graph.degree_centrality(artist_name)
        betweenness = artist_graph.betweenness_centrality(artist_name)
        return jsonify({
            'degree_centrality': degree,
            'betweenness_centrality': betweenness
        }), 200
    except KeyError:
        return jsonify({'error': 'Artist not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/api/artists/<artist_name>/extended-connections', methods=['GET'])
def get_extended_connections(artist_name):
    """
    Return extended connections of the specified artist, exploring up to second-degree connections.
    """
    try:
        first_degree_connections = artist_graph.get_connections(artist_name)
        extended_connections = {}

        for connection in first_degree_connections:
            secondary_connections = artist_graph.get_connections(connection)
            extended_connections[connection] = secondary_connections

        return jsonify({
            'first_degree': first_degree_connections,
            'extended': extended_connections
        }), 200
    except KeyError:
        return jsonify({'error': 'Artist not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

