# Seva Archakov
from typing import List
from queue import PriorityQueue

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

            if start not in adjacency_list:
                adjacency_list[start] = []

            adjacency_list[start].append((end, weight))

            stations.add(start)
            stations.add(end)

        return adjacency_list, stations

    def _dijkstra(self, start: StationNode):
        visited = []
        cost = {station: float("inf") for station in self._stations}
        cost[start] = 0

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

        return cost
