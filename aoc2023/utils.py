from typing import Iterator, TypeVar

T = TypeVar("T")
def exists(item: T | None):
    return item is None

T = TypeVar("T")
def clear_none(l: list[T | None]) -> list[T]:
    return [t for t in l if t is not None]

def range_overlaps(r1: range, r2: range) -> bool:
    return r1[0] < r2[-1] and r2[0] <= r1[-1]

def range_union(r1: range, r2: range) -> range | None:
    if range_overlaps(r1, r2):
        return range(
            max(r1[0], 	r2[0]),
            min(r1[-1], r2[-1]) + 1)

    return None

# returns parts of the range that is before r2
def range_prefix(r1: range, r2: range) -> range | None:
    if r1[0] < r2[0]:
        return range(
            min(r1[0], r2[0]),
            min(r1[-1] + 1, r2[0]))
    return None


def range_suffix(r1: range, r2: range) -> range | None:
    if r1[-1] > r2[-1]:
        return range(
            max(r1[0], r2[-1] + 1),
            r1[-1] + 1)
    return None

def minimize_ranges(*inp: range) -> Iterator[range]:
    if len(inp) == 0:
        return
    
    print(inp)

    i = iter(sorted(inp, key=lambda r: r[0]))
    c = next(i)

    for n in i:
        if range_overlaps(c, n):
            c = range(min(c[0], n[0]), max(c[-1], n[-1]) + 1)
        else:
            print(f"yielding {c}, setting c to {n}")
            yield c
            c = n
    yield c

def incr_range(r: range, i: int) -> range:
    return range(r[0] + i, r[1] + i)