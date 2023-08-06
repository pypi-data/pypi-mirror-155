import sys
import argparse
from typing import Callable

from rich.console import Console

from braillert.generator import generate_art
from braillert.colors import ColorTypes

FP_ARG_HELP_STRING: str = (
    """
    A required argument that represents the path where the convertible image is located
    e.g.
    --file-path=./my_folder/test.jpg
    """
)

MODE_ARG_HELP_STRING: str = (
    """
    A required argument that represents the mode in which the provided image should be converted
    e.g.
    --mode=rich or -m=discord
    """
)

def _get_printer_by_color_type(color_type: ColorTypes) -> Callable:
    if color_type == ColorTypes.RICH:
        return Console().print
    if color_type in (ColorTypes.COLORAMA, ColorTypes.DISCORD, ColorTypes.GRAYSCALE):
        return print
    raise Exception()

sys.stdin.reconfigure(encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")

def main() -> None:
    """Main function."""
    argument_parser = argparse.ArgumentParser()
    mode_choices = vars(ColorTypes)["_value2member_map_"].keys()
    argument_parser.add_argument("-fp", "--file-path", dest="file_path",
                                        required=True, help=FP_ARG_HELP_STRING)
    argument_parser.add_argument("-m", "--mode", dest="mode", choices=mode_choices,
                                        default="rich", help=MODE_ARG_HELP_STRING)

    arguments = argument_parser.parse_args()
    mode = ColorTypes(arguments.mode)

    _get_printer_by_color_type(mode)(generate_art(arguments.file_path, mode))
