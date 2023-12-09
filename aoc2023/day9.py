from functools import reduce
from io import TextIOWrapper
from itertools import pairwise
from typing import Iterator

def parse_series(file: TextIOWrapper) -> Iterator[list[int]]:
	file.seek(0)
	while True:
		row = file.readline()
		if row == "":
			break
		yield [int(i) for i in row.split()]


def steps(l: list[int]) -> list[int]:
	xs = []
	for (a,b) in pairwise(l):
		xs.append(b-a)
	return xs


def at_end(l: list[int]) -> bool:
	return all([x == 0 for x in l])


def get_next_step(xs: list[int]) -> int:
	edge_numbers = []
	while True:
		edge_numbers.append(xs[-1])
		if at_end(xs):
			break
		xs = steps(xs)
	
	return sum(edge_numbers)	


def get_prev_step(xs: list[int]) -> int:
	edge_numbers = []
	while True:
		edge_numbers.append(xs[0])
		if at_end(xs):
			break
		xs = steps(xs)
	return reduce(lambda sum,x: x - sum, reversed(edge_numbers), 0)


def run(file: TextIOWrapper):
	n = sum([get_next_step(ls) for ls in parse_series(file)])
	p = sum([get_prev_step(ls) for ls in parse_series(file)])
	print(f"prev, next= ({p}, {n})")	