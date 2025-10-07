# lab3_dfs.py
import networkx as nx
import sys

sys.setrecursionlimit(10000)

def dfs(graph, start, visited=None):
    if visited is None:
        visited = []
    visited.append(start)
    for neighbor in sorted(graph[start]):
        if neighbor not in visited:
            dfs(graph, neighbor, visited)
    return visited

def main():
    # Хардкод графа (тот же, что в lab2)
    G = nx.Graph()
    edges = [(1,2),(1,3),(2,4),(3,5),(4,6),(5,6)]
    G.add_edges_from(edges)

    start = 1
    order = dfs(G, start)
    print("Lab3 — DFS order from", start, ":")
    print(" -> ".join(map(str, order)))

if __name__ == "__main__":
    main()
