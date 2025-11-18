import networkx as nx
import heapq
from flask import Flask, request, jsonify


app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to the Route Finder API! Use the endpoint /<start>/<dest>?algorithm=UCS to find routes."

# Create graph with 10 locations in Perak
locations = ['V5', 'Block A', 'Pocket D', 'Cafe D', 'Admin Block', 'IRC']

G = nx.Graph()
G.add_nodes_from(locations)

# Add edges with approximate distances (in km)
edges = [
    ('V5', 'Block A', 8),
    ('V5', 'IRC', 5),
    ('IRC', 'Block A', 3),
    ('IRC', 'Pocket D', 10),
    ('Block A', 'Pocket D', 4),
    ('Cafe D', 'IRC', 4),
    ('Admin Block', 'Block A', 2)
]

G.add_weighted_edges_from(edges)

print("Graph created with nodes:", list(G.nodes()))
print("Edges:", list(G.edges(data=True)))

G.add_weighted_edges_from(edges)

print("Graph created with nodes:", list(G.nodes()))
print("Edges:", list(G.edges(data=True)))

def ucs_path(graph, start, goal):
    queue = [(0, start, [start])]  # (cost, node, path)
    visited = set()
    while queue:
        cost, node, path = heapq.heappop(queue)
        if node == goal:
            return path
        if node not in visited:
            visited.add(node)
            for neighbor in graph.neighbors(node):
                if neighbor not in visited:
                    edge_cost = graph[node][neighbor]['weight']
                    heapq.heappush(queue, (cost + edge_cost, neighbor, path + [neighbor]))
    return None


@app.route("/<start>/<dest>", methods=['GET'])
def get_route(start, dest):

    algorithm = request.args.get('algorithm', 'UCS')
    
    if algorithm != 'UCS':
        return jsonify({"error": "Only UCS algorithm is supported."}), 400
    
    path = ucs_path(G, start, dest)
    
    # Display path
    if path:
        print(f"Path from {start} to {dest} using {algorithm}: {' -> '.join(path)}")
    else:
        print(f"No path found from {start} to {dest} using {algorithm}.")
        
    return jsonify({"start": start, "dest": dest, "algorithm": algorithm, "path": path})
    
    
if __name__ == '__main__':
    app.run(debug=True)