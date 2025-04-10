import networkx as nx
import matplotlib.pyplot as plt
import math
import argparse
import sys
import os

parser = argparse.ArgumentParser(description='Graph Parser')
parser.add_argument('input_file',  type=argparse.FileType('r'), help='Path to the input file')
parser.add_argument("--plot", action="store_true", help="Plot the graph")
parser.add_argument("--interactive", action="store_true", help="Plot by round")
args = parser.parse_args()

def getPreferenceGraph(G, sellers, buyers):
    preference_edges = []
    for b in buyers:
        best_val = -float('inf')
        preferred_seller = None
        for s in sellers:
            if G.has_edge(b, s):
                valuation = G.edges[b, s]['valuation']
                price = G.nodes[s]['price']
                net_utility = valuation - price
                if net_utility > best_val:
                    best_val = net_utility
                    preferred_seller = s
        if preferred_seller is not None:
            preference_edges.append((b, preferred_seller))
    PG = nx.DiGraph()
    PG.add_edges_from(preference_edges)
    return PG

def plotGraph(graph, round_num):
    pos = nx.spring_layout(graph)
    prices = nx.get_node_attributes(graph, "price")
    labels = {n: f"{n}\n${prices[n]}" if n in prices else str(n) for n in graph.nodes}

    edge_labels = nx.get_edge_attributes(graph, "valuation")
    nx.draw(graph, pos, with_labels=True, labels=labels, node_color="skyblue", node_size=800, font_size=10)
    plt.title(f"Market Graph{' - Round ' + str(round_num) if round_num is not None else ''}")
    plt.show()

def marketClearing(graph, sellers, buyers, interactive=False):
    # Keep track of how many rounds to clear market
    round = 0
    while True:
        round += 1
        # Construct the preference graph
        PG = getPreferenceGraph(graph, sellers, buyers)
        matching = nx.bipartite.maximum_matching(PG, top_nodes=buyers)
        matched_buyers = set(k for k in matching if k in buyers)
        if len(matched_buyers) == len(buyers):
            print(f"Market cleared in {round} round(s)")
            break
        matched_sellers = set(v for k, v in matching.items() if k in buyers)
        constricted_set = set(sellers) - matched_sellers
        for s in constricted_set:
            graph.nodes[s]["price"] += 1
        if interactive:
            print(f"\n--- Round {round} ---")
            print(f"Matching: {matching}")
            print(f"Updated Prices: {[graph.nodes[n]['price'] for n in sellers]}")
            plotGraph(graph, round_num=round)
        if round >= 10:
            print("Market did not clear within 10 rounds.")
            break

def main():
    if not os.path.exists(sys.argv[1]):
        print(f"File {sys.argv[1]} not found.")
        sys.exit(1)
    graph = nx.read_gml(sys.argv[1])

    if not nx.is_bipartite(graph):
        print("Graph is not bipartite.")
        sys.exit(1)
    # Get bipartite sets from the graph
    sellers, buyers = nx.bipartite.sets(graph)

    # Start market clearing algorithm based on interactive flag
    marketClearing(graph, sellers, buyers, interactive=args.interactive)

if __name__ == '__main__':
    main()