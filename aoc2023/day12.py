from io import TextIOWrapper
import itertools
from typing import Iterator


def parse_pt1(f: TextIOWrapper) -> Iterator[tuple[str, list[int]]]:
    for l in f.readlines():
        [puz, runs] = l.strip().split()
        yield puz, list(map(int, runs.split(",")))

def parse_pt2(f: TextIOWrapper) -> Iterator[tuple[str, list[int]]]:
    for l in f.readlines():
        [puz, runs] = l.strip().split()
        yield ('?'.join(itertools.repeat(puz,5)),
               5*list(map(int, runs.split(","))))

def kf(s: str, rs: list[int], con: bool) -> int:
    return hash((s, ':'.join(map(str, rs)), con))


memo: dict[int,int] = {}
def memoize(key: int, val: int) -> int:
    memo[key] = val
    return val

def all_sols(p: str, rs: list[int], consuming: bool = False) -> int:
    mkey = kf(p, rs, consuming)

    if len(p)==0:
        return 1 if sum(rs) == 0 else 0

    match memo.get(mkey):
        case None: pass
        case i: return i

    match p[0], p[1:]:
        # broken but we got runs left
        case '#', rest if len(rs) > 0 and rs[0] > 0:
            return memoize(mkey, all_sols(rest, [rs[0] - 1, *rs[1:]], consuming=True))
        # no possible solutions unless we can consume runs
        case '#', _:
            return 0
        # ok but we have an empty rs we need to pop
        case '.', rest if consuming and len(rs) > 0 and rs[0] == 0:
            return memoize(mkey, all_sols(rest, rs[1:], consuming=False))
        # no possible oks as a consuming state wih none left to consume is bad
        case '.', rest if consuming:
            return 0
        # ok as we are not consuming
        case '.', rest:
            return memoize(mkey, all_sols(rest, rs, consuming))
        # branching case
        case '?', rest:
            return all_sols('.' + rest, rs, consuming) + all_sols('#' + rest, rs, consuming)
        case invalid:
            raise ValueError(invalid)

def part1(f: TextIOWrapper):
    s = 0
    for puzzle, runs in parse_pt1(f):
        print(f"{puzzle.ljust(25)}: {runs}", end ="")
        sols = all_sols(puzzle, runs)
        s += sols
        print(f" => {sols} solutions!")

    print(f"{s} total solutions!")

def run(f: TextIOWrapper, part: int):
    if part == 2:
        part2(f)
    else:
        part1(f)

def part2(f: TextIOWrapper):
    s = 0
    for puzzle, runs in parse_pt2(f):
        print(f"{puzzle}: {runs}")
        sols = all_sols(puzzle, runs)
        s += sols
        print(f"\t => {sols} solutions!")

    print(f"{s} total solutions!")

