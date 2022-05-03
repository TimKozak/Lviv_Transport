# Seva Archakov
from node import StationNode


class Edge:
    def __init__(self, start: StationNode, end: StationNode, weight: float) -> None:
        self.start = start
        self.end = end
        self.weight = weight
