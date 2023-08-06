from io import TextIOWrapper
from pathlib import Path
import sys
import argparse
import re


def parse_args(input_args: list[str]):
    """Parses terminal arguments and returns the parsed arguments"""
    parser = argparse.ArgumentParser(
        description="create a single latex file with no include/inputs"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Display file structure"
    )
    parser.add_argument("filename")
    return parser.parse_args(input_args)


def is_nested(input_line: str) -> bool:
    """Determines if a given line is actually a directive to expand another file."""
    return input_line.lstrip().startswith(
        r"\include"
    ) or input_line.lstrip().startswith(r"\input")


def inflate(included_path: str, output_file: TextIOWrapper):
    """Reads contents from included file and returns file as a string."""
    with open(included_path, encoding="utf-8") as included_file:
        for input_line in included_file:
            output_file.write(input_line)


def get_included_file_name(input_line: str) -> str:
    """Extracts the file name from an include statement"""
    res = re.findall(r"\{(.*?)\}", input_line)
    if not res:
        return ""
    return res[0] + ".tex"


def flat_it(input_file: TextIOWrapper, output_file: TextIOWrapper, verbose: bool):
    """Reads input file and writes as a flat file"""
    for input_line in input_file:
        if is_nested(input_line):
            included_file_name = get_included_file_name(input_line)
            if verbose:
                print(f"Expanding [{included_file_name}]")
            inflate(included_file_name, output_file)
        else:
            output_file.write(input_line)


def flat_file(input_args):
    """Reads input file and writes as a flat file"""
    input_file_name = input_args.filename
    verbose = input_args.verbose
    with open(input_file_name, encoding="utf-8") as input_file:
        print(f"input file: {input_file_name}")

        output_file_name = Path(input_file_name).with_suffix(".flt")

        with open(output_file_name, "w", encoding="utf-8") as output_file:
            flat_it(input_file, output_file, verbose)
    print(f"\tFile: {output_file_name} generated")


def cli():
    args = parse_args(sys.argv[1:])
    flat_file(args)
