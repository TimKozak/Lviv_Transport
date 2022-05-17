# Seva Archakov
from dataclasses import dataclass


@dataclass(frozen=True)
class Location:
    lat: float = 0.0
    long: float = 0.0

    def __str__(self) -> str:
        return f"({self.lat}, {self.long})"

    def __hash__(self) -> int:
        return hash((self.lat, self.long))

    def __eq__(self, other: object) -> bool:
        return (self.lat, self.long) == (other.lat, other.long)

    def __ne__(self, other: object) -> bool:
        return not (self == other)
