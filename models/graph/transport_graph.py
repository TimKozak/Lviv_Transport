# Seva Archakov
from collections import deque
from queue import PriorityQueue
from sys import maxsize as INT_MAX
from typing import List

import pandas as pd

from edge import Edge
from node import StationNode


class TransportGraph:
    def __init__(self, edges: List[Edge]) -> None:
        self._edges = edges
        data = self._process_edges(edges)
        self._adjacency_list = data[0]
        self._stations = data[1]

    def _process_edges(self, edges: List[Edge]) -> tuple:
        adjacency_list = {}
        stations = set()

        for edge in edges:
            start = edge.start
            end = edge.end
            weight = edge.weight
            distance = edge.distance

            if start not in adjacency_list:
                adjacency_list[start] = []
            if end not in adjacency_list:
                adjacency_list[end] = []

            adjacency_list[start].append((end, weight, distance))

            stations.add(start)
            stations.add(end)

        return adjacency_list, list(stations)

    def check_connectivity(self):
        visited_stations = self._dfs(self._stations[0])
        print(list(set(self._stations) - set(visited_stations)))

    def generate_route_changes_csv(self):
        df_route_changes = []
        for station in self._stations:
            print(station)
            print("-------------------------")
            route_changes, distances, station_coordinates = self._zero_one_bfs(station)
            station_data = []
            for end_station, changes in route_changes.items():
                row = [
                    station.name.split("-")[0],
                    station.location.lat,
                    station.location.long,
                    end_station,
                    station_coordinates[end_station].lat,
                    station_coordinates[end_station].long,
                    changes,
                    distances[end_station],
                ]
                station_data.append(row)
            df_route_changes.extend(station_data)

        df = pd.DataFrame(
            df_route_changes,
            columns=[
                "from",
                "from_lat",
                "from_long",
                "to",
                "to_lat",
                "to_long",
                "changes",
                "distance",
            ],
        )
        df.to_csv("./data/generated_data/route_changes.csv", index=False)

    def _dfs(self, start):
        stack = [start]
        visited_stations = []

        while stack:
            station = stack.pop()
            if station in visited_stations:
                continue
            visited_stations.append(station)
            for edge in self._adjacency_list[station]:
                stack.append(edge[0])

        return visited_stations

    def _dijkstra(self, start: StationNode):
        visited = []
        cost = {station: float("inf") for station in self._stations}
        cost[start] = 0
        pr = {}
        pr[start] = -1

        pq = PriorityQueue()
        pq.put((0, start))

        while not pq.empty():
            (curr_cost, curr_station) = pq.get()
            visited.append(curr_station)

            for edge in self._adjacency_list[curr_station]:
                next_station = edge[0]
                curr_weight = edge[1]

                if next_station not in visited:
                    old_cost = cost[next_station]
                    new_cost = cost[curr_station] + curr_weight

                    if new_cost < old_cost:
                        pq.put((new_cost, next_station))
                        cost[next_station] = new_cost
                        pr[next_station] = curr_station

        return cost, pr

    def _zero_one_bfs(self, start: StationNode):
        distances = {station: INT_MAX for station in self._stations}
        real_distances = {station: INT_MAX for station in self._stations}

        Q = deque()
        distances[start] = 0
        real_distances[start] = 0
        Q.append(start)

        while Q:
            curr_station = Q[0]
            Q.popleft()
            for edge in self._adjacency_list[curr_station]:
                next_station = edge[0]
                curr_weight = edge[1]
                curr_distance = edge[2]
                if distances[next_station] > distances[curr_station] + curr_weight:
                    distances[next_station] = distances[curr_station] + curr_weight
                    real_distances[next_station] = (
                        real_distances[curr_station] + curr_distance
                    )
                    if curr_weight == 0:
                        Q.appendleft(next_station)
                    else:
                        Q.append(next_station)

        min_distances = {}
        stations_coordinates = {}
        for station, changes in distances.items():
            station_name = station.name.split("-")[0]
            if station_name not in min_distances:
                min_distances[station_name] = INT_MAX
                stations_coordinates[station_name] = station.location

            min_distances[station_name] = min(min_distances[station_name], changes)

        min_real_distances = {}
        for station, real_distance in real_distances.items():
            station_name = station.name.split("-")[0]
            if station_name not in min_real_distances:
                min_real_distances[station_name] = INT_MAX

            min_real_distances[station_name] = min(
                min_real_distances[station_name], real_distance
            )

        return min_distances, min_real_distances, stations_coordinates
