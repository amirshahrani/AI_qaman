import networkx as nx
import heapq
from datetime import datetime, timedelta

    
time_now = datetime.now()
print(f"Current Time = {time_now.strftime('%H:%M')} ")

# Create graph with 10 locations in UTP
locations = ['V5', 'V3', 'V4', 'Pocket_D', 'Pocket_C', 'Block1', 'Block2','IRC','Block_K', 'Block_I']

# Add edges with approximate distances (in km)
# Weight(time) = Walking Distance / Average Student Speed (4 km/h)
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
    'IRC': [('Block_K', 0.75), ('Pocket_D', 2.5), ('Block_K', 0.5)],
    'Block_K': [('IRC', 0.75), ('Pocket_D', 1)],
    'Pocket_C': [('Pocket_D', 1), ('V5', 2)],
    'Block_I': [('V5', 2)],
}
heuristic = {
    'V5': 3.0, 'V3': 1.75, 'V4': 4.0, 'Pocket_D': 1.0, 'Pocket_C': 2.0, 
    'Block1': 0.0, 'Block2': 5.0, 'IRC': 2.75, 'Block_K': 2.0, 'Block_I': 5.0
}

buffer_time = 5  # in minutes 

def a_star(graph,heuristic, start, goal):
  pq = [(heuristic[start], 0, [start])]
  visited = set()

  while pq:
    est_cost, cost, path = heapq.heappop(pq)
    node = path[-1]


    if node == goal:
        added_time = timedelta(minutes=cost+buffer_time) 
        print(added_time)
        estimated_time = time_now + added_time
        print(f"Total time : {cost} minutes")
        print(f"Estimated Time Arrival (ETA)= {estimated_time.strftime("%H:%M")} ")
        print(f"path: {path}")
        return None
    
    if node not in visited:
      visited.add(node)
      for neighbor, weight in graph[node]:
        new_cost = cost + weight
        total_cost = new_cost + heuristic[neighbor]
        heapq.heappush(pq, (total_cost, new_cost, path + [neighbor]))

  return None

print(a_star(graph, heuristic, 'V5', 'Block_J'))
    