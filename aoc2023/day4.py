from dataclasses import dataclass
from io import TextIOWrapper
import math
from typing import Callable, List
from aoc2023 import unicode_symbols as u

@dataclass
class Card():
    id: int
    ticket: list[int]
    winning: list[int]
    ticket_winners: list[int]

    def __init__(self, id: int, ticket: List[int], winning: List[int]):
        self.id = id
        self.ticket = ticket
        self.winning = winning
        self.ticket_winners = [t for t in ticket
                               if t in winning]

    def pp(self) -> str:
        pp_l: Callable[[list[int]], str] = lambda l: " ".join(["{0: <3}".format(n) for n in l])
        fixed_score = "{0: <5}".format(self.get_score())
        copies = "{0: <3}".format(self.get_ticket_prize())
        return "\t".join([
            f"{u.card} {self.id}:",
            f"{u.points} {fixed_score}"
            f"{u.thin_ticket} {copies}"
            f"{u.ticket} {pp_l(self.ticket)}",
            f"{u.trophy} {pp_l(self.winning)}"
        ])

    def get_score(self) -> int:
        match len(self.ticket_winners):
            case 0: return 0
            case 1: return 1
            case n if n > 0: return int(math.pow(2, n-1))
            case n: raise ValueError(f"Needs a positive number! (got {n})")

    def get_ticket_prize(self) -> int:
        return len(self.ticket_winners)

def parse_card(row: str) -> Card:
    match [r for r in row.split(" ") if r != ""]:
        case ("Card", id_s, *rest):
            id = int("".join([n for n in id_s if n.isdigit()]))
            [ticket, winning] = parse_numbers(rest)
            return Card(id= id, ticket= ticket, winning= winning)
        case _:
            raise ValueError(f"Could not parse row as Card: {row}")

def parse_numbers(number_row: List[str]) -> tuple[List[int], List[int]]:
    get_nums:Callable[[str], list[int]] = lambda s: [
        int(n.strip())
        for n in s.split(" ")
        if n != ""]

    w, l = [get_nums(x) for x in " ".join(number_row).strip().split(" | ")]

    return (w, l)

def run(file: TextIOWrapper):
    sum, tickets = 0, 0
    cards = [parse_card(c) for c in file.readlines()]
    copies: dict[int, int] = {c.id: 1 for c in cards}

    for card in cards:
        sum += card.get_score()
        ticket_prize = card.get_ticket_prize()
        current_ticket_copies = 1 * copies[card.id]
        tickets += current_ticket_copies

        for id in range(card.id+1, card.id+1+ticket_prize):
            copies[id] += 1 * copies[card.id]

        print(card.pp())

    print(" ".join([f"{u.checkered_flag} Final score: {sum}",
                    f"{u.thin_ticket} Total tickets: {tickets}"]))