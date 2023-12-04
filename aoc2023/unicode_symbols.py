from enum import Enum


class Color(Enum):
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


def colored(text: str, fg: Color | None = None, bg: BgColor | None = None):
    set = "".join([
        "\u001b[",
        '' if fg is None else f'{fg.value}',
        '' if bg is None else f';{bg.value}'
        "m"])
    reset = "\u001b[0m"
    return f"{set}{text}{reset}"


tree = "\U0001F384" # 🎄
bell = "\U0001F514" # 🔔
santa = "\U0001F385" # 🎅
day = "\U0001F4C5" # 📅
warning = colored("\U000026A0 ", fg=Color.black, bg= BgColor.yellow) # ⚠
confused = "\U0001F914" # 🤔

#day2
red_cube = "\U0001F7E5" # 🟥
blue_cube = "\U0001F7E6" # 🟦
green_cube = "\U0001F7E9" # 🟩
wave = "\U0001F44B" #👋
text = colored("\U0001F5B9 ", fg=Color.black, bg=BgColor.white) # 🖹
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