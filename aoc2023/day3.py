from dataclasses import dataclass
from io import TextIOWrapper
from typing import TypeAlias, List, TypeVar
from aoc2023 import unicode_symbols as u

EngineMatrix: TypeAlias = List[str]
def ppem(em: EngineMatrix):
    print("  y")
    print("x ", end="")
    print("\n  ".join(em))

def safe_get(em: EngineMatrix, x: int, y: int) -> str | None:
    try:
        return em[y][x]
    except IndexError:
        return None


@dataclass
class PartNumber():
    number: int
    row: int
    span: tuple[int, int]

PartPos: TypeAlias = tuple[int, tuple[int, int]]

@dataclass
class Symbol():
    sym: str
    pos: tuple[int, int]
    numbers: dict[PartPos, PartNumber]

    def gear_ratio(self) -> int | None:
        if len(self.numbers) == 2 and self.sym == "*":
            [pn1, pn2] = map(lambda pn: pn.number, self.numbers.values())
            return pn1*pn2

def run(file: TextIOWrapper):
    em = parse_engine_matrix(file)

    symbols = get_all_symbols(em)

    print_symbols(symbols)
    print_part_nums(symbols)
    print_gear_ratios(symbols)

def parse_engine_matrix(file):
    em: EngineMatrix = []
    for line in file.readlines():
        em.append(line.strip())
    return em

def print_gear_ratios(symbols):
    gear_ratios = sum([
        ratio 
        for ratio in map(lambda s: s.gear_ratio(), symbols) 
        if ratio is not None])
    print(f"Gear ratios: {gear_ratios}")

def print_part_nums(symbols):
    sum_disc = 0
    for p in get_all_partnums(symbols):
        sum_disc += p.number
    print(f"Sum of part numbers: {sum_disc}")

def print_symbols(symbols):
    print(f"{u.presenter} Symbols found!")
    for s in symbols:
        char = f"{u.star}\t" if s.sym == "*" else f"{s.sym}\t"
        numbers = ", ".join([f"{n.number}" for _, n in s.numbers.items()])
        print(f"{char} at {s.pos} with gear ratio {s.gear_ratio()} has these parts: {numbers}")

def get_adjacent_partnums(em: EngineMatrix, pos: tuple[int, int]) -> dict[PartPos,PartNumber]:
    deltas = [-1, 0, 1]
    diagonals = [( pos[0] + xd, pos[1] + yd )
                 for xd in deltas
                 for yd in deltas
                 if not (xd,yd) == (0, 0)]

    adj_parts: dict[PartPos, PartNumber] = {}

    for (px, py) in diagonals:
        match determine_value(em, px, py):
            case PartNumber() as pn:
                adj_parts[(pn.row, pn.span)] = pn
            case _:
                pass

    return adj_parts

def get_all_partnums(symbols: List[Symbol]) -> List[PartNumber]:
    pns: dict[PartPos, PartNumber] = {}
    for symbol in symbols:
        pns = merge_onto_left(pns, symbol.numbers)

    return [v for v in pns.values()]

def get_all_overlapping(symbols: List[Symbol]) -> List[PartNumber]:
    pns: List[PartNumber] = []
    for symbol in symbols:
        for _, v in symbol.numbers.items():
            pns.append(v)

    return pns

def get_all_symbols(em: EngineMatrix) -> List[Symbol]:
    symbols: List[Symbol] = []
    for iy, row in enumerate(em):
        for ix, _ in enumerate(row):
            match determine_value(em, ix, iy):
                case Symbol() as s:
                    symbols.append(s)
                case _:
                    pass
    return symbols

K = TypeVar("K")
V = TypeVar("V")
def merge_onto_left(left: dict[K, V], right: dict[K, V]):
    fresh_dict = left.copy()
    for (k, v) in right.items():
        fresh_dict[k] = v
    return fresh_dict

def prompt_data(em: EngineMatrix):
    while True:
        try:
            print("Get char at pos x y:", end=" ")
            inp = input()
            if inp.strip() == "":
                break
            [x, y] = map(int, inp.split(" "))
            match determine_value(em, x, y):
                case PartNumber(num, row, (start, end)):
                    print(f"Part number {num} at row {row} spanning ({start}, {end})")
                case Symbol(sym, (x,y)):
                    print(f"Symbol {sym} at ({x}, {y})")
                case None:
                    print(f"Nothing found at ({x}, {y})")


            print(em[y][x])
        except Exception as e:
            print(f"I did not understand that ({type(e).__name__}: {e})")
    print("Exiting loop!")


def get_partnum(em: EngineMatrix, x: int, y: int):
    start = x
    try:
        while em[y][start-1].isdigit() and start > 0:
            start -= 1
            if start < 0:
                print(f"Start is {start}, why? isdigit = {em[y][start].isdigit()}")

    except IndexError:
        print(f"Got indexError for y={y}, start = {start}")
        pass

    end = x
    try:
        while em[y][end+1].isdigit():
            end += 1
            if end < 0:
                print(f"End is {end}, why?")
    except IndexError:
        pass

    try:
        value = int(em[y][start:end+1])
    except ValueError as e:
        print(f"{em[y]}\n[{y}] start, end = {start}, {end}; x == {x}")
        raise e

    return PartNumber(number=value, row=y, span=(start, end))


def determine_value(em: EngineMatrix, x:int , y: int) -> PartNumber | Symbol | None:
    match em[y][x]:
        case ".":
            return None
        case digit if digit.isdigit():
            return get_partnum(em, x, y)
        case symbol:
            return Symbol(symbol, (x,y), get_adjacent_partnums(em, (x, y)))



