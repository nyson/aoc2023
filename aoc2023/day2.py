from dataclasses import dataclass
from enum import Enum
from io import TextIOWrapper
import math
from typing import List, TypeAlias
from aoc2023 import unicode_symbols as u


class Color(Enum):
    blue = 1
    red = 2
    green = 3

all_colors: List[Color] = [Color.red, Color.green, Color.blue]

Showing: TypeAlias = dict[Color, int]

def col(input: str) -> Color:
    match f"{input}".strip().lower():
        case "blue":    return Color.blue
        case "red":     return Color.red
        case "green":   return Color.green
        case bad: raise ValueError(f"{bad} is not a valid color! use red, green or blue")

def col_sym(c: Color) -> str:
    match c:
        case Color.red:     return u.red_cube
        case Color.blue:    return u.blue_cube
        case Color.green:   return u.green_cube

@dataclass
class Game():
    def __init__(self, id: int, showings: List[Showing], raw: str = "") -> None:
        self.showings: List[Showing] = showings
        self.id = id
        self.raw = raw

    def fulfills_requirement(self, requirement: dict[Color, int]) -> bool:
        used = self.used_cubes()
        for color, value in requirement.items():
            if value < used[color]:
                return False

        return True

    def used_cubes(self) -> dict[Color,int]:
        req: dict[Color, int] = {
            Color.red: 0,
            Color.green: 0,
            Color.blue: 0
        }

        for s in self.showings:
            for color, value in s.items():
                if req[color] < value:
                    req[color] = value
        return req

    def pretty_used_cubes(self) -> str:
        return " ".join([f"{v}{col_sym(c)}" for c,v in self.used_cubes().items()])

    def print_showings(self) -> str:
        return " ║".join(map(
                lambda s: f"{u.wave} " + " ".join([f"{num}{col_sym(color)}" for color, num in s.items()]),
                self.showings))

    def power_level(self) -> int:
        return math.prod([v for _, v in self.used_cubes().items()])

def parse_id(id_s: str) -> int:
    return int(id_s[:-1])

def parse_showing(data: str) -> Showing:
    showing: Showing = {}
    for num, color in map(lambda d: d.strip().split(" "), data.split(",")):
        showing[col(color)] = int(num)

    return showing

def parse_showings(data: str) -> List[Showing]:
    showings: List[Showing] = []
    for d in data.split(";"):
        showings.append(parse_showing(d))

    return showings

def parse_game(row: str) -> Game:
    match row.split():
        case ("Game", id, *tail):
            return Game(id = parse_id(id), raw = row.strip(), showings= parse_showings(" ".join(tail)))
        case invalid:
            raise ValueError(f"Could not parse '{invalid}' as Game row")




def run(file: TextIOWrapper):
    games = map(lambda row: parse_game(row), file.readlines())
    # Sum of the game ids of games that fulfills the requirement
    sum_gids_possible = 0
    # Total sum of games power level (product of minimum value of cubes)
    sum_power_level = 0
    req: dict[Color, int] = {
        Color.blue: 14,
        Color.green: 13,
        Color.red: 12
    }

    for game in games:
        print(f"\nGame {game.id}: {game.print_showings()}")
        print(f" {u.text}: \"{game.raw}\"")
        print(f" {u.bolt}: {game.power_level()}")
        print(f" {u.bag}: {game.pretty_used_cubes()}")

        if game.fulfills_requirement(req):
            print(f" {u.check}: Fulfills requirement!")
            sum_gids_possible += game.id
        else:
            print(f" {u.fail}: Does not fulfill requirement :(")

        sum_power_level += game.power_level()

    print(f"\nSum of game ids fulfilling requirement: {sum_gids_possible}")
    print(f"Sum of power level: {sum_power_level}")