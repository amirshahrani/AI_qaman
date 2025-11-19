import networkx as nx
import heapq
from flask import Flask, request, jsonify


app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to the Route Finder API! Use the endpoint /<start>/<dest>?algorithm=UCS to find routes."

# Create graph with 10 locations in UTP
locations = ['V5', 'V3', 'V4', 'Pocket_D', 'Pocket_C', 'Block1', 'Block2','IRC','Block_K', 'Block_I']

G = nx.Graph()
G.add_nodes_from(locations)

# Add edges with approximate distances (in km)
edges = [
    ('V5', 'Block_I', 8),
    ('V5', 'V3', 5),
    ('V3', 'Pocket_D', 3),
    ('IRC', 'Block_K', 3),
    ('IRC', 'Pocket_D', 10),
    ('Block_K', 'Pocket_D', 4),
    ('Pocket_C', 'IRC', 4),
    ('IRC', 'Block_J', 2)
]

graph = {
    'V5': [('Block_I', 8), ('V3', 5)],
    'V3': [('V5', 5), ('Pocket_D', 3)],
    'Pocket_D': [('V3', 3), ('IRC', 10), ('Block_K', 4)],
    'IRC': [('Block_K', 3), ('Pocket_D', 10), ('Pocket_C', 4), ('Block_J', 2)],
    'Block_K': [('IRC', 3), ('Pocket_D', 4)],
    'Pocket_C': [('IRC', 4)],
    'Block_I': [('V5', 8)],
    'Block_J': [('IRC', 2)]
}
heuristic = {
'V5': 7, 'V3': 6, 'V4': 4, 'Pocket_D': 3, 'Pocket_C': 2, 'Block1': 2, 'Block2': 0, 'IRC': 5, 'Block_K': 1, 'Block_I': 3
}

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


def a_star(graph,heuristic, start, goal):
  pq = [(heuristic[start], 0, [start])]
  visited = set()

  while pq:
    est_cost, cost, path = heapq.heappop(pq)
    node = path[-1]

    if node == goal:
      return path,cost

    if node not in visited:
      visited.add(node)
      for neighbor, weight in graph[node]:
        new_cost = cost + weight
        total_cost = new_cost + heuristic[neighbor]
        heapq.heappush(pq, (total_cost, new_cost, path + [neighbor]))

  return None

@app.route("/route", methods=['GET'])
def get_route():

    algorithm = request.args.get('algorithm', 'UCS')
    start = request.args.get('start')
    dest = request.args.get('dest')
    
    if algorithm != 'UCS':
        return jsonify({"error": "Only UCS algorithm is supported."}), 400
    
    path = ucs_path(G, start, dest)
    
    # Display path
    if path:
        print(f"Path from {start} to {dest} using {algorithm}: {' -> '.join(path)}")
    else:
        print(f"No path found from {start} to {dest} using {algorithm}.")
        
    return jsonify({"start": start, "dest": dest, "algorithm": algorithm, "path": path})
    

@app.route("/<start>/<dest>", methods=['GET'])
def get_route_two(start, dest):

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