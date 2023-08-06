import zcommons.o2d
import zcommons.module
import zcommons.units
from zcommons.colorama import cprint
from zcommons.config import Config
from zcommons.counter import *
from zcommons.threadgroup import *
from zcommons.timer import *

# alias for colorama colors
FORE_BLACK = zcommons.colorama.Fore.BLACK
FORE_BLUE = zcommons.colorama.Fore.BLUE
FORE_CYAN = zcommons.colorama.Fore.CYAN
FORE_GREEN = zcommons.colorama.Fore.GREEN
FORE_MAGENTA = zcommons.colorama.Fore.MAGENTA
FORE_RED = zcommons.colorama.Fore.RED
FORE_RESET = zcommons.colorama.Fore.RESET
FORE_WHITE = zcommons.colorama.Fore.WHITE
FORE_YELLOW = zcommons.colorama.Fore.YELLOW
FORE_LIGHTBLACK_EX = zcommons.colorama.Fore.LIGHTBLACK_EX
FORE_LIGHTBLUE_EX = zcommons.colorama.Fore.LIGHTBLUE_EX
FORE_LIGHTCYAN_EX = zcommons.colorama.Fore.LIGHTCYAN_EX
FORE_LIGHTGREEN_EX = zcommons.colorama.Fore.LIGHTGREEN_EX
FORE_LIGHTMAGENTA_EX = zcommons.colorama.Fore.LIGHTMAGENTA_EX
FORE_LIGHTRED_EX = zcommons.colorama.Fore.LIGHTRED_EX
FORE_LIGHTWHITE_EX = zcommons.colorama.Fore.LIGHTWHITE_EX
FORE_LIGHTYELLOW_EX = zcommons.colorama.Fore.LIGHTYELLOW_EX

BACK_BLACK = zcommons.colorama.Back.BLACK
BACK_BLUE = zcommons.colorama.Back.BLUE
BACK_CYAN = zcommons.colorama.Back.CYAN
BACK_GREEN = zcommons.colorama.Back.GREEN
BACK_MAGENTA = zcommons.colorama.Back.MAGENTA
BACK_RED = zcommons.colorama.Back.RED
BACK_RESET = zcommons.colorama.Back.RESET
BACK_WHITE = zcommons.colorama.Back.WHITE
BACK_YELLOW = zcommons.colorama.Back.YELLOW
BACK_LIGHTBLACK_EX = zcommons.colorama.Back.LIGHTBLACK_EX
BACK_LIGHTBLUE_EX = zcommons.colorama.Back.LIGHTBLUE_EX
BACK_LIGHTCYAN_EX = zcommons.colorama.Back.LIGHTCYAN_EX
BACK_LIGHTGREEN_EX = zcommons.colorama.Back.LIGHTGREEN_EX
BACK_LIGHTMAGENTA_EX = zcommons.colorama.Back.LIGHTMAGENTA_EX
BACK_LIGHTRED_EX = zcommons.colorama.Back.LIGHTRED_EX
BACK_LIGHTWHITE_EX = zcommons.colorama.Back.LIGHTWHITE_EX
BACK_LIGHTYELLOW_EX = zcommons.colorama.Back.LIGHTYELLOW_EX

STYLE_BRIGHT = zcommons.colorama.Style.BRIGHT
STYLE_DIM = zcommons.colorama.Style.DIM
STYLE_NORMAL = zcommons.colorama.Style.NORMAL
STYLE_RESET_ALL = zcommons.colorama.Style.RESET_ALL
STYLE_ITALIC = zcommons.colorama.Style.ITALIC
STYLE_UNDERLINE = zcommons.colorama.Style.UNDERLINE
STYLE_SLOW_BLINK = zcommons.colorama.Style.SLOW_BLINK
STYLE_RAPID_BLINK = zcommons.colorama.Style.RAPID_BLINK
STYLE_INVERT = zcommons.colorama.Style.INVERT
STYLE_HIDE = zcommons.colorama.Style.HIDE
STYLE_STRIKE = zcommons.colorama.Style.STRIKE
STYLE_DOUBLE_UNDERLINE = zcommons.colorama.Style.DOUBLE_UNDERLINE
