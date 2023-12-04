
from re import search
from token import NUMBER
from tokenize import TokenInfo, DEDENT, NAME, INDENT

from _builtin import built_ins
from _errors import UnknownInstruction, BuiltinShadowing, WronglyStructuredInstruction, WronglyStructuredProcedure, \
    MissingMainProcedure
from _instruction import Instruction
from _interpreter import instructions
from _procedure import Procedure

def check_instruction(instruction_name: str, instruction_line: str, instruction_line_nb: int) -> None:
    if search(r'(^ +\w+ +\S+ *$)|(^ +\w+ +((\'.*\')|(".*")) *$)', instruction_line) is None:
        WronglyStructuredInstruction(instruction_name, instruction_line, instruction_line_nb)
    if instructions.get(instruction_name) is None:
        UnknownInstruction(instruction_name, instruction_line, instruction_line_nb)

def check_procedure(procedure_name: str, procedure_line: str, procedure_line_nb: int) -> None:
    if search(r'(^\w+ *: *$)|(^\w+( +\S+)+ *: *$)', procedure_line) is None:
        WronglyStructuredProcedure(procedure_name, procedure_line, procedure_line_nb)
    if procedure_name in built_ins:
        BuiltinShadowing(procedure_name, procedure_line, procedure_line_nb)

def check_main(procedures: dict[Procedure]):
    if 'main' not in procedures.keys():
        MissingMainProcedure()

def parse(lines: list[list[TokenInfo]]) -> dict[Procedure]:
    indented = False
    current_proc = None
    procedures = {}

    for line in lines:
        if line[0].type == DEDENT:
            line.pop(0)
            indented = False
        if line[0].type == INDENT:
            line.pop(0)
            indented = True
        if indented:
            check_instruction(line[0].string, line[0].line, line[0].start[0])
            if len(line) >= 3 and line[0].string != 'bo' and line[1].string == '-' and line[2].type == NUMBER:
                line[1] = TokenInfo(NUMBER, f'-{line[2].string}', line[1].start, line[2].end, line[1].line)
                line.pop()
            if len(line) > 2:
                WronglyStructuredInstruction(line[0].string, line[0].line, line[0].start[0])
            current_proc.program.append(Instruction(instructions[line[0].string], line[1], line[1].start[0]))
        elif line[0].type == NAME:
            check_procedure(line[0].string, line[0].line, line[0].start[0])
            index = 1
            params = list()
            while line[index].string != ':' and line[index].type == NAME:
                params.append(line[index].string)
                index += 1
            current_proc = procedures.setdefault(line[0].string, Procedure(params))

    check_main(procedures)
    return procedures
