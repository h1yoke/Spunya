""" Debug info logger module."""

class bcolors:
    """ ANSI escape sequences"""
    HEADER    = '\033[95m'
    OKBLUE    = '\033[94m'
    OKCYAN    = '\033[96m'
    OKGREEN   = '\033[92m'
    WARNING   = '\033[93m'
    FAIL      = '\033[91m'
    ENDC      = '\033[0m'
    BOLD      = '\033[1m'
    UNDERLINE = '\033[4m'

def set_debug_level(level: int):
    """ Sets debug output level.

    Level 0 outputs only necessary logs, 1 gives details about loading process,
    3 logs every sent message. Level -1 disables debug logging."""
    global __DEBUG_OUTPUT_LEVEL
    __DEBUG_OUTPUT_LEVEL = level

def debug_output(text: str, level: int, mode: str = bcolors.OKBLUE):
    global __DEBUG_OUTPUT_LEVEL
    if __DEBUG_OUTPUT_LEVEL is None:
        set_debug_level(0)
    if level <= __DEBUG_OUTPUT_LEVEL:
        print(f"{mode}{bcolors.BOLD}[DEBUG]{bcolors.ENDC} {text}")
