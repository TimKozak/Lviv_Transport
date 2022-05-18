import json
from pprint import pprint

import pandas as pd

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
            new_key = key + ">"
        elif direction == "backward":
            new_key = key + "<"
        else:
            raise Exception("Wrong direction!")
        changed_data[new_key] = value

    return changed_data


def create_graph(data):
    edges = []
    stations_map = {}
    same_stations = {}
    for route_number, route_data in data.items():
        last_station = None
        last_dist = 0.0
        for point in route_data:
            point_lat, point_long, point_dist, point_name = point
            if point_name:
                point_name_with_route = f"{point_name}-{route_number}"

                if point_name not in same_stations:
                    same_stations[point_name] = []

                new_station = StationNode(
                    location=Location(lat=point_lat, long=point_long),
                    name=point_name_with_route,
                )

                same_stations[point_name].append(new_station)
                stations_map[point_name_with_route] = new_station

                if last_station:
                    new_edge = Edge(
                        start=last_station,
                        end=stations_map[point_name_with_route],
                        weight=0,
                        distance=point_dist - last_dist,
                    )
                    edges.append(new_edge)
                    last_station = stations_map[point_name_with_route]
                    last_dist = point_dist
                else:
                    last_station = stations_map[point_name_with_route]
                    last_dist = point_dist

    for stations in same_stations.values():
        for first_station in stations:
            for second_station in stations:
                if first_station != second_station:
                    edges.append(
                        Edge(
                            start=first_station,
                            end=second_station,
                            weight=1,
                            distance=0,
                        )
                    )

    graph = TransportGraph(edges)
    return graph


if __name__ == "__main__":
    routes1 = change_keys(
        read_routes("./jsons/shapes_routes1.json"), direction="forward"
    )
    routes2 = change_keys(
        read_routes("./jsons/shapes_routes2.json"), direction="backward"
    )
    routes = {**routes1, **routes2}

    graph = create_graph(routes)

    graph.generate_route_changes_csv()
