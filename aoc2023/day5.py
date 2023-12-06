from dataclasses import dataclass
from io import TextIOWrapper
from typing import Callable
from aoc2023 import unicode_symbols as u


def range_union(r1: range, r2: range) -> range | None:
	print(f"{r1}, {r2}")
	if r1[0] < r2[-1] and r2[-1] > r1[0]:
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
	print("hello?")
	if r1[-1] > r2[-1]:
		return range(
			max(r1[0], r2[-1] + 1),
			r1[-1] + 1)
	return None

@dataclass
class Transform():
	""" dest source span <= 0 1 2 """
	dest: int
	source: int
	span: int

	def pp(self) -> str:
		return f"{self.dest} {self.source} {self.span}"

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
		return f"{self.source}-to-{self.destination}"

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

	def seed_pairs(self):
		i = iter(self.seeds)
		return zip(i, i)

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



def run(file: TextIOWrapper):
	agr = parse_agriculture(file)
	print(agr.pp())
	print(f"Lowest seed is {agr.find_lowest_seed()}")

def offset_range(r: range, offset: int):
	return range(r[0] + offset, r[-1] + offset)