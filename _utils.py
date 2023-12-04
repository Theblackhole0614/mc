
from token import NUMBER, NAME, STRING
from tokenize import TokenInfo

from _errors import Error
from _variable import Variable, Type

def token_to_variable(token: TokenInfo) -> Variable | Error:
    if token.type == STRING:
        return Variable(Type.STRING, token.string.removesuffix("'").removeprefix("'").replace('\\n', '\n'))
    if token.type == NAME and token.string == 'NULL':
        return Variable(Type.NULL, None)
    if token.type == NAME and token.string in ('TRUE', 'FALSE'):
        return Variable(Type.BOOL, token.string == 'TRUE')
    if token.type == NUMBER:
        if token.string.find('.') == -1:
            return Variable(Type.INT, int(token.string))
        return Variable(Type.FLOAT, float(token.string))
    return Error.Value
