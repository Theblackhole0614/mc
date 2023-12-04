
from tokenize import TokenInfo
from typing import Callable


class Instruction:
    def __init__(self, cmd: Callable, arg: TokenInfo, line_nb: int) -> None:
        self.cmd = cmd
        self.arg = arg
        self.line_nb = line_nb
