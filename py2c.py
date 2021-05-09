import dis
import marshal
import sys
import inspect
from ir import FunctionBlock, Assignment, Variable, FunctionPointer, FunctionCall

class CodeTranslator:
    
    def __init__(self, code):
        self.code = code
        self.includes = [
            '<stdio.h>'
        ]

    def translate(self):
        output = ''

        # list files to include
        for include in self.includes:
            output += f'#include {include}\n'

        compiled_code, func_table = FunctionTranslator(self.code).translate()

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
    py2c_type_map = {int: 'long', float: 'double', str: 'char*'}
    numeric_types = [int, float]

    def __init__(self, code):
        self.opcode_map = lambda name: getattr(self, name)

        # stack of function names
        # since pushing them to the actual stack is annoying
        self.func_stack = []
        self.func_decls = []

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

    def local_var(self, idx):
        return self.fb.local_vars[idx]

    def BINARY_ADD(self):
        lhs_type = self.stack_types[-2]
        rhs_type = self.stack_types[-1]
        if (lhs_type not in CodeTranslator.numeric_types) or (
                rhs_type not in CodeTranslator.numeric_types):
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

    def CALL_FUNCTION(self):
        argc = self.cur_instr.arg
        args = []
        for i in range(argc, 0, -1):
            args.append(self.get_stack_var(i - 1))
            self.stack_types.pop()
        func_name = self.func_stack.pop()
        # TODO append function's return type to type_stack
        self.stack_types.append(int)
        return FunctionCall(func_name, args)

    def LOAD_CONST(self):
        const_idx = self.cur_instr.arg
        const_val = self.code.co_consts[const_idx]
        const_type = type(const_val)
        self.stack_types.append(const_type)
        # TODO not loading None onto stack for now
        if const_val is None:
            return ''
        stack_var = self.res_stack_var(const_type)
        return Assignment(stack_var, Variable(const_val, const_type))

    def LOAD_NAME(self):
        local_idx = self.cur_instr.arg
        local_var = self.local_var(local_idx)
        if isinstance(local_var, FunctionPointer):
            # TODO push type of function?
            self.func_stack.append(local_var.name)
            self.stack_types.append(None)
            return ''
        # TODO get the actual type of the local var
        stack_var = self.res_stack_var(int)
        self.stack_types.append(int)
        return Assignment(stack_var, local_var)

    def MAKE_FUNCTION(self):
        # TODO implement make function
        # remove last 4 from statements
        # look back to signature tuple and figure out types
        # get rid of 1 + params statements
        # recursively compile the function
        # add it to func decls
        code_object = None # get from const table
        assert type(code_object) == types.CodeType
        func_body, rec_func_decls = CodeTranslator(code_object).translate()
        self.func_decls += rec_func_decls
        func_decl = f'void f() {{{func_body}}}' # construct function signature
        self.func_decls.append(func_decl)
        # do some other stuff to make it locally callible?

    def POP_TOP(self):
        self.stack_types.pop()
        return ''

    def RETURN_VALUE(self):
        self.stack_types.pop()
        if self.stack_types[-1] is None:
            return ''
        ret_var = self.get_stack_var(0)
        return f'return {ret_var};\n'

    def STORE_NAME(self):
        local_idx = self.cur_instr.arg
        local_var = self.local_var(local_idx)
        stack_var = self.get_stack_var(0)
        self.stack_types.pop()
        return Assignment(local_var, stack_var)

    def translate(self, main=False):
        output = ''
        
        # create a stack for each type
        for _type in CodeTranslator.c_types:
            for i in range(max(self.stack_depths)):
                self.fb.stack_vars.append(Variable(f's{_type[0]}{i}', _type))

        # create local variables
        # TODO figure out the actual types of local variables
        for i, name in enumerate(self.code.co_names):
            if name == 'print':
                fp = FunctionPointer('print', 'int (*print)(const char*, ...)')
                self.fb.local_vars.append(fp)
                self.fb.statements.append(Assignment(fp, Variable('printf')))
            else:
                self.fb.local_vars.append(Variable(f'l{i}', 'long'))

        for instr in self.instructions:
            self.cur_instr = instr
            self.fb.statements.append(self.opcode_map(instr.opname)())
            self.instr_idx += 1

        output += str(self.fb)

        return output, func_decls


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
        writefile.write(CodeTranslator(code).translate(main=True))
