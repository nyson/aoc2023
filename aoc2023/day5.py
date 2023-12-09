from dataclasses import dataclass
from io import TextIOWrapper
from typing import Callable, Iterator, TypeAlias
from aoc2023 import unicode_symbols as u
from aoc2023 import utils as utils



@dataclass
class Transform():
    """ dest source span <= 0 1 2 """
    dest: int
    source: int
    span: int

    def pp(self) -> str:
        return f"{self.source} {self.span + self.source} -> {self.dest}"

    def source_range(self) -> range:
        return range(self.source, self.source + self.span)

    def dest_range(self) -> range:
        return range(self.dest, self.dest + self.span)

    def delta(self):
        return self.dest - self.source

@dataclass
class MapTransform():
    """
    <source>-to-<destination> map:
    transforms 0
    transforms 1
    ...
    transforms n

    """
    source: str
    destination: str
    transforms: list[Transform]

    def name(self) -> str:
        return f"{self.symbol(self.source)}-to-{self.symbol(self.destination)}"

    def ranges(self) -> list[Transform]:
        s: list[Transform] = sorted(self.transforms, key=lambda t: t.source)
        if len(s) <= 0:
            raise ValueError("No elements in list")

        if s[0].source > 0:
            s = [Transform(dest=0, source=0, span= s[0].source), *s]
        return s

    def symbol(self, object: str) -> str:
        match object:
            case "seed": 		return u.seed
            case "soil": 		return u.soil
            case "fertilizer": 	return u.fertilizer
            case "water": 		return u.water
            case "light": 		return u.light
            case "temperature": return u.temperature
            case "humidity": 	return u.humidity
            case "location": 	return u.location
            case _: 			return object

    def lookup(self, input: int, reversed: bool = False) -> int:
        for t in self.transforms:
            if reversed and input in t.dest_range():
                return input - t.dest + t.source
            if not reversed and input in t.source_range():
                return input - t.source + t.dest
        return input
    
    def lookup_range(self, input: range) -> range:
        for t in self.transforms:
            match u.range_union(input, t.source_range()):
                case None:
                    pass
                case ur:
                    print(f"{self.name()} {input} to {t.source_range()} gives union {ur}")

    def iterate_range(self, rs: list[range]) -> list[range]:
        out: list[range] = []
        for r in rs:
            print(f"examining range {r}")
            for t in sorted(self.transforms, key=lambda t: t.source_range()[0]):
                match utils.range_union(r, t.source_range()):
                    case None:
                        print(f"\tno match in {t.pp()}, appending {r}")

                    case range(match):
                        prefix: range = utils.range_prefix(r, match)
                        suffix: range = utils.range_suffix(r, match)
                        if prefix is not None:
                            out.append(prefix)

                        r = suffix if suffix is not None else range(match[-1]+1, match[-1]+1)

                        new_range = utils.incr_range(match, t.delta)
                        out.append(new_range)

                        print(f"Got match on {t.pp()} with prefix {prefix} and suffix {suffix}")

        return utils.minimize_ranges(*out)
                                
    def __largest_number(self) -> int:
        mx = 0
        for t in self.transforms:
            for i in [t.source, t.dest, t.span]:
                mx = max(mx, i)
        return mx

    def pp_short(self) -> str:
        l =  len(str(self.__largest_number())) + 1
        fm: Callable[[int], str] = lambda n: f"{{0: <{l}}}".format(n)
        sts = sorted(self.transforms, key=lambda t: t.source)
        intervals = "\n".join([f"({fm(t.source)}, {fm(t.source + t.span)} (->{fm(t.dest)}))" for t in sts])
        return f"{self.symbol(self.source)}->{self.symbol(self.destination)}:\n{intervals}"

    def pp(self) -> str:
        out = f"{self.symbol(self.source)}"
        out += f"-to-{self.symbol(self.destination)}"
        out +=" map:"

        for t in self.transforms:
            out += "\n" + t.pp()

        return out

@dataclass
class Agriculture():
    """
    seeds: <seeds>

    <map transform 0>
    <map transform 1>
    ...
    <map transform n>
    """
    seeds: list[int]
    maps: dict[str, MapTransform]

    def pp(self) -> str:
        seeds = ' '.join([f"{n}" for n in self.seeds])
        out = f"{u.seed}s: {seeds}"

        for m in self.maps.values():
            out += "\n\n" + m.pp_short()

        return out

    def find_lowest_seed(self) -> int:
        lowest = None
        for n in self.seeds:
            for v in self.maps.values():
                n = v.lookup(n)
            if lowest == None or n < lowest:
                lowest = n

        if lowest is None:
            raise ValueError("No seeds found!")

        return lowest
    
    def seed_ranges(self) -> Iterator[range]:
        xs = iter(self.seeds)
        match (next(xs), next(xs)):
            case None:
                return
            case start, span:
                yield range(start, start + span)
    
    
    def lookup_range(self) -> range:
        i = iter(self.seeds)
        
        rn: range
        for base_seed_range in self.seed_ranges():
            lowest = base_seed_range
            for v in self.maps.values():
                msr = v.lookup_range(lowest)
                if msr is not None and msr[0] <= lowest[0]:
                    lowest = msr
                else: 
                    continue
                print(f"{v.name()} Next seed range is {lowest}")
            rn = lowest
            print(f"Current seed range is {lowest}")
        
        return rn
            

            

    def seed_pairs(self):
        i = iter(self.seeds)

def parse_agriculture(input: TextIOWrapper) -> Agriculture:
    current_map: MapTransform | None = None
    seeds: list[int] | None = None
    maps: dict[str, MapTransform] = {}

    while input.readable():
        line = input.readline()
        match line:
            case "":
                break
            case "\n":
                continue
            case _:
                pass

        match line.strip().split(" "):
            # seeds: 1 2 3
            case ("seeds:", *xs):
                seeds = [int(s) for s in xs]

            # source-to-destination map:
            case (st, "map:"):
                if current_map is not None:
                    maps[current_map.name()] = current_map

                [source, _, destination] = st.split("-")
                current_map = MapTransform(source, destination, [])

            # 1 2 3 # destination source span for transforms
            case (_, _, _) as ss if all([s.isdigit() for s in ss]):
                if current_map is None: raise ValueError("Expected map, got None")
                [dest, source, span] = [int(s) for s in ss]
                t = Transform(dest, source, span)
                current_map.transforms.append(t)

            case n:
                raise ValueError(f"unhandled parse: {n}")

    if current_map is not None:
        maps[current_map.name()] = current_map

    return Agriculture(seeds or [], maps)

def run_pt1(file: TextIOWrapper):
    agr = parse_agriculture(file)
    print(agr.pp())
    i = iter(agr.seeds)

    print(agr.maps.keys())
    print([g for g in agr.maps["🌱-to-🌾"].iterate_range(zip(i, i))])
    # print(f"lowest range is {agr.lookup_range()}")
    print(f"Lowest seed is {agr.find_lowest_seed()}")

def offset_range(r: range, offset: int):
    return range(r[0] + offset, r[-1] + offset)

@dataclass
class Range():
    start: int
    end: int

    def __len__(self):
        return self.end - self.start
    
    def __str__(self) -> str:
        return f"[{self.start} 🤝 {self.end}]"
    def __repr__(self):
        return self.__str__()


def shift_range(r: Range, offset: int) -> Range:
    return Range(r.start + offset, r.end + offset)

def range_intersection(r1: Range, r2: Range) -> Range | None:
    if r1.start <= r2.end and r1.end >= r2.start:
        return Range(max(r1.start, r2.start), min(r1.end, r2.end))
    return None

def union(r1: Range, r2: Range) -> Range | None:
    if r1.start <= r2.end and r1.end >= r2.start:
        return Range(min(r1.start, r2.start), max(r1.end, r2.end))
    return None


def minimize_ranges(inp: list[Range]) -> list[Range]:
    results = []
    if len(inp) == 0:
        return
    
    ranges = iter(sorted(inp, key=lambda r: r.start))
    c = next(ranges)

    for n in ranges:
        match union(c, n):
            case None:
                results.append(c)
                c = n
            case u:
                c = u

    results.append(c)

    return results


def before(left: Range, right: Range) -> Range | None:
    if left.start < right.start:
        return Range(left.start, min(left.end, right.start))
    return None

def after(left: Range, right: Range) -> Range | None:
    if left.end > right.end:
        return Range(max(right.end, left.start), left.end)
    return None


@dataclass
class Trans():
    r: Range
    offset: int

    def __lt__(self, other):
        return self.r.start < other.r.start
    
    def __contains__(self, item):
        return self.r.start <= item <= self.r.end


TMapKey: TypeAlias = tuple[str, str]

@dataclass
class Day5():
    seeds: list[Range]
    seeds_ind: list[int]
    ts: dict[TMapKey, list[Trans]]

def pairs(xs: list) -> list[tuple]:
    l = iter(xs)
    return list(zip(l, l))

def parse_day5_b(file: TextIOWrapper) -> Day5:
    seeds: list[int] | None = None
    ts: dict[TMapKey, list[Trans]] = {}
    current_key: TMapKey | None = None 


    while True:
        line = file.readline()
        if line == "":
            break
        
        match line.strip().split():
            case ["seeds:", *seeds_raw]:
                seeds = list(map(int, seeds_raw))
            
            case [mapping, "map:"]:				
                [source, target] = mapping.split("-to-")
                current_key = (source, target)
                ts[current_key] = []

            case [_, _, _] as xs:
                [target_start, source_start, num] = [int(x) for x in xs] 
                t = Trans(
                    r= Range(start= source_start, end = source_start + num - 1),
                    offset = target_start - source_start)
                ts[current_key].append(t)
            
            case _:
                pass
                

    for k in ts.keys():
        ts[k].sort()
    return Day5(seeds= [Range(start= s, end= s+o) for s, o in pairs(seeds)], seeds_ind=list(seeds), ts=ts)

def run(file: TextIOWrapper):
    d5 = parse_day5_b(file)

    print(f"seeds: {d5.seeds}; {d5.seeds_ind}")
    # for k,ts in d5.ts.items():
    # 	print(f"{k} map:")
    # 	for t in ts:
    # 		print(f"\t{t.r.start}-{t.r.end}:{'+' if t.offset > 0 else ''}{t.offset}")

    print(transform_ranges(d5.seeds, d5.ts))

def transform_single(seed: int, ts: dict[TMapKey, list[Trans]]) -> int:
    for k, v in ts.items():
        match = ""
        print(f"{k} map:")
        for t in v:

            if match == "" and seed in t:
                # print(f"{seed_i} got incremented to ", end="")
                seed += t.offset
                match = "*"
                # print(seed_i)

            print(f"\t{t.r.start}-{t.r.end}:{'+' if t.offset > 0 else ''}{t.offset} {match}")
        
        print(f"seed is {seed}")
    
    return seed

def transform_ranges(seeds: list[Range], ts: dict[TMapKey, list[Trans]]) -> list[Range]:
    xs = seeds
    for k, transformations in ts.items():
        next_ranges = []
        print(f"{k} map:")
        print(f"Looking for matches for {xs}")
        while len(xs) > 0:
            x = xs.pop(0)
            for t in transformations:
                try:
                    match range_intersection(x, t.r):
                        case None:
                            print(f"   * No overlap between {x} and {t.r}, keeping {x}")
                            next_ranges.append(x)
                            continue
                         
                        case union_range:
                            print(f"   * Found overlap between x={x} and {t.r}!")
                            b = before(x, t.r)
                            if b is not None:
                                print(f"\tBefore: {b}")
                                next_ranges.append(b)
                            shifted = shift_range(union_range, t.offset)
                            next_ranges.append(shifted)
                            
                            print(f"\tUnion: {union_range} => {shifted} after {t.offset}")
                            a = after(x, t.r)
                            if a is not None:
                                print(f"\tAfter: {a}")

                except AttributeError as e:
                    print(f"{e}; {x}, {t}")
                    raise e
                        
        xs = [z for z in minimize_ranges(next_ranges)]
        print(f"   Next ranges {next_ranges}")
        print(f"\t => {xs}")
        print()

    return min([n.start for n in xs])

