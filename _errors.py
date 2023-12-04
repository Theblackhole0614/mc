from enum import Enum, auto

RED = '\033[31m'
WHITE = '\033[37m'
RESET = '\033[39m'
NEW_LINE = '\n'


class Error(Enum):
    EmptyStack = auto()
    Value = auto()


def construct_error_message(base: str, name: str, line: str, line_nb: int, all_line_error: bool = False) -> str:
    formated_line_nb = f'  {line_nb}  |'
    if all_line_error:
        error_pointer = f'{RED}{" "*len(formated_line_nb)}{"^" * len(line)}\n'
    else:
        error_pointer = f'{RED}{" "*len(formated_line_nb)}{" " * line.find(name) + "^" * len(name)}\n'
    return f'{RED}Error at line {line_nb}:{RESET}\n{WHITE}{formated_line_nb}{line}' \
           f'{"" if line.endswith(NEW_LINE) else NEW_LINE}{RESET}' \
        + error_pointer + base + RESET


def UnknownInstruction(instruction_name: str, instruction_line: str, instruction_line_nb: int) -> None:
    error_message = construct_error_message(f'UnknownInstruction: \'{instruction_name}\' is not a valid instruction.',
                                            instruction_name,
                                            instruction_line,
                                            instruction_line_nb)
    print(error_message)
    exit()

def BuiltinShadowing(procedure_name: str, procedure_line: str, procedure_line_nb: int) -> None:
    error_message = construct_error_message(f'BuiltinShadowing: \'{procedure_name}\' is shadowing the builtin '
                                            f'procedure of the same name.',
                                            procedure_name,
                                            procedure_line,
                                            procedure_line_nb)
    print(error_message)
    exit()

def WronglyStructuredInstruction(instruction_name: str, instruction_line: str, instruction_line_nb: int) -> None:
    error_message = construct_error_message(f'WronglyStructuredInstruction: this line is wrongly structured.',
                                            instruction_name,
                                            instruction_line,
                                            instruction_line_nb,
                                            True)
    print(error_message)
    exit()

def WronglyStructuredProcedure(procedure_name: str, procedure_line: str, procedure_line_nb: int) -> None:
    error_message = construct_error_message(f'WronglyStructuredProcedure: this line is wrongly structured.',
                                            procedure_name,
                                            procedure_line,
                                            procedure_line_nb,
                                            True)
    print(error_message)
    exit()

def MissingMainProcedure() -> None:
    print(RED + 'MissingMainProcedure: no main procedure found, there must be one.' + RESET)
    exit()

def AlreadyCreatedVariable(variable_name: str, variable_line: str, variable_line_nb: int) -> None:
    error_message = construct_error_message(f'AlreadyCreatedVariable: the variable \'{variable_name}\' has already '
                                            f'been created in this procedure.',
                                            variable_name,
                                            variable_line,
                                            variable_line_nb)
    print(error_message)
    exit()

def UnknownVariable(variable_name: str, variable_line: str, variable_line_nb: int) -> None:
    error_message = construct_error_message(f'UnknownVariable: the variable \'{variable_name}\' has not been created '
                                            f'in this procedure yet.',
                                            variable_name,
                                            variable_line,
                                            variable_line_nb)
    print(error_message)
    exit()

def EmptyStack(name: str, line: str, line_nb: int) -> None:
    error_message = construct_error_message(f'EmptyStack: you attempted to pop the stack of the current procedure while'
                                            f' it was empty.',
                                            name,
                                            line,
                                            line_nb,
                                            True)
    print(error_message)
    exit()

def UnknownProcedure(procedure_name: str, procedure_line: str, procedure_line_nb: int) -> None:
    error_message = construct_error_message(f'UnknownProcedure: the procedure \'{procedure_name}\' has not been '
                                            f'defined in this file.',
                                            procedure_name,
                                            procedure_line,
                                            procedure_line_nb)
    print(error_message)
    exit()

def OutBoundJump(delta_name: str, delta_line: str, delta_line_nb: int) -> None:
    error_message = construct_error_message(f'OutBoundJump: you attempted to jump outside the bounds of the procedure.',
                                            delta_name,
                                            delta_line,
                                            delta_line_nb)
    print(error_message)
    exit()

def ConstantValueError(constant_name: str, constant_line: str, constant_line_nb: int) -> None:
    error_message = construct_error_message(f'ConstantValueError: \'{constant_name}\' is not a valid constant.',
                                            constant_name,
                                            constant_line,
                                            constant_line_nb)
    print(error_message)
    exit()

def ObjectTypeError(name: str, line: str, line_nb: int, current_type: str, expected_types: str) -> None:
    error_message = construct_error_message(f'ObjectTypeError: {current_type} was given but {expected_types} were '
                                            f'expected.',
                                            name,
                                            line,
                                            line_nb,
                                            True)
    print(error_message)
    exit()

def NoReturn(prev_name: str, prev_line: str, prev_line_nb: int) -> None:
    error_message = construct_error_message(f'NoReturn: Maybe you forgot a \'rt\' at line {prev_line_nb+1}.',
                                            prev_name,
                                            prev_line,
                                            prev_line_nb,
                                            True)
    print(error_message)
    exit()
