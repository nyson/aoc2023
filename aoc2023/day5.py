from dataclasses import dataclass
from io import TextIOWrapper
import itertools
from aoc2023 import unicode_symbols as u

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

	def symbol(self, object: str) -> str:
		match object:
			case "seed": return u.seed
			case "soil": return u.soil
			case "fertilizer": return u.fertilizer
			case "water": return u.water
			case "light": return u.light
			case "temperature": return u.temperature
			case "humidity": return u.humidity
			case "location": return u.location
			case _: return object
		
	def lookup(self, input: int) -> int:
		for t in self.transforms:
			if input in t.source_range():
				return input - t.source + t.dest
		
		return input
	
	def lookup_range(self, start, steps) -> list[tuple[int, int]]:
		"""
		
		"""
		for i, t in enumerate(self.transforms):
			if start in t.source_range():
				if start + steps - 1 not in t.source_range():
					raise NotImplementedError("not handling multiple ranges")
				return (start + t.delta(), start + steps + t.delta())

		return (start, steps)


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
			out += "\n\n" + m.pp()

		return out

	def find_lowest_seed(self) -> int:
		lowest = None
		for n in self.seeds:
			for v in self.maps.values():
				n = v.lookup(n)
			if lowest == None or n < lowest: 
				lowest = n

		return lowest
	
	def seed_pairs(self):
		i = iter(self.seeds)
		return zip(i, i)

	def find_lowest_seed_in_range(self) -> int:
		lowest = None
		for x, span in self.seed_pairs():
			print(f"{x} to {x+span-1} in {span} steps")

			for v in self.maps.values():
				(x, e) = v.lookup_range(x, span)
			if lowest == None or x < lowest:
				lowest = x
		return lowest

def parse_agriculture(input: TextIOWrapper) -> Agriculture:
	current_map: MapTransform = None
	seeds: list[int]
	maps: dict[str, MapTransform] = {}

	while input.readable():
		line = input.readline()
		match line:
			case "":
				break
			case "\n":
				continue

		match line.strip().split(" "):
			# seeds: 1 2 3
			case ("seeds:", *seeds): 
				seeds = [int(s) for s in seeds]
 			
			# source-to-destination map:
			case (st, "map:"):
				if current_map is not None:
					maps[current_map.name()] = current_map

				[source, _, destination] = st.split("-")
				current_map = MapTransform(source, destination, [])

			# 1 2 3 # destination source span for transforms
			case (_, _, _) as ss if all([s.isdigit() for s in ss]):
				[dest, source, span] = [int(s) for s in ss]
				t = Transform(dest, source, span)
				current_map.transforms.append(t)

			case n:
				raise ValueError(f"unhandled parse: {n}")

	if current_map is not None:
		maps[current_map.name()] = current_map
	
	return Agriculture(seeds, maps)

def run(file: TextIOWrapper):
	agr = parse_agriculture(file)
	print(agr.pp())

	print(f"Lowest seed is {agr.find_lowest_seed()}")
	# print(f"Lowest seed (with ranges) is {agr.find_lowest_seed_in_range()}")