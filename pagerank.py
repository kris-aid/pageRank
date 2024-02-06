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
    next_nodes_vector = np.zeros(size)
    next_nodes = graph.out_edges(current_node)
    
    for node in next_nodes:
        next_nodes_vector[node[1] - 1] = 1
    
    if teleport:
       prob_next_nodes = np.array([pagerank_vector[i] if next_nodes_vector[i] != 0 else 0 for i in range(len(pagerank_vector))]) * 0.8 + (np.ones(len(pagerank_vector)) / len(pagerank_vector)) * 0.2 
    else:
        prob_next_nodes = np.array([pagerank_vector[i] if next_nodes_vector[i] != 0 else 0 for i in range(len(pagerank_vector))])
        
    
    norm = np.sum(prob_next_nodes)
    
    if norm != 0:
        return prob_next_nodes / norm
    else:
        return prob_next_nodes
    
    
def random_walk(graph, start_node,pagerank_vector, teleport,walked_nodes):
    
    walk_prob=prob_next_nodes(graph, start_node, pagerank_vector, teleport)
    for node in walked_nodes:
        walk_prob[node - 1] = 0
    print("test prob",walk_prob)
    if any(weight != 0 for weight in walk_prob):
        current_node = random.choices(range(len(walk_prob)), weights=walk_prob)[0]
        current_node= current_node+1
        
        return current_node
    else:
        return start_node

def calculate_pagerank_vector(graph, pagerank_vector, teleport):
    alpha=0.8
    new_pagerank_vector=pagerank_vector.copy()
    M = weighted_adjacency_matrix(graph)
    n = len(graph.nodes)
    if teleport:      
        damping_matrix = np.full((n, n), 1 / n)
        M = alpha * M + (1 - alpha) * damping_matrix
        new_pagerank_vector = M @ pagerank_vector
    else:
        new_pagerank_vector = M @ pagerank_vector
    if np.linalg.norm(new_pagerank_vector - pagerank_vector, 1) < 1e-6:
        print("convergence achieved")
    return new_pagerank_vector

def power_iterate(graph, pagerank_vector, teleport, start_node,num_iterations,all_walked_nodes):
    pagerank_vectors=[pagerank_vector]
    walked_nodes=[]
    walk_rate_nodes=[prob_next_nodes(graph, start_node,pagerank_vector,teleport)]
    for _ in range(num_iterations):
        current_page_rank=calculate_pagerank_vector(graph, pagerank_vectors[-1], teleport)
        pagerank_vectors.append(current_page_rank)
        current_node=random_walk(graph,walked_nodes[-1],pagerank_vectors[-1],teleport,all_walked_nodes)
        walked_nodes.append(current_node)
        walk_rate_nodes.append(prob_next_nodes(graph, walked_nodes[-1],pagerank_vectors[-1],teleport))
    return pagerank_vectors,walked_nodes, walk_rate_nodes,current_node,current_page_rank
