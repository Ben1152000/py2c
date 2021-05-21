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


class IfStatement:
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body

    def __str__(self):
        return f'if({self.cond}){{\n{self.body}\n}}\n'


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
               f", {', '.join([arg.name for arg in self.args])});\n"


class Range:
    def __init__(self, args=None):
        if args:
            self.start = 0 if len(args) < 2 else args[0]
            self.stop = args[0] if len(args) < 2 else args[1]
            self.step = 1 if len(args) < 3 else args[2]


class ForLoop:
    def __init__(self, var, range_, gflc):
        self.var = var
        self.range = range_
        self.gflc = gflc

    def __str__(self):
        name = self.var.name
        output = ''

        start = self.range.start
        if isinstance(self.range.start, Variable):
            output += f'long for{self.gflc * 3} = {self.range.start.name};\n'
            start = f'for{self.gflc * 3}'

        output += f'long for{self.gflc * 3 + 1} = {self.range.stop.name};\n'
        stop = f'for{self.gflc * 3 + 1}'

        step = self.range.step
        if isinstance(self.range.step, Variable):
            output += f'long for{self.gflc * 3 + 2} = {self.range.step.name};\n'
            step = f'for{self.gflc * 3 + 2}'

        return f'{output}for ({name} = {start}; {name} < {stop}; {name} += {step}) {{\n'
