from dataclasses import dataclass, field
from enum import Enum
from io import TextIOWrapper
from itertools import count
import itertools
from typing import Any, Iterator, Literal, Sequence, Type, TypeVar

class D(Enum):
    up   = 1
    down = 2
    left = 3
    right= 4

def counterpart(direction: D) -> D:
    match direction:
        case D.up: 		return D.down
        case D.down: 	return D.up
        case D.left: 	return D.right
        case D.right: 	return D.left

def pp_d(d: D) -> str:
    return {D.up: "U", D.down: "D", D.left: "L", D.right: "R"}[d]
"""
    y | 	y is vertical
      V
  x ->		x is horizontal
    7-F7-
    .FJ|7
    SJLL7
    |F--J
    LJ.LJ
"""
Pipe = Literal["S"] | tuple[D, D]

def has_d(p: Pipe, d: D):
    match p:
        case "S": return True
        case (d1, _) if d1 == d: return True
        case (_, d2) if d2 == d: return True
        case _: return False

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
    
    def __hash__(self) -> int:
        return hash((self.x, self.y))
    
    def __str__(self) -> str:
        return f"({self.x}, {self.y})"
    
    def __repr__(self) -> str:
        return self.__str__()

T = TypeVar("T")
def assume(t: T | None) -> T:
    if t is None:
        raise ValueError(f"Assumed {type(t)} wasn't None!")
    else:
        return t

def filter_none(xs: list[T | None]) -> list[T]:
    return [x for x in xs if x is not None]    


@dataclass
class PipeField():
    start: Pos
    grid: dict[Pos, Pipe]
    max: Pos
    path: set[Pos] | None = field(default = None)

    def in_grid(self, p: Pos) -> bool:
        return 0 <= p.x <= self.max.x and 0 <= p.y <= self.max.y 

    def grid_size(self) -> int:
        return self.max.x * self.max.y

    def get_area(self, from_pos: set[Pos]) -> set[Pos]:
        if self.path is None:
            self.get_path()
            if self.path is None:
                raise ValueError("Expected path to be set")


        visited: set[Pos] = set()

        to_visit = list(from_pos)
        
        while len(to_visit) > 0:
            p = to_visit.pop()
            if p in self.path:
                pass
            elif self.in_grid(p):
                visited.add(p)  
                for x in p.adjs_diag():
                    if self.in_grid(p) and x not in visited:
                        to_visit.append(x)
                
        # print(visited)

        # print(f"self.grid_size()=>{self.grid_size()} - len(visited){len(visited)} - len(self.path){len(self.path)}: {self.grid_size() - len(visited) - len(self.path)}")
        all = set([Pos(x,y) for x in range(0, self.max.x + 1) for y in range(0, self.max.y + 1)])
        
        # self.pp(highlight= all.difference(visited, self.path))
        return(all.difference(visited, self.path))


    def get_path(self, pp: bool = False) -> tuple[list[tuple[Pos, D]], set[Pos], set[Pos]]:
        current = self.start
        breadcrumbs: list[tuple[Pos, D]] = []
        prev: D | None = None
        left, right = set(), set()
        self.path = set()
        while True:
            next, momentum = self.walk_one(current, prev)
            breadcrumbs.append((current, momentum))

            if prev is not None:
                l, r = self.get_lr(current, prev)
                for e in l: left.add(e)
                for e in r: right.add(e)

            self.path.add(current)
            current = next
            prev = momentum
            if pp: self.pp(current)
            if self.grid.get(next) == "S": 
                break

        self.path = set([p for p, _ in breadcrumbs])
        self.pp(highlight=left.difference(self.path))
        # self.pp(highlight=self.path.difference(right))
        return breadcrumbs, self.get_area(left.difference(self.path)), self.get_area(right.difference(self.path))
    
    def get_lr(self, p: Pos, d:D) -> tuple[list[Pos], list[Pos]]:
        match self.grid.get(p):
            case None:
                raise ValueError(f"{p} should be oon path")

            #   v
            # R ║ L
            #   v
            case (D.up, D.down) : 
                a = [Pos(p.x-1, p.y)]
                b = [Pos(p.x+1, p.y)]
                return (a,b) if d == D.down else (b,a)
            
            #  L
            # >═>
            #  R
            case (D.left, D.right) :
                a = [Pos(p.x, p.y+1)]
                b = [Pos(p.x, p.y-1)]
                return (a,b) if d == D.right else (b,a)
            
            #   v
            # L ╚> 
            #   L   
            case (D.up, D.right) :
                a = [Pos(p.x-1, p.y), Pos(p.x, p.y+1)]
                b = []
                return (a,b) if d == D.down else (b,a)
            
            #  Ä
            # >╝ R
            #  R   
            case (D.up, D.left) :
                a = []
                b = [Pos(p.x+1, p.y), Pos(p.x, p.y+1)]
                return (a,b) if d == D.down else (b,a)
            
            #   L
            # L ╔
            #   Ä
            case (D.down, D.right) :
                a = [Pos(p.x-1, p.y), Pos(p.x, p.y-1)]
                b = []
                return (a,b) if d == D.left else (b,a)
            
            # R 
            # ╗ R
            # Ä 
            case (D.down, D.left) :
                a = []
                b = [Pos(p.x+1, p.y), Pos(p.x, p.y-1)]
                return (a,b) if d == D.right else (b,a)
            


            case invalid:
                print(ValueError(f"Unhandled case: {invalid}"))
        
        return [],[]

    def get_segments(self):
        pass


    def move_pos(self, p: Pos, d: D) -> Pos | None:
        next: Pos | None = None
        match d:
            case D.up: next = Pos(p.x, p.y-1)
            case D.down: next = Pos(p.x, p.y+1)
            case D.left: next = Pos(p.x-1, p.y)
            case D.right: next = Pos(p.x+1, p.y)

        nextPipe = self.grid.get(next)
        if nextPipe is not None and has_d(nextPipe, counterpart(d)):
            return next
        else:
            return None

    def paths_from_pos(self, p:Pos) -> list[D]:
        match self.grid.get(p):
            case (d1,d2):
                return [d1, d2]
            case None:
                return []
            case "S":
                return list(D)

        raise ValueError("This is not a valid state!")

    
    def pp_tup(self, dt: tuple[D, D]):
        # ╝ 	╗ 	╔ 	╚ 	╣ 	╩ 	╦ 	╠ 	═ 	║ 	╬ 	
        match sorted([dt[0], dt[1]], key=lambda x: x.value):
            case [D.up, D.down]: return " ║"
            case [D.up, D.left]: return "═╝"
            case [D.up, D.right]: return " ╚"
            case [D.down, D.left]: return "═╗"
            case [D.down, D.right]: return " ╔"
            case [D.left, D.right]: return "══"
    
    def pp(self, current: Pos | None = None, highlight: set[Pos] =set()):
        stuff = itertools.cycle("🎄⭐🔔🎄🦌🎁🎄")
        for y in range(0, self.max.y):
            for x in range(0, self.max.x):
                match self.grid.get(Pos(x,y)):
                    case _ if Pos(x,y) in highlight:
                        print("💩", end="")
                    case "S" if Pos(x,y) == current:
                        print("🎅", end="")

                    case _ if Pos(x,y) == current:
                        print("🎅", end="")
                    case None:
                        print("  ", end="")
                    case "S":
                        print("🛷", end="")
                    case (a,b) if self.path is not None and Pos(x,y) not in self.path:
                        print(next(stuff), end="")
                    case (a,b):
                        print(self.pp_tup((a,b)), end="")
            print()

    def find_segments(self):
        pass
                
    def walk_one(self, current: Pos, prev: D | None) -> tuple[Pos, D]:    
        available_moves = [
            d for d in self.paths_from_pos(current) 
            if prev is None or d != counterpart(prev)]
        
        possible_moves = [(m, d) 
                        for m, d in [(self.move_pos(current, d), d) for d in available_moves]
                        if m is not None
                        ]
        if len(possible_moves) == 0:
            raise ValueError(f"No possible moves from {current}")
        
        return possible_moves[0]


def parse_pipe(ch: str) -> Pipe | None:
    match ch:
        case "S": return "S"
        case "|": return (D.up,   D.down )
        case "-": return (D.left, D.right)
        case "7": return (D.down, D.left ) 
        case "F": return (D.down, D.right)
        case "J": return (D.up,   D.left )
        case "L": return (D.up,   D.right)
        case _: return None

def parse_grid(file) -> PipeField:
    width, height = 0, 0
    start: Pos | None = None
    grid: dict[Pos, Pipe] = {}
    for y in count():
        height = max(y, height)
        row = file.readline()
        if row == "": 
            break

        for x,c in enumerate(row):
            width = max(x, width)
            match parse_pipe(c):
                case None:
                    pass
        
                case "S":
                    start = Pos(x,y)
                    grid[Pos(x, y)] = "S"
        
                case p if p is not None:
                    grid[Pos(x, y)] = p
        
                case invalid:
                    raise ValueError(f"Unhandled case {invalid}")

    if start is None:
        raise ValueError("Expected to find starting position!")

    return PipeField(start, grid, Pos(width, height))



def run(file: TextIOWrapper):
    f = parse_grid(file)

    bc, left_area, right_area = f.get_path()

  
    print(f"Farthest part on the path: {len(bc) / 2}")

    f.pp(highlight=left_area)
    print(f"Left area: {len(left_area)}")
    f.pp(highlight=right_area)
    print(f"Right area: {len(right_area)}")
