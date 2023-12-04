from copy import copy, deepcopy
from tokenize import TokenInfo

from _builtin import built_ins
from _errors import Error, AlreadyCreatedVariable, UnknownVariable, EmptyStack, UnknownProcedure, OutBoundJump, \
    ConstantValueError, ObjectTypeError, NoReturn
from _procedure import Procedure
from _stack import Stack
from _utils import token_to_variable
from _variable import Variable, Type, types, itypes


class Interpreter:
    def __init__(self, procedures: dict[Procedure]) -> None:
        self.runtime_procedures = Stack()
        self.procedures = procedures

    def start(self):
        self.runtime_procedures.push(self.procedures['main'])
        while len(self.runtime_procedures):
            current_proc = self.runtime_procedures.peak()
            if current_proc.counter >= len(current_proc.program):
                prev_instruction = current_proc.program[current_proc.counter-1]
                NoReturn(prev_instruction.arg.string, prev_instruction.arg.line, prev_instruction.arg.start[0])
            current_instruction = current_proc.program[current_proc.counter]
            if current_instruction.cmd in (call_proc, ret):
                current_instruction.cmd(self, current_instruction.arg)
            else:
                current_instruction.cmd(current_proc, current_instruction.arg)
            current_proc.counter += 1


def create_interpreter(procedures: dict[Procedure]) -> Interpreter:
    return Interpreter(procedures)

binary_operators = {
    '+': lambda a, b: a + b,
    '-': lambda a, b: a - b,
    '*': lambda a, b: a * b,
    '/': lambda a, b: a / b,
    '//': lambda a, b: a // b,
    '**': lambda a, b: a ** b,
    '%': lambda a, b: a % b,
}

compare_operators = {
    '==': lambda a, b: a == b,
    '<': lambda a, b: a < b,
    '>': lambda a, b: a > b,
    '>=': lambda a, b: a >= b,
    '<=': lambda a, b: a <= b,
    '!=': lambda a, b: a != b,
}
        
def load_const(procedure: Procedure, constant: TokenInfo) -> None:
    object = token_to_variable(constant)
    if object == Error.Value:
        ConstantValueError(constant.string, constant.line, constant.start[0])
    procedure.stack.push(object)

def create_var(procedure: Procedure, variable: TokenInfo) -> None:
    if variable.string in procedure.variables.keys():
        AlreadyCreatedVariable(variable.string, variable.line, variable.start[0])
    procedure.variables[variable.string] = Variable(Type.NULL, None) 

def load_var(procedure: Procedure, variable: TokenInfo) -> None:
    if variable.string not in procedure.variables.keys():
        UnknownVariable(variable.string, variable.line, variable.start[0])
    procedure.stack.push(deepcopy(procedure.variables[variable.string]))

def store_var(procedure: Procedure, variable: TokenInfo) -> None:
    if procedure.stack.is_empty():
        EmptyStack(variable.string, variable.line, variable.start[0])
    procedure.variables[variable.string] = procedure.stack.pop()

def binary_op(procedure: Procedure, operator: TokenInfo) -> None:
    if len(procedure.stack) < 2:
        EmptyStack(operator.string, operator.line, operator.start[0])
    b, a = procedure.stack.pop(), procedure.stack.pop()
    if a.vtype not in (Type.INT, Type.FLOAT):
        ObjectTypeError(operator.string, operator.line, operator.start[0], itypes[a.vtype],
                        f'INT or FLOAT')
    if b.vtype not in (Type.INT, Type.FLOAT):
        ObjectTypeError(operator.string, operator.line, operator.start[0], itypes[b.vtype],
                        f'INT or FLOAT')
    value = binary_operators[operator.string](a.value, b.value) 
    vtype = Type.INT
    if operator.string == '//' or str(value).find('.') == -1:
        vtype = Type.INT
    else:
        vtype = Type.FLOAT
    procedure.stack.push(Variable(vtype, value)) 

def compare_op(procedure: Procedure, operator: TokenInfo) -> None:
    if len(procedure.stack) < 2:
        EmptyStack(operator.string, operator.line, operator.start[0])
    b, a = procedure.stack.pop(), procedure.stack.pop()
    if operator.string in '<=>=':
        if a.vtype not in (Type.INT, Type.FLOAT):
            ObjectTypeError(operator.string, operator.line, operator.start[0], itypes[a.vtype],
                            f'INT or FLOAT with \'{operator.string}\'')
        if b.vtype not in (Type.INT, Type.FLOAT):
            ObjectTypeError(operator.string, operator.line, operator.start[0], itypes[b.vtype],
                            f'INT or FLOAT with \'{operator.string}\'')
    value = compare_operators[operator.string](a.value, b.value) 
    procedure.stack.push(Variable(Type.BOOL, value)) 

def jump_true(procedure: Procedure, delta: TokenInfo) -> None:
    if procedure.stack.is_empty():
        EmptyStack(delta.string, delta.line, delta.start[0])
    _object = procedure.stack.pop()
    if _object.vtype != Type.BOOL:
        ObjectTypeError(delta.string, delta.line, delta.start[0], itypes[_object.vtype], 'BOOL')
    if _object.value:
        rdelta = int(delta.string)
        if 0 >= procedure.counter + rdelta >= len(procedure.program)-1:
            OutBoundJump(delta.string, delta.line, delta.start[0])
        if rdelta < 0:
            rdelta -= 2
        procedure.counter += rdelta

def jump_false(procedure: Procedure, delta: TokenInfo) -> None:
    if procedure.stack.is_empty():
        EmptyStack(delta.string, delta.line, delta.start[0])
    _object = procedure.stack.pop()
    if _object.vtype != Type.BOOL:
        ObjectTypeError(delta.string, delta.line, delta.start[0], itypes[_object.vtype], 'BOOL')
    if not _object.value:
        rdelta = int(delta.string)
        if 0 >= procedure.counter + rdelta >= len(procedure.program)-1:
            OutBoundJump(delta.string, delta.line, delta.start[0])
        if rdelta < 0:
            rdelta -= 2
        procedure.counter += rdelta

def jump_always(procedure: Procedure, delta: TokenInfo) -> None:
    rdelta = int(delta.string)
    if not (0 < procedure.counter + rdelta < len(procedure.program) - 1):
        OutBoundJump(delta.string, delta.line, delta.start[0])
    if rdelta < 0:
        rdelta -= 2
    procedure.counter += rdelta

def call_proc(interpreter: Interpreter, proc: TokenInfo) -> None:
    parent_proc = interpreter.runtime_procedures.peak()
    if proc.string in built_ins:
        call_proc = built_ins[proc.string]
        if len(parent_proc.stack) < call_proc.nb_params:
            EmptyStack(proc.string, proc.line, proc.start[0])
        params = list(reversed([parent_proc.stack.pop() for _ in range(call_proc.nb_params)])) 
        ret_variable = call_proc.func(*params)
        if call_proc.ret:
            parent_proc.stack.push(ret_variable) 
        return None
    if proc.string not in interpreter.procedures.keys():
        UnknownProcedure(proc.string, proc.line, proc.start[0])
    call_proc = deepcopy(interpreter.procedures[proc.string])
    if len(parent_proc.stack) < call_proc.nb_params:
        EmptyStack(proc.string, proc.line, proc.start[0])
    params = list(reversed([parent_proc.stack.pop() for _ in range(call_proc.nb_params)])) 
    for i in range(call_proc.nb_params):
        current_var = call_proc.params[i]
        call_proc.variables[current_var] = params[i]
    interpreter.runtime_procedures.push(call_proc)

def is_instance(procedure: Procedure, _type: TokenInfo) -> None:
    if procedure.stack.is_empty():
        EmptyStack(_type.string, _type.line, _type.start[0])
    procedure.stack.push(Variable(Type.BOOL, procedure.stack.pop().vtype == types[_type.string])) 

def transform_into(procedure: Procedure, _type: TokenInfo) -> None:
    if procedure.stack.is_empty():
        EmptyStack(_type.string, _type.line, _type.start[0])
    var = procedure.stack.pop()
    var.vtype = types[_type.string] 
    if var.vtype == Type.NULL: 
        var.value = None 
    else:
        var.value = var.vtype(var.value) 
    procedure.stack.push(var)

def build_string(procedure: Procedure, number: TokenInfo) -> None:
    if len(procedure.stack) < int(number.string):
        EmptyStack(number.string, number.line, number.start[0])
    value = ''
    for i in range(int(number.string)):
        _object = procedure.stack.pop()
        if _object.vtype != Type.STRING:
            ObjectTypeError(number.string, number.line, number.start[0], itypes[_object.vtype], 'STR')
        value = _object.value + value
    procedure.stack.push(Variable(Type.STRING, value)) 

def ret(interpreter: Interpreter, number: TokenInfo) -> None:
    ret_proc = interpreter.runtime_procedures.pop()
    if len(ret_proc.stack) < int(number.string):
        EmptyStack(number.string, number.line, number.start[0])
    parent_proc = interpreter.runtime_procedures.peak()
    if parent_proc == Error.EmptyStack:
        return None
    return_values = list(reversed([ret_proc.stack.pop() for _ in range(int(number.string))])) 
    for value in return_values:
        parent_proc.stack.push(value) 
    ret_proc.variables = dict() 
    ret_proc.counter = 0 
    ret_proc.stack = Stack()


instructions = {
    'lc': load_const,
    'cv': create_var,
    'lv': load_var,
    'sv': store_var,
    'bo': binary_op,
    'co': compare_op,
    'jt': jump_true,
    'jf': jump_false,
    'ja': jump_always,
    'cp': call_proc,
    'ii': is_instance,
    'ti': transform_into,
    'bs': build_string,
    'rt': ret,

    'load_const': load_const,
    'create_var': create_var,
    'load_var': load_var,
    'store_var': store_var,
    'binary_op': binary_op,
    'compare_op': compare_op,
    'jump_true': jump_true,
    'jump_false': jump_false,
    'jump_always': jump_always,
    'call_proc': call_proc,
    'is_instance': is_instance,
    'transform_into': transform_into,
    'build_string': build_string,
    'return': ret
}