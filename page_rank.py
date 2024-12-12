import sys
import os
import time
import argparse
from progress import Progress
import random

def load_graph(args):
    graph = {}

    # Process the file line by line to build the graph.
    for line in args.datafile:
        # Each line contains two URLs representing a directed edge.
        node, target = line.split()

        # Add the node to the graph if not already present.
        if node not in graph:
            graph[node] = []

        # Append the target URL to the list of outgoing edges for the node.
        graph[node].append(target)

    return graph

def print_graph(graph):
    print("Graph structure:")
    for node, edges in graph.items():
        edges_str = ", ".join(edges) if edges else "(no outgoing edges)"
        print(f"{node} -> {edges_str}")

def print_stats(graph):
    # Calculate the total number of nodes (keys in the graph dictionary).
    num_nodes = len(graph)

    # Calculate the total number of edges (sum of the lengths of all adjacency lists).
    num_edges = sum(len(targets) for targets in graph.values())

    # Output the calculated statistics.
    print(f"Number of nodes: {num_nodes}")
    print(f"Number of edges: {num_edges}")

def stochastic_page_rank(graph, args):
    # Initialize a hit counter for each node in the graph.
    hit_count = {node: 0 for node in graph}

    # Choose a random starting node for the random walk.
    current_node = random.choice(list(graph.keys()))

    # Track progress using a progress bar.
    progress = Progress(args.steps, title="Stochastic PageRank", width=50)

    # Perform the random walk for the specified number of steps.
    for _ in range(args.steps):
        if not graph[current_node]:  # Handle nodes with no outgoing edges.
            current_node = random.choice(list(graph.keys()))  # Jump to a random node.
        else:
            current_node = random.choice(graph[current_node])  # Follow a random outgoing edge.

        # Record the visit to the current node.
        hit_count[current_node] += 1

        # Update and display the progress bar.
        progress += 1
        progress.show()

    # Clear the progress bar after completion.
    progress.finish()

    return hit_count

def distribution_page_rank(graph, args):
    # Start with equal probability for all nodes.
    num_nodes = len(graph)
    node_prob = {node: 1 / num_nodes for node in graph}

    # Track progress using a progress bar.
    progress = Progress(args.steps, title="Distribution PageRank", width=50)

    # Update probabilities iteratively over the specified number of steps.
    for _ in range(args.steps):
        # Reset probabilities for the next iteration.
        next_prob = {node: 0 for node in graph}

        for node in graph:
            # If the node has outgoing edges, distribute its probability across them.
            out_degree = len(graph[node])
            if out_degree > 0:
                p = node_prob[node] / out_degree
                for target in graph[node]:
                    next_prob[target] += p

        # Update current probabilities with the new values.
        node_prob = next_prob

        # Update and display the progress bar.
        progress += 1
        progress.show()

    # Clear the progress bar after completion.
    progress.finish()

    return node_prob

# Configure argument parser for command-line interaction.
parser = argparse.ArgumentParser(description="Estimate PageRank from web link data.")
parser.add_argument('datafile', nargs='?', type=argparse.FileType('r'), default=sys.stdin,
                    help="Text file containing URL pairs representing graph edges.")
parser.add_argument('-m', '--method', choices=('stochastic', 'distribution'), default='stochastic',
                    help="Choose the PageRank calculation method.")
parser.add_argument('-r', '--repeats', type=int, default=1_000_000,
                    help="Number of repetitions (not used in current algorithms).")
parser.add_argument('-s', '--steps', type=int, default=100,
                    help="Number of steps for the PageRank computation.")
parser.add_argument('-n', '--number', type=int, default=20,
                    help="Number of top-ranked results to display.")
parser.add_argument('-p', '--print-graph', action='store_true',
                    help="Print the graph in adjacency list format.")

if __name__ == '__main__':
    args = parser.parse_args()

    # Select the appropriate PageRank algorithm based on user input.
    algorithm = distribution_page_rank if args.method == 'distribution' else stochastic_page_rank

    # Load the graph data from the specified file.
    graph = load_graph(args)

    # Print the graph if the relevant argument is passed.
    if args.print_graph:
        print_graph(graph)

    # Measure the time taken for PageRank calculation.
    start = time.time()
    ranking = algorithm(graph, args)
    stop = time.time()
    elapsed_time = stop - start

    # Display the top-ranked pages based on the PageRank results.
    top = sorted(ranking.items(), key=lambda item: item[1], reverse=True)
    sys.stderr.write(f"Top {args.number} pages:\n")
    print('\n'.join(f'{100*v:.2f}\t{k}' for k, v in top[:args.number]))
    sys.stderr.write(f"Calculation took {elapsed_time:.2f} seconds.\n")
