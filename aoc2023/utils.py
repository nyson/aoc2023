from dataclasses import dataclass
from typing import Any, TypeVar

@dataclass
class Pos():
    x: int
    y: int

    def adjs(self):
        return [Pos(self.x + x,self.y + y) for (x,y) in [(1, 0), (-1, 0), (0, 1), (0, -1)]]

    def adjs_diag(self):
        ixs = [-1, 0, 1]
        return [Pos(self.x + x,self.y + y)
                for x in ixs
                for y in ixs
                if (x,y) != (0,0)]

    def __add__(self, other: Any):
        return Pos(self.x + other.x, self.y + other.y)

    def __lt__(self, other:Any) -> bool:
        return (self.x, self.y) < (other.x, other.y)

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __repr__(self) -> str:
        return self.__str__()


T = TypeVar("T")
def filter_empty(l: list[T | None]) -> list[T]:
    return [c for c in l if c is not None]