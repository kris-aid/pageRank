import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
import time
import os
import sys
from math import exp
from pagerank import prob_next_nodes, random_walk, calculate_pagerank_vector, power_iterate
def generate_spider_trap_subgraph(G,n, m):

    for i in range(1, n+1):
        G.add_node(i)
    for i in range(1, n+1):
        for j in range(1, n+1):
            if i != j:
                G.add_edge(i, j, weight=random.randint(1, m))
    return G

def create_digraph(number_of_nodes=100, number_of_edges=10):
    # G = nx.Graph()
    # G.add_nodes_from(range(1,number_of_nodes))
    # for i in range(1, number_of_edges):
    #     for j in range(1,number_of_edges):
    #         if i != j:
    #             G.add_edge(i, j, weight=random.randint(1, 20))
    G=nx.DiGrap()
    nx.add_path(G, [0, 1, 2, 3])
    G.in_degree(0)  # node 0 with degree 0
    return G


import networkx as nx
import matplotlib.pyplot as plt
import random

def generate_better_pos(G):
    column_nodes = []
    for i in range(0, len(G.nodes), 3):
        column_nodes.append(list(G.nodes)[i:i+3:None])

    pos = {}
    sizes = {}

    for col_index, nodes in enumerate(column_nodes):
        for row_index, node in enumerate(nodes):
            pos[node] = (col_index, row_index+0.3)

            # Calculate node size based on incoming edges
            incoming_edges = G.in_edges(node)
            size = len(list(incoming_edges)) + 1  # You can adjust this formula as needed
            sizes[node] = size

    return pos, sizes

def draw_graph(G, pos, node_sizes):
    pos=nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos,
                           node_size=[node_sizes[node] * 100* exp(len(list(G.in_edges(node)))*0.1) for node in G.nodes],
                           alpha=0.8,
                           node_color="indigo")
    nx.draw_networkx_edges(G, pos=pos, edge_color='black', style='solid', width=1.0, alpha=0.5)

    # Node labels
    nx.draw_networkx_labels(G, pos, font_size=10, font_family="sans-serif")

    # Edge weight labels
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels)

    plt.axis("off")
    plt.tight_layout()
    plt.show()

def retire_edges_of_spider_trap(G, trap_nodes):
    for i in range(len(trap_nodes)):
        neighbors_copy = list(G.neighbors(trap_nodes[i]))  # Create a copy of the neighbors list
        for node in neighbors_copy:
            G.remove_edge(trap_nodes[i], node)
    return G

def graph_normal():
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
    return G

def adjaceny_matrix(G):
    return nx.to_numpy_array(G)

# Define important nodes
def generate_graph(num_nodes, num_edges, num_spider_traps, num_dead_ends, num_important_nodes):
    # Create a directed graph
    graph = nx.DiGraph()

    # Add nodes
    graph.add_nodes_from(range(1, num_nodes + 1))

    # Ensure each node has at least one incoming edge
    for node in range(2, num_nodes + 1):
        source = random.choice(range(1, node))
        graph.add_edge(source, node)

    # Add remaining edges
    # for _ in range(num_edges - num_nodes + 1):
    #     source = random.choice(range(1, num_nodes + 1))
    #     target = random.choice(range(1, num_nodes + 1))
    #     graph.add_edge(source, target)



    # Introduce important nodes
    for _ in range(num_important_nodes):
        important_node = random.choice(range(1, num_nodes + 1))
        graph.add_node(important_node)
        number_of_incoming_edges = 4
        for _ in range(number_of_incoming_edges):
            source = random.choice(range(1, num_nodes + 1))
            graph.add_edge(source, important_node)
        print(f"Important Node: {important_node} with {number_of_incoming_edges} incoming edges")
     # Introduce spider traps
    for trap_index in range(num_spider_traps):
        num_nodes_to_choose = 3
        trap_nodes = random.sample(list(graph.nodes), num_nodes_to_choose)

        retire_edges_of_spider_trap(graph, trap_nodes)

        # Add edges between chosen nodes and the trap node
        for node, next_node in zip(trap_nodes, trap_nodes[1:] + [trap_nodes[0]]):
            graph.add_edge(node, next_node)



        print(f"Spider Trap {trap_index + 1}: Nodes involved - {trap_nodes}")

    # Introduce dead ends
    for _ in range(num_dead_ends):
        dead_end_node = max(graph.nodes) + 1  # Create a new node for the dead end
        graph.add_node(dead_end_node)
        source = random.choice(range(1, num_nodes + 1))
        graph.add_edge(source, dead_end_node)
        print(f"Dead End: {source} -> {dead_end_node}")


    return graph


if __name__ == "__main__":
    # num_nodes = 12
    # num_edges = 0
    # num_spider_traps = 2
    # num_dead_ends = 4
    # num_important_nodes = 3

    # generated_graph = generate_graph(num_nodes, num_edges, num_spider_traps, num_dead_ends, num_important_nodes)
    
    generated_graph=graph_normal()
    a=adjaceny_matrix(generated_graph)
    print(a)
    pos, node_sizes = generate_better_pos(generated_graph)

    #draw_graph(generated_graph, pos, node_sizes)

    pagerank_vector = np.ones(len(generated_graph.nodes)) / len(generated_graph.nodes)
    start_node=random.choice(list(generated_graph.nodes))
    pagerank_vectors, walked_nodes, walk_rate_nodes = [], [], []
    walked_nodes.append(start_node)
    while True:
            num_iterations = int(input("Enter the number of iterations (or '0' to exit): "))
            if num_iterations == 0:
                break  # Exit the loop if the user enters 0
            tp=bool(input("do you want to use teleportation? 1 is yes, 0 is no:"))
            result_pagerank, result_walked_nodes, result_walk_rate_nodes,current_node=power_iterate(generated_graph, pagerank_vector, teleport=tp, start_node=start_node ,num_iterations=num_iterations)
            
            pagerank_vectors.extend(result_pagerank)
            walked_nodes.extend(result_walked_nodes)
            walk_rate_nodes.extend(result_walk_rate_nodes)
            
            #print("pagerank vectors:", pagerank_vectors)
            print("walked nodes:", walked_nodes)
            #print("walk rate nodes:", walk_rate_nodes)
            start_node=current_node
            print("first pagerank vector:", pagerank_vectors[0])
            print("last pagerank vector:", pagerank_vectors[-1])
            # print("start node:", walked_nodes[0])
            # print("Estas en el nodo", walked_nodes[-1], "y tienes un" )
            print("prob to enter next nodes:", walk_rate_nodes[-1])


