import importlib
from os import path
import sys
import click
from aoc2023 import unicode_symbols as u


def cristmas_header():
    print(f"\t{u.tree}{u.bell}{u.santa}   Advent of Code 2023!   {u.santa}{u.bell}{u.tree}")
    

@click.command()
@click.option("--data-folder", default="./data", help="Path to data folder")
@click.option("-d", "--day", default=1, help="Day to verify")
@click.option("-f", "--data-file", default=None, help="path to data file")
@click.option("-x", "--example", is_flag=True, default=False)
def cli(data_folder: str, day: int, data_file: str, example: bool):
    """Launches a day"""
    ex_suffix = "" if not example else "ex"
    data_file = data_file if data_file is not None else f"day{day}{ex_suffix}.aoc"
    filename = f"{data_folder}/{data_file}"
   
    cristmas_header()
    print(f"\t{u.day} {day}: Running {filename}...")
    cristmas_header()

    match day:
        case n if 1 <= n <= 25:
            run_dynamic(filename, n)
        case _: print(f"{u.day} {day} not supported yet")

def run_dynamic(filename, n):
    if not path.exists(filename):
        print(f"\n{u.warning} Oops! {filename} doesn't exist! {u.confused}")
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