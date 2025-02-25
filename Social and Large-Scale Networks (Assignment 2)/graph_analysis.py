import networkx as nx
import matplotlib.pyplot as plt
import math
import sys
import argparse

parser = argparse.ArgumentParser(description='Graph Parser')
parser.add_argument('input_file',  type=argparse.FileType('r'), help='Path to the input file')
parser.add_argument("--components", type=int, help="Specifies that the graph should be partitioned into n components. " 
                                                    "This divides the graph into n subgraphs or clusters.\n")
parser.add_argument("--plot", type=str, help="Plot the graph. " 
                                             "Enter \'C\' to highlight clustering coefficients. "
                                             "Enter \'N\' to highlight neighborhood overlap. "
                                             "Enter \'P\' to color nodes according to specified attributes, if any.\n")
parser.add_argument("--verify_homophily", action="store_true", 
                                          help="Tests for homophily in the graph based on the assigned "
                                               "node colors using the Student t-test. Homophily measures "
                                               "whether nodes with the same color are more likely to be connected.\n")
parser.add_argument("--verify_balanced_graph", action="store_true", 
                                               help="Check if the graph is balanced based on the assigned edge signs. "
                                                    "A balanced graph is one where the signs on the edges are consistent " 
                                                    "with the node attributes.\n")
parser.add_argument("--output", type=str, help="Output file to store the graph.\n")

def partition(graph, n):
    while(nx.number_connected_components(graph) < n):
        edge = max(nx.edge_betweenness_centrality(graph).items(), key=lambda x: x[1])[0]
        graph.remove_edge(*edge)

def onClick(event, pos, node_sizes):
    x_click = event.xdata
    y_click = event.ydata
    for node, position in pos.items():
        x_center, y_center = position
        distance = math.sqrt((x_center - x_click) ** 2 + (y_center - y_click) ** 2)
        radius = node_sizes[int(node)] / 2
        if distance < radius:
            print(f"{position}, {distance}, {radius}")
            break

def plotGraph(graph, args):
    pos = nx.spring_layout(nx.read_gml(sys.argv[1]))
    node_sizes = []
    node_colors = []
    if 'C' in args.upper():
        dict_clustering_coefficients = nx.clustering(graph)
        clustering_coefficients = list(dict_clustering_coefficients.values())
        cluster_min = min(clustering_coefficients)
        cluster_max = max(clustering_coefficients)
        min_pixel = 100
        max_pixel = 500
        for c in clustering_coefficients:
            p = (c - cluster_min) / (cluster_max - cluster_min)
            size = min_pixel + (max_pixel - min_pixel) * p
            node_sizes.append(size)
        degree_values = list(dict(graph.degree()).values())
        max_degree = max(degree_values)
        for d in degree_values:
            s = (d / max_degree)
            node_colors.append((s, 0, 1))
    else:
        node_sizes = [100] * len(graph)
        node_colors = 'blue'
    if 'N' in args.upper():
        edge_labels = {}
        for u, v in graph.edges():
            common_neighbors = len(list(nx.common_neighbors(graph, u, v)))
            join_neighbors = len(set(graph.neighbors(u)).union(set(graph.neighbors(v)))) - 2
            if join_neighbors <= 0:
                overlap = 0
            else:
                overlap = common_neighbors / join_neighbors
            edge_labels[(u, v)] = round(overlap, 2)
        nx.draw_networkx_edge_labels(graph, edge_labels=edge_labels, pos=pos)
    if 'P' in args.upper():
        #color nodes according to specified attributes
        exit

    nx.draw(graph, node_size=node_sizes, node_color=node_colors, pos=pos, with_labels=True)
    plt.suptitle("Graph")
    plt.connect('button_press_event', lambda event: onClick(event, pos, node_sizes))
    plt.show()

def main():
    graph = nx.read_gml(sys.argv[1])
    args = parser.parse_args()
    if (args.components):
        partition(graph, args.components)
    if (args.plot):
        plotGraph(graph, args.plot)
    if (args.verify_homophily):
        exit
    if (args.verify_balanced_graph):
        exit
    if (args.output):
        output = args.output
        #nx.write_gml(graph, output)

if __name__ == "__main__":
    main()
