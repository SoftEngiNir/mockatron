from __future__ import annotations

from collections import defaultdict

import matplotlib.pyplot as plt
import networkx as nx

from ddgen.schema.table import Table


def construct_graph(graph_dict: dict[Table, list[Table]]) -> nx.DiGraph:
    G = nx.DiGraph()
    for node, neighbors in graph_dict.items():
        G.add_node(node)
        for neighbor in neighbors:
            G.add_edge(node, neighbor)
    return G


def sorted_in_degree(graph: nx.DiGraph) -> dict[int, list[Table]]:
    tree = graph.in_degree
    table_in_deg = defaultdict(list)
    for table, in_deg in tree:
        table_in_deg[in_deg].append(table)
    return {k: table_in_deg[k] for k in sorted(table_in_deg)}


def vizualize_graph(graph: nx.DiGraph) -> None:
    pos = nx.spring_layout(graph)
    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_color='lightblue',
        edge_color='gray',
        node_size=2000,
        font_size=16,
        font_weight='bold',
    )
    plt.title('Graph Visualization')
    plt.show()
