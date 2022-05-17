import json
from pprint import pprint

from edge import Edge
from location import Location
from node import StationNode
from transport_graph import TransportGraph


def read_routes(path_to_file: str):
    with open(path_to_file, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)

        return data


def change_keys(data, direction="forward"):
    changed_data = {}
    for key, value in data.items():
        if direction == "forward":
            new_key = key + "->"
        elif direction == "backward":
            new_key = key + "<-"
        else:
            raise Exception("Wrong direction!")
        changed_data[new_key] = value

    return changed_data


def get_id_from_station_name(station_name: str):
    return station_name[station_name.find("(") + 1 : station_name.find(")")]


def create_graph(data):
    edges = []
    stations = {}
    for route_data in data.values():
        last_station = None
        last_dist = 0.0
        for point in route_data:
            point_lat, point_long, point_dist, point_name = point
            if point_name:
                if point_name not in stations:
                    new_station = StationNode(
                        location=Location(lat=point_lat, long=point_long),
                        name=point_name,
                    )
                    stations[point_name] = new_station
                if last_station:
                    new_edge = Edge(
                        start=last_station,
                        end=stations[point_name],
                        weight=point_dist - last_dist,
                    )
                    edges.append(new_edge)
                    last_station = stations[point_name]
                    last_dist = point_dist
                else:
                    last_station = stations[point_name]
                    last_dist = point_dist

    graph = TransportGraph(edges)
    return graph


def check_optimality_of_routes(graph, routes):
    for route_data in routes.values():
        for point in route_data:
            if point[3]:
                station = StationNode(
                    location=Location(lat=point[0], long=point[1]), name=point[3]
                )
                compare_dijkstra_with_direct(graph, route_data, station)
                break
        print("-----------------------")
        print("-----------------------")
        print("-----------------------")


def compare_dijkstra_with_direct(graph, route, station):
    direct_distances = {}
    for point in route:
        point_lat, point_long, point_dist, point_name = point
        if point_name:
            curr_station = StationNode(
                Location(lat=point_lat, long=point_long), name=point_name
            )
            direct_distances[curr_station] = point_dist

    dijkstra_distances, dijkstra_pr = graph._dijkstra(station)

    distances = {}
    for station, distance in direct_distances.items():
        try:
            distances[station] = (distance, dijkstra_distances[station])
        except:
            continue

    pprint(distances)
    curr_station = StationNode(
        location=Location(lat=49.83592, long=24.07091), name="Автостанція №6 (256)"
    )
    while isinstance(curr_station, StationNode):
        print(curr_station)
        curr_station = dijkstra_pr[curr_station]


if __name__ == "__main__":
    routes1 = change_keys(
        read_routes("./jsons/shapes_routes1.json"), direction="forward"
    )
    routes2 = change_keys(
        read_routes("./jsons/shapes_routes2.json"), direction="backward"
    )
    routes = routes1 | routes2
    graph = create_graph(routes)
    graph.check_connectivity()
    print("---------------------------------")
    check_optimality_of_routes(graph, routes)
