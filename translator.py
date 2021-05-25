import dis, inspect, types
from ir import FunctionBlock, Assignment, \
    Variable, FunctionPointer, FunctionCall, Print, \
    IfStatement, Range, ForLoop

DEBUG = False


class CodeTranslator:
    def __init__(self, code):
        self.code = code
        self.includes = ['<stdio.h>']

    def translate(self):
        output = ''

        # list files to include
        for include in self.includes:
            output += f'#include {include}\n'

        compiled_code, func_table = FunctionTranslator(
            code=self.code, func_sig=[]).translate()

        # handle function table
        for func_decl in func_table:
            output += func_decl + '\n'

        # add main function declaration to main method
        output += 'int main(int argc, char* argv[]){\n'
        output += compiled_code
        output += 'return 0;\n}\n'

        return output


class FunctionTranslator:
    C_TYPES = ['long', 'double', 'char*']
    C_TYPE_MAP = {
        int: 'long',
        'int': 'long',
        float: 'double',
        'float': 'double',
        str: 'char*',
        'str': 'char*',
        bool: 'long',
        'bool': 'long'
    }
    STR_TO_TYPE = {'int': int, 'float': float, 'str': str, 'bool': bool}
    NUMERIC_TYPES = [int, float]

    def __init__(self, code, func_sig, globals_=None):
        self.opcode_map = lambda name: getattr(self, name)

        self.func_decls = []

        self.code = code
        self.func_sig = func_sig

        # The ir representation of the function output
        self.fb = FunctionBlock()

        self.globals = globals_
        if not self.globals:
            self.globals = {
                'names': self.code.co_names,
                'locals': self.fb.local_vars
            }

        # current instruction index and instruction
        self.instr_idx = 0
        self.cur_instr = None

        # current types on the stack
        self.stack_types = []

        self.instructions = list(dis.get_instructions(self.code))

        self.stack_depths = []
        depth = 0
        for instruction in self.instructions:
            self.stack_depths.append(depth)
            depth += dis.stack_effect(instruction.opcode, instruction.arg)

        # top of stack is the next closing bracket we need to add
        # this was Ben's idea
        self.for_stack = [-1]

        # global for-loop counter
        self.gflc = -1

    # return the variable corresponding to the result of the instruction
    # based on current stack depth and variable type
    def res_stack_var(self, _type):
        cur_depth = self.stack_depths[self.instr_idx + 1]
        c_type = self.C_TYPE_MAP[_type]
        return Variable(f's{c_type[0]}{cur_depth - 1}', c_type)

    # get the stack var at the offset from the top of the stack
    # get_stack_var(1) returns variable corresponding to TOS1
    def get_stack_var(self, offset):
        stack_var_idx = self.stack_depths[self.instr_idx] - offset - 1
        assert stack_var_idx >= 0
        stack_var_type = self.stack_types[stack_var_idx]
        c_type = self.C_TYPE_MAP[stack_var_type]
        return Variable(f's{c_type[0]}{stack_var_idx}', c_type)

    def BINARY_ADD(self):
        lhs_type = self.stack_types[-2]
        rhs_type = self.stack_types[-1]
        if (lhs_type not in FunctionTranslator.NUMERIC_TYPES) or (
                rhs_type not in FunctionTranslator.NUMERIC_TYPES):
            raise Exception(
                f'{inspect.stack()[0][3]}:'
                ' addition on non-numeric types is not implemented')

        res_type = float if (lhs_type == float or rhs_type == float) else int

        stack_var = self.res_stack_var(res_type)
        lhs_stack_var = self.get_stack_var(1)
        rhs_stack_var = self.get_stack_var(0)

        self.stack_types.pop()
        self.stack_types.pop()
        self.stack_types.append(res_type)

        return Assignment(stack_var,
                          f'{lhs_stack_var.name} + {rhs_stack_var.name}')

    def BINARY_FLOOR_DIVIDE(self):
        lhs_type = self.stack_types[-2]
        rhs_type = self.stack_types[-1]
        if (lhs_type not in FunctionTranslator.NUMERIC_TYPES) or (
                rhs_type not in FunctionTranslator.NUMERIC_TYPES):
            raise Exception(
                f'{inspect.stack()[0][3]}:'
                ' addition on non-numeric types is not implemented')

        res_type = float if (lhs_type == float or rhs_type == float) else int

        stack_var = self.res_stack_var(res_type)
        lhs_stack_var = self.get_stack_var(1)
        rhs_stack_var = self.get_stack_var(0)

        self.stack_types.pop()
        self.stack_types.pop()
        self.stack_types.append(res_type)

        return Assignment(stack_var,
                          f'{lhs_stack_var.name} / {rhs_stack_var.name}')

    def BINARY_MODULO(self):
        lhs_type = self.stack_types[-2]
        rhs_type = self.stack_types[-1]
        if (lhs_type not in FunctionTranslator.NUMERIC_TYPES) or (
                rhs_type not in FunctionTranslator.NUMERIC_TYPES):
            raise Exception(
                f'{inspect.stack()[0][3]}:'
                ' addition on non-numeric types is not implemented')

        res_type = float if (lhs_type == float or rhs_type == float) else int

        stack_var = self.res_stack_var(res_type)
        lhs_stack_var = self.get_stack_var(1)
        rhs_stack_var = self.get_stack_var(0)

        self.stack_types.pop()
        self.stack_types.pop()
        self.stack_types.append(res_type)

        return Assignment(stack_var,
                          f'{lhs_stack_var.name} % {rhs_stack_var.name}')

    def BINARY_MULTIPLY(self):
        lhs_type = self.stack_types[-2]
        rhs_type = self.stack_types[-1]
        if (lhs_type not in FunctionTranslator.NUMERIC_TYPES) or (
                rhs_type not in FunctionTranslator.NUMERIC_TYPES):
            raise Exception(
                f'{inspect.stack()[0][3]}:'
                ' multiplication on non-numeric types is not implemented')

        res_type = float if (lhs_type == float or rhs_type == float) else int

        stack_var = self.res_stack_var(res_type)
        lhs_stack_var = self.get_stack_var(1)
        rhs_stack_var = self.get_stack_var(0)

        self.stack_types.pop()
        self.stack_types.pop()
        self.stack_types.append(res_type)

        return Assignment(stack_var,
                          f'{lhs_stack_var.name} * {rhs_stack_var.name}')

    def BINARY_SUBTRACT(self):
        lhs_type = self.stack_types[-2]
        rhs_type = self.stack_types[-1]
        if (lhs_type not in FunctionTranslator.NUMERIC_TYPES) or (
                rhs_type not in FunctionTranslator.NUMERIC_TYPES):
            raise Exception(
                f'{inspect.stack()[0][3]}:'
                ' addition on non-numeric types is not implemented')

        res_type = float if (lhs_type == float or rhs_type == float) else int

        stack_var = self.res_stack_var(res_type)
        lhs_stack_var = self.get_stack_var(1)
        rhs_stack_var = self.get_stack_var(0)

        self.stack_types.pop()
        self.stack_types.pop()
        self.stack_types.append(res_type)

        return Assignment(stack_var,
                          f'{lhs_stack_var.name} - {rhs_stack_var.name}')

    def BUILD_CONST_KEY_MAP(self):
        count = self.cur_instr.arg
        self.stack_types.pop()  # tuple of keys
        # pop values
        for i in range(count):
            self.stack_types.pop()
        self.stack_types.append(dict)
        return ''

    def CALL_FUNCTION(self):
        argc = self.cur_instr.arg
        args = []
        for i in range(argc):
            args.append(self.get_stack_var(argc - i - 1))
        for i in range(argc):
            self.stack_types.pop()
        fp = self.stack_types.pop()
        if isinstance(fp, Print):
            self.stack_types.append(None)
            return Print(args=args)
        if isinstance(fp, Range):
            self.stack_types.append(Range(args=args))
            return ''
        ret_type = fp.func_sig[-1][0]
        self.stack_types.append(ret_type)
        if ret_type is None:
            return FunctionCall(fp.name, args)
        stack_var = self.res_stack_var(ret_type)
        return Assignment(stack_var, FunctionCall(fp.name, args))

    def COMPARE_OP(self):
        op_idx = self.cur_instr.arg
        op_name = dis.cmp_op[op_idx]

        stack_var = self.res_stack_var(bool)
        lhs_stack_var = self.get_stack_var(1)
        rhs_stack_var = self.get_stack_var(0)

        self.stack_types.pop()
        self.stack_types.pop()
        self.stack_types.append(bool)

        return Assignment(
            stack_var, f'{lhs_stack_var.name} {op_name} {rhs_stack_var.name}')

    def FOR_ITER(self):
        delta = self.cur_instr.arg
        self.for_stack.append(self.cur_instr.offset + delta)

        range_ = self.stack_types[-1]
        self.stack_types.append(int)
        stack_var = self.res_stack_var(int)

        self.gflc += 1
        return ForLoop(stack_var, range_, self.gflc)

    def GET_ITER(self):
        return ''

    def INPLACE_ADD(self):
        return self.BINARY_ADD()

    def INPLACE_FLOOR_DIVIDE(self):
        return self.BINARY_FLOOR_DIVIDE()
    
    def INPLACE_MULTIPLY(self):
        return self.BINARY_MULTIPLY()

    def JUMP_ABSOLUTE(self):
        if self.cur_instr.offset == self.for_stack[-1]:
            # we are the end of a for-loop
            self.for_stack.pop()
            # pop off the iterator
            # self.stack_types.pop()
            return '}\n'

        target = self.cur_instr.arg
        return f'goto L{target};\n'

    def JUMP_FORWARD(self):
        delta = self.cur_instr.arg
        target = self.cur_instr.offset + delta + 2
        return f'goto L{target};\n'

    def LOAD_CONST(self):
        const_idx = self.cur_instr.arg
        const_val = self.code.co_consts[const_idx]
        const_type = type(const_val)
        self.stack_types.append(const_type)  # Append type to stack
        if const_type == types.CodeType:
            return ''
        if const_type == FunctionPointer:
            return ''
        if const_type == tuple:
            return ''
        if const_val is None:
            return ''
        stack_var = self.res_stack_var(const_type)
        return Assignment(stack_var, Variable(const_val, const_type))

    def LOAD_FAST(self):
        local_idx = self.cur_instr.arg
        if local_idx < len(self.func_sig) - 1:
            local_type, local_var = self.func_sig[local_idx]
        else:
            local_var = self.fb.fast_local_vars[local_idx]
            local_type = type(local_var)
        if local_type == FunctionPointer:
            self.stack_types.append(local_var)
            return ''
        # TODO figure out the type of the local
        self.stack_types.append(int)
        stack_var = self.res_stack_var(int)
        if local_type == types.CodeType:
            return ''
        if local_type == tuple:
            return ''
        if local_var is None:
            return ''
        return Assignment(stack_var, local_var)

    def LOAD_GLOBAL(self):
        global_name = self.code.co_names[self.cur_instr.arg]
        if global_name in self.globals['names']:
            global_var = self.globals['locals'][self.globals['names'].index(global_name)]
        else:
            global_var = self.fb.local_vars[self.cur_instr.arg]
        global_type = type(global_var)
        if global_type == FunctionPointer:
            self.stack_types.append(global_var)
            return ''
        # if the global variable doesn't have a type assign it type of TOS
        if type(global_var) == Variable and global_var.py_type != '':
            self.stack_types.append(global_var.py_type)
            stack_var = self.res_stack_var(global_var.py_type)
            return Assignment(stack_var, global_var)
        if global_name == 'print':
            self.stack_types.append(Print())
            return ''
        if global_name == 'range':
            self.stack_types.append(Range())
            return ''
        # TODO get the actual type of the global var
        self.stack_types.append(None)
        return ''

    def LOAD_NAME(self):
        local_idx = self.cur_instr.arg
        local_name = self.code.co_names[local_idx]
        local_var = self.fb.local_vars[local_idx]
        if type(local_var) == FunctionPointer:
            self.stack_types.append(local_var)
            return ''
        # if the local variable doesn't have a type assign it type of TOS
        if type(local_var) == Variable and local_var.py_type != '':
            self.stack_types.append(local_var.py_type)
            stack_var = self.res_stack_var(local_var.py_type)
            return Assignment(stack_var, local_var)
        if local_name == 'print':
            self.stack_types.append(Print())
            return ''
        if local_name == 'range':
            self.stack_types.append(Range())
            return ''
        # TODO get the actual type of the local var
        self.stack_types.append(None)
        return ''

    def MAKE_FUNCTION(self):
        self.stack_types.pop()  # function name
        self.stack_types.pop()  # code object
        flags = self.cur_instr.arg
        # args corresponding to flags
        for bit in bin(flags):
            if bit == '1':
                self.stack_types.pop()

        # remove last 4 from statements
        self.fb.statements.pop()  # load function name
        name = self.code.co_consts[self.instructions[self.instr_idx - 1].arg]
        name = name.replace('.', '_').replace('<', '_').replace('>', '_')
        self.fb.statements.pop()  # load code object
        code_object = self.code.co_consts[self.instructions[self.instr_idx -
                                                            2].arg]
        assert isinstance(code_object, types.CodeType)
        self.fb.statements.pop()  # build const key map
        self.fb.statements.pop()  # load function type signature
        param_names = self.code.co_consts[self.instructions[self.instr_idx -
                                                            4].arg]
        param_types = []
        # look back to signature tuple and figure out types
        for i in range(len(param_names)):
            self.fb.statements.pop()
            param_types.append(
                self.code.co_names[self.instructions[self.instr_idx - 5 -
                                                     i].arg])
        param_types.reverse()
        func_sig = [(FunctionTranslator.STR_TO_TYPE[param_types[i]],
                     param_names[i]) for i in range(len(param_names))]

        fp = FunctionPointer(name, func_sig)
        # store the function pointer a bit sooner to handle recursive functions
        # assumes the next instruction is STORE_NAME
        local_idx = self.instructions[self.instr_idx + 1].arg
        self.fb.local_vars[local_idx] = fp

        # recursively compile the function, add it to func decls
        func_body, rec_func_decls = FunctionTranslator(
            code=code_object, func_sig=func_sig,
            globals_=self.globals).translate()
        self.func_decls += rec_func_decls
        func_decl = f'{FunctionTranslator.C_TYPE_MAP[func_sig[-1][0]]} {name}(' \
            f'{", ".join([f"{FunctionTranslator.C_TYPE_MAP[param[0]]} {param[1]}" for param in func_sig[:-1]])}' \
            f') {{{func_body}}}'  # construct function signature
        self.func_decls.append(func_decl)
        self.stack_types.append(fp)
        return ''

    def POP_TOP(self):
        self.stack_types.pop()
        return ''

    def POP_JUMP_IF_FALSE(self):
        target = self.cur_instr.arg
        target_instr = self.instructions[target // 2]
        if target_instr.opname == 'FOR_ITER':
            target = target_instr.offset + target_instr.arg
        stack_var = self.get_stack_var(0)
        self.stack_types.pop()
        return IfStatement(f'!{stack_var.name}', f'goto L{target};')

    def POP_JUMP_IF_TRUE(self):
        target = self.cur_instr.arg
        target_instr = self.instructions[target // 2]
        if target_instr.opname == 'FOR_ITER':
            target = target_instr.offset + target_instr.arg
        stack_var = self.get_stack_var(0)
        self.stack_types.pop()
        return IfStatement(f'{stack_var.name}', f'goto L{target};')

    def RETURN_VALUE(self):
        if self.stack_types[-1] == type(None):
            self.stack_types.pop()
            return ''
        ret_var = self.get_stack_var(0)
        self.stack_types.pop()
        return f'return {ret_var.name};\n'

    def SETUP_ANNOTATIONS(self):
        # create local dictionary call __annotations__
        return ''

    def STORE_FAST(self):
        local_idx = self.cur_instr.arg
        if local_idx < len(self.func_sig) - 1:
            local_type, local_var = self.func_sig[local_idx]
            local_var = Variable(local_var, local_type)
            local_var.py_type = self.stack_types[-1]
        else:
            local_var = self.fb.fast_local_vars[local_idx]
        if self.stack_types[-1] == tuple:
            self.stack_types.pop()
            return ''
        if isinstance(self.stack_types[-1], FunctionPointer):
            self.fb.fast_local_vars[local_idx] = self.stack_types.pop()
            return ''
        if local_var.type == '':
            local_var.py_type = self.stack_types[-1]
            local_var.type = self.C_TYPE_MAP[self.stack_types[-1]]
        elif local_var.py_type != self.stack_types[-1]:
            raise TypeError(
                f'variable {self.code.co_varnames[local_idx]} must have unchanging type'
            )
        stack_var = self.get_stack_var(0)
        self.stack_types.pop()
        return Assignment(local_var, stack_var)

    def STORE_NAME(self):
        local_idx = self.cur_instr.arg
        local_var = self.fb.local_vars[local_idx]
        if self.stack_types[-1] == tuple:
            self.stack_types.pop()
            return ''
        if isinstance(self.stack_types[-1], FunctionPointer):
            self.fb.local_vars[local_idx] = self.stack_types.pop()
            return ''
        if local_var.type == '':
            local_var.py_type = self.stack_types[-1]
            local_var.type = self.C_TYPE_MAP[self.stack_types[-1]]
        elif local_var.py_type != self.stack_types[-1]:
            raise TypeError(
                f'variable {self.code.co_names[local_idx]} must have unchanging type'
            )
        stack_var = self.get_stack_var(0)
        self.stack_types.pop()
        return Assignment(local_var, stack_var)

    def STORE_SUBSCR(self):
        array_idx = self.stack_types.pop()
        self.fb.statements.pop()
        array_name = self.stack_types.pop()
        self.fb.statements.pop()
        array_val = self.stack_types.pop()
        self.fb.statements.pop()
        # TODO actually do the right store_subscr
        return ''

    def translate(self):
        output = ''

        # create a stack for each type
        for _type in FunctionTranslator.C_TYPES:
            for i in range(max(self.stack_depths)):
                self.fb.stack_vars.append(Variable(f's{_type[0]}{i}', _type))

        # TODO figure out the actual types of local variables
        # create local variables
        for i, name in enumerate(self.code.co_names):
            self.fb.local_vars.append(Variable(f'loc{i}', ''))

        # create FAST local variables
        for i, name in enumerate(self.code.co_varnames):
            self.fb.fast_local_vars.append(Variable(f'fasloc{i}', ''))

        for instr in self.instructions:
            if DEBUG:
                print('\tstack_depths:', self.stack_depths[self.instr_idx])
                print('\tstack_types:', self.stack_types)
                print(instr.opname, '->', instr)
            self.cur_instr = instr
            # add a label if the instruction is a jump target
            if instr.is_jump_target or instr.opname == 'JUMP_ABSOLUTE':
                self.fb.statements.append(f'L{instr.offset}:;\n')

            self.fb.statements.append(self.opcode_map(instr.opname)())
            self.instr_idx += 1

        output += str(self.fb)

        return (output, self.func_decls)
