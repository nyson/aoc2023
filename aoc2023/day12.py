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
def all_sols(p: str, rs: list[int], consuming: bool = False, prefix:str="") -> int:
    if len(p)==0:
        if sum(rs) == 0:
            return 1
        else:
            return 0

    match memo.get(kf(p, rs, consuming)):
        case None: pass
        case i: return i

    match p[0], p[1:]:
        # broken but we got runs left
        case '#', rest if len(rs) > 0 and rs[0] > 0:
            rsN = [rs[0] - 1, *rs[1:]]
            sol = all_sols(rest, rsN, consuming=True, prefix=prefix + '#')
            memo[kf(p, rs, consuming)] = sol
            return sol

        # no possible solutions unless we can consume runs
        case '#', _:
            return 0

        # ok but we have an empty rs we need to pop
        case '.', rest if consuming and len(rs) > 0 and rs[0] == 0:
            sol = all_sols(rest, rs[1:], consuming=False, prefix=prefix + '.')
            memo[kf(p, rs, consuming)] = sol
            return sol

        # no possible oks as a consuming state wih none left to consume is bad
        case '.', rest if consuming:
            return 0

        # ok as we are not consuming
        case '.', rest:
            sol = all_sols(rest, rs, consuming, prefix=prefix + '.')
            memo[kf(p, rs, consuming)] = sol
            return sol

        # branching case
        case '?', rest:
            ok_sols = all_sols('.' + rest, rs, consuming, prefix)
            broken_sols = all_sols('#' + rest, rs, consuming, prefix)
            return ok_sols + broken_sols

        case invalid:
            conditions = [
                ("len(rs) > 0 and rs[0] > 0", len(rs) > 0 and rs[0] > 0),
                ("if len(rs) > 0 and rs[0] == 0", len(rs) > 0 and rs[0] == 0)]

            nl = "\n\t"
            raise ValueError(f"{invalid}: \n\t" + nl.join([f"{exp} => {evl}" for exp, evl in conditions]))

def run_pt1(f: TextIOWrapper):
    s = 0
    for puzzle, runs in parse_pt1(f):
        print(f"{puzzle.ljust(25)}: {runs}", end ="")
        sols = all_sols(puzzle, runs)
        s += sols
        print(f" => {sols} solutions!")

    print(f"{s} total solutions!")


def run(f: TextIOWrapper):
    s = 0
    for puzzle, runs in parse_pt2(f):
        print(f"{puzzle}: {runs}")
        sols = all_sols(puzzle, runs)
        s += sols
        print(f"\t => {sols} solutions!")

    print(f"{s} total solutions!")

