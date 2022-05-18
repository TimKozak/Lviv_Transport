# Seva Archakov
from dataclasses import dataclass

from node import StationNode


@dataclass(frozen=True)
class Edge:
    start: StationNode
    end: StationNode
    distance: float
    weight: float = 1

    def __str__(self) -> str:
        return f"From {self.start} to {self.end} with distance {self.distance}"

    def __hash__(self) -> int:
        return hash((self.start, self.end))

    def __eq__(self, other: object) -> bool:
        return (self.start, self.end) == (other.start, other.end)

    def __ne__(self, other: object) -> bool:
        return not (self == other)
