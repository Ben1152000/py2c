class Variable:
    def __init__(self, name, _type=None):
        self.name = name
        self.type = _type
        self.py_type = ''

    def __str__(self):
        return f'{self.type} {self.name};\n' if self.type else ''
    

# these have a different __str__ method so they are separate from Variable
class FunctionPointer:
    def __init__(self, name, func_sig):
        self.name = name
        self.func_sig = func_sig


class FunctionBlock:
    def __init__(self):
        self.stack_vars = []
        self.local_vars = []
        self.fast_local_vars = []
        self.statements = []

    def keep_good(self, val):
        return not isinstance(val, FunctionPointer)

    def __str__(self):
        output = ''
        output += ''.join(map(str, filter(self.keep_good, self.stack_vars)))
        output += ''.join(map(str, filter(self.keep_good, self.local_vars)))
        output += ''.join(
            map(str, filter(self.keep_good, self.fast_local_vars)))
        output += ''.join(map(str, filter(self.keep_good, self.statements)))
        return output


class Assignment:
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self):
        if isinstance(self.rhs, Variable):
            return f'{self.lhs.name} = {self.rhs.name};\n'
        return f'{self.lhs.name} = {self.rhs};\n'


class Statement:
    def __init__(self, expr):
        self.expr = expr

    def __str__(self):
        return f'{self.expr};\n'


class FunctionCall:
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def __str__(self):
        arg_str = ', '.join([arg.name for arg in self.args])
        return f'{self.name}({arg_str})'

class Print:
    FORMATTERS = {'long': '%ld', 'double': '%lf', 'char *': '%s'}

    def __init__(self, args=None):
        self.args = args

    def __str__(self):
        return f'printf("{" ".join([Print.FORMATTERS[arg.type] for arg in self.args])}\\n"' \
               f", {', '.join([arg.name for arg in self.args])});"