from dataclasses import dataclass,field
from enum import Enum
from io import TextIOWrapper
from typing import Any, Iterator
from .unicode_symbols import FgColor, Style, intersperse_at, styled, draw_box, take_n_chars
from .utils import Pos, filter_empty


class O(Enum):
	Rock = "#"
	Ash = "."

	def __lt__(self, other: Any) -> bool:
		return self.value < other.value

	def __hash__(self) -> int:
		return self.value.__hash__()

	def __str__(self) -> str:
		match self:
			case O.Rock: return "🪨 "
			case O.Ash: return styled("▒▒", Style.dim, FgColor.blue)

@dataclass
class MirroredGrid():
	grid: dict[Pos,O]
	max_size: Pos = field(init=False, default_factory=lambda: Pos(0,0))
	cols: list[str] = field(init=False, default_factory=list)
	rows: list[str] = field(init=False, default_factory=list)

	def __populate_max(self):
		for k in self.grid.keys():
			if self.max_size.x < k.x:
				self.max_size.x = k.x
			if self.max_size.y < k.y:
				self.max_size.y = k.y
		print(f"max is {self.max_size}")

	def __post_init__(self):
		self.__populate_max()
		positions: str = ""
		for x in range(0, self.max_size.x+1):
			positions = ""
			for y in reversed(range(0, self.max_size.y + 1)):
				o = self.grid.get(Pos(x,y))
				if o is not None:
					positions += o.value

			self.cols.append(positions)

		print("Cols:")
		[print(f"\t{i}: {c} {hash(c)}") for i, c in enumerate(self.cols)]

		for y in range(0, self.max_size.y+1):
			positions = ""
			for x in range(0, self.max_size.x + 1):
				o = self.grid.get(Pos(x,y))
				if o is not None:
					positions += o.value

			self.rows.append(positions)

		print("Rows:")
		[print(f"\t{i}: {c} {hash(c)}") for i, c in enumerate(self.rows)]

	def score(self) -> int:
		c, r = self.mirrors()
		print(f"c, r = {c}, {r}")
		return (c if c is not None else 0) + 100*(r if r is not None else 0)

	def mirrors(self) -> tuple[int | None, int | None]:
		mirror_at_col = (None, 0)
		col_size = len(self.cols)
		for i, _ in enumerate(self.cols):
			n = 0
			while 0 <= i-n-1 < i+n < col_size:
				if self.cols[i-n-1] == self.cols[i+n]:
					n += 1
				else:
					n = 0
					break

			if mirror_at_col[1] < n:
				mirror_at_col = (i, n)

		mirror_at_row = (None, 0)
		row_size = len(self.rows)
		for i, _ in enumerate(self.rows):
			n = 0
			while 0 <= i-n-1 < i+n < row_size and self.rows[i-n-1] == self.rows[i+n]:
				n += 1
			if mirror_at_row[1] < n:
				mirror_at_row = (i, n)

		return mirror_at_col[0], mirror_at_row[0]



	def __repr__(self) -> str:
		out = ""
		for y in range(0, self.max_size.y + 1):
			out += "\n"
			for x in range(0, self.max_size.x + 1):
				out += str(self.grid[Pos(x,y)])
		col_mirror, row_mirror = self.mirrors()
		print(f"{col_mirror}, {row_mirror}")
		return draw_box(out, col_at=filter_empty([col_mirror]), row_at=filter_empty([row_mirror]))

def part1(file: TextIOWrapper) -> Iterator[MirroredGrid]:
	grid: dict[Pos, O] = {}

	y = 0
	for line in file.readlines():
		match line.strip():
			case "":
				y = 0
				yield MirroredGrid(grid)

			case row:
				for x, ch in enumerate(row):
					grid[Pos(x,y)] = O(ch)
				y += 1
	yield MirroredGrid(grid)




def run(file: TextIOWrapper):
	for grid in part1(file):
		print(f"\nA new grid has appeared!\n{grid}")
		print(grid.score())


