import click
from aoc2023 import day1, day2, day3

@click.command()
@click.option("--data-folder", default="./data", help="Path to data folder")
@click.option("-d", "--day", default=1, help="Day to verify")
@click.option("-f", "--data-file", default="day1ex.aoc", help="path to data file")
def cli(data_folder: str, day: int, data_file: str):
    """Launches a day"""
    filename = f"{data_folder}/{data_file}"
    file = open(filename)
    print(f"\U0001F384\U0001F514\U0001F385 Advent of Code 2023!\U0001F385\U0001F514\U0001F384")
    print(f"\U0001F4C5 {day}: Running {filename}...")
    print(f"\U0001F384\U0001F514\U0001F385 Advent of Code 2023!\U0001F385\U0001F514\U0001F384\n")

    match day:
        case 1:
            day1.run(file)
        case 2:
            day2.run(file)
        case 3:
            day3.run(file)
        case _:
            print(f"Day {day} not supported yet")


if __name__ == '__main__':
    cli()