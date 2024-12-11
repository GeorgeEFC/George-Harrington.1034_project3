import sys
import os
import time
import argparse
from progress import Progress
import random


def load_graph(args):
    """Load graph from text file

    Parameters:
    args -- arguments named tuple

    Returns:
    A dict mapping a URL (str) to a list of target URLs (str).
    """
    graph = {}

    # Iterate through the file line by line
    for line in args.datafile:
        # And split each line into two URLs
        node, target = line.split()

        # If the node is not already in the graph, add it with an empty list
        if node not in graph:
            graph[node] = []

        # Add the target URL to the list of outgoing links for the node
        graph[node].append(target)

    return graph



def print_stats(graph):
    """Print number of nodes and edges in the given graph"""

    # Number of nodes is the number of keys in the graph dictionary
    num_nodes = len(graph)

    # Number of edges is the sum of the lengths of the lists in the graph
    num_edges = sum(len(targets) for targets in graph.values())

    # Print the results
    print(f"Number of nodes: {num_nodes}")
    print(f"Number of edges: {num_edges}")


def stochastic_page_rank(graph, args):
    """Stochastic PageRank estimation

    Parameters:
    graph -- a graph object as returned by load_graph()
    args -- arguments named tuple

    Returns:
    A dict that assigns each page its hit frequency

    This function estimates the Page Rank by counting how frequently
    a random walk that starts on a random node will after n_steps end
    on each node of the given graph.
    """
    # Initialize hit_count for all nodes in the graph
    hit_count = {node: 0 for node in graph}

    # Select a random starting node
    current_node = random.choice(list(graph.keys()))
    hit_count[current_node] += 1

    # Perform the random walk for the specified number of steps (n_steps)
    for _ in range(args.steps):
        if not graph[current_node]:  # If current node has no outgoing edges
            # Choose a new random node if there are no outgoing edges
            current_node = random.choice(list(graph.keys()))
        else:
            # Otherwise, choose a random outgoing edge
            current_node = random.choice(graph[current_node])

        # Increment the hit count for the visited node
        hit_count[current_node] += 1

    return hit_count

def distribution_page_rank(graph, args):
    """Probabilistic PageRank estimation

    Parameters:
    graph -- a graph object as returned by load_graph()
    args -- arguments named tuple

    Returns:
    A dict that assigns each page its probability to be reached

    This function estimates the Page Rank by iteratively calculating
    the probability that a random walker is currently on any node.
    """
    # Initialize node probabilities: each node starts with equal probability
    num_nodes = len(graph)
    node_prob = {node: 1 / num_nodes for node in graph}

    # Repeat the process for n_steps times
    for _ in range(args.steps):
        # Initialize the next probabilities to 0
        next_prob = {node: 0 for node in graph}

        for node in graph:
            # Get the probability for the current node, which is its current probability divided by its out-degree
            out_degree = len(graph[node])
            if out_degree > 0:
                p = node_prob[node] / out_degree
                # Distribute the probability to each target node among the outgoing edges
                for target in graph[node]:
                    next_prob[target] += p

        # Update node probabilities with next_prob
        node_prob = next_prob

    return node_prob


parser = argparse.ArgumentParser(description="Estimates page ranks from link information")
parser.add_argument('datafile', nargs='?', type=argparse.FileType('r'), default=sys.stdin,
                    help="Textfile of links among web pages as URL tuples")
parser.add_argument('-m', '--method', choices=('stochastic', 'distribution'), default='stochastic',
                    help="selected page rank algorithm")
parser.add_argument('-r', '--repeats', type=int, default=1_000_000, help="number of repetitions")
parser.add_argument('-s', '--steps', type=int, default=100, help="number of steps a walker takes")
parser.add_argument('-n', '--number', type=int, default=20, help="number of results shown")


if __name__ == '__main__':
    args = parser.parse_args()
    algorithm = distribution_page_rank if args.method == 'distribution' else stochastic_page_rank

    graph = load_graph(args)

    print_stats(graph)

    start = time.time()
    ranking = algorithm(graph, args)
    stop = time.time()
    time = stop - start

    top = sorted(ranking.items(), key=lambda item: item[1], reverse=True)
    sys.stderr.write(f"Top {args.number} pages:\n")
    print('\n'.join(f'{100*v:.2f}\t{k}' for k,v in top[:args.number]))
    sys.stderr.write(f"Calculation took {time:.2f} seconds.\n")
