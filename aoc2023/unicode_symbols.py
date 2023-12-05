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



tree = "\U0001F384" # 🎄
bell = "\U0001F514" # 🔔
santa = "\U0001F385" # 🎅
day = "\U0001F4C5" # 📅
warning = styled("\U000026A0 ", FgColor.red) # ⚠
confused = "\U0001F914" # 🤔

#day2
red_cube = "\U0001F7E5" # 🟥
blue_cube = "\U0001F7E6" # 🟦
green_cube = "\U0001F7E9" # 🟩
wave = "\U0001F44B" #👋
text = styled("\U0001F5B9 ", FgColor.black, BgColor.white) # 🖹
bolt = "\U000026A1" # ⚡
bag = "\U0001F45C" # 👜
check = "\U00002705" # ✅
fail = "\U00002614" # ☔

#day3
presenter = "\U0001F481" # 💁
star = "\U00002B50" # ⭐

#day4
card = "\U0001F3B4" # 🎴
points = "\U0001F4AF" # 💯
thin_ticket = "\U0001F39F" # 🎟 
ticket = "\U0001F3AB" # 🎫
trophy = "\U0001F3C6" # 🏆
checkered_flag = "\U0001F3C1" # 🏁

#day5
seed = "\U0001F331" # 🌱
soil = "\U0001F33E" # 🌾
fertilizer = "\U0001F4A9" # 💩
water = "\U0001F6B0" # 🚰
light = "\U0001F31E" # 🌞
temperature = "\U0001F321" # 🌡
humidity = "\U0001F4A7" # 💧
location = "\U0001F4CC" # 📌
