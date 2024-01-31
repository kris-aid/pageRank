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
    G=nx.DiGraph()
    nx.add_path(G, [0, 1, 2, 3])
    G.in_degree(0)  # node 0 with degree 0
    return G

def draw_graph(G,pos):
    pos = nx.spring_layout(G,seed=9)
    nx.draw_networkx_nodes(G, pos, node_color='r', node_size=500, alpha=0.8)
    nx.draw_networkx_edges(G, pos=pos,
                           edge_color='b',
                           arrowstyle="->"
                            ,arrowsize=10,
                           width=1.0, alpha=0.5)
    
    # node labels
    nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")
    
    # edge weight labels
    edge_labels = nx.get_edge_attributes(G, "weight")
    
    nx.draw_networkx_edge_labels(G, pos, edge_labels)
    ax = plt.gca()
    ax.margins(0.08)
    plt.axis("off")
    plt.tight_layout()
    plt.show()
    
def generate_better_pos(G):
    
    column_nodes = []
    for i in range(0, len(G.nodes),3):
        column_nodes.append(list(G.nodes)[i:i+3:None])
    print(column_nodes)    
    pos = {}
    for col_index, nodes in enumerate(column_nodes):
        for row_index, node in enumerate(nodes):
            pos[node] = (col_index, row_index + 0.5 * (len(nodes) - 1))
            
    return pos
    
def generate_graph(num_nodes, num_edges, num_spider_traps, num_dead_ends):
    # Create a directed graph
    graph = nx.DiGraph()

    # Add nodes
    graph.add_nodes_from(range(num_nodes))

    # Add edgess
    for _ in range(num_edges):
        source = random.choice(range(num_nodes))
        target = random.choice([node for node in range(num_nodes) if node != source])
        graph.add_edge(source, target)

    # Introduce spider traps
    for _ in range(num_spider_traps):
        trap_node = max(graph.nodes) + 1  # Create a new node for the trap
        graph.add_node(trap_node)
        for node in range(num_nodes):
            if random.random() < 0.5:  # Adjust the probability as needed
                graph.add_edge(node, trap_node)

    # Introduce dead ends
    for _ in range(num_dead_ends):
        dead_end_node = max(graph.nodes) + 1  # Create a new node for the dead end
        graph.add_node(dead_end_node)
        source = random.choice(range(num_nodes))
        graph.add_edge(source, dead_end_node)

    return graph
if __name__ == "__main__":
    num_nodes = 10
    num_edges = 20
    num_spider_traps = 2
    num_dead_ends = 2
    
    # generated_graph_1 = generate_graph(num_nodes, num_edges, num_spider_traps, num_dead_ends)
    # nodes=generated_graph_1.nodes
    # pos=generate_better_pos(generated_graph_1)
    # print(pos)
    # draw_graph(generated_graph_1,pos)
    # set the position according to column (x-coord)
    
    # group nodes by column
    left_nodes = [0, 1, 2]
    middle_nodes = [3, 4]
    right_nodes = [5, 6]
    pos = {n: (0, i) for i, n in enumerate(left_nodes)}
    pos.update({n: (1, i + 0.5) for i, n in enumerate(middle_nodes)})
    pos.update({n: (2, i + 0.5) for i, n in enumerate(right_nodes)})
    print(pos)

    