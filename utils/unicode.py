import enum


class Format(enum.Enum):
    """
    Enum class capturing ANSI escape sequences for formatting strings
        - For more information - visit https://codepoints.net/search
    """
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    REVERSE = '\033[07m'
    STRIKE_THROUGH = '\033[09m'


class ForeGroundColor(enum.Enum):
    """
    Enum class capturing ANSI escape sequences for manipulating foreground
    color of text
        - For more information - visit https://codepoints.net/search
    """
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    ORANGE = '\033[33m'
    BLUE = '\033[34m'
    PURPLE = '\033[35m'
    CYAN = '\033[36m'
    LIGHT_GREY = '\033[37m'
    DARK_GREY = '\033[90m'
    LIGHT_RED = '\033[91m'
    LIGHT_GREEN = '\033[92m'
    YELLOW = '\033[93m'
    LIGHT_BLUE = '\033[94m'
    PINK = '\033[95m'
    LIGHT_CYAN = '\033[96m'


class BackgroundColor(enum.Enum):
    """
    Enum class capturing ANSI escape sequences for manipulating background color
    of text
        - For more information - visit https://codepoints.net/search
    """
    BLACK = '\033[40m'
    RED = '\033[41m'
    GREEN = '\033[42m'
    ORANGE = '\033[43m'
    BLUE = '\033[44m'
    PURPLE = '\033[45m'
    CYAN = '\033[46m'
    LIGHT_GREY = '\033[47m'


class Symbols(enum.Enum):
    """
    Enum class capturing ANSI escape sequences for printing special characters
        - For more information - visit https://codepoints.net/search
    """
    TICK = '\u2713'
    CROSS = '\u274C'

