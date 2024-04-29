function fetchGraphData(categoryId) {
    if (!categoryId) return;

    console.trace('Fetching graph data for category:', categoryId);

    // Assuming you have modified the API endpoint to accept a category ID
    fetch(`/api/artist_network/category/${categoryId}`)
        .then(response => response.json())
        .then(graph => {
            if (graph.nodes && graph.nodes.length > 0) {
                drawGraph(graph);
            } else {
                console.log('Graph data is empty or malformed');
            }
        })
        .catch(error => console.error('Error fetching graph data:', error));
}

function drawGraph(graph) {
    d3.select("#graph svg").remove(); // Remove any existing graph before drawing a new one

    const width = document.getElementById('graph').clientWidth;
    const height = document.getElementById('graph').clientHeight;

    const svg = d3.select("#graph").append('svg')
        .attr('width', width)
        .attr('height', height)
        .call(d3.zoom().on("zoom", (event) => {
            svg.attr("transform", event.transform);
        }))
        .append('g');

    const tooltip = d3.select("#tooltip");

    const simulation = d3.forceSimulation(graph.nodes)
        .force("link", d3.forceLink(graph.links).id(d => d.id))
        .force("charge", d3.forceManyBody())
        .force("center", d3.forceCenter(width / 2, height / 2));

    const link = svg.selectAll(".link")
        .data(graph.links)
        .enter().append("line")
        .attr("class", "link")
        .attr("stroke-width", d => Math.sqrt(d.value));

    const node = svg.selectAll(".node")
        .data(graph.nodes)
        .enter().append("circle")
        .attr("class", "node")
        .attr("r", 5)
        .attr("fill", "blue")
        .call(d3.drag()
            .on("start", (event, d) => dragstarted(simulation, event, d))
            .on("drag", dragged)
            .on("end", (event, d) => dragended(simulation, event, d)))
        .on('mouseover', function(event, d) {
            let tooltipHtml = `Artist Name: ${d.name}<br/>`;
            if (d.playlists) {
                tooltipHtml += `Playlists: ${d.playlists}<br/>`;
            }
            if (d.genres) {
                tooltipHtml += `Genres: ${d.genres.join(', ')}<br/>`;
            }
            if (d.popularity) {
                tooltipHtml += `Popularity: ${d.popularity}`;
            }
            tooltip.style("display", "inline-block").html(tooltipHtml);
            })
        .on('mousemove', function(event) {
            tooltip.style("left", (event.pageX + 10) + "px")
                   .style("top", (event.pageY + 10) + "px");
        })
        .on('mouseout', function() {
            tooltip.style("display", "none");
        });

    node.append("title")
        .text(d => d.name);

    node.on('click', function(event, d) {
        fetch(`/api/related_artists/${d.id}`)
            .then(response => response.json())
            .then(data => {
                console.log('Related Artists:', data); 
            });
    
        fetch(`/api/artist_influence/${d.id}`)
            .then(response => response.json())
            .then(data => {
                console.log('Artist Influence:', data);
            });
    });

    simulation.on("tick", () => {
        link.attr("x1", d => d.source.x)
            .attr("y1", d => d.source.y)
            .attr("x2", d => d.target.x)
            .attr("y2", d => d.target.y);

        node.attr("cx", d => d.x)
            .attr("cy", d => d.y);
    });
}

function dragstarted(simulation, d) {
    if (!event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
}

function dragged(event, d) {
    d.fx = event.x;
    d.fy = event.y;
}

function dragended(simulation, d) {
    if (!event.active) simulation.alphaTarget(0);
    d.fx = null;
    d.fy = null;
}

// function searchArtist() {
//     const artistName = document.getElementById('artistSearch').value.trim();
//     if (!artistName) {
//         document.getElementById('artistInfo').innerHTML = "Please enter an artist name.";
//         return;
//     }
//     fetchArtistData(artistName);
// }

// function fetchArtistData(artistName) {
//     fetch(`/api/search_artist/${encodeURIComponent(artistName)}`)
//         .then(response => {
//             if (!response.ok) {
//                 console.log('Response: ', response);

//                 throw new Error('No data found for this artist');
//             }
//             return response.json();
//         })
//         .then(data => {
//             if (data.error) {
//                 document.getElementById('artistInfo').innerHTML = data.error;
//             } else {
//                 displayArtistInfo(data);
//             }
//         })
//         .catch(error => {
//             document.getElementById('artistInfo').innerHTML = error.message;
//         });
// }

// function displayArtistInfo(data) {
//     const infoBox = document.getElementById('artistInfo');
//     infoBox.innerHTML = `Name: ${data.name}<br>Popularity: ${data.popularity}<br>Genres: ${data.genres}`;
// }

function searchArtist() {
    const artistName = document.getElementById('artistSearch').value.trim();
    if (!artistName) {
        alert('Please enter an artist name.');
        return;
    }

    fetch(`/api/artist_details/${encodeURIComponent(artistName)}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert('Artist not found.');
            } else {
                console.log('Artist details:', data);
                updateUIWithArtistDetails(data);
            }
        })
        .catch(error => console.error('Error fetching artist details:', error));
}

function updateUIWithArtistDetails(data) {
    const artistInfoElement = document.getElementById('artistInfo');
    artistInfoElement.innerHTML = '';

    for (const connection of Object.entries(data.connections)) {
        ///const connectionsList = tracks.join(', ');
        artistInfoElement.innerHTML += `<p>${connection}</p>`;
    }

    for (const [artist, genres] of Object.entries(data.genres)) {
        const genresList = genres.join(', ');
        artistInfoElement.innerHTML += `<p>${artist} genres: ${genresList}</p>`;
    }
}

function fetchPopularArtists() {
    fetch('/api/recommend/popular_artists')
        .then(response => response.json())
        .then(data => {
            console.log('Top Popular Artists:', data);
            displayPopularArtists(data);
        })
        .catch(error => console.error('Error fetching popular artists:', error));
}

function fetchArtistInfluence() {
    const artistName = document.getElementById('artistInfluenceInput').value.trim();
    if (!artistName) {
        alert('Please enter an artist name.');
        return;
    }

    fetch(`/api/recommend/${encodeURIComponent(artistName)}/influence`)
        .then(response => response.json())
        .then(data => {
            console.log('Artist Influence:', data);
            const container = document.getElementById('artistInfluenceResults');
            container.innerHTML = '';
            for (const [artist, influence] of Object.entries(data)) {
                container.innerHTML += `<p>${artist}: ${influence}</p>`;
            }
        })
        .catch(error => console.error('Error fetching artist influence:', error));
}

function displayPopularArtists(artists) {
    const container = document.getElementById('popular-artists');
    container.innerHTML = ''; // Clear previous content
    artists.forEach(artist => {
        const element = document.createElement('div');
        element.textContent = `Artist: ${artist[0]}, Total Weight: ${artist[1]}`;
        container.appendChild(element);
    });
}

function fetchExtendedConnections() {
    const artistName = document.getElementById('extendedConnectionsInput').value.trim();
    if (!artistName) {
        alert("Please enter an artist name.");
        return;
    }

    fetch(`/api/artists/${encodeURIComponent(artistName)}/extended-connections`)
        .then(response => {
            if (!response.ok) throw new Error('Failed to retrieve data');
            return response.json();
        })
        .then(connectionData => {
            displayExtendedConnections(connectionData, artistName);
        })
        .catch(error => {
            console.error('Error fetching extended connections:', error);
            document.getElementById('extendedConnectionsResults').innerHTML = 'Failed to load connections data.';
        });
}

function displayExtendedConnections(connectionData, artistName) {
    const container = document.getElementById('extendedConnectionsResults');
    container.innerHTML = `<h4>Connections of ${artistName}</h4>`;

    const firstDegreeConnections = connectionData.first_degree;
    const extendedConnections = connectionData.extended;

    if (firstDegreeConnections.length > 0) {
        container.innerHTML += `<p>First Degree Connections:</p><ul>`;
        firstDegreeConnections.forEach(conn => {
            container.innerHTML += `<li>${conn}</li>`;
        });
        container.innerHTML += `</ul>`;
    } else {
        container.innerHTML += `<p>No first degree connections found.</p>`;
    }

    if (Object.keys(extendedConnections).length > 0) {
        container.innerHTML += `<p>Extended Connections:</p>`;
        Object.keys(extendedConnections).forEach(key => {
            container.innerHTML += `<p>${key}: ${extendedConnections[key].join(', ')}</p>`;
        });
    } else {
        container.innerHTML += `<p>No extended connections found.</p>`;
    }
}
