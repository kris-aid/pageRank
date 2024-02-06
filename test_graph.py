import networkx as nx
import matplotlib.pyplot as plt
import random
# Create a directed graph
G = nx.DiGraph()

# Add 15 nodes
nodes = range(1, 16)
G.add_nodes_from(nodes)
G.add_edges_from([(6,7),(7,11),(11,6),(9,6),(9,8),
                (9,13),(12,8),(12,10),
                (8,1),(12,1),(12,15),
                (3,2),(4,3),(15,5),
                (1,2),(3,14),(1,15),(15,4),(15,8),
                (4,9),(4,1),(9,1),(4,8),(14,3),(2,6)])
print("Spider Traps: Nodes involved - [3, 14],[6,11,7]")
print("Dead End: 9 -> 13")
print("Dead End: 12 -> 5")
print("Dead End: 15 -> 5")
print("Important Node: 1 with 4 incoming edges")
print("Important Node: 8 with 4 incoming edges")

# important_nodes = [1, 2, 3, 4]
# spider_traps = [5, 6, 7]
# dead_ends = [8, 9, 10]

# # Connect nodes randomly, ensuring that important nodes connect to other nodes
# for node in nodes:
#     if node in important_nodes:
#         neighbors = set(nodes) - {node}
#         target = None
#         while not target or target in important_nodes:
#             target = random.choice(list(neighbors))
#         G.add_edge(node, target)
#     elif node in spider_traps or node in dead_ends:
#         G.add_edge(node, random.choice(list(important_nodes)))

# # Print edges
# edges = G.edges()
# print("Edges:")
# for edge in edges:
#     print(edge)

# Draw the graph
pos = nx.planar_layout(G)
nx.draw(G, pos, with_labels=True, font_weight='bold', node_color='skyblue', node_size=700, arrowsize=15)
plt.show()
from pagerank import weighted_adjacency_matrix
print(weighted_adjacency_matrix(G))
