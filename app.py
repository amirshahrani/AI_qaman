# import networkx as nx
import heapq
from flask import Flask, json, request, jsonify
from datetime import datetime, timedelta
# import matplotlib.pyplot as plt
from zoneinfo import ZoneInfo

# Define your target timezone
# kl_timezone = ZoneInfo("Asia/Kuala_Lumpur")

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to the Route Finder API! Use the endpoint /<start>/<dest>?algorithm=UCS to find routes."

# Create graph with 10 locations in UTP
locations = ['V5', 'V3', 'V4', 'Pocket_D', 'Pocket_C', 'Block1', 'Block2','IRC','Block_K', 'Block_I']

# Add edges with approximate distances (in km)
# Weight(time (min)) = Walking Distance / Average Student Speed (4 km/h)
edges = [
    ('V5', 'Block_I', 15),
    ('V5', 'V3', 7.5),
    ('V3', 'Pocket_D', 4.5),
    ('V5', 'Pocket_C', 15),
    ('IRC', 'Block_K', 4.5),
    ('IRC', 'Pocket_D', 10),
    ('Block_K', 'Pocket_D', 4),
    ('Pocket_C', 'Pocket_D', 4),
    ('Pocket_D', 'Block1', 4),
    ('IRC', 'Block_K', 2)
]

graph = {
    'V5': [('Block_I', 2), ('V3', 1.25), ('Pocket_C', 2)],
    'V3': [('V5', 1.25), ('Pocket_D', 0.75)],
    'Pocket_D': [('V3', 0.75), ('IRC', 2.5), ('Block_K', 1), ('Pocket_C', 1), ('Block1', 1)],
    'IRC': [('Block_K', 0.75), ('Pocket_D', 2.5)],
    'Block_K': [('IRC', 0.75), ('Pocket_D', 1)],
    'Pocket_C': [('Pocket_D', 1), ('V5', 2)],
    'Block_I': [('V5', 2)],
    'Block1': [('Pocket_D', 1)],
}
heuristic = {
    'V5': 3.0, 'V3': 1.75, 'V4': 4.0, 'Pocket_D': 1.0, 'Pocket_C': 2.0, 
    'Block1': 0.0, 'Block2': 5.0, 'IRC': 2.75, 'Block_K': 2.0, 'Block_I': 5.0
}

buffer_time = 5  # in minutes 

def load_graph_data(filename="full_connected_graph.json"):
    with open(filename, 'r') as f:
        data = json.load(f)
    
    # Ensure all required keys are present
    graph = data.get('graph', {})
    # for place in graph:
    #     print(place)
    #     for distance in graph[place]:
    #         print(distance[1]/4)

    heuristic = data.get('heuristic', {})
    
    print(f"Data loaded successfully from {filename}.")
    return graph, heuristic


# def visualize_graph():
#     G = nx.Graph()
#     G.add_nodes_from(locations)
#     G.add_weighted_edges_from(edges)

#     print("Graph created with nodes:", list(G.nodes()))
#     print("Edges:", list(G.edges(data=True)))

#     # Visualize the graph
#     pos = nx.spring_layout(G)  # positions for all nodes
#     nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=2000, font_size=10, font_weight='bold')
#     labels = nx.get_edge_attributes(G, 'weight')
#     nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
#     plt.title("Graph of Locations in Perak")
#     plt.show()



def a_star(start, goal):
    

    GRAPH, HEURISTIC = load_graph_data()
    
    pq = [(HEURISTIC[start], 0, [start])]
    visited = set()

    time_now = datetime.now()
    print(f"Current Time = {time_now.strftime('%H:%M')} ")
       

    while pq:
        est_cost, cost, path = heapq.heappop(pq)
        node = path[-1]

        if node == goal:
            # distance = (cost+buffer_time)*60  # convert buffer time to seconds
            # added_time = timedelta(minutes=cost+buffer_time) 
            # print(added_time)
            # estimated_time = time_now + added_time
            # print(f"Total time : {cost} minutes")
            # print(f"Estimated Time Arrival (ETA)= {estimated_time.strftime("%H:%M")} ")
            # print(f"Distance: {distance} meters")
            # print(f"path: {path}")
            # return path,estimated_time,added_time,distance
            return path,cost

        if node not in visited:
            visited.add(node)
            for neighbor, weight in GRAPH[node]:
                new_cost = cost + weight
                total_cost = new_cost + HEURISTIC[neighbor]
                heapq.heappush(pq, (total_cost, new_cost, path + [neighbor]))
            
    return None


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


@app.route("/route", methods=['GET'])
def get_route():

    start = request.args.get('start')
    dest = request.args.get('dest')
    
    path,distance = a_star(start, dest)
    
    # Display path
    if path:
        print(f"Path from {start} to {dest}: {' -> '.join(path)}")
        # print(f"Estimated Time Arrival (ETA)= {estimated_time.strftime('%H:%M')}")
    else:
        print(f"No path found from {start} to {dest}.")
        
    # return jsonify({"start": start, "dest": dest, "estimated_time": estimated_time.strftime('%H:%M'), "path": path, "added_time": str(added_time), "distance": distance})
    return jsonify({"start": start, "dest": dest, "estimated_time": "0", "path": path, "added_time": "0", "distance": distance})
    

@app.route("/<start>/<dest>", methods=['GET'])
def get_route_two(start, dest):

    start = request.args.get('start')
    dest = request.args.get('dest')
    
    path,distance = a_star(graph, heuristic, start, dest)
    
    # Display path
    if path:
        print(f"Path from {start} to {dest}: {' -> '.join(path)}")
        # print(f"Estimated Time Arrival (ETA)= {estimated_time.strftime('%H:%M')}")
    else:
        print(f"No path found from {start} to {dest}.")
        
    # return jsonify({"start": start, "dest": dest, "estimated_time": estimated_time.strftime('%H:%M'), "path": path, "added_time": str(added_time), "distance": distance})
    return jsonify({"start": start, "dest": dest, "path": path,"distance": distance})
    
    
if __name__ == '__main__':
    app.run(debug=True)