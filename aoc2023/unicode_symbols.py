from enum import Enum
from functools import reduce
import itertools
from multiprocessing import Value
import re
from typing import Callable


class FgColor(Enum):
    black: int = 30
    red: int = 31
    green: int = 32
    yellow: int = 33
    blue: int = 34
    magenta: int = 35
    cyan: int = 36
    white: int = 37

class BgColor(Enum):
    black: int = 40
    red: int = 41
    green: int = 42
    yellow: int = 43
    blue: int = 44
    magenta: int = 45
    cyan: int = 46
    white: int = 47

class Style(Enum):
    bold: int = 1
    dim: int = 2
    italic: int = 3
    underline: int = 4
    blink: int = 5
    rapid_blink: int = 6
    fraktur: int = 20
    framed: int = 51

reset = "\u001b[0m"
reset_dbg = "u001b[0m"

def styled(text: str, *ins: Enum):
    set = mk_set_ins(ins)
    return f"{set}{text}{reset}"

def visible_length(s: str):
    return len(re.sub(re.compile("\\[\\d.*m"), '', s.strip()))

def take_n_chars(base: str, n: int) -> tuple[str, str]:
    """
    Take n chars, ignoring ansi formatting and considering unicode characters
    ^ tall order
    """
    out = ""
    while n > 0:
        match re.match("(^\u001b\\[\\d+(;\\d+)*m)", base):
            case None:
                pass
            case mg:
                start, end = mg.start(0), mg.end(0)
                out += base[start:end]
                base = base[end:]
                continue

        if n <= 0:
            break

        if base == "":
            return out, ""

        out += base[0]
        base = base[1:]
        n -= 1

    return out, base



def intersperse_at(base: str, sub: str, indexes: list[int], width:int =2):
    if len(indexes) == 0:
        return base
    sort_ixs: list[int] = sorted(list(set(indexes)))

    out = ""
    i = 0
    while len(sort_ixs) > 0 and base != "":

        i += 1
        chs, base = take_n_chars(base, width)
        out += chs
        if sort_ixs[0] == i:
            out += sub
            sort_ixs.pop(0)


    return out + base



def draw_box(string:str, col_at:list[int] = [], row_at: list[int] = [], cell_width: int=2) -> str:
    strs = string.strip().split("\n")
    x_max = reduce(lambda acc, s: max(acc, visible_length(s)), strs, 0)
    border_x: Callable[[str], str] = lambda ch: "─" + intersperse_at(
        "".join(itertools.repeat("─", (x_max + 3) * 2)) + "",
        ch,
        list(map(lambda x: x, col_at)),
        width=cell_width
        ) + "─"


    out = f"╭{border_x('┬')}╮\n"

    for i,s in enumerate(strs):
        if i in row_at:
            out += f"├{border_x('┼')}┤\n"

        formatted_s = intersperse_at(
            s.ljust(x_max),
            f"{reset}│",
            col_at,
            width = cell_width)
        out += f"│ {formatted_s}{reset} │\n"
        # out += f"│ {s.ljust(x_max)} │\n"
    out += f"╰{border_x('┴')}╯"

    return out


def carousel(text: str, *instruction_sets: list[Enum], base: list[Enum] | None = None):
    s = "" if base is None else mk_set_ins(base)
    i, l = 0, len(text)
    for ins in itertools.cycle(instruction_sets):
        ch = text[i]
        s += f"{mk_set_ins(ins)}{ch}"
        i += 1
        if i >= l: break
    return f"{s}{reset}"

def mk_set_ins(ins):
    ins_s = ";".join([f"{i.value}" for i in ins if i is not None])
    return f"\u001b[{ins_s}m"


# launcher
tree = "🎄"
bell = "🔔"
santa = "🎅"
day = "📅"
confused = "🤔"
warning = styled("⚠ ", FgColor.red)

#day2
red_cube = "🟥"
blue_cube = "🟦"
green_cube = "🟩"
wave = "👋"
bolt = "⚡"
bag = "👜"
check = "✅"
fail = "☔"
text = styled("🖹 ", FgColor.black, BgColor.white)

#day3"
presenter = "💁"
star = "⭐"

#day4
card = "🎴"
points = "💯"
thin_ticket = "🎟"
ticket = "🎫"
trophy = "🏆"
checkered_flag = "🏁"

#day5
seed = "🌱"
soil = "🌾"
fertilizer = "💩"
water = "🚰"
light = "🌞"
temperature = "🌡"
humidity = "💧"
location = "📌"
