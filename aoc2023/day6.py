from io import TextIOWrapper
from math import sqrt

def parse_file_part1(file: TextIOWrapper) -> list[tuple[int, int]]:
    times: list[int] | None = None
    distances: list[int] |None = None

    while True:
        line = file.readline()
        match line.partition(":"):
            case ("", "", _):
                break
            case ("\n", _, _):
                continue
            case ("Time", ":", values):
                times = [int(n) for n in values.split()]
            case ("Distance", ":", values):
                distances = [int(n) for n in values.split()]
            case (key, sep, rest):
                raise ValueError(f"Found unhandled case {key}{sep}{rest}")

    if times is None or distances is None:
        raise ValueError("Expected both Time: <ints> and Distance: <ints>!")
    else:
        return list(zip(times, distances))

def parse_file_part2(file: TextIOWrapper) -> tuple[int, int]:
    time: int | None = None
    distance: int |None = None

    while True:
        line = file.readline()
        match line.partition(":"):
            case ("", "", _):
                break
            case ("\n", _, _):
                continue
            case ("Time", ":", value):
                time = int("".join(value.split()))
            case ("Distance", ":", value):
                distance = int("".join(value.split()))
            case (key, sep, rest):
                raise ValueError(f"Found unhandled case {key}{sep}{rest}")

    if time is None or distance is None:
        raise ValueError("Expected both Time: <ints> and Distance: <ints>!")
    else:
        return time, distance

def wins_eq(time: int, distance: int) -> int:
    try:
        root = sqrt((-time)**2 - 4*distance)
    except ValueError:
        # No solutions means no wins
        return 0

    match round((time + root) // 2 - (time - root) // 2):
        case x if x >= 0:
            # odd numbers gets the wrong index
            if root % 1 == 0:
                x -= 1
            return x
        case _:
            return 0

def run(file: TextIOWrapper):
    part1(file)
    part2(file)

def part2(file: TextIOWrapper):
    file.seek(0)
    print("\nPART 2")
    time, distance = parse_file_part2(file)

    print(f"(Time: {time}, Distance: {distance})")
    ws = wins_eq(time, distance)
    print(f"Wins: {ws}")

def part1(file: TextIOWrapper):
    print("PART 1")
    p = 1
    for time, distance in parse_file_part1(file):
        l = wins_eq(time, distance)
        p *= l

    print(f"total result: {p}")


