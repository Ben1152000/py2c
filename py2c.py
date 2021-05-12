import dis
import inspect
from ir import FunctionBlock, Assignment, \
    Variable, FunctionPointer, FunctionCall
import marshal
import sys
import types


class CodeTranslator:
    def __init__(self, code):
        self.code = code
        self.includes = ['<stdio.h>']

    def translate(self):
        output = ''

        # list files to include
        for include in self.includes:
            output += f'#include {include}\n'

        compiled_code, func_table = FunctionTranslator(self.code,
                                                       []).translate()

        # handle function table
        for func_decl in func_table:
            output += func_decl + '\n'

        # add main function declaration to main method
        output += 'int main(int argc, char* argv[]){\n'
        output += compiled_code
        output += 'return 0;\n}\n'

        return output


class FunctionTranslator:
    c_types = ['long', 'double', 'char*', 'void*']
    py2c_type_map = {
        int: 'long',
        'int': 'long',
        float: 'double',
        'float': 'double',
        str: 'char*',
        'str': 'char*'
    }
    str_to_type = {'int': int, 'float': float, 'str': str}
    numeric_types = [int, float]

    def __init__(self, code, func_sig):
        self.opcode_map = lambda name: getattr(self, name)

        self.func_decls = []

        self.func_sig = func_sig

        # The ir representation of the function output
        self.fb = FunctionBlock()

        # current instruction index and instruction
        self.instr_idx = 0
        self.cur_instr = None

        self.stack_depths = []

        # current types on the stack
        self.stack_types = []

        self.code = code
        self.instructions = list(dis.get_instructions(self.code))

        depth = 0
        for instruction in self.instructions:
            self.stack_depths.append(depth)
            depth += dis.stack_effect(instruction.opcode, instruction.arg)

    # return the variable corresponding to the result of the instruction
    # based on current stack depth and variable type
    def res_stack_var(self, _type):
        cur_depth = self.stack_depths[self.instr_idx + 1]
        c_type = self.py2c_type_map[_type]
        return Variable(f's{c_type[0]}{cur_depth - 1}', c_type)

    # get the stack var at the offset from the top of the stack
    # get_stack_var(1) returns variable corresponding to TOS1
    def get_stack_var(self, offset):
        stack_var_idx = self.stack_depths[self.instr_idx] - offset - 1
        assert stack_var_idx >= 0
        stack_var_type = self.stack_types[stack_var_idx]
        c_type = self.py2c_type_map[stack_var_type]
        return Variable(f's{c_type[0]}{stack_var_idx}', c_type)

    def BINARY_ADD(self):
        lhs_type = self.stack_types[-2]
        rhs_type = self.stack_types[-1]
        if (lhs_type not in FunctionTranslator.numeric_types) or (
                rhs_type not in FunctionTranslator.numeric_types):
            raise Exception(
                f'{inspect.stack()[0][3]}:'
                ' addition on non-numeric types is not implemented')

        res_type = float if (lhs_type == float or rhs_type == float) else int

        res_stack_var = self.res_stack_var(res_type)
        lhs_stack_var = self.get_stack_var(1)
        rhs_stack_var = self.get_stack_var(0)

        self.stack_types.pop()
        self.stack_types.pop()
        self.stack_types.append(res_type)

        return Assignment(res_stack_var,
                          f'{lhs_stack_var.name} + {rhs_stack_var.name}')

    def BINARY_MULTIPLY(self):
        lhs_type = self.stack_types[-2]
        rhs_type = self.stack_types[-1]
        if (lhs_type not in FunctionTranslator.numeric_types) or (
                rhs_type not in FunctionTranslator.numeric_types):
            raise Exception(
                f'{inspect.stack()[0][3]}:'
                ' multiplication on non-numeric types is not implemented')

        res_type = float if (lhs_type == float or rhs_type == float) else int

        res_stack_var = self.res_stack_var(res_type)
        lhs_stack_var = self.get_stack_var(1)
        rhs_stack_var = self.get_stack_var(0)

        self.stack_types.pop()
        self.stack_types.pop()
        self.stack_types.append(res_type)

        return Assignment(res_stack_var,
                          f'{lhs_stack_var.name} * {rhs_stack_var.name}')

    def BUILD_CONST_KEY_MAP(self):
        self.stack_types.append(tuple)
        print("I'm building a const key map! whatever that means...")

    def CALL_FUNCTION(self):
        argc = self.cur_instr.arg
        args = []
        for i in range(argc, 0, -1):
            args.append(self.get_stack_var(i - 1))
            self.stack_types.pop()
        fp = self.stack_types.pop()
        ret_type = fp.func_sig[-1][1]
        self.stack_types.append(ret_type)
        stack_var = self.res_stack_var(ret_type)
        return Assignment(stack_var, FunctionCall(fp.name, args))

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
        if local_idx < len(self.func_sig):
            local_var = self.func_sig[local_idx]
        else:
            local_var = self.fb.fast_local_vars[local_idx]
        local_type = type(local_var)
        if local_type == FunctionPointer:
            self.stack_types.append(local_var)
            return ''
        # TODO figure out the time of the local
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
        self.stack_types.append(int)
        print("I just loaded your global.")
        return ''

    def LOAD_NAME(self):
        local_idx = self.cur_instr.arg
        local_var = self.fb.local_vars[local_idx]
        local_type = type(local_var)
        if local_type == FunctionPointer:
            self.stack_types.append(local_var)
            return ''
        # TODO get the actual type of the local var
        self.stack_types.append(int)
        stack_var = self.res_stack_var(int)
        if local_type == types.CodeType:
            return ''
        if local_type == tuple:
            return ''
        if local_type is None:
            return ''
        return Assignment(stack_var, local_var)

    def MAKE_FUNCTION(self):
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
        func_sig = [(param_names[i],
                     FunctionTranslator.str_to_type[param_types[i]])
                    for i in range(len(param_names))]

        # recursively compile the function, add it to func decls
        func_body, rec_func_decls = FunctionTranslator(code_object,
                                                       func_sig).translate()
        self.func_decls += rec_func_decls
        func_decl = f'{FunctionTranslator.py2c_type_map[func_sig[-1][1]]} {name}(' \
            f'{", ".join([f"{FunctionTranslator.py2c_type_map[param[1]]} {param[0]}" for param in func_sig[:-1]])}' \
            f') {{{func_body}}}'  # construct function signature
        self.func_decls.append(func_decl)
        fp = FunctionPointer(name, func_sig)
        self.stack_types.append(fp)
        return ''

    def POP_TOP(self):
        self.stack_types.pop()
        return ''

    def RETURN_VALUE(self):
        if self.stack_types[-1] == type(None):
            self.stack_types.pop()
            return ''
        ret_var = self.get_stack_var(0)
        self.stack_types.pop()
        return f'return {ret_var.name};\n'

    def STORE_FAST(self):
        local_idx = self.cur_instr.arg
        local_var = self.fb.fast_local_vars[local_idx]
        if self.stack_types[-1] == tuple:
            self.stack_types.pop()
            return ''
        if isinstance(self.stack_types[-1], FunctionPointer):
            self.fb.fast_local_vars[local_idx] = self.stack_types.pop()
            return ''
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
        stack_var = self.get_stack_var(0)
        self.stack_types.pop()
        return Assignment(local_var, stack_var)

    def translate(self):
        output = ''

        # create a stack for each type
        for _type in FunctionTranslator.c_types:
            for i in range(max(self.stack_depths)):
                self.fb.stack_vars.append(Variable(f's{_type[0]}{i}', _type))

        # TODO figure out the actual types of local variables
        # create local variables
        for i, name in enumerate(self.code.co_names):
            self.fb.local_vars.append(Variable(f'l{i}', 'long'))

        # create FAST local variables
        for i, name in enumerate(self.code.co_varnames):
            self.fb.fast_local_vars.append(Variable(f'fl{i}', 'long'))

        for instr in self.instructions:
            print(self.stack_types)
            print(instr.opname)
            self.cur_instr = instr
            self.fb.statements.append(self.opcode_map(instr.opname)())
            self.instr_idx += 1

        output += str(self.fb)

        return (output, self.func_decls)


def get_code(fname):
    f = open(fname, "rb")
    f.read(16)
    code = marshal.load(f)
    return code


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} pyc_file [out_file]')
        exit(1)
    if len(sys.argv) < 3:
        sys.argv.append('.'.join(sys.argv[1].split('.')[:-1]) + '.c')
    code = get_code(sys.argv[1])
    with open(sys.argv[2], 'w') as writefile:
        writefile.write(CodeTranslator(code).translate())
