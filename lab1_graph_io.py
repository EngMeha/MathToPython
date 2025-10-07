# lab1_graph_io.py
import matplotlib.pyplot as plt
import networkx as nx

def main():
    # Хардкод: простой граф с вершинами v1..v5
    nodes = ["v1", "v2", "v3", "v4", "v5"]
    edges = [("v1", "v2"), ("v1", "v3"), ("v2", "v4"), ("v3", "v5"), ("v4", "v5")]

    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    print(f"Nodes: {G.number_of_nodes()}, Edges: {G.number_of_edges()}")
    print("Nodes list:", nodes)
    print("Edges list:", edges)

    plt.figure(figsize=(6, 5))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=600, node_color='lightblue', font_weight='bold')
    plt.title("Lab1 — Input Graph (hardcoded)")
    plt.show()

if __name__ == "__main__":
    main()
