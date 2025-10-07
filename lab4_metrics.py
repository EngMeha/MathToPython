# lab4_metrics.py
import networkx as nx

def graph_metrics(G):
    if G.number_of_nodes() == 0:
        print("Пустой граф.")
        return
    if nx.is_connected(G):
        ecc = nx.eccentricity(G)
        radius = nx.radius(G)
        diameter = nx.diameter(G)
        centers = list(nx.center(G))
        print(f"Lab4 — Метрики (граф связный):")
        print(f" Радиус = {radius}")
        print(f" Диаметр = {diameter}")
        print(f" Центр(ы) = {centers}")
        print(" Эксцентриситеты вершин:")
        for v in sorted(ecc.keys(), key=lambda x: (int(x[1:]) if isinstance(x, str) and x.startswith('v') else x)):
            print(f"  {v}: {ecc[v]}")
    else:
        print("Lab4 — Граф несвязный. Метрики по компонентам:")
        for i, comp in enumerate(nx.connected_components(G), start=1):
            sub = G.subgraph(comp)
            ecc = nx.eccentricity(sub)
            radius = nx.radius(sub)
            diameter = nx.diameter(sub)
            centers = list(nx.center(sub))
            print(f" Компонента {i}: n={sub.number_of_nodes()} radius={radius}, diameter={diameter}, centers={centers}")

def main():
    # Хардкод: цикл из 6 вершин (подходит для метрик — связный)
    G = nx.cycle_graph(6)  # вершины 0..5
    # при желании можно перекодировать в формат v1..v6, но networkx удобно с целыми
    graph_metrics(G)

if __name__ == "__main__":
    main()
