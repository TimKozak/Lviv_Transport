# Seva Archakov
from dataclasses import dataclass
from location import Location


@dataclass(frozen=True)
class StationNode:
    location: Location
    name: str = None

    def __str__(self) -> str:
        return f"Station {self.name} with coordinates {str(self.location)}"

    def __hash__(self) -> int:
        return hash((self.name, self.location))

    def __eq__(self, other: object) -> bool:
        return (self.name, self.location) == (other.name, other.location)

    def __ne__(self, other: object) -> bool:
        return not (self == other)
