from dataclasses import dataclass
from email.policy import default
from io import TextIOWrapper
import itertools
from typing import Any, Callable, Iterable

from click import style
from .unicode_symbols import BgColor, FgColor, styled, Style

@dataclass
class Pos():
	x: int
	y: int

	def __lt__(self, other:Any) -> bool:
		return (self.x, self.y) < (other.x, other.y)

	def __hash__(self) -> int:
		return hash((self.x, self.y))

@dataclass
class Grid():
	max: Pos
	grid: set[Pos]
	column_empty: dict[int, bool]
	row_empty: dict[int, bool]

	def __pp_header(self, sub: Callable[[str], str], header:bool =True):
		for i in range(-1, self.max.x + 2):
			match i:
				case -1:
					print(
						sub("╔") if header else sub("╚"),
						end="")
				case n if self.column_empty.get(n):
					print(
						sub("╦═") if header else sub("╩═"),
						end="")
				case n if n == self.max.x+1:
					print(
						sub("╗") if header else sub("╝"),
						end="")
				case _:
					print(sub("══"), end="")
		print()

	def pp(self, grid: set[Pos] | None = None, substitutions: dict[str, Iterable[str]] | None = None):
		def sub(s:str) -> str:
			if substitutions is not None:
				for k, v in substitutions.items():
					if k in s:
						s = s.replace(k, next(iter(v)))
			return s
		set_grid: set[Pos] = self.grid if grid is None else grid

		table: dict[Pos, str] = {k: "#" for k in set_grid}

		self.__pp_header(sub)
		for y in range(0, self.max.y + 1):
			if self.row_empty.get(y):
				print(sub("╠"), end="")
			else:
				print(sub("║"), end="")
			for x in range(0, self.max.x +1):
				match table.get(Pos(x,y)):
					case None:
						match self.column_empty[x], self.row_empty[y]:
							case True, True:
								print(sub("╬═"), end="")
							case True, _:
								print(sub("║░"), end="")
							case _, True:
								print(sub("══"), end="")
							case _:
								print(sub("░░"), end="")
					case "#":
						print(sub("##"), end="")
					case invalid:
						print(f"Invalid case: {invalid}")
			if self.row_empty.get(y):
				print(sub("╣"), end="")
			else:
				print(sub("║"), end="")

			print()
		self.__pp_header(sub, header=False)

	def get_expanded_grid(self, replace_with:int = 2) -> set[Pos]:
		replace_with -= 1
		out: set[Pos] = set()
		for p in sorted(self.grid):
			cols_before_i = [
				k for k,v in self.column_empty.items()
				if k < p.x and v]

			rows_before_i = [
				k for k,v in self.row_empty.items()
				if k < p.y and v]

			expanded = Pos(
				x= p.x + replace_with*len(cols_before_i),
				y= p.y + replace_with*len(rows_before_i))

			out.add(expanded)
		return out




def incr_l(l: dict[int, int], key: int) -> dict[int, int]:
	if key in l:	l[key] += 1
	else:			l[key] = 1
	return l

def parse_grid(file: TextIOWrapper):
	grid: set[Pos] = set()
	rows: dict[int, int] = {}
	columns: dict[int, int] = {}
	size: Pos = Pos(0, 0)

	for y, r in enumerate(file.readlines()):
		if y not in rows:
			rows[y] = 0

		if r.strip() == "":
			break
		size.y = max(y, size.y)
		for x, ch in enumerate(r.strip()):
			if x not in columns:
				columns[x] = 0

			size.x = max(x, size.x)

			match ch:
				case '#':
					grid.add(Pos(x,y))
					incr_l(rows, y)
					incr_l(columns, x)
				case '.':
					pass
				case invalid:
					raise ValueError(f"Invalid case {invalid}")


	return Grid(size, grid,
			 {k: v == 0 for k,v in columns.items()},
			 {k: v == 0 for k,v in rows.items()})

def taxicab(p1: Pos, p2: Pos) -> int:
	return abs(p2.x-p1.x) + abs(p2.y-p1.y)

def all_distances(grid: set[Pos]) -> int:
	sum = 0
	for (a,b) in itertools.combinations(grid, 2):
		sum += taxicab(a,b)

	return sum


def run(file: TextIOWrapper):
	file.seek(0)

	grid = parse_grid(file)

	border_color = FgColor.cyan
	grid.pp(substitutions={
		"##": itertools.cycle("🪐🌍⭐🌠🌚🌞👾"),
		"░": itertools.cycle([styled("░", Style.dim, FgColor.yellow)]),
		"═": itertools.cycle([styled("═", border_color)]),
		"║": itertools.cycle([styled("║", border_color)]),
		"╬": itertools.cycle([styled("╬", border_color)]),
		"╔": itertools.cycle([styled("╔", border_color)]),
		"╦": itertools.cycle([styled("╦", border_color)]),
		"╗": itertools.cycle([styled("╗", border_color)]),
		"╠": itertools.cycle([styled("╠", border_color)]),
		"╣": itertools.cycle([styled("╣", border_color)]),
		"╚": itertools.cycle([styled("╚", border_color)]),
		"╩": itertools.cycle([styled("╩", border_color)]),
		"╝": itertools.cycle([styled("╝", border_color)])


		})

	print(f"Grid length: {len(grid.grid)}, with {len(list(itertools.combinations(grid.grid, 2)))} distances")
	print(f"Taxicab orig: {all_distances(grid.grid)}")
	print(f"Taxicab expanded: {all_distances(grid.get_expanded_grid())}")
	print(f"Taxicab expanded by 100: {all_distances(grid.get_expanded_grid(100))}")
	print(f"Taxicab expanded by 1000000: {all_distances(grid.get_expanded_grid(1000000))}")

