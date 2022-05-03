# Seva Archakov
from dataclasses import dataclass
from node import StationNode


@dataclass(frozen=True)
class Edge:
    start: StationNode
    end: StationNode
    weight: float
