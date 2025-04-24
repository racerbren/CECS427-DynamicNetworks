import networkx as nx
import matplotlib.pyplot as plt
import argparse
import scrapy
import numpy as np
from scrapy.crawler import CrawlerProcess
import logging
logging.getLogger('matplotlib').setLevel(logging.CRITICAL)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--crawler", type=str, help="Specifies the file containing the initial web pages to crawl.")
    parser.add_argument("--input", type=str,help="Specifies the directed graph (graph.gml) to be used in the page rank algorithm and Loglog plot if the crawling is not provided")
    parser.add_argument("--loglogplot", action="store_true", help="Generates a log-log plot of the degree distribution of the graph")
    parser.add_argument("--crawler_graph", type=str, help="Saves the processed graph to out_graph.gml")
    parser.add_argument("--pagerank_values", type=str)
    return parser.parse_args()

class Spider(scrapy.Spider):
    name = "test_spider"
    
    def __init__(self, start_urls, allowed_domain, max_pages, graph):
        self.start_urls = start_urls
        self.allowed_domain = allowed_domain
        self.max_pages = max_pages
        self.graph = graph
        self.visited = set()

    def parse(self, response):
        if len(self.graph.nodes) >= self.max_pages:
            return
        
        url = response.url
        self.visited.add(url)
        self.graph.add_node(url)

        for link in response.css('a::attr(href)').getall():
            full_url = response.urljoin(link)
            if not full_url.endswith(".html"):
                continue
            if self.allowed_domain in full_url and len(self.graph.nodes) <= self.max_pages:
                self.graph.add_edge(url, full_url)
                self.visited.add(full_url)
                yield scrapy.Request(full_url, callback=self.parse)

def crawl(crawler):
    with open(crawler, "r") as f:
        n = f.readline()
        domain = f.readline()
        start_urls = f.read().splitlines()
    G = nx.DiGraph()
    process = CrawlerProcess()
    process.crawl(Spider, start_urls=start_urls, allowed_domain=domain.strip(), max_pages=int(n.strip()), graph=G)
    process.start()
    
    return G

def plot_loglog(graph):
    degrees = [d for n, d in graph.degree()]
    degree_count = np.bincount(degrees)
    x = np.arange(len(degree_count))
    y = degree_count[degree_count > 0]

    plt.figure()
    plt.loglog(x, y, 'b-')
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel("Degree")
    plt.ylabel("Frequency")
    plt.title("Log-Log Degree Distribution")
    plt.grid(True)
    plt.savefig("loglogplot.png")

def main():
    args = parse_args()
    
    if args.crawler:
        G = crawl(args.crawler)
    elif args.input:
        G = nx.read_gml(args.input)
    
    if args.loglogplot:
        #plot_loglog(G)
        pass
    
    if args.crawler_graph:
        nx.write_gml(G, args.crawler_graph)
        nx.draw(G, with_labels=True)
        plt.show()

    if args.pagerank_values:
        pagerank = nx.pagerank(G)
        with open(args.pagerank_values, "w") as f:
            for node, rank in pagerank.items():
                f.write(f"{node} {rank:.6f}\n")

if __name__ == "__main__":
    main()