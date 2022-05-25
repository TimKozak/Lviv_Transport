# Seva Archakov
from collections import deque
from queue import PriorityQueue
from sys import maxsize as INT_MAX
from typing import List

import pandas as pd

from edge import Edge
from node import StationNode
from utils import UNIT_SIZE, lat_lon2km


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
            route_changes, station_coordinates = self._zero_one_bfs(station)
            station_data = []
            for end_station, changes in route_changes.items():
                row = [
                    station.name.split("-")[0],
                    station.location.lat,
                    station.location.lon,
                    end_station,
                    station_coordinates[end_station].lat,
                    station_coordinates[end_station].lon,
                    changes,
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
            ],
        )
        df.to_csv("./data/generated_data/route_changes.csv", index=False)

    def add_edges_for_close_stations(self, threshold=0.5):
        stations_pairs_list = self._get_close_pairs(threshold)

        for idx, pair in enumerate(stations_pairs_list):
            first_station, second_station = pair
            print(idx)
            print(first_station, second_station)
            first_connected_stations = [
                station[0] for station in self._adjacency_list[first_station]
            ]
            if second_station not in first_connected_stations:
                self._adjacency_list[first_station].append((second_station, 1, 0))

            second_connected_stations = [
                station[0] for station in self._adjacency_list[second_station]
            ]
            if first_station not in second_connected_stations:
                self._adjacency_list[second_station].append((first_station, 1, 0))

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

        Q = deque()
        distances[start] = 0
        Q.append(start)

        while Q:
            curr_station = Q[0]
            Q.popleft()
            for edge in self._adjacency_list[curr_station]:
                next_station = edge[0]
                curr_weight = edge[1]
                if distances[next_station] > distances[curr_station] + curr_weight:
                    distances[next_station] = distances[curr_station] + curr_weight
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

        return min_distances, stations_coordinates

    def _get_close_pairs(self, threshold: float):
        stations_km = lat_lon2km(stations=self._stations, unit_size=UNIT_SIZE)

        close_stations = []
        grid = dict()
        square_dist = threshold**2

        for idx, st in enumerate(stations_km):
            px, py = st.location.lat, st.location.lon
            fx = px // threshold
            fy = py // threshold

            if (fx, fy) not in grid:
                grid[(fx, fy)] = []

            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    nx = fx + dx
                    ny = fy + dy

                    if (nx, ny) in grid:
                        for jdx in grid[(nx, ny)]:
                            qx, qy = (
                                stations_km[jdx].location.lat,
                                stations_km[jdx].location.lon,
                            )
                            rijsq = (px - qx) ** 2 + (py - qy) ** 2

                            if square_dist >= rijsq:
                                close_stations.append(
                                    (self._stations[idx], self._stations[jdx])
                                )

            grid[(fx, fy)].append(idx)

        return close_stations
