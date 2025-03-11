import networkx as nx
import matplotlib.pyplot as plt
import math
import argparse
import sys

parser = argparse.ArgumentParser(description='Graph Parser')
parser.add_argument('input_file',  type=argparse.FileType('r'), help='Path to the input file')
parser.add_argument('n',  type=int, help='Number of vehicles')
parser.add_argument('initial',  type=str, help='Starting node')
parser.add_argument('final',  type=str, help='Ending node')
parser.add_argument("--plot", action="store_true", help="Plot the graph")

def plotTravelEquilibriumGraph(graph, flow):
    pos = nx.spring_layout(graph)
    plt.figure(figsize=(8, 6))
    nx.draw(graph, pos, with_labels=True, node_color='skyblue', edge_color='gray', node_size=2000, font_size=10)
    edge_labels = {edge: f"Vehicles = {flow[edge]}\n"
                f"({graph[edge[0]][edge[1]].get('a', 1)}x + {graph[edge[0]][edge[1]].get('b', 1)})" for edge in graph.edges}
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=10)
    plt.suptitle("Travel Equilibrium", fontsize=16)
    plt.show()

def compute_travel_equilibrium(graph, num_vehicles, initial_node, final_node):
    flow = {edge: 0 for edge in graph.edges}
    shortest_paths = list(nx.all_shortest_paths(graph, source=initial_node, target=final_node, weight="b"))
    
    vehicles_per_path = num_vehicles / len(shortest_paths)
    
    for path in shortest_paths:
        for i in range(len(path) - 1):
            edge = (path[i], path[i + 1])
            flow[edge] += vehicles_per_path

    return flow

def compute_social_optima(graph, num_vehicles, initial_node, final_node):
    pass

def main():
    graph = nx.read_gml(sys.argv[1])
    num_vehicles = int(sys.argv[2])
    initial_node = (sys.argv[3])
    final_node = (sys.argv[4])

    flow = compute_travel_equilibrium(graph, num_vehicles, initial_node, final_node)
    compute_social_optima(graph, num_vehicles, initial_node, final_node)

    args = parser.parse_args()
    if (args.plot):
        plotTravelEquilibriumGraph(graph, flow)

if __name__ == "__main__":
    main()
