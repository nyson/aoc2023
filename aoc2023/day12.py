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

	def populate_all_unknowns(
			self,
			prefix: list[E] | None = None,
			unknown_at: list[int] | None = None) -> list[list[E]]:
		if prefix is None:
			prefix = []
		if unknown_at is None:
			unknown_at = [i for i,v in enumerate(self.symbols)
						  if v == E.unknown]


		match unknown_at:
			case [i, *rest]:
				if self.symbols[i] != E.unknown:
					raise ValueError(f"Expected unknown, got i: {i}, prefix: {prefix}, \
					  sym: {zip(self.symbols, itertools.count())}")

				print(f"{prefix}{self.symbols[len(prefix):i]}Matching at {i} before {rest}")
				known_prefix = prefix + self.symbols[len(prefix):i]
				possible_prefixes = [known_prefix + [x] for x in [E.broken, E.ok]]
				strs: list[list[list[E]]] = [
					self.populate_all_unknowns(prefix=p, unknown_at=rest)
					for p in possible_prefixes]
				return flatten(strs)
			case []:
				return [prefix + self.symbols[:len(prefix)]]
			case invalid:
				raise ValueError(f"Did not expect {invalid}")


	def __all_possible(self, prefix: list[E], symbols: list[E]) -> list[list[E]]:
		match symbols:
			case [E.unknown, *rest]:
				pos = [self.__all_possible(prefix + [sub], rest)
					   for sub in [E.ok, E.broken]]
				return flatten(pos)
			case [ch, *rest]:
				return self.__all_possible(prefix + [ch], rest)
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
	def possible_solutions(self) -> list[list[E]]:
		xs = self.__all_possible([], self.symbols)
		return [x for x in xs if self.fulfills_predicate(x)]

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
		sum += len(picrow.possible_solutions())

	print(f"Total valid solutions: {sum}")