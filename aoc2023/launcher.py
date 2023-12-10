import importlib
from os import path
import click
from aoc2023 import unicode_symbols as u
from aoc2023.unicode_symbols import FgColor, carousel, styled, Style

def print_christmas_header(day, filename):
    s = ""
    s += f"{u.tree}{u.bell}{u.santa}   "
    s += carousel(
        "Advent of Code 2023!",
        [FgColor.red], 
        [FgColor.green], 
        [FgColor.yellow],
        base= [Style.bold, Style.underline])
    s += "   "
    s += f"{u.santa}{u.bell}{u.tree}"

    print(s, end="\n\n")
    print(f"{u.day} {day}: Running {filename}...".center(44))
    print(f"\n{s}")

@click.command()
@click.option("--data-folder", default="./data", help="Path to data folder")
@click.option("-d", "--day", default=1, help="Day to verify")
@click.option("-f", "--data-file", default=None, help="path to data file")
@click.option("-x", "--example", is_flag=True, default=False)
@click.option("-n", "--example-number", default=0, help="Example number")
def cli(data_folder: str, day: int, data_file: str, example: bool, example_number):
    """Launches a day"""
    ex_suffix = "" if not example else f"ex{'' if example_number == 0 else example_number}"
    data_file = data_file if data_file is not None else f"day{day}{ex_suffix}.aoc"
    filename = f"{data_folder}/{data_file}"
   
    print_christmas_header(day, filename)
    
    match day:
        case n if 1 <= n <= 25:
            run_dynamic(filename, n)
        case _: print(f"{u.day} {day} not supported yet")

def run_dynamic(filename, n):
    if not path.exists(filename):
        print(f"\n{u.warning}", end= " ")
        print(styled(f"Oops! {filename} doesn't exist!", Style.framed, Style.bold, Style.underline) + f" {u.confused}")
        print("Did you download the data for the day?")
        return

    try:
        with open(filename) as file: 
            importlib.import_module(
                f".day{n}", 
                ".aoc2023"
                ).run(file)
    except ImportError as e:
        print(f"Could not import day{n}: {e}")


if __name__ == '__main__':
    cli()