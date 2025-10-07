# lab5_euler.py
import matplotlib.pyplot as plt
import networkx as nx

def show_graph_with_path(G, path_edges=None, title="Graph"):
    pos = nx.spring_layout(G)
    plt.figure(figsize=(6,5))
    nx.draw_networkx_nodes(G, pos, node_size=600)
    nx.draw_networkx_labels(G, pos)
    base_edges = [e for e in G.edges() if (path_edges is None) or (e not in path_edges and (e[1], e[0]) not in path_edges)]
    nx.draw_networkx_edges(G, pos, edgelist=base_edges)
    if path_edges:
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, width=3, edge_color='r')
    plt.title(title)
    plt.axis('off')
    plt.show()

def main():
    # Хардкод: простой эйлеров граф — цикл 4 вершин
    G = nx.Graph()
    edges = [(1,2),(2,3),(3,4),(4,1)]
    G.add_edges_from(edges)

    print("Lab5 — Euler check:")
    if nx.is_eulerian(G):
        print(" Граф эйлеров — существует эйлеров цикл.")
        circuit = list(nx.eulerian_circuit(G))
        print(" Эйлеров цикл (последовательность ребер):")
        print("  " + " -> ".join([f"{u}-{v}" for u,v in circuit]))
        # выделим цикл (в undirected представим как упорядоченные пары)
        path_edges = [(u,v) for u,v in circuit]
        show_graph_with_path(G, path_edges, title="Eulerian circuit (red)")
    else:
        odd = [v for v,d in G.degree() if d%2==1]
        if len(odd) == 2:
            print(" Граф имеет эйлеров путь (но не цикл). Нечетные вершины:", odd)
            show_graph_with_path(G, None, title="Eulerian trail (no circuit)")
        else:
            print(" Не Эйлеров. Нечетные вершины:", odd)
            show_graph_with_path(G, None, title="Not Eulerian")

if __name__ == "__main__":
    main()
