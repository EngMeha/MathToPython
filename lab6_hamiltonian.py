# lab6_hamiltonian.py
import matplotlib.pyplot as plt
import networkx as nx
import itertools

def find_hamiltonian_cycle(G, time_limit_nodes=16):
    n = G.number_of_nodes()
    if n == 0:
        return None
    if n > time_limit_nodes:
        print(f"Warning: n={n} > {time_limit_nodes}. Поиск может занять очень много времени.")
    nodes = list(G.nodes())
    # пробуем все перестановки (брутфорс). Для детерминированности сортируем узлы
    for perm in itertools.permutations(sorted(nodes)):
        ok = True
        for i in range(len(perm)-1):
            if not G.has_edge(perm[i], perm[i+1]):
                ok = False
                break
        if ok and G.has_edge(perm[-1], perm[0]):
            return list(perm) + [perm[0]]  # возвращаем цикл с возвращением в начальную
    return None

def show_graph_with_cycle(G, cycle):
    pos = nx.spring_layout(G)
    plt.figure(figsize=(6,5))
    nx.draw_networkx_nodes(G, pos, node_size=600)
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edges(G, pos, edgelist=G.edges())
    if cycle:
        cycle_edges = [(cycle[i], cycle[i+1]) for i in range(len(cycle)-1)]
        nx.draw_networkx_edges(G, pos, edgelist=cycle_edges, width=3, edge_color='r')
    plt.title("Hamiltonian cycle (red) if found")
    plt.axis('off')
    plt.show()

def main():
    # Хардкод: цикл из 5 вершин (гарантированно гамильтонов)
    G = nx.cycle_graph(5)  # вершины 0..4
    cycle = find_hamiltonian_cycle(G)
    print("Lab6 — Hamiltonian check:")
    if cycle:
        print(" Найден гамильтонов цикл (порядок вершин):")
        print(" -> ".join(map(str, cycle)))
        show_graph_with_cycle(G, cycle)
    else:
        print(" Гамильтонова цикла не найдено.")

if __name__ == "__main__":
    main()
