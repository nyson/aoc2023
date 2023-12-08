from dataclasses import dataclass
from enum import Enum
from io import TextIOWrapper
import itertools
import math
from typing import Callable
import aoc2023.unicode_symbols as u


class Direction(Enum):
	left = 0
	right = 1

	def __str__(self) -> str:
		return "L" if self.value == 0 else "R"

@dataclass
class Node():
	id: str
	left: str
	right: str



def parse_directions(directions: str) -> list[Direction]:
	out: list[Direction] = []
	for d in directions:
		match d:
			case "L": out.append(Direction.left)
			case "R": out.append(Direction.right)
			case d:
				raise ValueError(f"Unhandled case {d}")

	return out

def clean_non_alpha(s: str) -> str:
	return "".join(filter(lambda x: x.isalnum(), s))

def parse_day8(file: TextIOWrapper) -> tuple[list[Direction], dict[str, Node]]:
	route = None
	nodes: dict[str, Node] = {}

	while True:
		line = file.readline()
		if line == "":
			break
		match line.split():
			case ["\n"] | []:
				pass
			case [directions]:
				route = parse_directions(directions)
			case [node_id, "=", left_raw, right_raw]:
				nodes[node_id] = Node(
					node_id,
					clean_non_alpha(left_raw),
					clean_non_alpha(right_raw))
			case invalid:
				raise ValueError(f"parse_day8: Unhandled parse: {invalid}")

	if route is None:
		raise ValueError("Expected a route!")

	return (route, nodes)


def walk(route: list[Direction], start: str, nodes: dict[str, Node], goal: str) -> int:
	i = 0
	curr: Node = nodes[start]

	for d in itertools.cycle(route):
		if curr.id == goal:
			return i

		match d:
			case Direction.left:
				curr = nodes[curr.left]
			case Direction.right:
				curr = nodes[curr.right]

		i += 1


def node_walk(node: Node, nodes: dict[str, Node], direction: Direction) -> Node:
	match direction:
		case Direction.left:
			return nodes[node.left]
		case Direction.right:
			return nodes[node.right]

def walk_to_goal(
	route: list[Direction],
	node: Node,
	nodes: dict[str, Node],
	goal: Callable[[str], bool]) -> int:

	steps = 0
	for d in itertools.cycle(route):
		if goal(node.id):
			return steps
		node = node_walk(node, nodes, d)
		steps += 1

	return 0

def walk_lcm(
	route: list[Direction],
	start: list[str],
	nodes: dict[str, Node],
	goal: Callable[[str], bool]):
	least_steps: dict[str, int] = {}

	for n in [nodes[s] for s in start]:
		least_steps[n.id] = walk_to_goal(route, n, nodes, goal)

	return math.lcm(*least_steps.values())





def run(file: TextIOWrapper):
	route, nodes = parse_day8(file)
	start_nodes: list[str] = [n for n in nodes.keys() if n[-1] == "A"]
	print(walk_lcm(route, start_nodes, nodes, lambda x: x[-1] == "Z"))