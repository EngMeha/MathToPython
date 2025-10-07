# lab7_greedy_shortest_path.py
import matplotlib.pyplot as plt
import networkx as nx
import heapq

def dijkstra(G, source):
    dist = {v: float('inf') for v in G.nodes()}
    prev = {v: None for v in G.nodes()}
    dist[source] = 0.0
    pq = [(0.0, source)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, data in G[u].items():
            w = data.get('weight', 1.0)
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))
    return dist, prev

def reconstruct_path(prev, s, t):
    if t not in prev:
        return None
    if prev[t] is None and s != t:
        if s == t:
            return [s]
        return None
    path = []
    cur = t
    while cur is not None:
        path.append(cur)
        if cur == s:
            break
        cur = prev[cur]
    path.reverse()
    if path[0] != s:
        return None
    return path

def show_graph_with_path(G, path, title="Shortest path"):
    pos = nx.spring_layout(G)
    plt.figure(figsize=(6,5))
    nx.draw_networkx_nodes(G, pos, node_size=600)
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edges(G, pos, edgelist=G.edges())
    if path and len(path) >= 2:
        path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, width=3, edge_color='r')
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.title(title)
    plt.axis('off')
    plt.show()

def main():
    # Хардкод: взвешенный граф
    G = nx.Graph()
    weighted_edges = [(1,2,2),(1,3,5),(2,4,1),(3,4,2),(4,5,3)]
    G.add_weighted_edges_from(weighted_edges)

    source = 1
    target = 5
    dist, prev = dijkstra(G, source)
    if dist[target] == float('inf'):
        print("Lab7 — Нет пути от", source, "до", target)
        return
    path = reconstruct_path(prev, source, target)
    print(f"Lab7 — Dijkstra: shortest path {source} -> {target}:")
    print(" -> ".join(map(str, path)))
    print(f"Distance: {dist[target]}")

    show_graph_with_path(G, path, title=f"Shortest path {source} -> {target}")

if __name__ == "__main__":
    main()
