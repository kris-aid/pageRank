import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random

def weighted_adjacency_matrix(graph):
    size = len(graph.nodes)
    vectors=[]
    for node in range(1,size):
        vectors.append(prob_next_nodes(graph,node))
    
    return vectors
    
def prob_next_nodes(graph, current_node):
    size = len(graph.nodes)
    position_vector = np.zeros(size)
    position_vector[current_node-1] = 1
    prob_next_nodes=calculate_pagerank_vector(graph,position_vector,teleport=False)
    norm=np.sum(prob_next_nodes)
    if norm == 0:
        return prob_next_nodes
    else:
        return prob_next_nodes / norm
    
def random_walk(graph, start_node, teleport):
    current_node=start_node
    neighbors = list(graph.neighbors(current_node))
    all_nodes= list(range(1,len(graph.nodes)))
    if ((teleport) and (random.random()<=0.8)):
        if neighbors:
            current_node = random.choice(neighbors)
        return current_node
    else:
    
        if neighbors:
            current_node = random.choice(all_nodes)
        return current_node

def calculate_pagerank_vector(graph, pagerank_vector, teleport):
    alpha=0.8
    new_pagerank_vector=pagerank_vector
    adjacency_matrix = nx.to_numpy_array(graph)
    n = len(graph.nodes)
    if teleport:      
        damping_matrix = np.full((n, n), 1 / n)
        M = alpha * adjacency_matrix + (1 - alpha) * damping_matrix
        new_pagerank_vector = M @ pagerank_vector
    else:
        new_pagerank_vector = adjacency_matrix @ pagerank_vector

    return new_pagerank_vector

def power_iterate(graph, pagerank_vector, teleport, start_node,num_iterations):
    pagerank_vectors=[pagerank_vector]
    walked_nodes=[start_node]
    walk_rate_nodes=[prob_next_nodes(graph, start_node)]
    for _ in range(num_iterations):
        pagerank_vectors.append(calculate_pagerank_vector(graph, pagerank_vectors[-1], teleport))
        walked_nodes.append(random_walk(graph,walked_nodes[-1],teleport))
        walk_rate_nodes.append(prob_next_nodes(graph, walked_nodes[-1]))
    return pagerank_vectors,walked_nodes, walk_rate_nodes

