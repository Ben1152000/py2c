class Variable:
    def __init__(self, name, _type=None):
        self.name = name
        self.type = _type

    def __str__(self):
        if not self.type:
            raise Exception(
                f'Variable "{self.name}" does not have a known type')

        return f'{self.type} {self.name};\n'


# these have a different __str__ method so they are separate from Variable
class FunctionPointer:
    def __init__(self, name, decl):
        self.name = name
        self.decl = decl

    def __str__(self):
        return f'{self.decl};\n'


class FunctionBlock:
    def __init__(self):
        self.stack_vars = []
        self.local_vars = []
        self.statements = []

    def __str__(self):
        output = ''
        output += ''.join(map(str, self.stack_vars))
        output += ''.join(map(str, self.local_vars))
        output += ''.join(map(str, self.statements))
        return output


class Assignment:
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self):
        if isinstance(self.rhs, Variable):
            return f'{self.lhs.name} = {self.rhs.name};\n'
        return f'{self.lhs.name} = {self.rhs};\n'


class FunctionCall:
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def __str__(self):
        arg_str = ', '.join([arg.name for arg in self.args])
        return f'{self.name}({arg_str});\n'
