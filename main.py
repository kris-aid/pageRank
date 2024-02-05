import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
import time
import os
import sys
import math

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
    #pos = nx.shell_layout(G)
    nx.draw_networkx_nodes(G, pos, node_color='r', node_size=[node_sizes[node] * 100 for node in G.nodes], alpha=0.8)
    nx.draw_networkx_edges(G, pos=pos, edge_color='b', style='solid', width=1.0, alpha=0.5)
    
    # Node labels
    nx.draw_networkx_labels(G, pos, font_size=10, font_family="sans-serif")
    
    # Edge weight labels
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels)
    
    plt.axis("off")
    plt.tight_layout()
    plt.show()


    
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

   
    # Introduce dead ends
    for _ in range(num_dead_ends):
        dead_end_node = max(graph.nodes) + 1  # Create a new node for the dead end
        graph.add_node(dead_end_node)
        source = random.choice(range(1, num_nodes + 1))
        graph.add_edge(source, dead_end_node)
        print(f"Dead End: {source} -> {dead_end_node}")

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


        # Add edges between chosen nodes and the trap node
        for i in range(num_nodes_to_choose):
            # for node in graph.neighbors(trap_nodes[i]):  
            #     graph.remove_edge(trap_nodes[i], node)
            graph.add_edge(trap_nodes[i], trap_nodes[i+1 if i+1 < num_nodes_to_choose else 0])
            
        print(f"Spider Trap {trap_index + 1}: Nodes involved - {trap_nodes}")


    return graph


if __name__ == "__main__":
    num_nodes = 12
    num_edges = 0
    num_spider_traps = 2
    num_dead_ends = 3
    num_important_nodes = 3

    generated_graph = generate_graph(num_nodes, num_edges, num_spider_traps, num_dead_ends, num_important_nodes)
    # pos = nx.spring_layout(generated_graph, seed=42)
    # nx.draw(generated_graph, pos, with_labels=True, font_weight='bold', node_size=500)
    # plt.show()
    pos, node_sizes = generate_better_pos(generated_graph)

    draw_graph(generated_graph, pos, node_sizes)
 
    pagerank_vector = np.ones(len(generated_graph_1.nodes)) / len(generated_graph_1.nodes)
    start_node=1
    while True:
            num_iterations = int(input("Enter the number of iterations (or '0' to exit): "))
            if num_iterations == 0:
                break  # Exit the loop if the user enters 0
            tp=bool(input("do you want to use teleportation? "))
            pagerank_vectors,walked_nodes, walk_rate_nodes=power_iterate(generated_graph_1, pagerank_vector, teleport=tp, start_node=start_node ,num_iterations=num_iterations)
            
            print("first pagerank vector:", pagerank_vectors[0])
            print("last pagerank vector:", pagerank_vectors[-1])
            print("start node:", walked_nodes[0])
            print("current node:", walked_nodes[-1])
            print("prob to enter next nodes:", walk_rate_nodes[-1])
    
