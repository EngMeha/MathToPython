import matplotlib.pyplot as plt
import networkx as nx
import re
from collections import deque
import itertools
import sys

def parse_input(raw: str):
    """
    Ожидается формат:
    {{v1, v2, v3},{(v1, v2), (v2, v3)}}
    Возвращает (list_nodes, list_edges)
    """
    # Разделяем по "},{", но сначала убираем начальные/концевые пробелы
    formal_input = raw.strip().split("},{")
    list_formal_input = [item.replace("{{", "").replace("}}", "").replace("{", "").replace("}", "") for item in formal_input]
    if len(list_formal_input) != 2:
        raise ValueError("Неверный формат ввода. Пример: {{v1, v2, v3},{(v1, v2), (v2, v3)}}")

    # Ноды — разделяем по запятой
    list_node = [item.strip() for item in list_formal_input[0].split(",") if item.strip()]

    # Парсинг рёбер. Поддерживаем формат (vX, vY) с возможными пробелами.
    # Постарался сделать гибкий шаблон: захватывает слова/идентификаторы, не только v\d+
    pair_tuples = re.findall(r'\(\s*([^\s,()]+)\s*,\s*([^\s,()]+)\s*\)', list_formal_input[1])
    list_connection = [(a, b) for a, b in pair_tuples]

    return list_node, list_connection

def show_graph(list_node, list_connection):
    G = nx.Graph()
    G.add_nodes_from(list_node)
    G.add_edges_from(list_connection)

    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=600)
    plt.show()
    return G

# ------------- Traversals -------------
def bfs(G, start):
    """Возвращает порядок обхода в ширину от start (если start нет — берём любую вершину)."""
    if start not in G:
        # попробуем взять первую вершину
        start = next(iter(G.nodes), None)
        if start is None:
            return []
    visited = set()
    q = deque([start])
    order = []
    visited.add(start)
    while q:
        v = q.popleft()
        order.append(v)
        for nbr in G.neighbors(v):
            if nbr not in visited:
                visited.add(nbr)
                q.append(nbr)
    return order

def dfs_iterative(G, start):
    """Итеративный DFS (стек)."""
    if start not in G:
        start = next(iter(G.nodes), None)
        if start is None:
            return []
    visited = set()
    stack = [start]
    order = []
    while stack:
        v = stack.pop()
        if v in visited:
            continue
        visited.add(v)
        order.append(v)
        # добавляем соседей в порядке, обратном желаемому (чтобы левый обход шел как рекурсивный)
        for nbr in reversed(list(G.neighbors(v))):
            if nbr not in visited:
                stack.append(nbr)
    return order

def dfs_recursive(G, start, visited=None, order=None):
    if visited is None:
        visited = set()
    if order is None:
        order = []
    if start not in G:
        return order
    visited.add(start)
    order.append(start)
    for nbr in G.neighbors(start):
        if nbr not in visited:
            dfs_recursive(G, nbr, visited, order)
    return order

# ------------- Metrics -------------
def graph_metrics(G):
    metrics = {}
    metrics['num_nodes'] = G.number_of_nodes()
    metrics['num_edges'] = G.number_of_edges()
    metrics['degrees'] = dict(G.degree())
    # Компоненты связности
    comps = list(nx.connected_components(G))
    metrics['num_components'] = len(comps)
    metrics['components'] = comps
    # Эксцентриситет / диаметр / радиус — только для каждой связной компоненты отдельно
    ecc = {}
    diam = {}
    rad = {}
    avg_shortest = {}
    for i, comp in enumerate(comps, start=1):
        sub = G.subgraph(comp)
        if sub.number_of_nodes() == 1:
            ecc[i] = {next(iter(sub.nodes())): 0}
            diam[i] = 0
            rad[i] = 0
            avg_shortest[i] = 0.0
        else:
            try:
                ecc_map = nx.eccentricity(sub)
                ecc[i] = ecc_map
                diam[i] = nx.diameter(sub)
                rad[i] = nx.radius(sub)
                # средняя длина кратчайшего пути в компоненте
                avg_shortest[i] = nx.average_shortest_path_length(sub)
            except nx.NetworkXError as e:
                ecc[i] = {}
                diam[i] = None
                rad[i] = None
                avg_shortest[i] = None
    metrics['eccentricity_by_component'] = ecc
    metrics['diameter_by_component'] = diam
    metrics['radius_by_component'] = rad
    metrics['avg_shortest_path_by_component'] = avg_shortest
    # Кластер коэффициент (локальный и средний)
    metrics['clustering'] = nx.clustering(G)
    metrics['average_clustering'] = nx.average_clustering(G) if G.number_of_nodes() > 0 else 0.0
    return metrics

# ------------- Eulerian check -------------
def is_eulerian_manual(G):
    """Проверка эйлеровости для неориентированного графа: связен (с учётом только вершин с degree>0) и все степени чётные."""
    if G.number_of_nodes() == 0:
        return False
    # Берём вершины с положительной степенью
    non_zero_nodes = [n for n, d in G.degree() if d > 0]
    if not non_zero_nodes:
        # пустой граф — условно эйлеров (нет ребер)
        return True
    sub = G.subgraph(non_zero_nodes)
    if not nx.is_connected(sub):
        return False
    for _, d in sub.degree():
        if d % 2 != 0:
            return False
    return True

# ------------- Hamiltonian search (backtracking) -------------
def find_hamiltonian_cycle_backtracking(G, time_limit_nodes=17):
    """
    Ищет гамильтонов цикл (если найдёт — возвращает список вершин в цикле, иначе None).
    Ограничение: комбинаторно сложно; ставим мягкое предупреждение по размеру N.
    """
    n = G.number_of_nodes()
    if n == 0:
        return None
    if n > 20:
        # предупреждение: слишком много вершин, взрывной поиск
        print("Внимание: поиск гамильтонова цикла экспоненциален. N >", 20, " — может работать очень долго.")
    nodes = list(G.nodes())

    def backtrack(path, used):
        if len(path) == n:
            # проверим, есть ли ребро от последней к первой (цикл)
            if path[0] in G[path[-1]]:
                return path[:]
            else:
                return None
        for nbr in G.neighbors(path[-1]):
            if nbr not in used:
                used.add(nbr)
                path.append(nbr)
                res = backtrack(path, used)
                if res:
                    return res
                path.pop()
                used.remove(nbr)
        return None

    for start in nodes:
        res = backtrack([start], {start})
        if res:
            res.append(res[0])  # замкнём цикл для наглядности
            return res
    return None

def find_hamiltonian_path_backtracking(G):
    """Ищет гамильтонов путь (не обязательно цикл)."""
    n = G.number_of_nodes()
    if n == 0:
        return None
    nodes = list(G.nodes())

    def backtrack(path, used):
        if len(path) == n:
            return path[:]
        for nbr in G.neighbors(path[-1]):
            if nbr not in used:
                used.add(nbr)
                path.append(nbr)
                res = backtrack(path, used)
                if res:
                    return res
                path.pop()
                used.remove(nbr)
        return None

    for start in nodes:
        res = backtrack([start], {start})
        if res:
            return res
    return None

# ------------- Greedy algorithms -------------
def greedy_coloring(G):
    """Жадная раскраска вершин (networkx реализует уже greedy_color)"""
    coloring = nx.coloring.greedy_color(G, strategy='largest_first')
    # Вернуть как список (vertex -> color)
    return coloring

def greedy_nearest_neighbor_path(G, start=None):
    """
    Жадный nearest-neighbor для получения пути (эвристика TSP-like).
    Работает для взвешенных/невзвешенных: если веса есть, берёт наименьший вес; иначе — просто первый сосед.
    Возвращает порядок посещения всех вершин (если граф несвязен — посетит компоненту start).
    """
    if G.number_of_nodes() == 0:
        return []
    if start is None or start not in G:
        start = next(iter(G.nodes()))
    visited = {start}
    path = [start]
    cur = start
    while len(visited) < G.number_of_nodes():
        # выбираем ближайшего соседа, который ещё не посещён
        candidates = [v for v in G.nodes() if v not in visited and G.has_edge(cur, v)]
        if not candidates:
            # если нет непросмотренных соседей — пробуем найти ближайшую непросмотренную вершину через кратчайший путь
            # найдём непросмотренную вершину с минимальным расстоянием (в смысле числа ребер)
            min_dist = None
            next_node = None
            for v in G.nodes():
                if v in visited:
                    continue
                try:
                    d = nx.shortest_path_length(G, source=cur, target=v)
                except nx.NetworkXNoPath:
                    d = None
                if d is not None and (min_dist is None or d < min_dist):
                    min_dist = d
                    next_node = v
            if next_node is None:
                # не сможем достигнуть оставшиеся вершины из текущей компоненты
                break
            # достроим кратчайший путь до next_node и пометим вершины посещёнными по пути
            sp = nx.shortest_path(G, source=cur, target=next_node)
            # первый в sp = cur, пропускаем его
            for node in sp[1:]:
                if node not in visited:
                    visited.add(node)
                    path.append(node)
            cur = path[-1]
        else:
            # если граф взвешенный, используем вес; иначе — берем любую (deterministic: min by name)
            best = None
            best_w = None
            for c in candidates:
                if 'weight' in G[cur][c]:
                    w = G[cur][c]['weight']
                else:
                    w = 1
                if best is None or w < best_w or (w == best_w and str(c) < str(best)):
                    best = c
                    best_w = w
            visited.add(best)
            path.append(best)
            cur = best
    return path

# ------------- CLI и запуск -------------
def main():
    try:
        raw = input("Введите данные графа (пример: {{v1, v2, v3},{(v1, v2), (v2, v3)}}):\n")
        nodes, edges = parse_input(raw)
    except Exception as e:
        print("Ошибка разбора ввода:", e)
        sys.exit(1)

    G = show_graph(nodes, edges)

    # Меню операций (быстро и прямо)
    print("\nВыполняю вычисления...")

    # Traversals
    start = nodes[0] if nodes else None
    print("BFS from", start, ":", bfs(G, start))
    print("DFS iterative from", start, ":", dfs_iterative(G, start))
    print("DFS recursive from", start, ":", dfs_recursive(G, start))

    # Metrics
    metrics = graph_metrics(G)
    print("\n--- Метрические характеристики ---")
    print("Число вершин:", metrics['num_nodes'])
    print("Число ребер:", metrics['num_edges'])
    print("Степени вершин:", metrics['degrees'])
    print("Число компонент связности:", metrics['num_components'])
    for i, comp in enumerate(metrics['components'], start=1):
        print(f" Компонента {i}: {len(comp)} вершин")
    print("Средняя кластеризация:", metrics['average_clustering'])
    print("Коэффициент кластеризации по вершинам:", metrics['clustering'])
    print("Эксцентриситет по компонентам:", metrics['eccentricity_by_component'])
    print("Диаметры по компонентам:", metrics['diameter_by_component'])
    print("Радиусы по компонентам:", metrics['radius_by_component'])
    print("Средняя длина кратчайшего пути по компонентам:", metrics['avg_shortest_path_by_component'])

    # Eulerian
    print("\n--- Эйлеровость ---")
    manual_euler = is_eulerian_manual(G)
    nx_euler = nx.is_eulerian(G)
    print("Проверка (manual):", manual_euler)
    print("Проверка networkx.is_eulerian():", nx_euler)
    if manual_euler:
        try:
            euler_circuit = list(nx.eulerian_circuit(G)) if nx.is_eulerian(G) else None
            print("Эйлеров цикл (edge sequence):", euler_circuit)
        except Exception:
            print("Не удалось получить эйлеров цикл через networkx.")

    # Hamiltonian (backtracking — может быть медленно)
    print("\n--- Гамильтонов поиск (backtracking) ---")
    ham_cycle = find_hamiltonian_cycle_backtracking(G)
    if ham_cycle:
        print("Найден гамильтонов цикл:", ham_cycle)
    else:
        ham_path = find_hamiltonian_path_backtracking(G)
        if ham_path:
            print("Найден гамильтонов путь (но не цикл):", ham_path)
        else:
            print("Гамильтонова пути/цикла не найдено (или поиск слишком дорог).")

    # Greedy algorithms
    print("\n--- Жадные алгоритмы ---")
    coloring = greedy_coloring(G)
    print("Жадная раскраска (вершина -> цвет):", coloring)
    nn_path = greedy_nearest_neighbor_path(G, start)
    print("Жадный nearest-neighbor путь (эвристика):", nn_path)

    print("\nГотово.")

if __name__ == "__main__":
    main()