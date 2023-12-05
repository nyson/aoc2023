from enum import Enum
import itertools


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

def styled(text: str, *ins: Enum):
    set = mk_set_ins(ins)
    return f"{set}{text}{reset}"

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
    set = f"\u001b[{ins_s}m"
    return set


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
