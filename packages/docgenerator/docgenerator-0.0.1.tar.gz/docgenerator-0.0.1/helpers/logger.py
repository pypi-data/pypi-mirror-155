import setup


class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    CLEAN = '\033[0m'


def logger(message, color):
    if setup.VERBOSE:
        if color == "RED":
            print(Colors.RED + message + Colors.CLEAN)
        if color == "GREEN":
            print(Colors.GREEN + message + Colors.CLEAN)
        if color == "BLUE":
            print(Colors.BLUE + message + Colors.CLEAN)
        if color == "YELLOW":
            print(Colors.YELLOW + message + Colors.CLEAN)
