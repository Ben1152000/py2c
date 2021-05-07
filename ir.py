class Variable:
    def __init__(self, name):
        self.name = name
        self.type = None


class FunctionBlock:
    def __init__(self):
        self.stack_vars = []
        self.local_vars = []
