import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random


def weighted_adjacency_matrix(graph):
    size = len(graph.nodes)
    vectors=[]
    for node in range(1,size+1):
        out_edges = np.zeros(size)
        len_out_edges = len(list(graph.out_edges(node)))
        if len_out_edges==0:
            out_edges[node-1]=0
        else:
            for edge in list(graph.out_edges(node)):
                out_edges[edge[1]-1]=1/len_out_edges
        vectors.append(out_edges)
    matrix=np.array(vectors)
    return matrix
        
  
def prob_next_nodes(graph, current_node, pagerank_vector, teleport):
    size = len(graph.nodes)
    position_vector = np.zeros(size)
    position_vector[current_node-1] = 1
    next_nodes= nx.to_numpy_array(graph) @ position_vector
    prob_next_nodes = []

    if teleport:

        for i in range(len(pagerank_vector)):
            prob_next_nodes.append(pagerank_vector[i] * next_nodes[i]*0.8+pagerank_vector[i]*0.2)
        
        norm=np.sum(prob_next_nodes)
        if norm!=0:
            return prob_next_nodes/norm
        else:
            return prob_next_nodes
    else:
        for i in range(len(pagerank_vector)):
            prob_next_nodes.append(pagerank_vector[i] * next_nodes[i])
        norm=np.sum(prob_next_nodes)
        
        if norm!=0:
            return prob_next_nodes/norm
        else:
            return prob_next_nodes
    
def random_walk(graph, start_node,pagerank_vector, teleport):

    walk_prob=prob_next_nodes(graph, start_node, pagerank_vector, teleport)
    current_node = random.choices(range(len(walk_prob)), weights=walk_prob)[0]
    return current_node


def calculate_pagerank_vector(graph, pagerank_vector, teleport):
    alpha=0.8
    new_pagerank_vector=pagerank_vector
    adjacency_matrix = weighted_adjacency_matrix(graph)
    n = len(graph.nodes)
    if teleport:      
        damping_matrix = np.full((n, n), 1 / n)
        M = alpha * adjacency_matrix + (1 - alpha) * damping_matrix
        new_pagerank_vector = M @ pagerank_vector
    else:
        new_pagerank_vector = adjacency_matrix @ pagerank_vector

    return new_pagerank_vector

# def power_iterate(graph, pagerank_vector, teleport, start_node,num_iterations):
#     pagerank_vectors=[pagerank_vector]
#     walked_nodes=[]
#     walk_rate_nodes=[prob_next_nodes(graph, start_node)]
#     for _ in range(num_iterations):
#         pagerank_vectors.append(calculate_pagerank_vector(graph, pagerank_vectors[-1], teleport))
#         current_node=random_walk(graph,start_node,teleport)
#         walked_nodes.append(current_node)
#         walk_rate_nodes.append(prob_next_nodes(graph, walked_nodes[-1]))
#     return pagerank_vectors,walked_nodes, walk_rate_nodes,current_node

def power_iterate(graph, pagerank_vector, teleport, start_node,num_iterations):
    pagerank_vectors=[pagerank_vector]
    walked_nodes=[]
    walk_rate_nodes=[prob_next_nodes(graph, start_node,pagerank_vector,teleport)]
    for _ in range(num_iterations):
        pagerank_vectors.append(calculate_pagerank_vector(graph, pagerank_vectors[-1], teleport))
        current_node=random_walk(graph,start_node,pagerank_vectors[-1],teleport)
        walked_nodes.append(current_node)
        walk_rate_nodes.append(prob_next_nodes(graph, walked_nodes[-1],pagerank_vectors[-1],teleport))
    return pagerank_vectors,walked_nodes, walk_rate_nodes,current_node