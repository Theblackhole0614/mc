
from _errors import Error


class Stack:
    def __init__(self) -> None:
        self.stack = list()

    def __len__(self) -> int:
        return len(self.stack)

    def push(self, element: object) -> None:
        self.stack.append(element)

    def pop(self) -> object:
        return self.stack.pop()

    def peak(self) -> object:
        if self.is_empty():
            return Error.EmptyStack
        return self.stack[-1]

    def is_empty(self) -> bool:
        return not self.stack
