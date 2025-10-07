# lab2_bfs.py
import networkx as nx
from collections import deque

def bfs(graph, start):
    visited = []
    queue = deque([start])
    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.append(node)
            # добавляем соседей в очередь (сортируем для детерминизма)
            neighbors = sorted(list(graph[node]))
            for n in neighbors:
                if n not in visited and n not in queue:
                    queue.append(n)
    return visited

def main():
    # Хардкод графа (целочисленные вершины)
    # Структура: 1 связан с 2,3; 2 с 4; 3 с 5; 4 и 5 соединены с 6
    G = nx.Graph()
    edges = [(1,2),(1,3),(2,4),(3,5),(4,6),(5,6)]
    G.add_edges_from(edges)

    start = 1
    order = bfs(G, start)
    print("Lab2 — BFS order from", start, ":")
    print(" -> ".join(map(str, order)))

if __name__ == "__main__":
    main()
