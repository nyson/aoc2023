import click
from aoc2023 import day1, day2, day3, day4
from aoc2023 import unicode_symbols as u


def cristmas_header():
    print(f"\t{u.tree}{u.bell}{u.santa}   Advent of Code 2023!   {u.santa}{u.bell}{u.tree}")

@click.command()
@click.option("--data-folder", default="./data", help="Path to data folder")
@click.option("-d", "--day", default=1, help="Day to verify")
@click.option("-f", "--data-file", default="day1ex.aoc", help="path to data file")
def cli(data_folder: str, day: int, data_file: str):
    """Launches a day"""
    filename = f"{data_folder}/{data_file}"
    file = open(filename)
    
    cristmas_header()
    print(f"\t{u.day} {day}: Running {filename}...")
    cristmas_header()
    
    match day:
        case 1: day1.run(file)
        case 2: day2.run(file)
        case 3: day3.run(file)
        case 4: day4.run(file)
        case _: print(f"{u.day} {day} not supported yet")


if __name__ == '__main__':
    cli()