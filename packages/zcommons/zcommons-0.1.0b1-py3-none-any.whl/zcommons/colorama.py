"""
Colorama extension
"""

__all__ = [
    "cprint",
    "init", "deinit", "reinit", "colorama_text",
    "Fore", "Back", "Style", "Cursor",
    "AnsiToWin32"
]

import sys

from colorama import *
from colorama.ansi import code_to_chars


def __extend_colorama():
    def __add_code(cls, name, code):
        setattr(cls, name, code_to_chars(code))

    __add_code(Style, "ITALIC", 3)
    __add_code(Style, "UNDERLINE", 4)
    __add_code(Style, "SLOW_BLINK", 5)
    __add_code(Style, "RAPID_BLINK", 6)
    __add_code(Style, "INVERT", 7)
    __add_code(Style, "HIDE", 8)
    __add_code(Style, "STRIKE", 9)
    __add_code(Style, "DOUBLE_UNDERLINE", 21)


__extend_colorama()
init()


def __wrap_value(v, style):
    style = "".join(style)
    return style + v + Style.RESET_ALL


def cprint(*values, sep=' ', end='\n', file=sys.stdout, flush=False, style=None) -> None:
    """
    Print text in the terminal with styles such as color.

    :param values:
    :param sep:
    :param end:
    :param file:
    :param flush:
    :param style: the text styles, str or list.
    :return:
    """
    if style is None:
        print(*values, sep=sep, end=end, file=file, flush=flush)
    else:
        if file is sys.__stdout__ or file is sys.__stderr__ or (hasattr(file, "isatty") and file.isatty()):
            new_values = [__wrap_value(v, style) for v in values]
            print(*new_values, sep=sep, end=end, file=file, flush=flush)
        else:
            print(*values, sep=sep, end=end, file=file, flush=flush)
