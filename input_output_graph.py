import matplotlib.pyplot as plt
import networkx as nx
import re

def input_data_graph():
    print("Введите данные алгоритма по формальному описанию")
    print("Пример: {{v1, v2, v3, v4, v5, v6},{(v1, v2), (v1, v3), (v1, v4), (v1, v5), (v2, v3), (v3, v4)}}")
    formal_input = input("Вводите по примеру: ").split("},{")

    list_formal_input = [item.replace("{{", "").replace("}}", "") for item in formal_input]
    list_node = []
    list_connection = []

    if len(list_formal_input) == 2:
        list_node = [item.replace(" ", "") for item in list_formal_input[0].split(",")]

        pairs = re.findall(r'\(v(\d+), v(\d+)\)', list_formal_input[1])
        list_connection = [(f"v{a}", f"v{b}") for a, b in pairs]

        show_graph(list_node, list_connection)


def show_graph(list_node, list_connection):
    G = nx.Graph()
    G.add_nodes_from(list_node)
    G.add_edges_from(list_connection)

    nx.draw(G, with_labels=True, font_weight='bold')

    plt.show()

input_data_graph()