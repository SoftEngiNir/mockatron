import networkx as nx
import matplotlib.pyplot as plt
from ddgen.schema.column import Column
from ddgen.schema.table import TableSchema
from typing import List, Dict
from collections import defaultdict

def construct_graph(graph_dict: Dict[Column, List[Column]]) -> nx.DiGraph:
    G = nx.DiGraph()
    for node, neighbors in graph_dict.items():
        for neighbor in neighbors:
            G.add_edge(node.table, neighbor.table)
    return G

def sorted_in_degree(graph: nx.DiGraph) -> Dict[int, TableSchema]:
    tree = graph.in_degree
    table_in_deg = defaultdict(list)
    for table, in_deg in tree:
        table_in_deg[in_deg].append(table)
    return {k: table_in_deg[k] for k in sorted(table_in_deg)}

def vizualize_graph(graph: nx.DiGraph) -> None:
    # Draw the graph
    pos = nx.spring_layout(graph)  # Layout for visualization
    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_color="lightblue",
        edge_color="gray",
        node_size=2000,
        font_size=16,
        font_weight="bold",
    )
    plt.title("Graph Visualization")
    plt.show()




