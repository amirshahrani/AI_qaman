import json
import math

def haversine_distance(coord1, coord2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees).
    Input coordinates expected as [Longitude, Latitude].
    Returns distance in meters.
    """
    lon1, lat1 = coord1
    lon2, lat2 = coord2

    # Convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

    # Haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a)) 
    r = 6371000 # Radius of earth in meters
    return c * r

def generate_graph_data(input_file, output_file):
    try:
        with open(input_file, 'r') as f:
            locations = json.load(f)
    except FileNotFoundError:
        print(f"Error: {input_file} not found. Please upload it or check the name.")
        return

    graph = {}
    heuristic = {}
    
    # The target for the heuristic calculation (matching your original data's style)
    # We try to find 'V5', if not found, we try 'V5A', otherwise pick the first key
    target_node = "V5"
    if target_node not in locations:
        if "V5A" in locations:
            print("Note: Exact match for 'V5' not found. Using 'V5A' as the heuristic target.")
            target_node = "V5A"
        else:
            target_node = list(locations.keys())[0]
            print(f"Warning: Target node not found. Using '{target_node}' instead.")

    print(f"Generating graph with {len(locations)} nodes...")
    print(f"Using '{target_node}' as the heuristic target (distance 0).\n")

    # 1. Generate the Graph (Every node links to every other node)
    for start_node, start_coords in locations.items():
        connections = []
        
        for end_node, end_coords in locations.items():
            if start_node == end_node:
                continue # Don't link a node to itself
            
            # Calculate distance in meters
            dist = haversine_distance(start_coords, end_coords)
            
            # Rounding to 2 decimal places for cleanliness
            dist = round(dist, 2)
            
            # Append to connections: ["NodeName", distance]
            connections.append([end_node, dist])
        
        graph[start_node] = connections

    # 2. Generate the Heuristic (Straight line distance to Main_Hall)
    target_coords = locations[target_node]
    for node, coords in locations.items():
        dist_to_target = haversine_distance(coords, target_coords)
        heuristic[node] = round(dist_to_target, 2)

    # Combine into final structure
    final_data = {
        "graph": graph,
        "heuristic": heuristic
    }

    # Write to file
    with open(output_file, 'w') as f:
        json.dump(final_data, f, indent=4)
    
    print(f"Success! Data written to {output_file}")

# Run the function
if __name__ == "__main__":
    generate_graph_data("location_output.json", "full_connected_graph.json")