import itertools
from multiprocessing import Value
from time import time
from typing import TypeVar
from dataclasses import dataclass, field
from enum import Enum
from io import TextIOWrapper

class E(Enum):
	broken = '#'
	ok = '.'
	unknown = '?'

	def __repr__(self) -> str:
		return self.value if self.value in "#.?" else "x"

T = TypeVar("T")
def flatten(xss: list[list[T]]) -> list[T]:
	return [x for xs in xss for x in xs]


@dataclass
class PicrossRow():
	symbols: list[E]
	indicators: list[int]
	size: int = field(init=False)
	known_broken_ranges: list[int] = field(init=False)

	def __repr__(self) -> str:
		out = ""
		out += "symbols:" + "".join([repr(s) for s in self.symbols])
		out += f"\nindicators: {self.indicators}"
		out += f"\nknown broken: {self.known_broken_ranges}"
		out += "\n"
		return out

	def __populate_broken(self):
		self.known_broken_ranges =[]
		break_c = 0
		for s in self.symbols:
			match s:
				case E.broken:
					break_c += 1
				case _ if break_c > 0:
					self.known_broken_ranges.append(break_c)
					break_c = 0
				case _:
					pass

		if break_c > 0:
			self.known_broken_ranges.append(break_c)

	def __post_init__(self):
		self.__populate_broken()
		self.size = len(self.symbols)

	def all_possible(self, prefix: list[E], symbols: list[E]) -> list[list[E]]:
		match symbols:
			case [E.unknown, *rest]:
				pos = [self.all_possible(prefix + [sub], rest)
					   for sub in [E.ok, E.broken]]
				return flatten(pos)
			case [ch, *rest]:
				return self.all_possible(prefix + [ch], rest)
			case []:
				return [prefix]
			case invalid:
				raise ValueError(f"__all_possible unhandled case: {invalid}")


	def fulfills_predicate(self, symbols: list[E]) -> bool:
		[ind, *inds] = self.indicators.copy()
		c: int = 0
		for s in symbols:
			match s:
				case E.ok if c > 0 and c == ind:
					if len(inds) > 0:
						[ind, *inds] = inds
					else:
						ind = 0
					c = 0

				case E.ok if c > 0 and c != ind:
					return False

				case E.ok:
					pass

				case E.broken:
					if ind == 0:
						return False
					c += 1

				case E.unknown:
					raise ValueError("I can't handle unknowns in __fulfills_predicate")

		if c > 0:
			if c == ind and len(inds) == 0:
				return True
			else:
				return False
		return len(inds) == 0 and ind == 0

	# for instance ???.###
	# => #.#.###
	def valid_solutions(self) -> list[list[E]]:
		xs = self.all_possible([], self.symbols)
		return [x for x in xs if self.fulfills_predicate(x)]
	
	def __can_generate_broken(self, indicators: list[int], broken_c: int):
		return len(indicators) > 0 and broken_c < indicators[0]

	def __gen_ok(self, prefix: list[E], rest: list[E], indicators: list[int], broken_c: int) -> list[E]:
		if broken_c > 0:
			if len(indicators) > 0 and indicators[0] == broken_c:
				indicators.pop(0)
			else:
				return []
		return self.get_valid_branchese(prefix + [E.ok], rest, indicators, broken_c=0)
	
	def __gen_broken(self, prefix: list[E], rest: list[E], indicators: list[int], broken_c: int) -> list[E]:
		if self.__can_generate_broken(indicators, broken_c):
			return self.get_valid_branchese(
							prefix + [E.broken], 
							rest, 
							indicators, 
							broken_c=broken_c + 1)
		else:
			return []

	def get_valid_branchese(self, prefix, symbols: list[E], indicators: list[int], broken_c:int =0) -> list[E]:
		match symbols:
			case [E.unknown, *rest]:
				pos = [
					self.__gen_ok(prefix, rest, indicators, broken_c),
					self.__gen_broken(prefix, rest, indicators, broken_c)
				]

				return flatten(pos)

			case [E.broken, *rest]:
				return self.__gen_broken(prefix, rest, indicators, broken_c)
			
			case [E.ok, *rest]:
				return self.__gen_ok(prefix, rest, indicators, broken_c)
			
			case []:
				return [prefix]
			
			case invalid:
				raise ValueError(f"__all_possible unhandled case: {invalid}")


	def iteratively_valid_solutions(self):
		return self.get_valid_branchese([], self.symbols.copy(), self.indicators.copy())
	
def parse_picross_row(s: str) -> PicrossRow:
	symbols: list[E] = []
	state, indicators = s.split(" ")
	for c in state:
		match c:
			case ch if ch in ['#', '.', '?']:
				symbols.append(E(ch))
			case invalid:
				raise ValueError(f"Unhandled char: '{invalid}'")


	return PicrossRow(symbols, [int(c) for c in indicators.split(",")])

def run(file: TextIOWrapper):
	sum = 0
	lines = list(map(str.strip, file.readlines()))
	_ = len(lines)

	for _, r in enumerate(lines):
		picrow = parse_picross_row(r)
		sols = picrow.iteratively_valid_solutions()
		sum += len([_ for s in sols if picrow.fulfills_predicate(s)])
		print(f"{picrow} with solutions:")
		for s in sols:
			print(f"\t{'✅' if picrow.fulfills_predicate(s) else '☔'}: {s}")
		
		

	print(f"Total valid solutions: {sum}")