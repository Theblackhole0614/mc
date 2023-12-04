
class Type:
    STRING = str
    INT = int
    FLOAT = float
    BOOL = bool
    NULL = None


types = {
    'STR': Type.STRING,
    'INT': Type.INT,
    'FLOAT': Type.FLOAT,
    'BOOL': Type.BOOL,
    'NULL': Type.NULL,
}

itypes = {
    Type.STRING: 'STR',
    Type.INT: 'INT',
    Type.FLOAT: 'FLOAT',
    Type.BOOL: 'BOOL',
    Type.NULL: 'NULL',
}



class Variable:
    def __init__(self, vtype: Type, value: object) -> None:
        self.vtype = vtype
        self.value = value