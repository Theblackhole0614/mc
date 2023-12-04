
from _stack import Stack


class Procedure:
    def __init__(self, params: list[str]) -> None:
        self.variables = dict()
        self.params = params
        self.nb_params = len(self.params)
        self.stack = Stack()
        self.program = list()
        self.counter = 0