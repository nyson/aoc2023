from io import TextIOWrapper
from typing import List


def run(file: TextIOWrapper):
    sum, sum_old = 0, 0
    for row in file.readlines():
        res = replace_str_digits_and_words(row)
        res_old = get_first_last_digit(row)
        sum += res
        sum_old += res_old
        if res != res_old:
            print(f"[{sum}] {rmnl(row)} -> {res} (old = {res_old})")

    print(f"Sum is {sum} (old= {sum_old})")

def rmnl(s: str) -> str:
    return s.replace("\n", "")

def get_first_last_digit(row: str) -> int:
    return first_digit(row) * 10 + first_digit(row[::-1])

def first_digit(s: str) -> int:
    for l in s:
        if l.isdigit():
            return int(l)

    return 0

def word_of_digit(i: int) -> str:
    match i:
        case 1: return "one"
        case 2: return "two"
        case 3: return "three"
        case 4: return "four"
        case 5: return "five"
        case 6: return "six"
        case 7: return "seven"
        case 8: return "eight"
        case 9: return "nine"
        case _: raise ValueError("word_of_digit only works on 1 to 9")

def replace_str_digits_and_words(s: str) -> int:
    nums: List[tuple[str, int]] = [(f"{n}", n) for n in range(1,10)]
    nums += [(word_of_digit(n), n) for n in range(1,10)]

    return find_first(s, nums) * 10 + find_first(s, nums, reversed=True)

def find_first(s: str, checks: List[tuple[str, int]], reversed: bool=False) -> int:
    if reversed: s = s[::-1]

    results: List[tuple[int, int]] = []
    for (check_val, num) in checks:
        if reversed: check_val = check_val[::-1]
        results.append((s.find(check_val), num))

    min = 99999
    val = 0

    for (pos, value) in results:
        if pos < min and pos >= 0:
            min = pos
            val = value

    return val