import networkx as nx
import matplotlib.pyplot as plt
import math
import sys
import argparse

parser = argparse.ArgumentParser(description='Graph Parser')
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

def plotGraph(graph):
    nx.draw(graph, with_labels=True)
    plt.suptitle("Graph")
    plt.show()

def main():
    graph = nx.read_gml(sys.argv[1])
    args = parser.parse_args()
    if (args.components):
        partition(graph, args.components)
    if (args.plot):
        #plotGraph(graph)
        exit
    if (args.verify_homophily):
        exit
    if (args.verify_balanced_graph):
        exit
    if (args.output):
        output = args.output
        #nx.write_gml(graph, output)

if __name__ == "__main__":
    main()
