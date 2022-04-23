import json
import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()

def read_routes(path_to_file):
    with open(path_to_file, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

        return data


def transform_routes(routes, count=None):
    all_routes = []
    for name, route in routes.items():
        current_route = []
        for idx in range(len(route)-1):
            current_route.append((route[idx], route[idx+1]))
        all_routes.append(current_route)
    
    if count:
        all_routes = all_routes[:count]

    return all_routes


def visualize_graph(routes):
    c = 0
    for m in routes:
        G.add_edges_from(m, color=c)
        c+=1

    pos = nx.circular_layout(G)
    colors = nx.get_edge_attributes(G,'color').values()

    fig = plt.figure()
    nx.draw(G, pos, connectionstyle='arc3, rad = 0.1', with_labels = True, edge_color=colors, 
            node_size=40, node_color="#A0CBE2", edge_cmap = plt.cm.Blues)
    fig.set_facecolor('#DEDEDE')
    plt.show()


if __name__ == '__main__':
    direct_routes = read_routes('route1.json')
    reverse_routes = read_routes('route2.json')
    graph_routes = transform_routes(direct_routes, 5)
    visualize_graph(graph_routes)