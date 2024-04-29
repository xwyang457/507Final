import networkx as nx
import json
from .spotify_api import get_playlist_artists
import os
import hashlib

class ArtistGraph:
    def __init__(self):
        """
        Initialize an empty graph to store artist relationships.
        This graph will use artist names as nodes and shared playlists as weights for edges.
        """
        self.graph = nx.Graph()
    
    def reset_graph(self):
        """Clears the current graph to allow for a new build."""
        self.graph.clear()

    def add_artist(self, artist_name, additional_info):
        """
        Add a single artist to the graph or update the artist's details if they already exist.

        Parameters:
            artist_name (str): The name of the artist to add or update.
            additional_info (dict): Additional details about the artist.
        """
        if self.graph.has_node(artist_name):
            # Update the node's attributes with the additional_info
            for key, value in additional_info.items():
                self.graph.nodes[artist_name][key] = value
        else:
            # Add the new artist with the provided additional_info
            self.graph.add_node(artist_name, **additional_info)


    def add_connection(self, artist1, artist2, playlists):
        """
        Add a connection between two artists with the number of shared playlists as weight.
        Increments the weight if the edge already exists.
        
        Parameters:
            artist1 (str): Name of the first artist.
            artist2 (str): Name of the second artist.
            playlists (list): List of playlists that both artists appear on.
        """
        if self.graph.has_edge(artist1, artist2):
            self.graph[artist1][artist2]['weight'] += len(playlists)
        else:
            self.graph.add_edge(artist1, artist2, weight=len(playlists))

    def load_data(self, data):
        """
        Load artist connections from a list of tuples (artist1, artist2, playlists).

        Parameters:
            data (list of tuples): Each tuple contains two artist names and a list of playlists they share.
        """
        for artist1, artist2, playlists in data:
            self.add_artist(artist1)
            self.add_artist(artist2)
            self.add_connection(artist1, artist2, playlists)

    def save_graph(self, filename="graph.json"):
        """
        Serialize the graph to a JSON file.

        Parameters:
            filename (str): The name of the file to save the graph to.
        """
        with open(filename, 'w') as f:
            json.dump(nx.node_link_data(self.graph), f)

    def load_graph(self, filename):
        """
        Deserialize the graph from a JSON file.

        Parameters:
            filename (str): The name of the file to load the graph from.

        Returns:
            bool: True if the graph was successfully loaded, False otherwise.
        """
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                self.graph = nx.node_link_graph(data)
                return True
        except FileNotFoundError:
            return False

    def get_artists(self):
        """
        Return a list of all artists in the graph.

        Returns:
            list: A list of artist names.
        """
        return list(self.graph.nodes())
    
    # def get_artist_details(self, artist_name):
    #     """
    #     Return details for a given artist if they exist in the graph.
        
    #     Parameters:
    #         artist_name (str): The artist name to query details for.
        
    #     Returns:
    #         dict: A dictionary containing artist details (name, connections, playlists).
    #     """
    #     if artist_name in self.graph:
    #         details = {
    #             'name': artist_name,
    #             'connections': len(list(self.graph.neighbors(artist_name))),
    #             'playlists': sum(self.graph[artist_name][n]['weight'] for n in self.graph.neighbors(artist_name))
    #         }
    #         return details
    #     return None

    def get_artist_details(self, artist_name):
        """
        Return details for a given artist if they exist in the graph.
        
        Parameters:
            artist_name (str): The artist name to query details for.
        
        Returns:
            dict: A dictionary containing artist details, including their name, connections,
                shared playlists, and genres.
        """
        if artist_name in self.graph:
            # Basic artist details
            details = {
                'name': artist_name,
                'connections': [],
                'genres': self.graph.nodes[artist_name].get('genres', []),
                'playlists': []
            }
            
            # Gather information about connections and shared playlists
            for neighbor in self.graph.neighbors(artist_name):
                connection_details = {
                    'artist_name': neighbor,
                    'shared_playlists': self.graph[artist_name][neighbor]['playlists']
                }
                details['connections'].append(connection_details)
                details['playlists'].extend(connection_details['shared_playlists'])

            # Remove duplicates from the playlists list
            details['playlists'] = list(set(details['playlists']))

            return details
        return None


    def get_connections(self, artist_name):
        """
        Return connected artists and the weight of their connections.

        Parameters:
            artist_name (str): The artist name to query connections for.

        Returns:
            list: A list of tuples (connected artist name, weight).
        """
        if artist_name in self.graph:
            # return [(n, self.graph[artist_name][n]['weight']) for n in self.graph.neighbors(artist_name)]
            return [n for n in self.graph.neighbors(artist_name)]
        return []

    def find_shortest_path(self, artist1, artist2):
        """
        Find and return the shortest path between two artists, if they're connected.

        Parameters:
            artist1 (str): Name of the first artist.
            artist2 (str): Name of the second artist.

        Returns:
            list: A list of artist names representing the shortest path, or None if no path exists.
        """
        try:
            return nx.shortest_path(self.graph, source=artist1, target=artist2)
        except nx.NetworkXNoPath:
            return None

    def degree_centrality(self, artist_name):
        """
        Calculate and return the degree centrality of an artist.

        Parameters:
            artist_name (str): The artist name to calculate centrality for.

        Returns:
            float: The degree centrality of the artist.
        """
        if artist_name in self.graph:
            return nx.degree_centrality(self.graph)[artist_name]
        return 0

    def betweenness_centrality(self, artist_name):
        """
        Calculate and return the betweenness centrality of an artist.

        Parameters:
            artist_name (str): The artist name to calculate centrality for.

        Returns:
            float: The betweenness centrality of the artist.
        """
        if artist_name in self.graph:
            return nx.betweenness_centrality(self.graph)[artist_name]
        return 0
    
    def get_artist_shared_tracks(self, artist_name):
        """
        Get tracks that the given artist shares with other artists in the graph.
        """
        shared_tracks = {}
        for neighbor in self.graph.neighbors(artist_name):
            playlists = self.graph[artist_name][neighbor].get('playlists', [])
            shared_tracks[neighbor] = playlists
        return shared_tracks

    def get_genres_for_artists(self, artist_names):
        """
        Get genres for the given list of artists.
        """
        genres = {}
        for artist in artist_names:
            artist_info = self.graph.nodes[artist]
            genres[artist] = artist_info.get('genres', [])
        return genres
    
    def recommend_popular_artists(self, top_n=4):
        """
        Recommend the top N most popular artists based on the total weight of their connections.

        Parameters:
            top_n (int): The number of top artists to return.

        Returns:
            list of tuples: Each tuple contains an artist's name and their total connection weight.
        """
        artist_popularity = {}

        for artist in self.graph.nodes():
            total_weight = sum(self.graph[artist][neighbor]['weight'] for neighbor in self.graph.neighbors(artist))
            artist_popularity[artist] = total_weight

        sorted_artists = sorted(artist_popularity.items(), key=lambda item: item[1], reverse=True)
        return sorted_artists[:top_n]
    
    # def build_category_graph(self, playlists_data):
    #     """
    #     Build a graph based on the artists appearing in the playlists.
    #     Each artist is a node, and an edge is created between every pair of artists
    #     who appear in the same playlist. The weight of the edge is incremented for
    #     each additional playlist they share.

    #     Parameters:
    #         playlists_data (list): A list of playlist information, each containing playlist details.
    #     """
    #     for playlist in playlists_data:
    #         playlist_id = playlist['id']
    #         if not self.load_graph(f"data/{playlist_id}.json"):
    #             artists_info = get_playlist_artists(playlist_id)  # Fetch artist details for the playlist
    #             artist_names = list(artists_info.keys())

    #             for i in range(len(artist_names)):
    #                 for j in range(i + 1, len(artist_names)):
    #                     artist1, artist2 = artist_names[i], artist_names[j]
                        
    #                     # Add or update the artists in the graph with their additional info
    #                     self.add_artist(artist1, artists_info[artist1])
    #                     self.add_artist(artist2, artists_info[artist2])

    #                     # Create or update the edge between artist1 and artist2
    #                     if self.graph.has_edge(artist1, artist2):
    #                         self.graph[artist1][artist2]['weight'] += 1
    #                     else:
    #                         self.graph.add_edge(artist1, artist2, weight=1)
    #             self.save_graph(f"data/{playlist_id}.json")

    # def build_category_graph(self, playlists_data):
    #     """
    #     Build a graph where each artist is a node, and an edge is created between every pair
    #     of artists who appear in the same playlist more than once. The weight of the edge
    #     is the count of how many times they have shared in the same playlist.

    #     Parameters:
    #         playlists_data (list): A list of playlist information, each containing playlist details.
    #     """
    #     shared_playlists_count = {}

    #     for playlist in playlists_data:
    #         playlist_id = playlist['id']
    #         if not self.load_graph(f"data/{playlist_id}.json"):
    #             artists_info = get_playlist_artists(playlist_id)
    #             artist_names = list(artists_info.keys())

    #             # Compare each artist in the playlist with every other artist
    #             for i in range(len(artist_names)):
    #                 for j in range(i + 1, len(artist_names)):
    #                     artist1, artist2 = artist_names[i], artist_names[j]
    #                     pair = tuple(sorted([artist1, artist2]))
                        
    #                     if pair in shared_playlists_count:
    #                         shared_playlists_count[pair] += 1
    #                     else:
    #                         shared_playlists_count[pair] = 1

    #                     self.add_artist(artist1, artists_info[artist1])
    #                     self.add_artist(artist2, artists_info[artist2])

    #             self.save_graph(f"data/{playlist_id}.json")

    #     for pair, count in shared_playlists_count.items():
    #         if count > 1:
    #             artist1, artist2 = pair
    #             if self.graph.has_edge(artist1, artist2):
    #                 self.graph[artist1][artist2]['weight'] = max(self.graph[artist1][artist2]['weight'], count)
    #             else:
    #                 self.graph.add_edge(artist1, artist2, weight=count)

    def build_category_graph(self, playlists_data):
        """
        Build a graph where each artist is a node, and an edge is created between every pair
        of artists who appear in the same playlist more than once. The weight of the edge
        is the count of how many times they have shared in the same playlist.
        """
        playlists_string = json.dumps(playlists_data, sort_keys=True)
        hash_object = hashlib.sha256(playlists_string.encode('utf-8'))
        graph_id = hash_object.hexdigest()
        
        self.graph.clear()
        pairs = {}

        if not self.load_graph(f"data/{graph_id}.json"):
            for playlist in playlists_data:
                playlist_id = playlist['id']
                    
                artists_info = get_playlist_artists(playlist_id)
                artist_names = list(artists_info.keys())

                for i in range(len(artist_names)):
                    for j in range(i + 1, len(artist_names)):
                        pair = frozenset([artist_names[i], artist_names[j]])
                        pairs[pair] = pairs.get(pair, 0) + 1
                    
                        # pairs[pair].append(playlist['name'])

                for artist_name, details in artists_info.items():
                    self.add_artist(artist_name, details)

            for pair, shared_count in pairs.items():
                if shared_count > 1:
                    artist1, artist2 = pair
                    if self.graph.has_edge(artist1, artist2):
                        self.graph[artist1][artist2]['weight'] += shared_count
                    else:
                        self.graph.add_edge(artist1, artist2, weight=shared_count)
            
            self.save_graph(f"data/{graph_id}.json")

        return graph_id


# if __name__ == "__main__":
#     ag = ArtistGraph()
#     ag.add_artist("Artist A")
#     ag.add_artist("Artist B")
#     ag.add_connection("Artist A", "Artist B", ["Playlist 1", "Playlist 2"])
#     print(ag.get_connections("Artist A"))
